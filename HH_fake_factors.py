from __future__ import annotations  # needed for type annotations in > python 3.7

import json
import os
from dataclasses import dataclass, field
from typing import List, Union, Callable

import correctionlib
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift

from .producers import fakefactors_test as fakefactors
# from .producers import ml as ml
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
        if "process_fractions" in name:
            return "fraction_variation"

        process = name.split("_")[0]  # QCD, Wjets, ttbar
        if "fake_factors" in name:
            return f"{process}_variation"

        suffix = "DR_SR" if "DR_SR" in name else "non_closure"
        return f"{process}_{suffix}_correction"

    def load_ff_correctionlib(path: str) -> correctionlib.CorrectionSet:
        path = os.path.join("analysis_configurations/tau", path)
        return json.loads(correctionlib.CorrectionSet.from_file(path)._data)["corrections"]

    def apply_variation_based_on_granularity(name: str) -> bool:
        if "non_closure" not in name:
            return True
        return non_closure_granularity.check(name)

    # ---

    if "et" in scopes:
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
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/fake_factors_et.json.gz",
                    }
                ),
                "corr_file": EraModifier(
                    {
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/FF_corrections_et.json.gz",
                    }
                ),
            },
        )

    if "mt" in scopes:
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
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/fake_factors_mt.json.gz",
                    }
                ),
                "corr_file": EraModifier(
                    {
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/FF_corrections_mt.json.gz",
                    }
                ),
            },
        )
    
    if "tt" in scopes:
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
                "ttbar_variation": "nominal",
                "ttbar_non_closure_correction": "nominal",
                "ttbar_subleading_variation": "nominal",
                "ttbar_subleading_non_closure_correction": "nominal",
                # ---------------------------------------
                "file": EraModifier(
                    {
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/fake_factors_tt.json.gz",
                    }
                ),
                "corr_file": EraModifier(
                    {
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/FF_corrections_tt.json.gz",
                    }
                ),
            },
        )
    
    if era == "2018":
        configuration.add_producers(
            ["et"],
            [
                fakefactors.VariableConversionToFloatProducerGroup,
                fakefactors.FFInput_QCD_2018_mt,
                fakefactors.FFInput_Wjets_2018_mt,
                fakefactors.FFInput_ttbar_2018_mt,
                fakefactors.FFInput_fractions_2018_mt,
                fakefactors.FFInput_DR_QCD_2018_mt,
                fakefactors.FFInput_DR_Wjets_2018_mt,
                fakefactors.FFInput_NC_QCD_2018_et,
                fakefactors.FFInput_NC_Wjets_2018_et,
                fakefactors.FFInput_NC_ttbar_2018_et,
                fakefactors.RawFakeFactors_sm_2018_mt,
                *([fakefactors.FakeFactors_sm_et_split_info, fakefactors.FakeFactors_sm_et] if USE_SPLIT_INFO_PRODUCER else [fakefactors.FakeFactors_sm_et]),
            ],
        )
        configuration.add_producers(
            ["mt"],
            [
                fakefactors.VariableConversionToFloatProducerGroup,
                fakefactors.FFInput_QCD_2018_mt,
                fakefactors.FFInput_Wjets_2018_mt,
                fakefactors.FFInput_ttbar_2018_mt,
                fakefactors.FFInput_fractions_2018_mt,
                fakefactors.FFInput_DR_QCD_2018_mt,
                fakefactors.FFInput_DR_Wjets_2018_mt,
                fakefactors.FFInput_NC_QCD_2018_mt,
                fakefactors.FFInput_NC_Wjets_2018_mt,
                fakefactors.FFInput_NC_ttbar_2018_mt,
                fakefactors.RawFakeFactors_sm_2018_mt,
                *([fakefactors.FakeFactors_sm_mt_split_info, fakefactors.FakeFactors_sm_mt] if USE_SPLIT_INFO_PRODUCER else [fakefactors.FakeFactors_sm_mt]),
            ],
        )

    active_outputs = [
        q.fake_factor_2,
        q.raw_qcd_fake_factor_2,
        q.raw_wjets_fake_factor_2,
        q.raw_ttbar_fake_factor_2,
        q.qcd_fake_factor_fraction_2,
        q.wjets_fake_factor_fraction_2,
        q.ttbar_fake_factor_fraction_2,
        q.qcd_DR_SR_correction_2,
        q.wjets_DR_SR_correction_2,
        q.ttbar_DR_SR_correction_2,
        q.qcd_correction_wo_DR_SR_2,
        q.wjets_correction_wo_DR_SR_2,
        q.ttbar_correction_wo_DR_SR_2,
        q.qcd_fake_factor_correction_2,
        q.wjets_fake_factor_correction_2,
        q.ttbar_fake_factor_correction_2,
        q.qcd_fake_factor_2,
        q.wjets_fake_factor_2,
        q.ttbar_fake_factor_2,
    ] if USE_SPLIT_INFO_PRODUCER else [q.raw_fake_factor_2 ,q.fake_factor_2]

    configuration.add_outputs(["mt", "et"], active_outputs)


    for scope in scopes:
        if scope == "et":
            scope_producer = fakefactors.FakeFactors_sm_et
        elif scope == "mt":
            scope_producer = fakefactors.FakeFactors_sm_mt
        elif scope == "tt":
            print("No systematic variations implemented for tt yet.")
            continue
        all_variations = (
            (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
            for corrections in (
                load_ff_correctionlib(configuration.config_parameters[scope]["file"]),
                load_ff_correctionlib(configuration.config_parameters[scope]["corr_file"]),
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
                configuration.add_shift(
                    SystematicShift(
                        name=f"{_name}{_shift}",
                        shift_config={(scope,): {_key: f"{_name}{_shift}"}},
                        producers={(scope,): (scope_producer,)},
                    ),
                )
    
    if "tt" in scopes:
        configuration.add_producers(
            ["tt"],
            [
                fakefactors.VariableConversionToFloatProducerGroup,
                fakefactors.RawFakeFactors_sm_tt_1,
                fakefactors.RawFakeFactors_sm_tt_2,
                fakefactors.FakeFactors_sm_tt_1,
                fakefactors.FakeFactors_sm_tt_2,
            ],
        )
        configuration.add_outputs(
            ["tt"],
            [
                q.raw_fake_factor_1,
                q.raw_fake_factor_2,
                q.fake_factor_1,
                q.fake_factor_2,
            ]
        )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
