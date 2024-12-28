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
                    "2018": "data/fake_factors/nmssm/2018/fake_factors_et.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/nmssm/2018/FF_corrections_et.json.gz",
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
                    "2018": "data/fake_factors/nmssm/2018/fake_factors_mt.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/2018/nmssm/FF_corrections_mt.json.gz",
                }
            ),
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "ff_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/nmssm/2018/fake_factors_tt.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/nmssm/2018/FF_corrections_tt.json.gz",
                }
            ),
        },
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            fakefactors.RawFakeFactors_nmssm_lt,
            fakefactors.FakeFactors_nmssm_lt,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.raw_fake_factor,
            q.fake_factor,
        ],
    )

    configuration.add_producers(
        ["tt"],
        [
            fakefactors.RawFakeFactors_nmssm_tt_1,
            fakefactors.RawFakeFactors_nmssm_tt_2,
            fakefactors.FakeFactors_nmssm_tt_1,
            fakefactors.FakeFactors_nmssm_tt_2,
        ],
    )

    configuration.add_outputs(
        ["tt"],
        [
            q.raw_fake_factor_1,
            q.raw_fake_factor_2,
            q.fake_factor_1,
            q.fake_factor_2,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
