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

# the column each friend variant reads, as the call of its main variant writes
# it. `friend_flags` fills in the working points and the era dependent ditau
# flag from the configuration parameters.
FRIEND_COLUMNS = {
    selection.PreselTriggerFlag_friend: "{presel_trigger_flag}",
    selection.PreselTriggerFlag_tt_friend: "{presel_trigger_flag}",
    selection.PreselVsEleTauID_1_friend: "id_tau_vsEle_{presel_vsele_wp}_1",
    selection.PreselVsEleTauID_2_friend: "id_tau_vsEle_{presel_vsele_wp}_2",
    selection.PreselVsMuTauID_1_friend: "id_tau_vsMu_{presel_vsmu_wp}_1",
    selection.PreselVsMuTauID_2_friend: "id_tau_vsMu_{presel_vsmu_wp}_2",
    selection.TauIsoFlag_1_friend: "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1",
    selection.TauIsoFlag_2_friend: "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2",
    selection.TauNonIsoFlag_1_friend: "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1",
    selection.TauNonIsoFlag_2_friend: "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2",
    selection.TauVVVLooseFlag_1_friend: "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_1",
    selection.TauVVVLooseFlag_2_friend: "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_2",
}


def friend_flags(configuration, scope: str):
    """Point the friend variants at the columns the parameters of `scope` name.

    Their input is what this production matches against the shift map of the
    ntuple, so it has to be a quantity carrying the resolved column name, which
    is only known once `add_selection` added the parameters. Handed to
    `add_selection`, which calls this once the parameters are in.
    """
    parameters = configuration.config_parameters[scope]
    for producer, template in FRIEND_COLUMNS.items():
        if scope not in producer.scopes:
            continue
        column = Quantity(template.format(**parameters))
        for output_quantity in producer.output:
            column.adopt(output_quantity, scope)
        producer.input[scope] = [column]
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
