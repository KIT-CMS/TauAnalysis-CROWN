from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from .producers import selection as selection
from .scripts.CROWNWrapper import Quantity
from .selection_config import (
    FRIEND_MASK_GROUPS,
    add_selection,
    restrict_selection_shifts,
)


##############################################################################
# main production producer -> the variant this production uses instead
##############################################################################

FRIEND_FLAGS = {
    selection.PreselTriggerFlag: selection.PreselTriggerFlag_friend,
    selection.PreselTriggerFlag_tt: selection.PreselTriggerFlag_tt_friend,
    selection.PreselVsEleTauID_1: selection.PreselVsEleTauID_1_friend,
    selection.PreselVsEleTauID_2: selection.PreselVsEleTauID_2_friend,
    selection.PreselVsMuTauID_1: selection.PreselVsMuTauID_1_friend,
    selection.PreselVsMuTauID_2: selection.PreselVsMuTauID_2_friend,
    selection.TauIsoFlag_1: selection.TauIsoFlag_1_friend,
    selection.TauIsoFlag_2: selection.TauIsoFlag_2_friend,
    selection.TauNonIsoFlag_1: selection.TauNonIsoFlag_1_friend,
    selection.TauNonIsoFlag_2: selection.TauNonIsoFlag_2_friend,
    selection.TauVVVLooseFlag_1: selection.TauVVVLooseFlag_1_friend,
    selection.TauVVVLooseFlag_2: selection.TauVVVLooseFlag_2_friend,
}

def friend_flags(configuration, scope: str):
    """Resolve the columns of the friend variants for `scope`.

    Each of them spells its column with the parameters of the call of its main
    variant, `id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2` and the like. The values are
    only known once `add_selection` added the parameters, so it is what calls
    this, and the resolved name is what this production matches against the
    shift map of the ntuple.
    """
    parameters = configuration.config_parameters[scope]
    for producer in FRIEND_FLAGS.values():
        if scope not in producer.scopes:
            continue
        # a new quantity per scope, the template one is shared between them
        producer.input[scope] = [
            Quantity(template.name.format(**parameters))
            for template in producer.input[scope]
        ]
        for column in producer.input[scope]:
            for output_quantity in producer.output:
                column.adopt(output_quantity, scope)
    return FRIEND_FLAGS


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

    # Every shift the input ntuple carries is propagated to the preselection
    shifts_to_add = [
        "__" + shift
        for scope in configuration.selected_scopes
        for shift in configuration.requested_shifts[scope]
        if shift != "nominal"
    ]

    #########################
    # The selection masks
    #########################

    if not FRIEND_MASK_GROUPS:
        raise ValueError(
            "`NTUPLE_MASK_GROUPS` of `selection_config.py` already covers every "
            "mask group, so there is nothing left for a friend tree. Drop a "
            "group there to produce it here instead."
        )

    configuration = add_selection(
        configuration,
        scopes,
        era,
        sample,
        apply_preselection_filter=False,
        friend_flags=friend_flags,
        groups=FRIEND_MASK_GROUPS,
    )

    # the regions that are only consumed on nominal ntuples do not need a copy
    # per systematic shift, this has to run before the shifts are added
    configuration = restrict_selection_shifts(
        configuration, configuration.selected_scopes, shifts=shifts_to_add
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
