from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from .selection_config import (
    FRIEND_MASK_GROUPS,
    add_selection,
    restrict_selection_shifts,
)


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

    # Every shift the input ntuple carries is propagated to the preselection:
    # the flags read their columns from the ntuple, so `optimize()` swaps in the
    # shifted copy of each of them and `presel_mask` inherits the shift. The
    # fake factor regions are frozen to nominal below.
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
        friend=True,
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
