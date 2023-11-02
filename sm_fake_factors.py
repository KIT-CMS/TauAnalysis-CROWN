from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import fakefactors as fakefactors
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier


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

    # fake factor configurations
    configuration.add_config_parameters(
        ["et"],
        {
            "ff_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/sm/2018/fake_factors_et.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/sm/2018/FF_corrections_et.json.gz",
                }
            ),
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "ff_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/sm/2018/fake_factors_mt.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/sm/2018/FF_corrections_mt.json.gz",
                }
            ),
        },
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            fakefactors.RawFakeFactors_sm_lt,
            fakefactors.FakeFactors_sm_lt,
	    # fakefactors.FakeFactors_sm_lt_nodR,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.raw_fake_factor,
            q.raw_qcd_fake_factor,
            q.raw_wjets_fake_factor,
            q.raw_ttbar_fake_factor,
            q.fake_factor,
            q.ttbar_fake_factor,
            q.wjets_fake_factor,
            q.qcd_fake_factor,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
