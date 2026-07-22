from __future__ import annotations

import json
import os
from typing import List, Union

import correctionlib
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift

from .fakefactors import NonClosureGranularity
from .producers import fakefactors_ml as fakefactors_ml
from .producers import nn_output as nn_output
from .quantities import output as q
from .scripts.CROWNWrapper import (defaults,
                                   get_adjusted_add_shift_SystematicShift)


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
        era, sample, scopes, shifts, available_sample_types, available_eras, available_scopes, quantities_map
    )

    non_closure_granularity = NonClosureGranularity("coarse")
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)
    USE_SPLIT_INFO_PRODUCER = False

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

    if "mt" in scopes:
        base_ml = "payloads/fake_factors_ml/models"
        base_ff_path = "2018/onnx_model/ff/model.onnx"
        base_nn_output_path = "2018/onnx_model/nn_output/model.onnx"

        def get_model_path(process):
            return f"{base_ml}/{process}/{base_ff_path if 'fractions' not in process else base_nn_output_path}"

        configuration.add_config_parameters(
            ["mt"],
            {
                # ---
                "model_ff_QCD": get_model_path("QCD"),
                "model_ff_QCD_Up": get_model_path("QCD_Up"),
                "model_ff_QCD_Down": get_model_path("QCD_Down"),
                "model_ff_QCD_StatUp": get_model_path("QCD_StatUp"),
                "model_ff_QCD_StatDown": get_model_path("QCD_StatDown"),
                "model_ff_QCD_NormalizationUp": get_model_path("QCD_NormalizationUp"),
                "model_ff_QCD_NormalizationDown": get_model_path("QCD_NormalizationDown"),
                # ---
                "model_ff_Wjets": get_model_path("Wjets"),
                "model_ff_Wjets_Up": get_model_path("Wjets_Up"),
                "model_ff_Wjets_Down": get_model_path("Wjets_Down"),
                "model_ff_Wjets_StatUp": get_model_path("Wjets_StatUp"),
                "model_ff_Wjets_StatDown": get_model_path("Wjets_StatDown"),
                "model_ff_Wjets_NormalizationUp": get_model_path("Wjets_NormalizationUp"),
                "model_ff_Wjets_NormalizationDown": get_model_path("Wjets_NormalizationDown"),
                # ---
                "model_ff_ttbar": get_model_path("ttbar"),
                "model_ff_ttbar_Up": get_model_path("ttbar_Up"),
                "model_ff_ttbar_Down": get_model_path("ttbar_Down"),
                "model_ff_ttbar_StatUp": get_model_path("ttbar_StatUp"),
                "model_ff_ttbar_StatDown": get_model_path("ttbar_StatDown"),
                "model_ff_ttbar_NormalizationUp": get_model_path("ttbar_NormalizationUp"),
                "model_ff_ttbar_NormalizationDown": get_model_path("ttbar_NormalizationDown"),
                # ---
                "model_fractions": get_model_path("fractions"),
                "model_fractions_QCD_Up": get_model_path("fractions_QCD_Up"),
                "model_fractions_QCD_Down": get_model_path("fractions_QCD_Down"),
                "model_fractions_Wjets_Up": get_model_path("fractions_Wjets_Up"),
                "model_fractions_Wjets_Down": get_model_path("fractions_Wjets_Down"),
                "model_fractions_ttbar_Up": get_model_path("fractions_ttbar_Up"),
                "model_fractions_ttbar_Down": get_model_path("fractions_ttbar_Down"),
                "model_fractions_QCD_StatUp": get_model_path("fractions_QCD_StatUp"),
                "model_fractions_QCD_StatDown": get_model_path("fractions_QCD_StatDown"),
                "model_fractions_Wjets_StatUp": get_model_path("fractions_Wjets_StatUp"),
                "model_fractions_Wjets_StatDown": get_model_path("fractions_Wjets_StatDown"),
                "model_fractions_ttbar_StatUp": get_model_path("fractions_ttbar_StatUp"),
                "model_fractions_ttbar_StatDown": get_model_path("fractions_ttbar_StatDown"),
                # ---
                "model_DR_SR_correction_QCD": get_model_path("QCD_DR_SR_correction"),
                "model_DR_SR_correction_QCD_Up": get_model_path("QCD_DR_SR_correction_Up"),
                "model_DR_SR_correction_QCD_Down": get_model_path("QCD_DR_SR_correction_Down"),
                "model_DR_SR_correction_QCD_StatUp": get_model_path("QCD_DR_SR_correction_StatUp"),
                "model_DR_SR_correction_QCD_StatDown": get_model_path("QCD_DR_SR_correction_StatDown"),
                "model_DR_SR_correction_QCD_NormalizationUp": get_model_path("QCD_DR_SR_correction_NormalizationUp"),
                "model_DR_SR_correction_QCD_NormalizationDown": get_model_path("QCD_DR_SR_correction_NormalizationDown"),
                # ---
                "model_DR_SR_correction_Wjets": get_model_path("Wjets_DR_SR_correction"),
                "model_DR_SR_correction_Wjets_Up": get_model_path("Wjets_DR_SR_correction_Up"),
                "model_DR_SR_correction_Wjets_Down": get_model_path("Wjets_DR_SR_correction_Down"),
                "model_DR_SR_correction_Wjets_StatUp": get_model_path("Wjets_DR_SR_correction_StatUp"),
                "model_DR_SR_correction_Wjets_StatDown": get_model_path("Wjets_DR_SR_correction_StatDown"),
                "model_DR_SR_correction_Wjets_NormalizationUp": get_model_path("Wjets_DR_SR_correction_NormalizationUp"),
                "model_DR_SR_correction_Wjets_NormalizationDown": get_model_path("Wjets_DR_SR_correction_NormalizationDown"),
                # ---
                "ff_QCD_variation": "nominal",
                "ff_Wjets_variation": "nominal",
                "ff_ttbar_variation": "nominal",
                "ml_fractions_variation": "nominal",
                "QCD_DR_SR_correction_variation": "nominal",
                "Wjets_DR_SR_correction_variation": "nominal",
                # ---
                "QCD_non_closure_correction": "nominal",
                "Wjets_non_closure_correction": "nominal",
                "ttbar_non_closure_correction": "nominal",
                # ---
                "corr_file": EraModifier({
                    "2018": "payloads/fake_factors_ml/classic_corrections/2018/with_embedding/FF_corrections_mt.json.gz",
                }),
            },
        )

        active_ff_producer = [fakefactors_ml.FakeFactors_ml_lt_split_info, fakefactors_ml.FakeFactors_ml_lt] if USE_SPLIT_INFO_PRODUCER else [fakefactors_ml.FakeFactors_ml_lt]
        configuration.add_producers(
            ["mt"],
            [
                nn_output.VariableConversionToFloatProducerGroup,
                nn_output.event_parity_Float,
                fakefactors_ml.FFModelInput_QCD_lt,
                fakefactors_ml.FFModelInput_Wjets_lt,
                fakefactors_ml.FFModelInput_ttbar_lt,
                fakefactors_ml.FFModelInput_fractions_lt,
                fakefactors_ml.FFModelInput_DR_QCD_lt,
                fakefactors_ml.FFModelInput_DR_Wjets_lt,
                fakefactors_ml.FFModelInput_NC_lt,
                *active_ff_producer,
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
        ] if USE_SPLIT_INFO_PRODUCER else [q.fake_factor_2]

        configuration.add_outputs(["mt"], active_outputs)

        ml_systematics = {
            "ff_QCD_variation": ["Up", "Down", "StatUp", "StatDown", "NormalizationUp", "NormalizationDown"],
            "ff_Wjets_variation": ["Up", "Down", "StatUp", "StatDown", "NormalizationUp", "NormalizationDown"],
            "ff_ttbar_variation": ["Up", "Down", "StatUp", "StatDown", "NormalizationUp", "NormalizationDown"],
            "QCD_DR_SR_correction_variation": ["Up", "Down", "StatUp", "StatDown", "NormalizationUp", "NormalizationDown"],
            "Wjets_DR_SR_correction_variation": ["Up", "Down", "StatUp", "StatDown", "NormalizationUp", "NormalizationDown"],
        }

        ml_fractions_systematics = {
            "ml_fractions_variation": [
                "QCD_Up", "QCD_Down",
                "Wjets_Up", "Wjets_Down",
                "ttbar_Up", "ttbar_Down",
                "QCD_StatUp", "QCD_StatDown",
                "Wjets_StatUp", "Wjets_StatDown",
                "ttbar_StatUp", "ttbar_StatDown",
            ]
        }

        with defaults(
            scopes="mt",
            producers=[fakefactors_ml.FakeFactors_ml_lt]
        ):
            for config_key, uncs in ml_systematics.items():
                sys_prefix = config_key.replace("_variation", "")
                for unc in uncs:
                    add_shift(
                        name=f"{sys_prefix}",
                        shift_key=config_key,
                        shift_map={unc: unc}
                    )

            for config_key, uncs in ml_fractions_systematics.items():
                for unc in uncs:
                    if unc in ("StatUp", "StatDown"):
                        frac_name = "fractions_Stat"
                        frac_key = unc
                    else:
                        frac_name = f"fractions_{unc.split('_')[0]}"
                        frac_key = unc.split("_")[1]
                    add_shift(
                        name=frac_name,
                        shift_key=config_key,
                        shift_map={frac_key: unc}
                    )

        if era == "2018":
            all_variations = (
                (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
                for corrections in (
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
                    if "_correction" not in _key:
                        continue

                    configuration.add_shift(
                        SystematicShift(
                            name=f"{_name}{_shift}",
                            shift_config={("mt",): {_key: f"{_name}{_shift}"}},
                            producers={("mt",): active_ff_producer},
                        ),
                    )

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
