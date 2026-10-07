import glob
import json
import os
from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.quantity import Quantity
from code_generation.rules import AppendProducer, RemoveProducer

from .producers import selection as selection
from .producers import weights as weight_producers
from .quantities import output as q
from .config import RUN2_ERAS
from .tau_triggersetup import DOUBLETAU_HPS_ERAS

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

NOMINAL_ONLY_QUANTITIES = (
    q.presel_mask,
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
            # Run 2 has no Medium/VVVLoose split, uses Tight/VLoose instead.
            "ff_tau_iso_vsjet_wp": EraModifier({era: "Tight" for era in RUN2_ERAS}, default="Medium"),
            "ff_tau_antiiso_vsjet_wp": EraModifier({era: "VLoose" for era in RUN2_ERAS}, default="VVVLoose"),
        },
    )

    configuration.add_config_parameters(
        ["et", "mt", "em"],
        {
            "lep_iso_max": 0.15,
        },
    )
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "mt_cut": 70.0,
            "mt_cut_qcd": EraModifier(
                {era: 50.0 for era in RUN2_ERAS},
                default=70.0,
            ),
        },
    )

    configuration.add_config_parameters(
        ["mt"],
        {
            "lep_iso_min_qcd": EraModifier(
                {era: 0.05 for era in RUN2_ERAS},
                default=0.0),
            "presel_vsele_wp": "VVLoose",  # et needs the tighter Tight cut against electron fakes
            "presel_vsmu_wp": EraModifier(
                {era: "Tight" for era in RUN2_ERAS},
                default="Tight_VVLoose",
            ),
            "presel_lep_pt_2": EraModifier(
                {
                    "2016preVFP": 20.0,
                    "2016postVFP": 20.0,
                    "2017": 30.0,
                    "2018": 30.0
                },
                default=20.0,
            ),
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
                    # mutau cross-trigger switches from HPS to PNet only in 2025 (unlike
                    # the tt doubletau trigger, which switches already in 2024)
                    **{era: ["trg_single_mu24", "trg_cross_mu20tau27_hps"] for era in [*DOUBLETAU_HPS_ERAS, "2024"]},
                },
                default=["trg_single_mu24", "trg_cross_mu20tau27_pnet"],  # 2025, 2026
            ),
        },
    )
    configuration.add_config_parameters(
        ["et"],
        {
            "lep_iso_min_qcd": EraModifier(
                {era: 0.02 for era in RUN2_ERAS},
                default=0.0),
            "presel_vsele_wp": "Tight",  # tighter cut against electron fakes than mt/tt
            "presel_vsmu_wp": EraModifier(
                {era: "VLoose" for era in RUN2_ERAS},
                default="VLoose_Tight",
            ),
            "presel_lep_pt_2": EraModifier(
                {"2017": 30.0, "2018": 30.0},
                default=20.0),
            "presel_trigger_pt2_min": EraModifier(
                {"2017": 30.0, "2018": 30.0},
                default=0.0),
            "singleelectron_trigger_flags": EraModifier(
                {
                    "2017": ["trg_single_ele32", "trg_single_ele35"],
                    "2018": ["trg_single_ele35", "trg_single_ele32"],
                    # eletau cross-trigger switches from HPS to PNet only in 2025 (unlike
                    # the tt doubletau trigger, which switches already in 2024)
                    **{era: ["trg_single_ele30", "trg_cross_ele24tau30_hps"] for era in [*DOUBLETAU_HPS_ERAS, "2024"]},
                },
                default=["trg_single_ele30", "trg_cross_ele24tau30_pnet"],  # 2025, 2026
            ),
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "presel_vsele_wp": "VVLoose",
            "presel_vsmu_wp": EraModifier(
                {era: "VLoose" for era in RUN2_ERAS},
                default="VLoose_VVLoose",
            ),
            "doubletau_trigger_flags": EraModifier(
                {
                    **{era: ['""'] for era in RUN2_ERAS},
                    "2018": [
                        "trg_double_tau35_tightiso_tightid",
                        "trg_double_tau35_mediumiso_hps",
                        "trg_double_tau40_mediumiso_tightid",
                        "trg_double_tau40_tightiso",
                    ],
                    **{era: ["trg_double_tau35_mediumiso_hps", "trg_double_tau30_jet_mediumiso_hps"] for era in DOUBLETAU_HPS_ERAS},
                },
                default=["trg_double_tau30_mediumiso_pnet", "trg_double_tau26_jet_pnet"],  # 2024, 2025, 2026
            ),
        },
    )
    configuration.add_config_parameters(
        ["em"],
        {
            "presel_lep_pt_1": 25.0,  # electron
            "presel_lep_pt_2": 26.0,  # muon
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
                *([] if era in RUN2_ERAS else [selection.PreselLepPt_2]),
                selection.PreselMaskSwitch.get(era),
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
                selection.SRMaskSwitch.get(era),
                selection.SRMaskSsSwitch.get(era),
                selection.FFQcdSRlikeSwitch.get(era),
                selection.FFQcdARlikeSwitch.get(era),
                selection.ff_wjets_SRlike,
                selection.ff_wjets_ARlike,
                selection.ff_wjets_SRlike_ss,
                selection.ff_wjets_ARlike_ss,
                selection.FFTtbarSRSwitch.get(era),
                selection.FFTtbarARSwitch.get(era),
                selection.FFTtbarSRlikeSwitch.get(era),
                selection.FFTtbarARlikeSwitch.get(era),
                selection.ff_ttbar_SRlike_ss,
                selection.ff_ttbar_ARlike_ss,
                selection.ff_fraction_SR,
                selection.ff_fraction_AR,
                selection.ff_qcd_DR_SR_SRlike,
                selection.ff_qcd_DR_SR_ARlike,
                selection.ff_qcd_AR_SR_SRlike,
                selection.ff_qcd_AR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike,
                selection.ff_wjets_DR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike_ss,
                selection.ff_wjets_DR_SR_ARlike_ss,
                selection.ff_wjets_AR_SR_SRlike,
                selection.ff_wjets_AR_SR_ARlike,
                selection.ff_wjets_AR_SR_SRlike_ss,
                selection.ff_wjets_AR_SR_ARlike_ss,
                selection._gen_category_T_leg1_et,
                selection._gen_category_T_leg2_et,
                selection.gen_category_T_et,
                selection.gen_category_J_et,
                selection.gen_category_L_et,
            ],
        )
        configuration.add_outputs(
            ["et"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.gen_category_T,
                q.gen_category_J,
                q.gen_category_L,
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
                *([] if era in RUN2_ERAS else [selection.PreselLepPt_2]),
                selection.PreselMaskSwitch.get(era),
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
                selection.SRMaskSwitch.get(era),
                selection.SRMaskSsSwitch.get(era),
                selection.FFQcdSRlikeSwitch.get(era),
                selection.FFQcdARlikeSwitch.get(era),
                selection.ff_wjets_SRlike,
                selection.ff_wjets_ARlike,
                selection.ff_wjets_SRlike_ss,
                selection.ff_wjets_ARlike_ss,
                selection.FFTtbarSRSwitch.get(era),
                selection.FFTtbarARSwitch.get(era),
                selection.FFTtbarSRlikeSwitch.get(era),
                selection.FFTtbarARlikeSwitch.get(era),
                selection.ff_ttbar_SRlike_ss,
                selection.ff_ttbar_ARlike_ss,
                selection.ff_fraction_SR,
                selection.ff_fraction_AR,
                selection.ff_qcd_DR_SR_SRlike,
                selection.ff_qcd_DR_SR_ARlike,
                selection.ff_qcd_AR_SR_SRlike,
                selection.ff_qcd_AR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike,
                selection.ff_wjets_DR_SR_ARlike,
                selection.ff_wjets_DR_SR_SRlike_ss,
                selection.ff_wjets_DR_SR_ARlike_ss,
                selection.ff_wjets_AR_SR_SRlike,
                selection.ff_wjets_AR_SR_ARlike,
                selection.ff_wjets_AR_SR_SRlike_ss,
                selection.ff_wjets_AR_SR_ARlike_ss,
                selection._gen_category_T_leg1_mt,
                selection._gen_category_T_leg2_mt,
                selection.gen_category_T_mt,
                selection.gen_category_J_mt,
                selection.gen_category_L_mt,
            ],
        )
        configuration.add_outputs(
            ["mt"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.gen_category_T,
                q.gen_category_J,
                q.gen_category_L,
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
                selection.SRMaskTTSwitch.get(era),
                selection.SRMaskSsTTSwitch.get(era),
                selection.ff_qcd_SRlike_tt,
                selection.ff_qcd_ARlike_tt,
                selection.ff_qcd_sub_SRlike_tt,
                selection.ff_qcd_sub_ARlike_tt,
                selection.ff_fraction_SR_tt,
                selection.ff_fraction_AR_tt,
                selection.ff_fraction_sub_SR_tt,
                selection.ff_fraction_sub_AR_tt,
                selection.ff_qcd_DR_SR_SRlike_tt,
                selection.ff_qcd_DR_SR_ARlike_tt,
                selection.ff_qcd_AR_SR_SRlike_tt,
                selection.ff_qcd_AR_SR_ARlike_tt,
                selection.ff_qcd_sub_DR_SR_SRlike_tt,
                selection.ff_qcd_sub_DR_SR_ARlike_tt,
                selection.ff_qcd_sub_AR_SR_SRlike_tt,
                selection.ff_qcd_sub_AR_SR_ARlike_tt,
                selection._gen_category_T_leg1_tt,
                selection._gen_category_T_leg2_tt,
                selection.gen_category_T_tt,
                selection._gen_category_J_leg1_tt,
                selection._gen_category_J_leg2_tt,
                selection.gen_category_J_tt,
                selection.gen_category_L_tt,
            ],
        )
        configuration.add_outputs(
            ["tt"],
            [
                q.presel_mask,
                q.SR_mask,
                q.SR_mask_ss,
                q.gen_category_T,
                q.gen_category_J,
                q.gen_category_L,
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

    if "em" in scopes:
        _resolve_templated_quantities(configuration, "em")
        configuration.add_producers(
            ["em"],
            [
                selection.JetVetoMapFlag,
                *_presel_trigger_producers(configuration, "em", era),
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
                selection._gen_category_T_leg1_em,
                selection._gen_category_T_leg2_em,
                selection.gen_category_T_em,
                selection.gen_category_L_em,
            ],
        )
        configuration.add_outputs(
            ["em"], [q.SR_mask, q.SR_mask_ss, q.gen_category_T, q.gen_category_L]
        )

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


def build_norm_table(output_dir: str, sample_database_root: str = None) -> str:
    # Writes data/normalization/norm_table.json
    sample_database_root = sample_database_root or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "sample_database")
    table = {}
    for datasets_path in glob.glob(os.path.join(sample_database_root, "*", "datasets.json")):
        with open(datasets_path) as f:
            datasets = json.load(f)
        for entry in datasets.values():
            if None in (entry.get("xsec"), entry.get("nevents"), entry.get("generator_weight")):
                continue
            table[entry["nick"]] = {
                "xsec": float(entry["xsec"]),
                "nevents": float(entry["nevents"]),
                "generator_weight": float(entry["generator_weight"]),
            }
    if not table:
        raise ValueError(f"build_norm_table: no entries found under {sample_database_root}")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "norm_table.json"), "w") as f:
        json.dump(table, f)
    return "data/normalization/norm_table.json"


def _resolve_templated_quantities(configuration, scope: str, templated_producers=TEMPLATED_QUANTITY_PRODUCERS) -> None:
    parameters = configuration.config_parameters[scope]
    for producer in templated_producers:
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
    if parameters.get("presel_trigger_pt2_min"):
        return selection.build_trigger_pt_or_flag(
            scope,
            flags,
            [q.selcut_presel_trigger],
            pt1_max_by_flag={"trg_single_ele32": 36.0} if (scope, era) == ("et", "2017") else None,
            pt2_min_param="presel_trigger_pt2_min",
        )
    _exclusivity_bound = {
        "mt": 26.0,
        "et": 32.0,
        "tt": 40.0 if era in DOUBLETAU_HPS_ERAS else 35.0,
    }.get(scope)
    if _exclusivity_bound is not None and len(flags) == 2:
        secondary_flag = flags[1]
        return selection.build_trigger_pt_or_flag(
            scope,
            flags,
            [q.selcut_presel_trigger],
            pt1_max_by_flag={secondary_flag: _exclusivity_bound},
            pt2_max_by_flag={secondary_flag: _exclusivity_bound} if scope == "tt" else None,
        )
    return [selection.build_trigger_or_flag(scope, flags, [q.selcut_presel_trigger])]


def restrict_selection_shifts(configuration, scopes, shifts=None):
    announced = list(shifts or [])
    for scope in scopes:
        for quantity in NOMINAL_ONLY_QUANTITIES:
            for shift in list(quantity.shifts.get(scope, set())) + announced:
                quantity.ignore_shift(shift, scope)
            quantity.shifts[scope] = set()

    return configuration


def _add_normalization_and_weight(configuration, era: str, sample: str) -> None:
    scopes_list = list(configuration.selected_scopes)
    if sample not in ["data", "embedding", "embedding_mc"]: #don't apply normalisation
        norm_table_path = build_norm_table(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "normalization"))
        configuration.add_config_parameters(
            scopes_list,
            {"norm_table_path": norm_table_path},
        )
        configuration.add_producers(
            scopes_list,
            [weight_producers.SampleNormalization],
        )
        for scope in scopes_list:
            configuration.add_config_parameters(
                scope,
                {
                    # same per-channel WPs as presel_vsele_wp above; et is tighter,
                    # everything else (incl. em, with no presel vsEle cut) falls back to VVLoose
                    "vs_ele_wp": "Tight" if scope == "et" else "VVLoose",
                    "vs_jet_wp": EraModifier({era: "Tight" for era in RUN2_ERAS}, default="Medium"),
                    "luminosity_pb": EraModifier(weight_producers.LUMI_PB),
                    "mc_campaign_split_factor": EraModifier(weight_producers.MC_CAMPAIGN_SPLIT_FACTOR, default=1.0),
                },
            )
            if scope in ["et", "mt", "tt", "em"]:
                weight_switch = {
                    "et": weight_producers.WeightETSwitch,
                    "mt": weight_producers.WeightMTSwitch,
                    "tt": weight_producers.WeightTTSwitch,
                    "em": weight_producers.WeightEMSwitch,
                }[scope]
                configuration.add_producers(scope, [weight_switch.get(era)])
                configuration.add_outputs(scope, [q.weight])
                _resolve_templated_quantities(configuration, scope, weight_producers.TEMPLATED_QUANTITY_PRODUCERS)
            else:
                configuration.add_producers(scope, [weight_producers.ConstantWeight])
                configuration.add_outputs(scope, [q.weight])
    else:
        configuration.add_producers(
            scopes_list,
            [
                weight_producers.ConstantCrossSectionPerEventWeight,
                weight_producers.ConstantNumberGeneratedEventsWeight,
                weight_producers.ConstantNegativeEventsFraction,
                weight_producers.ConstantWeight,
            ],
        )
        configuration.add_outputs(scopes_list, [q.weight])
    configuration.add_outputs(
        scopes_list,
        [
            q.crossSectionPerEventWeight,
            q.numberGeneratedEventsWeight,
            q.negative_events_fraction,
        ],
    )


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

    shifts_to_add = [
        "__" + shift
        for scope in configuration.selected_scopes
        for shift in configuration.requested_shifts[scope]
        if shift != "nominal"
    ]

    configuration = add_selection(configuration, scopes, era, sample)
    configuration = restrict_selection_shifts(
        configuration, configuration.selected_scopes, shifts=shifts_to_add
    )

    _add_normalization_and_weight(configuration, era, sample)

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
