from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier

from .producers import selection as selection
from .quantities import output as q
from code_generation.quantity import Quantity
from code_generation.rules import AppendProducer, RemoveProducer
from .tau_triggersetup import RUN2_ERAS, DOUBLETAU_HPS_ERAS

# producers whose input column name is templated with a config parameter resolved by `_resolve_templated_quantities` below
TEMPLATED_QUANTITY_PRODUCERS = [
    selection.PreselVsEleTauID_1,
    selection.PreselVsEleTauID_2,
    selection.PreselVsMuTauID_1,
    selection.PreselVsMuTauID_2,
    selection.TauIsoFlag_1,
    selection.TauIsoFlag_2,
    selection.TauNonIsoFlag_1,
    selection.TauNonIsoFlag_2,
    selection.TauVVVLooseFlag_1,
    selection.TauVVVLooseFlag_2,
]

# quantities kept nominal-only for fake factors
NOMINAL_ONLY_QUANTITIES = (
    q.presel_mask,
    # atomic flags used only by the fake-factor regions
    q.selcut_tau_noniso_1,
    q.selcut_tau_noniso_2,
    q.selcut_tau_vvvloose_1,
    q.selcut_tau_vvvloose_2,
    q.selcut_lep_antiiso,
    q.selcut_lep_iso_qcd_run2,
    q.selcut_lep_iso_min_qcd_run2,
    q.selcut_mt_lt_qcd,
    q.selcut_wjets_mt,
    q.selcut_nbtag_eq_0,
    q.selcut_ttbar_nbtag,
    q.selcut_ss,
    q.selcut_lepton_veto_inv,
    # the fake-factor region masks themselves
    q.ff_qcd_SRlike,
    q.ff_qcd_ARlike,
    q.ff_qcd_sub_SRlike,
    q.ff_qcd_sub_ARlike,
    q.ff_wjets_SRlike,
    q.ff_wjets_ARlike,
    q.ff_wjets_SRlike_ss,
    q.ff_wjets_ARlike_ss,
    q.ff_ttbar_SR,
    q.ff_ttbar_AR,
    q.ff_ttbar_SRlike,
    q.ff_ttbar_ARlike,
    q.ff_ttbar_SRlike_ss,
    q.ff_ttbar_ARlike_ss,
    q.ff_fraction_SR,
    q.ff_fraction_AR,
    q.ff_fraction_sub_SR,
    q.ff_fraction_sub_AR,
    q.ff_qcd_DR_SR_SRlike,
    q.ff_qcd_DR_SR_ARlike,
    q.ff_qcd_AR_SR_SRlike,
    q.ff_qcd_AR_SR_ARlike,
    q.ff_qcd_sub_DR_SR_SRlike,
    q.ff_qcd_sub_DR_SR_ARlike,
    q.ff_qcd_sub_AR_SR_SRlike,
    q.ff_qcd_sub_AR_SR_ARlike,
    q.ff_wjets_DR_SR_SRlike,
    q.ff_wjets_DR_SR_ARlike,
    q.ff_wjets_DR_SR_SRlike_ss,
    q.ff_wjets_DR_SR_ARlike_ss,
    q.ff_wjets_AR_SR_SRlike,
    q.ff_wjets_AR_SR_ARlike,
    q.ff_wjets_AR_SR_SRlike_ss,
    q.ff_wjets_AR_SR_ARlike_ss,
)


def _resolve_templated_quantities(configuration, scope: str) -> None:
    """Resolve `TEMPLATED_QUANTITY_PRODUCERS` columns once config parameters for `scope` are known."""
    parameters = configuration.config_parameters[scope]
    for producer in TEMPLATED_QUANTITY_PRODUCERS:
        if scope not in producer.scopes:
            continue
        producer.input[scope] = [
            Quantity(template.name.format(**parameters))
            for template in producer.input[scope]
        ]
        for column in producer.input[scope]:
            for output_quantity in producer.output:
                column.adopt(output_quantity, scope)


def _presel_trigger_producers(configuration, scope: str, era: str) -> list:
    """Producers combining the scope's per-era HLT flag list into `selcut_presel_trigger`."""
    parameters = configuration.config_parameters[scope]
    flags = parameters[
        {
            "et": "singleelectron_trigger_flags",
            "ee": "singleelectron_trigger_flags",
            "mt": "singlemuon_trigger_flags",
            "mm": "singlemuon_trigger_flags",
            "tt": "doubletau_trigger_flags",
            "em": "cross_trigger_flags",
        }[scope]
    ]
    # a nonzero `presel_trigger_pt2_min` means the era's legs also need an offline leg-2 pt bound the flags can't express
    if parameters.get("presel_trigger_pt2_min"):
        return selection.build_trigger_pt_or_flag(
            scope,
            flags,
            [q.selcut_presel_trigger],
            # only the 2017 ele32 leg needs an upper pt_1 band (ele35 takes over from 36 up)
            pt1_max_by_flag={"trg_single_ele32": 36.0} if (scope, era) == ("et", "2017") else None,
            pt2_min_param="presel_trigger_pt2_min",
        )
    return [selection.build_trigger_or_flag(scope, flags, [q.selcut_presel_trigger])]


def add_selection(
    configuration,
    scopes,
    era: str,
    sample: str,
) -> object:
    
    ###########################
    ####### Parameters ########
    ###########################

    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            # tau vs jet working points of the fake factor regions (Run 2: Tight/VLoose, Run 3: Medium/VVVLoose)
            "ff_tau_iso_vsjet_wp": EraModifier(
                {era: "Tight" for era in RUN2_ERAS},
                default="Medium"
            ),
            "ff_tau_antiiso_vsjet_wp": EraModifier(
                {era: "VLoose" for era in RUN2_ERAS},
                default="VVVLoose"
            ),
        },
    )

    # light lepton isolation of the signal region (SR_mask) and of the fake factor regions
    configuration.add_config_parameters(
        ["et", "mt", "em"],
        {
            "lep_iso_max": 0.15,
        },
    )
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            # transverse mass cut splitting the signal region (mt_1 < mt_cut) from the W+jets determination region (mt_1 >= mt_cut)
            "mt_cut": 70.0,
            # QCD region transverse mass cut: tighter in Run 2 (50) than the {mt_cut} used everywhere else (70, same as Run 3)
            "mt_cut_qcd": EraModifier(
                {era: 50.0 for era in RUN2_ERAS},
                default=70.0,
            ),
        },
    )
    
    configuration.add_config_parameters(
        ["mt"],
        {
            # Run 2 QCD region only: narrows the lepton isolation window on the low side too (mt: 0.05, et: 0.02)
            "lep_iso_min_qcd": EraModifier(
                {era: 0.05 for era in RUN2_ERAS},
                default=0.0),
            "presel_vsele_wp": "VVLoose",
                        # Run 2 tau ID has no combined vsMu WPs; use the first part of the Run 3 combined WP
                        "presel_vsmu_wp": EraModifier(
                            {era: "Tight" for era in RUN2_ERAS},
                            default="Tight_VVLoose",
                        ),
                        # leg 1 (muon) pt is already encoded in trigger
                        "presel_lep_pt_2": EraModifier(
                            {
                                "2016preVFP": 20.0,
                                "2016postVFP": 20.0,
                                "2017": 30.0,
                                "2018": 30.0
                            },
                            default=20.0,
                        ),
                        # nonzero only where the OR'd trigger legs need an offline tau pt bound of their own
                        "presel_trigger_pt2_min": EraModifier(
                            {
                                "2016preVFP": 20.0,
                                "2016postVFP": 20.0,
                                "2017": 30.0,
                                "2018": 30.0},
                            default=0.0,
                        ),
                        "singlemuon_trigger_flags": EraModifier(
                            {
                                "2016preVFP": ["trg_single_mu22", "trg_single_mu22_tk", "trg_single_mu22_eta2p1", "trg_single_mu22_tk_eta2p1"],
                                "2016postVFP": ["trg_single_mu22", "trg_single_mu22_tk", "trg_single_mu22_eta2p1", "trg_single_mu22_tk_eta2p1"],
                                "2017": ["trg_single_mu27"],
                                "2018": ["trg_single_mu24", "trg_single_mu27"],
                            },
                            default=["trg_single_mu24"],
                        ),
        },
    )
    configuration.add_config_parameters(
        ["et"],
        {
            # Run 2 QCD region only: narrows the lepton isolation window on the low side too (mt: 0.05, et: 0.02)
            "lep_iso_min_qcd": EraModifier(
                {era: 0.02 for era in RUN2_ERAS},
                default=0.0),

            # preselection tau ID WPs, trigger flag names, and offline lepton/tau pt thresholds matching the trigger turn-on plateau
            "presel_vsele_wp": "Tight",
                        # Run 2 tau ID has no combined vsMu WPs; use the first part of the Run 3 combined WP
                        "presel_vsmu_wp": EraModifier(
                            {era: "VLoose" for era in RUN2_ERAS},
                            default="VLoose_Tight",
                        ),
                        # leg 1 (electron) pt is already encoded in the trigger
                        "presel_lep_pt_2": EraModifier(
                            {"2017": 30.0, "2018": 30.0},
                            default=20.0),
                        # nonzero only where the OR'd trigger legs need an offline tau pt bound of their own
                        "presel_trigger_pt2_min": EraModifier(
                            {"2017": 30.0, "2018": 30.0},
                            default=0.0),
                        # per-era OR of single-electron HLT paths
                        "singleelectron_trigger_flags": EraModifier(
                            {
                                "2017": ["trg_single_ele32", "trg_single_ele35"],
                                "2018": ["trg_single_ele35", "trg_single_ele32"],
                            },
                            default=["trg_single_ele30"],
                        ),
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "presel_vsele_wp": "VVLoose",
            # Run 2 tau ID has no combined vsMu WPs; use the first part of the Run 3 combined WP
            "presel_vsmu_wp": EraModifier(
                {era: "VLoose" for era in RUN2_ERAS},
                default="VLoose_VVLoose",
            ),
            # both tau legs' pt are already encoded in the doubletau trigger flag's own p1/p2 ptcuts, so no flat lep-pt cuts are needed here
            "doubletau_trigger_flags": EraModifier(
                {
                    # 2016/2017 have no doubletau trigger defined (see tau_triggersetup.py)
                    **{era: ['""'] for era in RUN2_ERAS},
                    "2018": [
                        "trg_double_tau35_tightiso_tightid",
                        "trg_double_tau35_mediumiso_hps",
                        "trg_double_tau40_mediumiso_tightid",
                        "trg_double_tau40_tightiso",
                    ],
                    **{era: ["trg_double_tau35_mediumiso_hps"] for era in DOUBLETAU_HPS_ERAS},
                },
                default=["trg_double_tau30_mediumiso_pnet"],  # 2024, 2025, 2026
            ),
        },
    )
    configuration.add_config_parameters(
        ["em"],
        {
            # Run 3 only -- 2018's cross-trigger legs are not modeled here
            "presel_lep_pt_1": 26.0,
            "presel_lep_pt_2": 25.0,
            "cross_trigger_flags": EraModifier(
                {"2018": ["trg_cross_mu23ele12", "trg_cross_mu8ele23"]},
                default=["trg_single_mu24"],
            ),
        },
    )
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemuon_trigger_flags": EraModifier(
                {
                    "2016preVFP": ["trg_single_mu22", "trg_single_mu22_tk", "trg_single_mu22_eta2p1", "trg_single_mu22_tk_eta2p1"],
                    "2016postVFP": ["trg_single_mu22", "trg_single_mu22_tk", "trg_single_mu22_eta2p1", "trg_single_mu22_tk_eta2p1"],
                    "2017": ["trg_single_mu27"],
                    "2018": ["trg_single_mu27"],
                },
                default=["trg_single_mu24"],
            )
        },
    )
    configuration.add_config_parameters(
        ["ee"],
        {
            "singleelectron_trigger_flags": EraModifier(
                {
                    "2016preVFP": ["trg_single_ele25"],
                    "2016postVFP": ["trg_single_ele25"],
                    "2017": ["trg_single_ele35"],
                    "2018": ["trg_single_ele32", "trg_single_ele35"],
                },
                default=["trg_single_ele30"],
            )
        },
    )

    #########################
    # Producers
    #########################

    if "et" in scopes:
        _resolve_templated_quantities(configuration, "et")
        configuration.add_producers(
            ["et"],
            [
                selection.JetVetoMapFlag,
                *_presel_trigger_producers(configuration, "et", era),
                selection.PreselVsEleTauID_2,
                selection.PreselVsMuTauID_2,
                # the Run 2 masks fold the leg-2 pt bound into `selcut_presel_trigger` instead
                *([] if era in RUN2_ERAS else [selection.PreselLepPt_2]),
                selection.PreselMaskSwitch.get(era),
                # `q_1 * q_2`, the shared input of both sign flags
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                selection.SameSignFlag,
                selection.NoExtraElectronFlag,
                selection.NoExtraMuonFlag,
                selection.NoDileptonFlag,
                selection.LeptonVetoFlag,
                selection.LeptonVetoInvertedFlag,
                selection.TauIsoFlag_2,
                selection.TauNonIsoFlag_2,
                selection.TauVVVLooseFlag_2,
                selection.LepIsoFlag,
                selection.LepAntiIsoFlag,
                selection.MtBelow70Flag,
                selection.MtBelowQcdCutFlag,
                selection.WjetsMtFlag,
                selection.NBtagEqZeroFlag,
                selection.TTbarNBtagFlag,
                # the signal region
                selection.SRMaskSwitch.get(era),
                selection.SRMaskSsSwitch.get(era),
                # QCD
                selection.FFQcdSRlikeSwitch.get(era),
                selection.FFQcdARlikeSwitch.get(era),
                # W+jets
                selection.ff_wjets_SRlike,
                selection.ff_wjets_ARlike,
                selection.ff_wjets_SRlike_ss,
                selection.ff_wjets_ARlike_ss,
                # ttbar
                selection.FFTtbarSRSwitch.get(era),
                selection.FFTtbarARSwitch.get(era),
                selection.FFTtbarSRlikeSwitch.get(era),
                selection.FFTtbarARlikeSwitch.get(era),
                selection.ff_ttbar_SRlike_ss,
                selection.ff_ttbar_ARlike_ss,
                # process fractions
                selection.ff_fraction_SR,
                selection.ff_fraction_AR,
                # QCD DR/AR to SR corrections
                selection.ff_qcd_DR_SR_SRlike,
                selection.ff_qcd_DR_SR_ARlike,
                selection.ff_qcd_AR_SR_SRlike,
                selection.ff_qcd_AR_SR_ARlike,
                # W+jets DR/AR to SR corrections
                selection.ff_wjets_DR_SR_SRlike,
                selection.ff_wjets_DR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike_ss,
                selection.ff_wjets_DR_SR_ARlike_ss,
                selection.ff_wjets_AR_SR_SRlike,
                selection.ff_wjets_AR_SR_ARlike,
                selection.ff_wjets_AR_SR_SRlike_ss,
                selection.ff_wjets_AR_SR_ARlike_ss,
            ],
        )
        configuration.add_outputs(
            ["et"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.ff_qcd_SRlike,
                q.ff_qcd_ARlike,
                q.ff_wjets_SRlike,
                q.ff_wjets_ARlike,
                q.ff_wjets_SRlike_ss,
                q.ff_wjets_ARlike_ss,
                q.ff_ttbar_SR,
                q.ff_ttbar_AR,
                q.ff_ttbar_SRlike,
                q.ff_ttbar_ARlike,
                q.ff_ttbar_SRlike_ss,
                q.ff_ttbar_ARlike_ss,
                q.ff_fraction_SR,
                q.ff_fraction_AR,
                q.ff_qcd_DR_SR_SRlike,
                q.ff_qcd_DR_SR_ARlike,
                q.ff_qcd_AR_SR_SRlike,
                q.ff_qcd_AR_SR_ARlike,
                q.ff_wjets_DR_SR_SRlike,
                q.ff_wjets_DR_SR_ARlike,
                q.ff_wjets_DR_SR_SRlike_ss,
                q.ff_wjets_DR_SR_ARlike_ss,
                q.ff_wjets_AR_SR_SRlike,
                q.ff_wjets_AR_SR_ARlike,
                q.ff_wjets_AR_SR_SRlike_ss,
                q.ff_wjets_AR_SR_ARlike_ss,
            ],
        )

    if "mt" in scopes:
        _resolve_templated_quantities(configuration, "mt")
        configuration.add_producers(
            ["mt"],
            [
                selection.JetVetoMapFlag,
                *_presel_trigger_producers(configuration, "mt", era),
                selection.PreselVsEleTauID_2,
                selection.PreselVsMuTauID_2,
                # the Run 2 masks fold the leg-2 pt bound into `selcut_presel_trigger` instead
                *([] if era in RUN2_ERAS else [selection.PreselLepPt_2]),
                selection.PreselMaskSwitch.get(era),
                # `q_1 * q_2`, the shared input of both sign flags
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                selection.SameSignFlag,
                selection.NoExtraElectronFlag,
                selection.NoExtraMuonFlag,
                selection.NoDileptonFlag,
                selection.LeptonVetoFlag,
                selection.LeptonVetoInvertedFlag,
                selection.TauIsoFlag_2,
                selection.TauNonIsoFlag_2,
                selection.TauVVVLooseFlag_2,
                selection.LepIsoFlag,
                selection.LepAntiIsoFlag,
                selection.MtBelow70Flag,
                selection.MtBelowQcdCutFlag,
                selection.WjetsMtFlag,
                selection.NBtagEqZeroFlag,
                selection.TTbarNBtagFlag,
                # the signal region
                selection.SRMaskSwitch.get(era),
                selection.SRMaskSsSwitch.get(era),
                # QCD
                selection.FFQcdSRlikeSwitch.get(era),
                selection.FFQcdARlikeSwitch.get(era),
                # W+jets
                selection.ff_wjets_SRlike,
                selection.ff_wjets_ARlike,
                selection.ff_wjets_SRlike_ss,
                selection.ff_wjets_ARlike_ss,
                # ttbar
                selection.FFTtbarSRSwitch.get(era),
                selection.FFTtbarARSwitch.get(era),
                selection.FFTtbarSRlikeSwitch.get(era),
                selection.FFTtbarARlikeSwitch.get(era),
                selection.ff_ttbar_SRlike_ss,
                selection.ff_ttbar_ARlike_ss,
                # process fractions
                selection.ff_fraction_SR,
                selection.ff_fraction_AR,
                # QCD DR/AR to SR corrections
                selection.ff_qcd_DR_SR_SRlike,
                selection.ff_qcd_DR_SR_ARlike,
                selection.ff_qcd_AR_SR_SRlike,
                selection.ff_qcd_AR_SR_ARlike,
                # W+jets DR/AR to SR corrections
                selection.ff_wjets_DR_SR_SRlike,
                selection.ff_wjets_DR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike_ss,
                selection.ff_wjets_DR_SR_ARlike_ss,
                selection.ff_wjets_AR_SR_SRlike,
                selection.ff_wjets_AR_SR_ARlike,
                selection.ff_wjets_AR_SR_SRlike_ss,
                selection.ff_wjets_AR_SR_ARlike_ss,
            ],
        )
        configuration.add_outputs(
            ["mt"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.ff_qcd_SRlike,
                q.ff_qcd_ARlike,
                q.ff_wjets_SRlike,
                q.ff_wjets_ARlike,
                q.ff_wjets_SRlike_ss,
                q.ff_wjets_ARlike_ss,
                q.ff_ttbar_SR,
                q.ff_ttbar_AR,
                q.ff_ttbar_SRlike,
                q.ff_ttbar_ARlike,
                q.ff_ttbar_SRlike_ss,
                q.ff_ttbar_ARlike_ss,
                q.ff_fraction_SR,
                q.ff_fraction_AR,
                q.ff_qcd_DR_SR_SRlike,
                q.ff_qcd_DR_SR_ARlike,
                q.ff_qcd_AR_SR_SRlike,
                q.ff_qcd_AR_SR_ARlike,
                q.ff_wjets_DR_SR_SRlike,
                q.ff_wjets_DR_SR_ARlike,
                q.ff_wjets_DR_SR_SRlike_ss,
                q.ff_wjets_DR_SR_ARlike_ss,
                q.ff_wjets_AR_SR_SRlike,
                q.ff_wjets_AR_SR_ARlike,
                q.ff_wjets_AR_SR_SRlike_ss,
                q.ff_wjets_AR_SR_ARlike_ss,
            ],
        )

    if "tt" in scopes:
        _resolve_templated_quantities(configuration, "tt")
        configuration.add_producers(
            ["tt"],
            [
                selection.JetVetoMapFlag,
                *_presel_trigger_producers(configuration, "tt", era),
                # both tau legs, hence every tau flag twice
                selection.PreselVsEleTauID_1,
                selection.PreselVsEleTauID_2,
                selection.PreselVsMuTauID_1,
                selection.PreselVsMuTauID_2,
                selection.PreselMaskTTSwitch.get(era),
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                selection.SameSignFlag,
                selection.NoExtraElectronFlag,
                selection.NoExtraMuonFlag,
                selection.NoDileptonFlag,
                selection.LeptonVetoFlag,
                selection.TauIsoFlag_1,
                selection.TauIsoFlag_2,
                selection.TauNonIsoFlag_1,
                selection.TauNonIsoFlag_2,
                selection.TauVVVLooseFlag_1,
                selection.TauVVVLooseFlag_2,
                # the signal region
                selection.SRMaskTTSwitch.get(era),
                selection.SRMaskSsTTSwitch.get(era),
                # QCD, leading tau
                selection.ff_qcd_SRlike_tt,
                selection.ff_qcd_ARlike_tt,
                # QCD, subleading tau
                selection.ff_qcd_sub_SRlike_tt,
                selection.ff_qcd_sub_ARlike_tt,
                # process fractions
                selection.ff_fraction_SR_tt,
                selection.ff_fraction_AR_tt,
                selection.ff_fraction_sub_SR_tt,
                selection.ff_fraction_sub_AR_tt,
                # DR/AR to SR corrections, leading tau
                selection.ff_qcd_DR_SR_SRlike_tt,
                selection.ff_qcd_DR_SR_ARlike_tt,
                selection.ff_qcd_AR_SR_SRlike_tt,
                selection.ff_qcd_AR_SR_ARlike_tt,
                # DR/AR to SR corrections, subleading tau
                selection.ff_qcd_sub_DR_SR_SRlike_tt,
                selection.ff_qcd_sub_DR_SR_ARlike_tt,
                selection.ff_qcd_sub_AR_SR_SRlike_tt,
                selection.ff_qcd_sub_AR_SR_ARlike_tt,
            ],
        )
        configuration.add_outputs(
            ["tt"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.ff_qcd_SRlike,
                q.ff_qcd_ARlike,
                q.ff_qcd_sub_SRlike,
                q.ff_qcd_sub_ARlike,
                q.ff_fraction_SR,
                q.ff_fraction_AR,
                q.ff_fraction_sub_SR,
                q.ff_fraction_sub_AR,
                q.ff_qcd_DR_SR_SRlike,
                q.ff_qcd_DR_SR_ARlike,
                q.ff_qcd_AR_SR_SRlike,
                q.ff_qcd_AR_SR_ARlike,
                q.ff_qcd_sub_DR_SR_SRlike,
                q.ff_qcd_sub_DR_SR_ARlike,
                q.ff_qcd_sub_AR_SR_SRlike,
                q.ff_qcd_sub_AR_SR_ARlike,
            ],
        )

    # used as control for Run 3 and proper signal region for Run 2
    if "em" in scopes:
        _resolve_templated_quantities(configuration, "em")
        configuration.add_producers(
            ["em"],
            [
                selection.JetVetoMapFlag,
                *_presel_trigger_producers(configuration, "em", era),
                # the Run 2 mask has no separate lep-pt terms
                *([] if era in RUN2_ERAS else [selection.PreselLepPt_1, selection.PreselLepPt_2]),
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                selection.SameSignFlag,
                selection.NoExtraElectronFlag,
                selection.NoExtraMuonFlag,
                selection.NoDileptonFlag,
                selection.LeptonVetoFlag,
                selection.EleIsoFlag_em,
                selection.MuonIsoFlag_em,
                selection.SRMaskEMSwitch.get(era),
                selection.SRMaskSsEMSwitch.get(era),
            ],
        )
        configuration.add_outputs(["em"], [q.SR_mask, q.SR_mask_ss])

    # only used as control for Run 2 so far
    if "mm" in scopes:
        configuration.add_producers(
            ["mm"],
            [
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                *_presel_trigger_producers(configuration, "mm", era),
                selection.SR_mask_mm,
            ],
        )
        configuration.add_outputs(["mm"], [q.SR_mask])

    if "ee" in scopes:
        configuration.add_producers(
            ["ee"],
            [
                selection.ChargeProduct,
                selection.OppositeSignFlag,
                *_presel_trigger_producers(configuration, "ee", era),
                selection.SR_mask_ee,
            ],
        )
        configuration.add_outputs(["ee"], [q.SR_mask])

    #####################
    # Run 2 modifications
    #####################

    for mod_scopes, rule_cls, producers, rule_filter in [
        (["et", "mt", "tt", "em"], RemoveProducer, [selection.JetVetoMapFlag], {"eras": RUN2_ERAS}),
        (["et", "mt"], AppendProducer, [selection.LepIsoQCDWindowFlag_Run2], {"eras": RUN2_ERAS}),
    ]:
        mod_scopes = [s for s in mod_scopes if s in scopes]
        if mod_scopes:
            configuration.add_modification_rule(mod_scopes, rule_cls(producers=producers, **rule_filter))

    return configuration


def restrict_selection_shifts(configuration, scopes, shifts=None):
    # Keep `presel_mask` and the fake factor regions on nominal only.
    announced = list(shifts or [])
    for scope in scopes:
        for quantity in NOMINAL_ONLY_QUANTITIES:
            for shift in list(quantity.shifts.get(scope, set())) + announced:
                quantity.ignore_shift(shift, scope)
            quantity.shifts[scope] = set()

    return configuration


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

    # every shift the input ntuple carries is propagated to the signal region (SR_mask)
    shifts_to_add = [
        "__" + shift
        for scope in configuration.selected_scopes
        for shift in configuration.requested_shifts[scope]
        if shift != "nominal"
    ]

    #########################
    # The selection masks
    #########################

    configuration = add_selection(configuration, scopes, era, sample)

    # presel_mask and the fake-factor regions are nominal-only; must run before shifts are added
    configuration = restrict_selection_shifts(
        configuration, configuration.selected_scopes, shifts=shifts_to_add
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
