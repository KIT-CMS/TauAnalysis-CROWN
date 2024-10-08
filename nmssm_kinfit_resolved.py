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
            hhkinfit.YHKinFit,
        ],
    )

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.kinfit_convergence_YToBB,
            q.kinfit_mX_YToBB,
            q.kinfit_mY_YToBB,
            q.kinfit_mh_YToBB,
            q.kinfit_chi2_YToBB,
            q.kinfit_prob_YToBB,
            q.kinfit_convergence_YToTauTau,
            q.kinfit_mX_YToTauTau,
            q.kinfit_mY_YToTauTau,
            q.kinfit_mh_YToTauTau,
            q.kinfit_chi2_YToTauTau,
            q.kinfit_prob_YToTauTau,
            q.kinfit_convergence,
            q.kinfit_mX,
            q.kinfit_mY,
            q.kinfit_mh,
            q.kinfit_chi2,
            q.kinfit_prob,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
