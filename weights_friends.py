"""
Weights friend (Phase 3, in progress) -- see project memory
(crown-weights-friend-project-status.md) for the full phased plan.

Currently produces only the per-file MC normalization constants
(crossSectionPerEventWeight, numberGeneratedEventsWeight,
negative_events_fraction), replacing the legacy Python
xsec/build_friend_tree.py KingMaker friend task with a CROWN producer (see
cpp_addons/src/normalization.cxx -- ROOT's DefinePerSample looks up this
file's sample nick, parsed at runtime from the input path, in a
per-(sample_type,era) table generated at code-gen time from
sample_database). Deliberately its own FriendTreeConfiguration, not folded
into selection_friends.py: keeps a database-content rebuild from forcing a
rebuild of the mask/gen_category friend, at the cost of consumers attaching
two friends instead of one.

For data/embedding, where there is no per-nick normalization to look up,
the same three columns are still produced, as a constant 1.0 -- a friend
with a different schema (or no friend at all) per sample_type breaks
downstream code that attaches this friend and multiplies by these columns
uniformly across samples. CROWN's own framework refuses to build a friend
with zero producers/outputs (confirmed empirically), so this isn't
optional -- data/embedding need *something* wired, not just a skip.

Not yet wired downstream (TFF/TauKITFlow still read the legacy xsec friend
or their own gen_weight()); needs to be built and validated against real
ntuples first (numberGeneratedEventsWeight/crossSectionPerEventWeight must
byte-match the legacy friend's output, per nick, before any cutover).
"""
from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from . import normalization
from .producers import normalization as normalization_producers
from .quantities import output as q

# samples with no per-nick normalization to look up (matches
# normalization.build_norm_table()'s own skip list) -- these get the
# constant-1.0 fake-normalization producers instead, see module docstring
NO_NORMALIZATION_SAMPLES = ("data", "embedding", "embedding_mc")


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
    else:
        configuration.add_producers(
            scopes_list,
            [
                normalization_producers.ConstantCrossSectionPerEventWeight,
                normalization_producers.ConstantNumberGeneratedEventsWeight,
                normalization_producers.ConstantNegativeEventsFraction,
            ],
        )
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
