"""Builds the per-channel `weight` producer chain (shapes_preparation.py, Phase 3)."""
from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer
from code_generation.quantity import Quantity

# data/embedding, mm/ee, and em's trigger term (not implemented): constant no-op weight
with defaults(
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    call='''event::quantity::Define<double>({df}, {output}, 1.0)''',
    input=[],
):
    ConstantWeight = Producer(output=[q.weight])

# populated by build_weight_chain(); resolved by resolve_templated_quantities()
TEMPLATED_QUANTITY_PRODUCERS = []

# 2024/2025/2026 Summer24 campaigns split in half, one per era (EvenIDFilter/OddIDFilter)
MC_CAMPAIGN_SPLIT_FACTOR = {"2024": 2.0, "2025": 2.0, "2026": 2.0}

# per-era luminosity in pb^-1, matching TauKITFlow's config/samples.yaml
LUMI_PB = {
    "2016preVFP": 19500.0, "2016postVFP": 16800.0, "2017": 41500.0, "2018": 59830.0,
    "2022preEE": 8086.0, "2022postEE": 26679.0,
    "2023preBPix": 17964.0, "2023postBPix": 9677.0,
    "2024": 109816.0, "2025": 109898.0, "2026": 25140.0,
}

DOUBLETAU_HPS_ERAS = ("2022preEE", "2022postEE", "2023preBPix", "2023postBPix")


def resolve_templated_quantities(configuration, scope: str) -> None:
    parameters = configuration.config_parameters[scope]
    for producer in TEMPLATED_QUANTITY_PRODUCERS:
        if scope not in producer.scopes:
            continue
        producer.input[scope] = [
            Quantity(template.name.format(**parameters))
            for template in producer.input[scope]
        ]
        for column in producer.input[scope]:
            for output_quantity in producer.output:
                column.adopt(output_quantity, scope)


def _product_step(scope, step_name, running_quantity, running_type,
                   factor_quantity, factor_type, templated=False, output_quantity=None):
    out = output_quantity if output_quantity is not None else Quantity(step_name)
    producer = Producer(
        name=f"WeightStep_{step_name}",
        call=f'''event::quantity::Product<{running_type},{factor_type}>({{df}}, {{output}}, {{input}})''',
        input=[running_quantity, factor_quantity],
        output=[out],
        scopes=[scope],
    )
    if templated:
        TEMPLATED_QUANTITY_PRODUCERS.append(producer)
    return producer, out


def _gate_step(scope, step_name, cond_quantity, value_quantity, templated=False):
    out = Quantity(step_name)
    producer = Producer(
        name=f"WeightStep_{step_name}",
        call='''weights::Gate({df}, {output}, {input})''',
        input=[cond_quantity, value_quantity],
        output=[out],
        scopes=[scope],
    )
    if templated:
        TEMPLATED_QUANTITY_PRODUCERS.append(producer)
    return producer, out


def _select_step(scope, step_name, cond_quantity, true_quantity, false_quantity):
    out = Quantity(step_name)
    producer = Producer(
        name=f"WeightStep_{step_name}",
        call='''weights::Select({df}, {output}, {input})''',
        input=[cond_quantity, true_quantity, false_quantity],
        output=[out],
        scopes=[scope],
    )
    return producer, out


def _equal_flag_int(scope, step_name, input_quantity, value):
    out = Quantity(step_name)
    producer = Producer(
        name=f"WeightStep_{step_name}",
        call=f'''event::quantity::EqualFlag<int>({{df}}, {{output}}, {{input}}, {value})''',
        input=[input_quantity],
        output=[out],
        scopes=[scope],
    )
    return producer, out


def _trigger_weight(scope, era, next_name, run2_eras):
    """Single-trigger-fired ? single-trigger SF : cross/jet-trigger legs SF, matching
    config.py's trigger SF producers exactly (real branches on any new production --
    safe to reference even though older ntuples predating them can't). Run2: not
    implemented (config.py's own setup differs there too), em: not implemented."""
    if scope not in ("et", "mt", "tt") or era in run2_eras:
        return [], None
    producers = []
    if scope == "et":
        cond = Quantity("trg_single_ele30")
        single_sf = Quantity("trg_wgt_single_ele30")
        p, cross = _product_step(scope, next_name(), Quantity("trg_wgt_ele24tau30_leg1"), "double",
                                  Quantity("trg_wgt_ele24tau30_leg2"), "float")
        producers.append(p)
        p, combined = _select_step(scope, next_name(), cond, single_sf, cross)
        producers.append(p)
    elif scope == "mt":
        cond = Quantity("trg_single_mu24")
        single_sf = Quantity("trg_wgt_single_mu24")
        p, cross = _product_step(scope, next_name(), Quantity("trg_wgt_mu20tau27_leg1"), "double",
                                  Quantity("trg_wgt_mu20tau27_leg2"), "float")
        producers.append(p)
        p, combined = _select_step(scope, next_name(), cond, single_sf, cross)
        producers.append(p)
    else:  # tt
        if era in DOUBLETAU_HPS_ERAS:
            plain_cond = "trg_double_tau35_mediumiso_hps"
            plain_leg1, plain_leg2 = "trg_wgt_doubletau35_leg1", "trg_wgt_doubletau35_leg2"
            jet_leg1, jet_leg2 = "trg_wgt_doubletau_jet30_leg1", "trg_wgt_doubletau_jet30_leg2"
        else:
            plain_cond = "trg_double_tau30_mediumiso_pnet"
            plain_leg1, plain_leg2 = "trg_wgt_doubletau30_leg1", "trg_wgt_doubletau30_leg2"
            jet_leg1, jet_leg2 = "trg_wgt_doubletau_jet26_leg1", "trg_wgt_doubletau_jet26_leg2"
        p, plain = _product_step(scope, next_name(), Quantity(plain_leg1), "float", Quantity(plain_leg2), "float")
        producers.append(p)
        p, jet = _product_step(scope, next_name(), Quantity(jet_leg1), "float", Quantity(jet_leg2), "float")
        producers.append(p)
        p, combined = _select_step(scope, next_name(), Quantity(plain_cond), plain, jet)
        producers.append(p)
    return producers, combined


def build_weight_chain(configuration, scope: str, era: str, run2_eras) -> None:
    producers = []
    prefix = f"weight_{scope}"
    step = 0

    def next_name():
        nonlocal step
        step += 1
        return f"{prefix}_step{step}"

    # generator normalization: xsec * (1/nevents) * sign(genWeight)/negative_fraction
    sign_out = Quantity(next_name())
    sign_producer = Producer(
        name=f"WeightStep_{sign_out.name}",
        call='''weights::NormalizedGenWeightSign({df}, {output}, {input})''',
        input=[nanoAOD.genWeight, q.negative_events_fraction],
        output=[sign_out],
        scopes=[scope],
    )
    producers.append(sign_producer)

    p, running = _product_step(scope, next_name(), q.crossSectionPerEventWeight, "double",
                                q.numberGeneratedEventsWeight, "double")
    producers.append(p)
    p, running = _product_step(scope, next_name(), running, "double", sign_out, "double")
    producers.append(p)

    # lumi
    lumi_out = Quantity(next_name())
    lumi_producer = Producer(
        name=f"WeightStep_{lumi_out.name}",
        call=f'''event::quantity::Define<double>({{df}}, {{output}}, {LUMI_PB[era]})''',
        input=[],
        output=[lumi_out],
        scopes=[scope],
    )
    producers.append(lumi_producer)
    p, running = _product_step(scope, next_name(), running, "double", lumi_out, "double")
    producers.append(p)

    # pileup
    p, running = _product_step(scope, next_name(), running, "double", q.puweight, "double")
    producers.append(p)

    # lepton id/iso
    if scope == "mt":
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_mu_1, "double")
        producers.append(p)
        p, running = _product_step(scope, next_name(), running, "double", q.iso_wgt_mu_1, "double")
        producers.append(p)
    elif scope == "et":
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_ele_wp90iso_1, "double")
        producers.append(p)
    elif scope == "em":
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_ele_wp90iso_1, "double")
        producers.append(p)
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_mu_2, "double")
        producers.append(p)
        p, running = _product_step(scope, next_name(), running, "double", q.iso_wgt_mu_2, "double")
        producers.append(p)

    # tau vsJet (gated) / vsMu / vsEle -- no tau leg in em
    if scope in ("et", "mt", "tt"):
        tau_legs = [2] if scope in ("et", "mt") else [1, 2]
        for leg in tau_legs:
            cond_name = f"{prefix}_is_genuine_tau_{leg}"
            p, cond = _equal_flag_int(scope, cond_name, getattr(q, f"gen_match_{leg}"), 5)
            producers.append(p)
            gated_name = f"{prefix}_tauid_vsjet_gated_{leg}"
            p, gated = _gate_step(
                scope, gated_name, cond,
                Quantity(f"id_wgt_tau_vsJet_{{vs_jet_wp}}_{leg}"), templated=True,
            )
            producers.append(p)
            p, running = _product_step(scope, next_name(), running, "double", gated, "double")
            producers.append(p)

        vsmu_wp_prefix = {"et": "VLoose", "mt": "Tight", "tt": "VLoose"}[scope]
        for leg in tau_legs:
            p, running = _product_step(
                scope, next_name(), running, "double",
                Quantity(f"id_wgt_tau_vsMu_{vsmu_wp_prefix}_{{vs_ele_wp}}_{leg}"), "double",
                templated=True,
            )
            producers.append(p)
        for leg in tau_legs:
            p, running = _product_step(
                scope, next_name(), running, "double",
                Quantity(f"id_wgt_tau_vsEle_{{vs_ele_wp}}_{leg}"), "double",
                templated=True,
            )
            producers.append(p)

    # trigger SF (Run3 et/mt/tt only, see _trigger_weight)
    trig_producers, trig_combined = _trigger_weight(scope, era, next_name, run2_eras)
    producers.extend(trig_producers)
    if trig_combined is not None:
        p, running = _product_step(scope, next_name(), running, "double", trig_combined, "double")
        producers.append(p)

    # btag (Run3 only)
    if era not in run2_eras:
        p, running = _product_step(scope, next_name(), running, "double", q.btag_weight, "float")
        producers.append(p)

    # MC campaign split
    split_factor = MC_CAMPAIGN_SPLIT_FACTOR.get(era, 1.0)
    split_out = Quantity(next_name())
    split_producer = Producer(
        name=f"WeightStep_{split_out.name}",
        call=f'''event::quantity::Define<double>({{df}}, {{output}}, {split_factor})''',
        input=[],
        output=[split_out],
        scopes=[scope],
    )
    producers.append(split_producer)
    p, running = _product_step(scope, "weight", running, "double", split_out, "double",
                                output_quantity=q.weight)
    producers.append(p)

    configuration.add_producers(scope, producers)
    configuration.add_outputs(scope, [q.weight])
