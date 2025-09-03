from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):

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

    configuration.add_producers(
        ["mt", "et", "tt"],
        [
            pairquantities.FastMTTQuantities,
        ],
    )

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.m_fastmtt,
            q.pt_fastmtt,
            q.eta_fastmtt,
            q.phi_fastmtt,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
