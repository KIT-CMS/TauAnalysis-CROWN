"""
Weights friend (Phase 3, in progress) -- see project memory
(crown-weights-friend-project-status.md) for the full phased plan.

Produces:
- crossSectionPerEventWeight / numberGeneratedEventsWeight / negative_events_fraction:
  per-file MC normalization constants, replacing the legacy Python
  xsec/build_friend_tree.py KingMaker friend task with a CROWN producer (see
  cpp_addons/src/normalization.cxx -- ROOT's DefinePerSample looks up this file's
  sample nick, parsed at runtime from the input path, in a per-(sample_type,era) table
  generated at code-gen time from sample_database).
- weight: the combined per-event MC weight for et/mt/tt (see producers/weights.py's
  build_weight_chain() for exactly what's folded in and what's deliberately excluded --
  trigger SF, lumi, process-specific terms). em/mm/ee not implemented yet: constant 1.0,
  same reasoning as the data/embedding fallback below.

Deliberately its own FriendTreeConfiguration, not folded into selection_friends.py:
keeps a database-content rebuild from forcing a rebuild of the mask/gen_category
friend, at the cost of consumers attaching two friends instead of one.

For data/embedding, where there is no per-nick normalization or MC weight to compute,
the same columns are still produced, as a constant 1.0 -- a friend with a different
schema (or no friend at all) per sample_type breaks downstream code that attaches this
friend and multiplies by these columns uniformly across samples. CROWN's own framework
refuses to build a friend with zero producers/outputs (confirmed empirically), so this
isn't optional -- data/embedding need *something* wired, not just a skip.

Not yet wired downstream (TFF/TauKITFlow still read the legacy xsec friend or their own
gen_weight()/mc_weights strings); needs to be built and validated against real ntuples
first (weight and its components must byte-match the legacy per-nick, per event).
"""
from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from . import normalization
from .producers import normalization as normalization_producers
from .producers import weights as weight_producers
from .quantities import output as q

# samples with no per-nick normalization to look up (matches
# normalization.build_norm_table()'s own skip list) -- these get the
# constant-1.0 fake-normalization producers instead, see module docstring
NO_NORMALIZATION_SAMPLES = ("data", "embedding", "embedding_mc")

# channels build_weight_chain() implements a real formula for; everything else
# (em/mm/ee) gets a constant-1.0 placeholder weight, same reasoning as the
# data/embedding fallback -- see module docstring
IMPLEMENTED_WEIGHT_CHANNELS = ("et", "mt", "tt")

# Run2 eras -- btag_weight isn't produced there (see producers/weights.py); also used
# to pick vs_ele_wp's WP_DEFAULTS is channel-only so this doesn't affect that.
RUN2_ERAS = ("2016preVFP", "2016postVFP", "2017", "2018")

# vsEle WP per channel: the SF's own gen_match-aware behavior means this must match
# the tau's own preselection vsEle WP for that channel (TauKITFlow's
# config.analysis.vs_ele_wp_for(): "Tight" for et -- the electron leg needs the
# tighter cut against electron fakes -- "VVLoose" for every other channel). Config
# parameter, not hardcoded into a producer/cpp_addons call: change a WP here, not there.
VS_ELE_WP_DEFAULTS = {"et": "Tight", "mt": "VVLoose", "tt": "VVLoose"}
# vsJet WP: fixed to Medium (the only WP CROWN produces an SF for -- config.py's
# vsjet_tau_id dict has only Medium uncommented for Run3); the plain ID flags at every
# WP (VVVLoose..Tight) still exist as selection_friends.py flags for the FF regions,
# just without an SF applied outside Medium.
VS_JET_WP_DEFAULT = "Medium"


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
) -> FriendTreeConfiguration:
    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    scopes_list = list(configuration.selected_scopes)
    if sample not in NO_NORMALIZATION_SAMPLES:
        norm_table_path = normalization.build_norm_table(
            era, sample, normalization.DATA_NORMALIZATION_DIR
        )
        configuration.add_config_parameters(
            scopes_list,
            {"norm_table_path": norm_table_path},
        )
        configuration.add_producers(
            scopes_list,
            [normalization_producers.SampleNormalization],
        )
        for scope in scopes_list:
            configuration.add_config_parameters(
                scope,
                {
                    "vs_ele_wp": VS_ELE_WP_DEFAULTS.get(scope, VS_ELE_WP_DEFAULTS["mt"]),
                    "vs_jet_wp": VS_JET_WP_DEFAULT,
                },
            )
            if scope in IMPLEMENTED_WEIGHT_CHANNELS:
                weight_producers.build_weight_chain(configuration, scope, era, RUN2_ERAS)
                weight_producers.resolve_templated_quantities(configuration, scope)
            else:
                configuration.add_producers(scope, [weight_producers.ConstantWeight])
                configuration.add_outputs(scope, [q.weight])
    else:
        configuration.add_producers(
            scopes_list,
            [
                normalization_producers.ConstantCrossSectionPerEventWeight,
                normalization_producers.ConstantNumberGeneratedEventsWeight,
                normalization_producers.ConstantNegativeEventsFraction,
                weight_producers.ConstantWeight,
            ],
        )
        configuration.add_outputs(scopes_list, [q.weight])
    configuration.add_outputs(
        scopes_list,
        [
            q.crossSectionPerEventWeight,
            q.numberGeneratedEventsWeight,
            q.negative_events_fraction,
        ],
    )

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
