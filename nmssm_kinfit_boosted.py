from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import hhkinfit as hhkinfit
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
            hhkinfit.YHKinFit_boosted,
        ],
    )

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.kinfit_convergence_YToBB_boosted,
            q.kinfit_mX_YToBB_boosted,
            q.kinfit_mY_YToBB_boosted,
            q.kinfit_mh_YToBB_boosted,
            q.kinfit_chi2_YToBB_boosted,
            q.kinfit_prob_YToBB_boosted,
            q.kinfit_convergence_YToTauTau_boosted,
            q.kinfit_mX_YToTauTau_boosted,
            q.kinfit_mY_YToTauTau_boosted,
            q.kinfit_mh_YToTauTau_boosted,
            q.kinfit_chi2_YToTauTau_boosted,
            q.kinfit_prob_YToTauTau_boosted,
            q.kinfit_convergence_boosted,
            q.kinfit_mX_boosted,
            q.kinfit_mY_boosted,
            q.kinfit_mh_boosted,
            q.kinfit_chi2_boosted,
            q.kinfit_prob_boosted,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
