"""Builds the per-channel `weight` producer chain (shapes_preparation.py, Phase 3)."""
from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer
from code_generation.quantity import Quantity

# data/embedding, mm/ee: constant no-op weight
with defaults(
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    call='''event::quantity::Define<double>({df}, {output}, 1.0)''',
    input=[],
):
    ConstantWeight = Producer(output=[q.weight])

# WP-templated producers, resolved once config parameters for a scope are known --
# same pattern as shapes_preparation.py's own TEMPLATED_QUANTITY_PRODUCERS/
# _resolve_templated_quantities.
TEMPLATED_QUANTITY_PRODUCERS = []


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


# 2024/2025/2026 Summer24 campaigns split in half, one per era (EvenIDFilter/OddIDFilter)
MC_CAMPAIGN_SPLIT_FACTOR = {"2024": 2.0, "2025": 2.0, "2026": 2.0}

# per-era luminosity in pb^-1; "2025" is 2025+2026 data combined (MC comes exclusively
# from 2025, OddIDFilter)
LUMI_PB = {
    "2016preVFP": 19500.0, "2016postVFP": 16800.0, "2017": 41500.0, "2018": 59830.0,
    "2022preEE": 8086.069205, "2022postEE": 26674.924045,
    "2023preBPix": 17964.217998, "2023postBPix": 9676.737966,
    "2024": 109816.515335, "2025": 135047.093128, "2026": 25148.977841,
}

DOUBLETAU_HPS_ERAS = ("2022preEE", "2022postEE", "2023preBPix", "2023postBPix")


def _product(scope, name, out_name, in1, type1, in2, type2, templated=False):
    out = Quantity(out_name)
    producer = Producer(
        name=name,
        call=f'''event::quantity::Product<{type1},{type2}>({{df}}, {{output}}, {{input}})''',
        input=[in1, in2],
        output=[out],
        scopes=[scope],
    )
    if templated:
        TEMPLATED_QUANTITY_PRODUCERS.append(producer)
    return producer, out


def _gate(scope, name, out_name, cond, value, templated=False):
    out = Quantity(out_name)
    producer = Producer(
        name=name,
        call='''weights::Gate({df}, {output}, {input})''',
        input=[cond, value],
        output=[out],
        scopes=[scope],
    )
    if templated:
        TEMPLATED_QUANTITY_PRODUCERS.append(producer)
    return producer, out


def _select(scope, name, out_name, cond, if_true, if_false):
    out = Quantity(out_name)
    producer = Producer(
        name=name,
        call='''weights::Select({df}, {output}, {input})''',
        input=[cond, if_true, if_false],
        output=[out],
        scopes=[scope],
    )
    return producer, out


def _normalization_producers(scope, era):
    """xsec * (1/nevents) * sign(genWeight)/negative_fraction * lumi * pileup -- the
    same formula for every channel, only the scope differs."""
    producers = []

    gen_weight_sign = Producer(
        name=f"GenWeightSign_{scope}",
        call='''weights::NormalizedGenWeightSign({df}, {output}, {input})''',
        input=[nanoAOD.genWeight, q.negative_events_fraction],
        output=[Quantity(f"weight_{scope}_gen_sign")],
        scopes=[scope],
    )
    producers.append(gen_weight_sign)

    p, xsec_ngen = _product(
        scope, f"Normalization_{scope}", f"weight_{scope}_xsec_ngen",
        q.crossSectionPerEventWeight, "double", q.numberGeneratedEventsWeight, "double",
    )
    producers.append(p)

    p, norm_signed = _product(
        scope, f"NormalizationSigned_{scope}", f"weight_{scope}_norm_signed",
        xsec_ngen, "double", gen_weight_sign.output[0], "double",
    )
    producers.append(p)

    lumi = Producer(
        name=f"Lumi_{scope}",
        call=f'''event::quantity::Define<double>({{df}}, {{output}}, {LUMI_PB[era]})''',
        input=[],
        output=[Quantity(f"weight_{scope}_lumi")],
        scopes=[scope],
    )
    producers.append(lumi)

    p, norm_lumi = _product(
        scope, f"NormalizationLumi_{scope}", f"weight_{scope}_norm_lumi",
        norm_signed, "double", lumi.output[0], "double",
    )
    producers.append(p)

    p, norm_pileup = _product(
        scope, f"NormalizationPileup_{scope}", f"weight_{scope}_norm_pileup",
        norm_lumi, "double", q.puweight, "double",
    )
    producers.append(p)

    return producers, norm_pileup


def _mc_campaign_split_producer(scope, era, running):
    split_factor = MC_CAMPAIGN_SPLIT_FACTOR.get(era, 1.0)
    split = Producer(
        name=f"MCCampaignSplit_{scope}",
        call=f'''event::quantity::Define<double>({{df}}, {{output}}, {split_factor})''',
        input=[],
        output=[Quantity(f"weight_{scope}_campaign_split")],
        scopes=[scope],
    )
    weight = Producer(
        name=f"Weight_{scope}",
        call='''event::quantity::Product<double,double>({df}, {output}, {input})''',
        input=[running, split.output[0]],
        output=[q.weight],
        scopes=[scope],
    )
    return [split, weight]


def _btag_producer(scope, era, running):
    if era in ("2016preVFP", "2016postVFP", "2017", "2018"):
        return [], running
    p, out = _product(
        scope, f"NormalizationBtag_{scope}", f"weight_{scope}_norm_btag",
        running, "double", q.btag_weight, "float",
    )
    return [p], out


def et_weight_producers(era, run2_eras) -> list:
    producers, running = _normalization_producers("et", era)

    p, running = _product(
        "et", "NormalizationLepID_et", "weight_et_norm_lepid",
        running, "double", q.id_wgt_ele_wp90iso_1, "double",
    )
    producers.append(p)

    is_genuine_tau_2 = Producer(
        name="IsGenuineTau2_et",
        call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 5)''',
        input=[q.gen_match_2],
        output=[Quantity("weight_et_is_genuine_tau_2")],
        scopes=["et"],
    )
    producers.append(is_genuine_tau_2)
    p, tauid_vsjet = _gate(
        "et", "TauIdVsJetGated_et", "weight_et_tauid_vsjet_gated",
        is_genuine_tau_2.output[0], Quantity("id_wgt_tau_vsJet_{vs_jet_wp}_2"), templated=True,
    )
    producers.append(p)
    p, running = _product(
        "et", "NormalizationTauIdVsJet_et", "weight_et_norm_tauid_vsjet",
        running, "double", tauid_vsjet, "double",
    )
    producers.append(p)

    p, running = _product(
        "et", "NormalizationTauIdVsMu_et", "weight_et_norm_tauid_vsmu",
        running, "double", Quantity("id_wgt_tau_vsMu_VLoose_{vs_ele_wp}_2"), "double",
        templated=True,
    )
    producers.append(p)
    p, running = _product(
        "et", "NormalizationTauIdVsEle_et", "weight_et_norm_tauid_vsele",
        running, "double", Quantity("id_wgt_tau_vsEle_{vs_ele_wp}_2"), "double",
        templated=True,
    )
    producers.append(p)

    # single-trigger-fired ? single SF : cross-trigger legs SF, matching
    # config.py's trigger SF producers exactly. Run2 not implemented -- config.py's
    # own trigger SF setup differs there too.
    if era not in run2_eras:
        p, cross = _product(
            "et", "EleTauCrossTriggerSF_et", "weight_et_eletau_cross_trigger_sf",
            Quantity("trg_wgt_ele24tau30_leg1"), "double", Quantity("trg_wgt_ele24tau30_leg2"), "float",
        )
        producers.append(p)
        p, trigger = _select(
            "et", "TriggerSF_et", "weight_et_trigger_sf",
            Quantity("trg_single_ele30"), Quantity("trg_wgt_single_ele30"), cross,
        )
        producers.append(p)
        p, running = _product(
            "et", "NormalizationTrigger_et", "weight_et_norm_trigger",
            running, "double", trigger, "double",
        )
        producers.append(p)

    btag_producers, running = _btag_producer("et", era, running)
    producers.extend(btag_producers)

    producers.extend(_mc_campaign_split_producer("et", era, running))
    return producers


def mt_weight_producers(era, run2_eras) -> list:
    producers, running = _normalization_producers("mt", era)

    p, running = _product(
        "mt", "NormalizationLepID_mt", "weight_mt_norm_lepid",
        running, "double", q.id_wgt_mu_1, "double",
    )
    producers.append(p)
    p, running = _product(
        "mt", "NormalizationLepIso_mt", "weight_mt_norm_lepiso",
        running, "double", q.iso_wgt_mu_1, "double",
    )
    producers.append(p)

    is_genuine_tau_2 = Producer(
        name="IsGenuineTau2_mt",
        call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 5)''',
        input=[q.gen_match_2],
        output=[Quantity("weight_mt_is_genuine_tau_2")],
        scopes=["mt"],
    )
    producers.append(is_genuine_tau_2)
    p, tauid_vsjet = _gate(
        "mt", "TauIdVsJetGated_mt", "weight_mt_tauid_vsjet_gated",
        is_genuine_tau_2.output[0], Quantity("id_wgt_tau_vsJet_{vs_jet_wp}_2"), templated=True,
    )
    producers.append(p)
    p, running = _product(
        "mt", "NormalizationTauIdVsJet_mt", "weight_mt_norm_tauid_vsjet",
        running, "double", tauid_vsjet, "double",
    )
    producers.append(p)

    p, running = _product(
        "mt", "NormalizationTauIdVsMu_mt", "weight_mt_norm_tauid_vsmu",
        running, "double", Quantity("id_wgt_tau_vsMu_Tight_{vs_ele_wp}_2"), "double",
        templated=True,
    )
    producers.append(p)
    p, running = _product(
        "mt", "NormalizationTauIdVsEle_mt", "weight_mt_norm_tauid_vsele",
        running, "double", Quantity("id_wgt_tau_vsEle_{vs_ele_wp}_2"), "double",
        templated=True,
    )
    producers.append(p)

    if era not in run2_eras:
        p, cross = _product(
            "mt", "MuTauCrossTriggerSF_mt", "weight_mt_mutau_cross_trigger_sf",
            Quantity("trg_wgt_mu20tau27_leg1"), "double", Quantity("trg_wgt_mu20tau27_leg2"), "float",
        )
        producers.append(p)
        p, trigger = _select(
            "mt", "TriggerSF_mt", "weight_mt_trigger_sf",
            Quantity("trg_single_mu24"), Quantity("trg_wgt_single_mu24"), cross,
        )
        producers.append(p)
        p, running = _product(
            "mt", "NormalizationTrigger_mt", "weight_mt_norm_trigger",
            running, "double", trigger, "double",
        )
        producers.append(p)

    btag_producers, running = _btag_producer("mt", era, running)
    producers.extend(btag_producers)

    producers.extend(_mc_campaign_split_producer("mt", era, running))
    return producers


def tt_weight_producers(era, run2_eras) -> list:
    producers, running = _normalization_producers("tt", era)

    for leg in (1, 2):
        is_genuine_tau = Producer(
            name=f"IsGenuineTau{leg}_tt",
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 5)''',
            input=[getattr(q, f"gen_match_{leg}")],
            output=[Quantity(f"weight_tt_is_genuine_tau_{leg}")],
            scopes=["tt"],
        )
        producers.append(is_genuine_tau)
        p, tauid_vsjet = _gate(
            "tt", f"TauIdVsJetGated{leg}_tt", f"weight_tt_tauid_vsjet_gated_{leg}",
            is_genuine_tau.output[0], Quantity(f"id_wgt_tau_vsJet_{{vs_jet_wp}}_{leg}"), templated=True,
        )
        producers.append(p)
        p, running = _product(
            "tt", f"NormalizationTauIdVsJet{leg}_tt", f"weight_tt_norm_tauid_vsjet_{leg}",
            running, "double", tauid_vsjet, "double",
        )
        producers.append(p)

    for leg in (1, 2):
        p, running = _product(
            "tt", f"NormalizationTauIdVsMu{leg}_tt", f"weight_tt_norm_tauid_vsmu_{leg}",
            running, "double", Quantity(f"id_wgt_tau_vsMu_VLoose_{{vs_ele_wp}}_{leg}"), "double",
            templated=True,
        )
        producers.append(p)
    for leg in (1, 2):
        p, running = _product(
            "tt", f"NormalizationTauIdVsEle{leg}_tt", f"weight_tt_norm_tauid_vsele_{leg}",
            running, "double", Quantity(f"id_wgt_tau_vsEle_{{vs_ele_wp}}_{leg}"), "double",
            templated=True,
        )
        producers.append(p)

    # plain-DiTau-fired ? plain-DiTau legs SF : DiTau+Jet legs SF -- era-branched
    # exactly like tau_triggersetup.py's own EraModifiers for these branch names.
    if era not in run2_eras:
        if era in DOUBLETAU_HPS_ERAS:
            plain_cond = Quantity("trg_double_tau35_mediumiso_hps")
            plain_leg1, plain_leg2 = Quantity("trg_wgt_doubletau35_leg1"), Quantity("trg_wgt_doubletau35_leg2")
            jet_leg1, jet_leg2 = Quantity("trg_wgt_doubletau_jet30_leg1"), Quantity("trg_wgt_doubletau_jet30_leg2")
        else:
            plain_cond = Quantity("trg_double_tau30_mediumiso_pnet")
            plain_leg1, plain_leg2 = Quantity("trg_wgt_doubletau30_leg1"), Quantity("trg_wgt_doubletau30_leg2")
            jet_leg1, jet_leg2 = Quantity("trg_wgt_doubletau_jet26_leg1"), Quantity("trg_wgt_doubletau_jet26_leg2")
        p, plain = _product(
            "tt", "DoubleTauTriggerSF_tt", "weight_tt_doubletau_trigger_sf",
            plain_leg1, "float", plain_leg2, "float",
        )
        producers.append(p)
        p, jet = _product(
            "tt", "DoubleTauJetTriggerSF_tt", "weight_tt_doubletau_jet_trigger_sf",
            jet_leg1, "float", jet_leg2, "float",
        )
        producers.append(p)
        p, trigger = _select(
            "tt", "TriggerSF_tt", "weight_tt_trigger_sf",
            plain_cond, plain, jet,
        )
        producers.append(p)
        p, running = _product(
            "tt", "NormalizationTrigger_tt", "weight_tt_norm_trigger",
            running, "double", trigger, "double",
        )
        producers.append(p)

    btag_producers, running = _btag_producer("tt", era, running)
    producers.extend(btag_producers)

    producers.extend(_mc_campaign_split_producer("tt", era, running))
    return producers


def em_weight_producers(era, run2_eras) -> list:
    producers, running = _normalization_producers("em", era)

    p, running = _product(
        "em", "NormalizationEleID_em", "weight_em_norm_ele_id",
        running, "double", q.id_wgt_ele_wp90iso_1, "double",
    )
    producers.append(p)
    p, running = _product(
        "em", "NormalizationMuID_em", "weight_em_norm_mu_id",
        running, "double", q.id_wgt_mu_2, "double",
    )
    producers.append(p)
    p, running = _product(
        "em", "NormalizationMuIso_em", "weight_em_norm_mu_iso",
        running, "double", q.iso_wgt_mu_2, "double",
    )
    producers.append(p)

    # (pt_1>26)*trg_wgt_single_mu24, matching TauKITFlow's
    # shapes/selection/process_selection.py em trgweight exactly. config.py's
    # SingleMuTriggerSF is unconditional across all eras for em, so this applies
    # to Run2 too (unlike et/mt/tt's trigger SF).
    lep_pt_1_above_26 = Producer(
        name="LepPt1Above26_em",
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, 26.0)''',
        input=[q.pt_1],
        output=[Quantity("weight_em_lep_pt_1_above_26")],
        scopes=["em"],
    )
    producers.append(lep_pt_1_above_26)
    p, trigger = _product(
        "em", "TriggerSF_em", "weight_em_trigger_sf",
        lep_pt_1_above_26.output[0], "bool", Quantity("trg_wgt_single_mu24"), "double",
    )
    producers.append(p)
    p, running = _product(
        "em", "NormalizationTrigger_em", "weight_em_norm_trigger",
        running, "double", trigger, "double",
    )
    producers.append(p)

    btag_producers, running = _btag_producer("em", era, running)
    producers.extend(btag_producers)

    producers.extend(_mc_campaign_split_producer("em", era, running))
    return producers


CHANNEL_WEIGHT_PRODUCERS = {
    "et": et_weight_producers,
    "mt": mt_weight_producers,
    "tt": tt_weight_producers,
    "em": em_weight_producers,
}


def build_weight_chain(configuration, scope: str, era: str, run2_eras) -> None:
    producers = CHANNEL_WEIGHT_PRODUCERS[scope](era, run2_eras)
    configuration.add_producers(scope, producers)
    configuration.add_outputs(scope, [q.weight])
