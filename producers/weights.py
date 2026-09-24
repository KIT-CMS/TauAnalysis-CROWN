"""
Builds the per-channel `weight` producer chain for weights_friends.py (Phase 3).

WP choice as a config parameter, not hardcoded: `vs_ele_wp`/`vs_jet_wp` are set via
configuration.add_config_parameters() per scope (see weights_friends.py's WP_DEFAULTS),
the same pattern selection_friends.py uses for its own WP-templated quantities
(TEMPLATED_QUANTITY_PRODUCERS there). Producer inputs that depend on the WP carry a
"{vs_ele_wp}"/"{vs_jet_wp}" placeholder in their Quantity name, resolved into the real
branch name by resolve_templated_quantities() below, once the config parameters for
that scope are known -- changing a WP later is a one-line edit to WP_DEFAULTS, not a
producer or cpp_addons change.
"""
from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer
from code_generation.quantity import Quantity

# data/embedding, and channels build_weight_chain() doesn't implement yet (em/mm/ee):
# a constant no-op weight, same schema-consistency reasoning as
# producers/normalization.py's Constant* producers.
with defaults(
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    call='''event::quantity::Define<double>({df}, {output}, 1.0)''',
    input=[],
):
    ConstantWeight = Producer(output=[q.weight])

# producers whose input column name(s) are templated with a config parameter, resolved
# by resolve_templated_quantities() once config parameters for a scope are known --
# mirrors selection_friends.py's TEMPLATED_QUANTITY_PRODUCERS/_resolve_templated_quantities.
# Populated by build_weight_chain() as it constructs each channel's producer chain (the
# exact set of templated producers differs per channel).
TEMPLATED_QUANTITY_PRODUCERS = []

# 2024/2025/2026 Summer24 MC campaigns were each produced once and split into two equal
# halves, one per era (see EvenIDFilter/OddIDFilter in producers/event.py) --
# numberGeneratedEventsWeight is computed from the *full* campaign's nevents (Phase 1's
# normalization friend), so each era's shapes undercount by this factor without this
# correction. Mirrors TauKITFlow's shapes/selection/process_selection.py
# MC_CAMPAIGN_SPLIT_FACTOR exactly -- single source of truth once this friend replaces
# that Python-side factor (not yet -- see project memory).
MC_CAMPAIGN_SPLIT_FACTOR = {"2024": 2.0, "2025": 2.0, "2026": 2.0}


def resolve_templated_quantities(configuration, scope: str) -> None:
    """Resolve TEMPLATED_QUANTITY_PRODUCERS columns for `scope` once its config
    parameters are known. Separate copy of selection_friends.py's helper of the same
    name/purpose -- weights_friends.py is deliberately its own FriendTreeConfiguration,
    not sharing producer/quantity state with selection_friends.py's."""
    parameters = configuration.config_parameters[scope]
    for producer in TEMPLATED_QUANTITY_PRODUCERS:
        if scope not in producer.scopes:
            continue
        producer.input[scope] = [
            Quantity(template.name.format(**parameters))
            for template in producer.input[scope]
        ]
        # resolved input inherits shifts from the (now-concrete) column it was
        # templated from, so this producer's output follows e.g. tau-ID SF shifts --
        # matches selection_friends.py's _resolve_templated_quantities exactly
        for column in producer.input[scope]:
            for output_quantity in producer.output:
                column.adopt(output_quantity, scope)


def _product_step(scope, step_name, running_quantity, running_type,
                   factor_quantity, factor_type, templated=False, output_quantity=None):
    """One event::quantity::Product<running_type,factor_type> step: running * factor ->
    a new running double Quantity, named step_name (or output_quantity, if given -- used
    for the chain's final step, whose output is the friend's public "weight" column). If
    templated, factor_quantity's name may contain a "{vs_ele_wp}"/"{vs_jet_wp}"
    placeholder -- the returned producer is registered in TEMPLATED_QUANTITY_PRODUCERS
    for resolve_templated_quantities()."""
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
    """weights::Gate: value_quantity if cond_quantity else 1.0 -- the tau-vsJet SF
    gating pattern (SF only applies to a genuine hadronic tau leg)."""
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


def build_weight_chain(configuration, scope: str, era: str, run2_eras) -> None:
    """Builds and registers the full `weight` producer chain for one scope (et/mt/tt).
    Adds producers/outputs to `configuration` directly. Not yet implemented for em
    (simpler formula, no tau leg) or embedding (separate weight structure entirely) --
    see project memory.

    Deliberately excluded from `weight` (see project memory for why): trigger SF
    (fragile/era-dependent, TauKITFlow's own trgweight has a documented history of
    crashing RDataFrame's JIT on missing branches), lumi (stays downstream, value still
    unresolved), zPt/topPt/ggH-NNLO (process-specific, not universal per-channel terms).
    """
    producers = []
    prefix = f"weight_{scope}"
    step = 0

    def next_name():
        nonlocal step
        step += 1
        return f"{prefix}_step{step}"

    # -- generator normalization: xsec * (1/nevents) * sign(genWeight)/negative_fraction
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

    # -- pileup
    p, running = _product_step(scope, next_name(), running, "double", q.puweight, "double")
    producers.append(p)

    # -- lepton id/iso (channel-specific)
    if scope == "mt":
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_mu_1, "double")
        producers.append(p)
        p, running = _product_step(scope, next_name(), running, "double", q.iso_wgt_mu_1, "double")
        producers.append(p)
    elif scope == "et":
        p, running = _product_step(scope, next_name(), running, "double", q.id_wgt_ele_wp90iso_1, "double")
        producers.append(p)
    # tt: no lepton leg

    # -- tau vsJet SF, gated per genuine leg (leg 1 only for tt/et absent, leg 2 always
    # present for et/mt; both legs for tt)
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

    # -- tau vsMu / vsEle SF, ungated (correctionlib already gen_match-aware), one or
    # both legs depending on channel
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

    # -- btag (Run3 only; channel != mm, but this friend never runs for mm)
    if era not in run2_eras:
        p, running = _product_step(scope, next_name(), running, "double", q.btag_weight, "float")
        producers.append(p)

    # -- MC campaign split (2024/2025/2026 halved-campaign correction), a plain
    # per-era constant known at code-gen time -- event::Define, no new C++
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
