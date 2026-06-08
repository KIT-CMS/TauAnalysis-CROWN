from __future__ import annotations  # needed for type annotations in > python 3.7

import json
import os
from dataclasses import dataclass, field
from typing import List, Union, Callable

import correctionlib
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift

from .producers import fakefactors as fakefactors
from .producers import ml as ml
from .quantities import output as q

@dataclass
class NonClosureGranularity:
    granularity: str
    coarse_check: Callable[[str], bool] = field(default=lambda x: "_non_closure_Corr" in x)

    def check(self, name: str) -> bool:
        if self.granularity == "both":
            return True
        is_coarse = self.coarse_check(name)

        if self.granularity == "coarse":
            return is_coarse

        if self.granularity == "fine":
            return not is_coarse

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

    non_closure_granularity = NonClosureGranularity("coarse")  # "both", "coarse", "fine"
    USE_SPLIT_INFO_PRODUCER = False

    # --- helper ---

    def ff_process_name(name: str) -> str:
        if name == "process_fractions_subleading":
            return "fraction_variation_subleading"
        if name == "process_fractions":
            return "fraction_variation"

        if name.startswith("QCD_subleading_"):
            process = "QCD_subleading"
            remainder = name[len("QCD_subleading_"):]
        else:
            process = name.split("_")[0]
            remainder = name[len(process) + 1:]

        if remainder == "fake_factors":
            return f"{process}_variation"

        if "DR_SR" in remainder:
            return f"{process}_DR_SR_correction"

        return f"{process}_non_closure_correction"

    def load_ff_correctionlib(path: str) -> correctionlib.CorrectionSet:
        path = os.path.join("analysis_configurations/tau", path)
        return json.loads(correctionlib.CorrectionSet.from_file(path)._data)["corrections"]

    def apply_variation_based_on_granularity(name: str) -> bool:
        if "non_closure" not in name:
            return True
        return non_closure_granularity.check(name)

    # ---


    configuration.add_config_parameters(
        ["et"],
        {
            "fraction_variation": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_DR_SR_correction": "nominal",
            "QCD_non_closure_correction": "nominal",
            # ---------------------------------------
            "Wjets_variation": "nominal",
            "Wjets_DR_SR_correction": "nominal",
            "Wjets_non_closure_correction": "nominal",
            # ---------------------------------------
            "ttbar_variation": "nominal",
            "ttbar_non_closure_correction": "nominal",
            # ---------------------------------------
            "file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "",
                    "2022preEE": "payloads/fake_factors/sm/2022/fake_factors_et.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/fake_factors_et.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/fake_factors_et.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/fake_factors_et.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/fake_factors_et.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/fake_factors_et.json.gz",
                }
            ),
            "corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "",
                    "2022preEE": "payloads/fake_factors/sm/2022/FF_corrections_et.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/FF_corrections_et.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/FF_corrections_et.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/FF_corrections_et.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/FF_corrections_et.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/FF_corrections_et.json.gz",
                }
            ),
        },
    )
    configuration.add_producers(
        ["et"],
        [
            ml.VariableConversionToFloatProducerGroup,
            fakefactors.FFInput_lt,
            fakefactors.FFInput_fractions_lt,
            fakefactors.FFInput_DR_lt,
            fakefactors.FFInput_NC_lt,
            fakefactors.RawFakeFactors_sm_lt,
            fakefactors.FakeFactors_sm_lt,
        ],
    )
    configuration.add_outputs(
        ["et"],
        [
            q.raw_fake_factor_2,
            q.fake_factor_2,
        ],
    )

    all_variations = (
        (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
        for corrections in (
            load_ff_correctionlib(configuration.config_parameters["et"]["file"]),
            load_ff_correctionlib(configuration.config_parameters["et"]["corr_file"]),
        )
        for correction in corrections
        for value in correction["data"]["content"]
        if value["key"].endswith("Up")
        # ("<producer variation argument>", "<variation name without direction>")
    )

    for _key, _name in set(all_variations):
        if not apply_variation_based_on_granularity(_name):
            continue
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.FakeFactors_sm_lt, fakefactors.RawFakeFactors_sm_lt)
            if "_correction" in _key:
                variables = (fakefactors.FakeFactors_sm_lt,)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={("et",): {_key: f"{_name}{_shift}"}},
                    producers={("et",): variables},
                ),
            )

    #-------

    configuration.add_config_parameters(
        ["mt"],
        {
            "fraction_variation": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_DR_SR_correction": "nominal",
            "QCD_non_closure_correction": "nominal",
            # ---------------------------------------
            "Wjets_variation": "nominal",
            "Wjets_DR_SR_correction": "nominal",
            "Wjets_non_closure_correction": "nominal",
            # ---------------------------------------
            "ttbar_variation": "nominal",
            "ttbar_non_closure_correction": "nominal",
            # ---------------------------------------
            "file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/with_embedding/fake_factors_mt.json.gz",
                    "2022preEE": "payloads/fake_factors/sm/2022/fake_factors_mt.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/fake_factors_mt.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/fake_factors_mt.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/fake_factors_mt.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/fake_factors_mt.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/fake_factors_mt.json.gz",
                }
            ),
            "corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/with_embedding/FF_corrections_mt.json.gz",
                    "2022preEE": "payloads/fake_factors/sm/2022/FF_corrections_mt.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/FF_corrections_mt.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/FF_corrections_mt.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/FF_corrections_mt.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/FF_corrections_mt.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/FF_corrections_mt.json.gz",
                }
            ),
        },
    )
    configuration.add_producers(
        ["mt"],
        [
            ml.VariableConversionToFloatProducerGroup,
            fakefactors.FFInput_lt,
            fakefactors.FFInput_fractions_lt,
            fakefactors.FFInput_DR_lt,
            fakefactors.FFInput_NC_lt,
            fakefactors.RawFakeFactors_sm_lt,
            fakefactors.FakeFactors_sm_lt,
        ],
    )
    configuration.add_outputs(
        ["mt"],
        [
            q.raw_fake_factor_2,
            q.fake_factor_2,
        ],
    )

    all_variations = (
        (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
        for corrections in (
            load_ff_correctionlib(configuration.config_parameters["mt"]["file"]),
            load_ff_correctionlib(configuration.config_parameters["mt"]["corr_file"]),
        )
        for correction in corrections
        for value in correction["data"]["content"]
        if value["key"].endswith("Up")
        # ("<producer variation argument>", "<variation name without direction>")
    )

    for _key, _name in set(all_variations):
        if not apply_variation_based_on_granularity(_name):
            continue
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.FakeFactors_sm_lt, fakefactors.RawFakeFactors_sm_lt)
            if "_correction" in _key:
                variables = (fakefactors.FakeFactors_sm_lt,)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={("mt",): {_key: f"{_name}{_shift}"}},
                    producers={("mt",): variables},
                ),
            )

    configuration.add_config_parameters(
        ["tt"],
        {
            "fraction_variation": "nominal",
            "fraction_variation_subleading": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_DR_SR_correction": "nominal",
            "QCD_non_closure_correction": "nominal",
            "QCD_subleading_variation": "nominal",
            "QCD_subleading_DR_SR_correction": "nominal",
            "QCD_subleading_non_closure_correction": "nominal",
            # ---------------------------------------
            "file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "",
                    "2022preEE": "payloads/fake_factors/sm/2022/fake_factors_tt.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/fake_factors_tt.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/fake_factors_tt.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/fake_factors_tt.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/fake_factors_tt.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/fake_factors_tt.json.gz",
                }
            ),
            "corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "",
                    "2022preEE": "payloads/fake_factors/sm/2022/FF_corrections_tt.json.gz",
                    "2022postEE": "payloads/fake_factors/sm/2022/FF_corrections_tt.json.gz",
                    "2023preBPix": "payloads/fake_factors/sm/2023/FF_corrections_tt.json.gz",
                    "2023postBPix": "payloads/fake_factors/sm/2023/FF_corrections_tt.json.gz",
                    "2024": "payloads/fake_factors/sm/2024/FF_corrections_tt.json.gz",
                    "2025": "payloads/fake_factors/sm/2025/FF_corrections_tt.json.gz",
                }
            ),
        },
    )
    configuration.add_producers(
        ["tt"],
        [
            ml.VariableConversionToFloatProducerGroup,
            fakefactors.FFInput_QCD_tt,
            fakefactors.FFInput_QCDsub_tt,
            fakefactors.FFInput_fractions_tt,
            fakefactors.FFInput_DR_tt,
            fakefactors.FFInput_NC_QCD_tt,
            fakefactors.FFInput_NC_QCDsub_tt,
            fakefactors.RawFakeFactors_sm_tt_1,
            fakefactors.FakeFactors_sm_tt_1,
            fakefactors.RawFakeFactors_sm_tt_2,
            fakefactors.FakeFactors_sm_tt_2,
        ],
    )
    configuration.add_outputs(
        ["tt"],
        [   
            q.raw_fake_factor_1,
            q.fake_factor_1,
            q.raw_fake_factor_2,
            q.fake_factor_2,
        ],
    )

    all_variations = (
        (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
        for corrections in (
            load_ff_correctionlib(configuration.config_parameters["tt"]["file"]),
            load_ff_correctionlib(configuration.config_parameters["tt"]["corr_file"]),
        )
        for correction in corrections
        for value in correction["data"]["content"]
        if value["key"].endswith("Up")
        # ("<producer variation argument>", "<variation name without direction>")
    )

    for _key, _name in set(all_variations):
        if not apply_variation_based_on_granularity(_name):
            continue
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.RawFakeFactors_sm_tt_1, fakefactors.RawFakeFactors_sm_tt_2, 
                        fakefactors.FakeFactors_sm_tt_1, fakefactors.FakeFactors_sm_tt_2)
            if "_correction" in _key:
                variables = (fakefactors.FakeFactors_sm_tt_1, fakefactors.FakeFactors_sm_tt_2)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={("tt",): {_key: f"{_name}{_shift}"}},
                    producers={("tt",): variables},
                ),
            )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
