from __future__ import annotations  # needed for type annotations in > python 3.7
import json
import os
from typing import List, Union
import correctionlib
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift
from .producers import fakefactors as fakefactors
from .quantities import output as q


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

    # ---

    if "et" in scopes:
        raise NotImplementedError("The ET scope is not implemented yet.")

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
                        "2018": "payloads/fake_factors/sm/2018/with_embedding/fake_factors_mt.json.gz",
                    }
                ),
                "corr_file": EraModifier(
                    {
                        "2016": "",
                        "2017": "",
                        "2018": "payloads/fake_factors/sm/2018/with_embedding/FF_corrections_mt.json.gz",
                    }
                ),
            },
        )
        configuration.add_producers(
            ["mt"],
            [
                fakefactors.RawFakeFactors_sm_lt,
                fakefactors.FakeFactors_sm_lt,
                fakefactors.FakeFactors_sm_lt_split_info,
            ],
        )
        configuration.add_outputs(
            ["mt"],
            [
                q.raw_fake_factor_2,
                q.fake_factor_2,
                # ----------------------
                q.raw_qcd_fake_factor_2,
                q.raw_wjets_fake_factor_2,
                q.raw_ttbar_fake_factor_2,
                # ---
                q.qcd_fake_factor_fraction_2,
                q.wjets_fake_factor_fraction_2,
                q.ttbar_fake_factor_fraction_2,
                # ---
                q.qcd_DR_SR_correction_2,
                q.wjets_DR_SR_correction_2,
                q.ttbar_DR_SR_correction_2,
                # ---
                q.qcd_correction_wo_DR_SR_2,
                q.wjets_correction_wo_DR_SR_2,
                q.ttbar_correction_wo_DR_SR_2,
                # ---
                q.qcd_fake_factor_correction_2,
                q.wjets_fake_factor_correction_2,
                q.ttbar_fake_factor_correction_2,
                # ---
                q.qcd_fake_factor_2,
                q.wjets_fake_factor_2,
                q.ttbar_fake_factor_2,
            ],
        )

        for _key, _name in [
            (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
            for corrections in (
                load_ff_correctionlib(configuration.config_parameters["mt"]["file"]),
                load_ff_correctionlib(configuration.config_parameters["mt"]["corr_file"]),
            )
            for correction in corrections
            for value in correction["data"]["content"]
            if value["key"].endswith("Up")
            # ("<producer variation argument>", "<variation name without direction>")
        ]:
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

    if "tt" in scopes:
        raise NotImplementedError("The TT scope is not implemented yet.")

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
