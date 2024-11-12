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
            # --- QCD ---------------------------------
            "qcd_ff_variation": "nominal",
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            # --- Wjets -------------------------------
            "wjets_ff_variation": "nominal",
            "wjets_ff_corr_leppt_variation": "nominal",
            "wjets_ff_corr_drsr_variation": "nominal",
            # --- ttbar -------------------------------
            "ttbar_ff_variation": "nominal",
            "ttbar_ff_corr_leppt_variation": "nominal",
            # --- extra -------------------------------
            "qcd_ff_corr_lep_iso_variation": "nominal",
            "wjets_ff_corr_lep_iso_variation": "nominal",
            # -----------------------------------------
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/fake_factors_et.json.gz",
                },
            ),
            "ff_corr_file": EraModifier(
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
            # --- QCD ---------------------------------
            "qcd_ff_variation": "nominal",
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            # --- Wjets -------------------------------
            "wjets_ff_variation": "nominal",
            "wjets_ff_corr_leppt_variation": "nominal",
            "wjets_ff_corr_drsr_variation": "nominal",
            # --- ttbar -------------------------------
            "ttbar_ff_variation": "nominal",
            "ttbar_ff_corr_leppt_variation": "nominal",
            # --- extra -------------------------------
            "qcd_ff_corr_lep_iso_variation": "nominal",
            "wjets_ff_corr_lep_iso_variation": "nominal",
            # -----------------------------------------
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/fake_factors_mt.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
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
            "fraction_subleading_variation": "nominal",
            # --- QCD leading -------------------------
            "qcd_ff_variation": "nominal",
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            # --- QCD subleading ----------------------
            "qcd_subleading_ff_variation": "nominal",
            "qcd_subleading_ff_corr_leppt_variation": "nominal",
            "qcd_subleading_ff_corr_drsr_variation": "nominal",
            # --- extra -------------------------------
            "qcd_ff_corr_taumass_variation": "nominal",
            "qcd_subleading_ff_corr_taumass_variation": "nominal",
            # -----------------------------------------
            "ff_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/sm/2018/fake_factors_tt.json.gz",
                },
            ),
            "ff_corr_file": EraModifier(
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
        ],
    )
    configuration.add_producers(
        ["tt"],
        [
            fakefactors.RawFakeFactors_sm_tt_1,
            fakefactors.RawFakeFactors_sm_tt_2,
            fakefactors.FakeFactors_sm_tt_1,
            fakefactors.FakeFactors_sm_tt_2,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.raw_fake_factor,
            q.fake_factor,
            # ----------------------
            # q.raw_qcd_fake_factor,
            # q.raw_ttbar_fake_factor,
            # q.raw_wjets_fake_factor,
            # ----------------------
            # q.qcd_fake_factor,
            # q.ttbar_fake_factor,
            # q.wjets_fake_factor,
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
            # q.raw_qcd_fake_factor_1,
            # q.raw_qcd_fake_factor_2,
            # q.raw_ttbar_fake_factor_1,
            # q.raw_ttbar_fake_factor_2,
            # q.raw_wjets_fake_factor_1,
            # q.raw_wjets_fake_factor_2,
            # ----------------------
            # q.qcd_fake_factor_1,
            # q.qcd_fake_factor_2,
            # q.ttbar_fake_factor_1,
            # q.ttbar_fake_factor_2,
            # q.wjets_fake_factor_1,
            # q.wjets_fake_factor_2
        ],
    )

    # --- et, mt specific shifts ---

    for _key, _name, *_scope in (
        ("qcd_ff_variation", "QCDFFslopeUnc", ("et", "mt")),
        ("qcd_ff_variation", "QCDFFnormUnc"),
        ("qcd_ff_variation", "QCDFFmcSubUnc"),
        # --------------------------------------
        ("wjets_ff_variation", "WjetsFFslopeUnc"),
        ("wjets_ff_variation", "WjetsFFnormUnc"),
        ("wjets_ff_variation", "WjetsFFmcSubUnc"),
        # --------------------------------------
        ("ttbar_ff_variation", "ttbarFFslopeUnc"),
        ("ttbar_ff_variation", "ttbarFFnormUnc"),
        # --------------------------------------
        ("fraction_variation", "process_fractionsfracQCDUnc"),
        ("fraction_variation", "process_fractionsfracWjetsUnc"),
        ("fraction_variation", "process_fractionsfracTTbarUnc"),
        # --------------------------------------
        ("qcd_ff_corr_drsr_variation", "QCDDRtoSRCorr"),
        ("wjets_ff_corr_drsr_variation", "WjetsDRtoSRCorr"),
        # --------------------------------------
        ("qcd_ff_corr_leppt_variation", "QCDClosureLeadingLepPtCorr"),
        ("wjets_ff_corr_leppt_variation", "WjetsClosureLeadingLepPtCorr"),
        ("ttbar_ff_corr_leppt_variation", "ttbarClosureLeadingLepPtCorr"),
        # --------------------------------------
        ("qcd_ff_corr_lep_iso_variation", "QCDClosureLepIsoCorr"),
        ("wjets_ff_corr_lep_iso_variation", "WjetsClosureLepIsoCorr"),
    ):
        for _shift in ["Up", "Down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        _scope[0] if _scope else ("et", "mt"): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        _scope[0] if _scope else ("et", "mt"): (
                            fakefactors.RawFakeFactors_sm_lt,
                            fakefactors.FakeFactors_sm_lt,
                        )
                    },
                ),
            )

    # --- tt specific shifts ---

    # _tt_1

    for _key, _name in (
        ("qcd_ff_variation", "QCDFFslopeUnc"),
        ("qcd_ff_variation", "QCDFFnormUnc"),
        ("qcd_ff_variation", "QCDFFmcSubUnc"),
        # --------------------------------------
        ("fraction_variation", "process_fractionsfracQCDUnc"),
        # --------------------------------------
        ("qcd_ff_corr_leppt_variation", "QCDClosureSubleadingLepPtCorr"),
        ("qcd_ff_corr_taumass_variation", "QCDClosureLeadingLepMassCorr"),
        # --------------------------------------
        ("qcd_ff_corr_drsr_variation", "QCDDRtoSRCorr"),
    ):
        for _shift in ["Up", "Down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        ("tt",): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        ("tt",): (
                            fakefactors.RawFakeFactors_sm_tt_1,
                            fakefactors.FakeFactors_sm_tt_1,
                        )
                    },
                ),
            )

    # _tt_2

    for _key, _name in (
        ("qcd_subleading_ff_variation", "QCD_subleadingFFslopeUnc"),
        ("qcd_subleading_ff_variation", "QCD_subleadingFFnormUnc"),
        ("qcd_subleading_ff_variation", "QCD_subleadingFFmcSubUnc"),
        # --------------------------------------
        ("fraction_subleading_variation", "process_fractions_subleadingfracQCDUnc"),
        # --------------------------------------
        ("qcd_subleading_ff_corr_leppt_variation", "QCD_subleadingClosureLeadingLepPtCorr"),
        ("qcd_subleading_ff_corr_taumass_variation", "QCD_subleadingClosureSubleadingLepMassCorr"),
        # --------------------------------------
        ("qcd_subleading_ff_corr_drsr_variation", "QCD_subleadingDRtoSRCorr"),
    ):
        for _shift in ["Up", "Down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"{_name}{_shift}",
                    shift_config={
                        ("tt",): {
                            _key: f"{_name}{_shift}",
                        }
                    },
                    producers={
                        ("tt",): (
                            fakefactors.RawFakeFactors_sm_tt_2,
                            fakefactors.FakeFactors_sm_tt_2,
                        )
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
