from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import fakefactors as fakefactors
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer


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
            "fraction_variation": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_DR_SR_correction": "nominal",
            "QCD_non_closure_leading_lep_pt_correction": "nominal",
            "QCD_non_closure_lep_iso_correction": "nominal",
            # ---------------------------------------
            "Wjets_variation": "nominal",
            "Wjets_DR_SR_correction": "nominal",
            "Wjets_non_closure_leading_lep_pt_correction": "nominal",
            # ---------------------------------------
            "ttbar_variation": "nominal",
            "ttbar_non_closure_m_vis_correction": "nominal",
            # ---------------------------------------
            "file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/fake_factors_et.json.gz",
                },
            ),
            "corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/FF_corrections_et.json.gz",
                },
            ),
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "fraction_variation": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_DR_SR_correction": "nominal",
            "QCD_non_closure_leading_lep_pt_correction": "nominal",
            "QCD_non_closure_lep_iso_correction": "nominal",
            # ---------------------------------------
            "Wjets_variation": "nominal",
            "Wjets_DR_SR_correction": "nominal",
            "Wjets_non_closure_leading_lep_pt_correction": "nominal",
            # ---------------------------------------
            "ttbar_variation": "nominal",
            "ttbar_non_closure_m_vis_correction": "nominal",
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

    configuration.add_config_parameters(
        ["tt"],
        {
            "fraction_variation": "nominal",
            "fraction_variation_subleading": "nominal",
            # ---------------------------------------
            "QCD_variation": "nominal",
            "QCD_subleading_variation": "nominal",
            # ---------------------------------------
            "QCD_DR_SR_correction": "nominal",
            "QCD_subleading_DR_SR_correction": "nominal",
            # ---------------------------------------
            "QCD_non_closure_m_vis_correction": "nominal",
            "QCD_subleading_non_closure_m_vis_correction": "nominal",
            # ---------------------------------------
            "QCD_non_closure_subleading_lep_pt_correction": "nominal",
            "QCD_subleading_non_closure_leading_lep_pt_correction": "nominal",
            # ---------------------------------------
            "file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/fake_factors_tt.json.gz",
                },
            ),
            "corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/FF_corrections_tt.json.gz",
                },
            ),
        }
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            fakefactors.RawFakeFactors_sm_lt,
            fakefactors.FakeFactors_sm_lt,
            fakefactors.FakeFactors_sm_lt_split_info,
        ],
    )
    configuration.add_producers(
        ["tt"],
        [
            fakefactors.RawFakeFactors_sm_tt_1,
            fakefactors.RawFakeFactors_sm_tt_2,
            fakefactors.FakeFactors_sm_tt_1,
            fakefactors.FakeFactors_sm_tt_2,
            fakefactors.FakeFactors_sm_tt_1_split_info,
            fakefactors.FakeFactors_sm_tt_2_split_info,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.raw_fake_factor_2,
            q.fake_factor_2,
            # ----------------------
            q.raw_qcd_fake_factor_2,
            q.raw_ttbar_fake_factor_2,
            q.raw_wjets_fake_factor_2,
            # ----------------------
            q.qcd_fake_factor_2,
            q.ttbar_fake_factor_2,
            q.wjets_fake_factor_2,
            # ----------------------
            q.qcd_fake_factor_fraction_2,
            q.ttbar_fake_factor_fraction_2,
            q.wjets_fake_factor_fraction_2,
            # ----------------------
            q.qcd_fake_factor_correction_2,
            q.ttbar_fake_factor_correction_2,
            q.wjets_fake_factor_correction_2,
        ],
    )
    configuration.add_outputs(
        ["tt"],
        [
            q.raw_fake_factor_1,
            q.raw_fake_factor_2,
            q.fake_factor_1,
            q.fake_factor_2,
            # ----------------------
            q.raw_qcd_fake_factor_1,
            q.raw_qcd_fake_factor_2,
            # ----------------------
            q.qcd_fake_factor_1,
            q.qcd_fake_factor_2,
            # ----------------------
            q.qcd_fake_factor_fraction_1,
            q.qcd_fake_factor_fraction_2,
            # ----------------------
            q.qcd_fake_factor_correction_1,
            q.qcd_fake_factor_correction_2,
        ],
    )

    # --- et, mt specific shifts ---

    for _key, _name, *_scope in (
        ("fraction_variation", "process_fractionsfracQCDUnc", ("et", "mt")),
        ("fraction_variation", "process_fractionsfracTTbarUnc"),
        ("fraction_variation", "process_fractionsfracWjetsUnc"),
        # ---------------------------------------
        ("QCD_variation", "QCDFFUnc"),
        ("QCD_variation", "QCDFFmcSubUnc"),
        ("QCD_DR_SR_correction", "QCDDRtoSRCorr"),
        ("QCD_non_closure_leading_lep_pt_correction", "QCDnonClosureLeadingLepPtCorr"),
        ("QCD_non_closure_lep_iso_correction", "QCDnonClosureLepIsoCorr"),
        # ---------------------------------------
        ("Wjets_variation", "WjetsFFUnc"),
        ("Wjets_variation", "WjetsFFmcSubUnc"),
        ("Wjets_DR_SR_correction", "WjetsDRtoSRCorr"),
        ("Wjets_non_closure_leading_lep_pt_correction", "WjetsnonClosureLeadingLepPtCorr"),
        # ---------------------------------------
        ("ttbar_variation", "ttbarFFUnc"),
        ("ttbar_non_closure_m_vis_correction", "ttbarnonClosureMvisCorr"),
        # ---------------------------------------
    ):
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.FakeFactors_sm_lt, fakefactors.RawFakeFactors_sm_lt)
            if "_corr_" in _key:
                variables = (fakefactors.FakeFactors_sm_lt,)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        _scope[0] if _scope else ("et", "mt"): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        _scope[0] if _scope else ("et", "mt"): variables,
                    },
                ),
            )

    # --- tt specific shifts ---

    # _tt_1

    for _key, _name in (
        ("fraction_variation", "process_fractionsfracQCDUnc"),
        # ---------------------------------------
        ("QCD_variation", "QCDFFUnc"),
        ("QCD_variation", "QCDFFmcSubUnc"),
        ("QCD_DR_SR_correction", "QCDDRtoSRCorr"),
        ("QCD_non_closure_m_vis_correction", "QCDnonClosureMvisCorr"),
        ("QCD_non_closure_subleading_lep_pt_correction", "QCDnonClosureSubleadingLepPtCorr"),
        # ---------------------------------------
    ):
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.RawFakeFactors_sm_tt_1, fakefactors.FakeFactors_sm_tt_1)
            if "_corr_" in _key:
                variables = (fakefactors.FakeFactors_sm_tt_1,)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        ("tt",): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        ("tt",): variables,
                    },
                ),
            )

    # _tt_2

    for _key, _name in (
        ("fraction_variation_subleading", "process_fractions_subleadingfracQCDUnc"),
        # ---------------------------------------
        ("QCD_subleading_variation", "QCD_subleadingFFUnc"),
        ("QCD_subleading_variation", "QCD_subleadingFFmcSubUnc"),
        ("QCD_subleading_DR_SR_correction", "QCD_subleadingDRtoSRCorr"),
        ("QCD_subleading_non_closure_leading_lep_pt_correction", "QCD_subleadingnonClosureLeadingLepPtCorr"),
        ("QCD_subleading_non_closure_m_vis_correction", "QCD_subleadingnonClosureMvisCorr"),
        # ---------------------------------------
    ):
        for _shift in ["Up", "Down"]:

            variables = (fakefactors.RawFakeFactors_sm_tt_2, fakefactors.FakeFactors_sm_tt_2)
            if "_corr_" in _key:
                variables = (fakefactors.FakeFactors_sm_tt_2,)

            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        ("tt",): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        ("tt",): variables,
                    },
                ),
            )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
