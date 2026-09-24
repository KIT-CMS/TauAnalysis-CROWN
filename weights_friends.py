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
- weight: the combined per-event MC weight for et/mt/tt/em (see producers/weights.py's
  build_weight_chain() for exactly what's folded in and what's deliberately excluded --
  trigger SF, lumi, process-specific terms). mm/ee not implemented, and embedding left
  alone entirely (Run3 doesn't use it, and its weight structure differs enough that
  guessing risks a Run2 mistake for no Run3 benefit, per user direction): constant 1.0,
  same reasoning as the data fallback below.

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
from .wp_config import VSELE_WP, VSJET_WP

# samples with no per-nick normalization to look up (matches
# normalization.build_norm_table()'s own skip list) -- these get the
# constant-1.0 fake-normalization producers instead, see module docstring
NO_NORMALIZATION_SAMPLES = ("data", "embedding", "embedding_mc")

# channels build_weight_chain() implements a real formula for; everything else
# (mm/ee) gets a constant-1.0 placeholder weight, same reasoning as the
# data/embedding fallback -- see module docstring
IMPLEMENTED_WEIGHT_CHANNELS = ("et", "mt", "tt", "em")

# Run2 eras -- btag_weight isn't produced there (see producers/weights.py).
RUN2_ERAS = ("2016preVFP", "2016postVFP", "2017", "2018")

# vsEle/vsJet WPs: imported from wp_config.py, NOT duplicated here -- the same values
# selection_friends.py uses for presel_vsele_wp/ff_tau_iso_vsjet_wp, since the SF must
# be evaluated at whatever WP defines "selected" for the event. Config parameters, not
# hardcoded into a producer/cpp_addons call: change a WP in wp_config.py, not here or
# in selection_friends.py -- both friends pick it up automatically.


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
                    "vs_ele_wp": VSELE_WP.get(scope, VSELE_WP["mt"]),
                    "vs_jet_wp": VSJET_WP,
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
