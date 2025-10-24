from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift
from .producers import scalefactors as scalefactors


def add_diTauTriggerSetup(configuration: Configuration) -> Configuration:

    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            "singlemuon_trigger": 
                [
                    {
                    "flagname": "trg_single_mu24",
                    "hlt_path": "HLT_IsoMu24",
                    "ptcut": 25,
                    "etacut": 2.4,
                    "filterbit": 1,
                    "trigger_particle_id": 13,
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_cross_trigger":
                [
                    {
                    "flagname": "trg_cross_mu20tau27_hps",
                    "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                    "p1_ptcut": 20,
                    "p2_ptcut": 32,
                    "p1_etacut": 2.1,
                    "p2_etacut": 2.1,
                    "p1_filterbit": 1,
                    "p1_trigger_particle_id": 13,
                    "p2_filterbit": 9,  
                    "p2_trigger_particle_id": 15,
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            "singleelectron_trigger": 
                [
                    {
                    "flagname": "trg_single_ele30",
                    "hlt_path": "HLT_Ele30_WPTight_Gsf",
                    "ptcut": 32,
                    "etacut": 2.1,
                    "filterbit": 1,  # matching the tight WP
                    "trigger_particle_id": 11,
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    configuration.add_config_parameters(
        ["et"],
        {
            "eltau_cross_trigger":
                [
                    {
                    "flagname": "trg_cross_ele24tau30_hps",
                    "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                    "p1_ptcut": 25,
                    "p2_ptcut": 35,
                    "p1_etacut": 2.1,
                    "p2_etacut": 2.1, 
                    "p1_trigger_particle_id": 11,
                    "p1_filterbit": 2, 
                    "p2_trigger_particle_id": 15,
                    "p2_filterbit": 3,  
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger": 
                [
                    {
                    "flagname": "trg_double_tau35_mediumiso_hps",
                    "hlt_path": "HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1", 
                    "p1_ptcut": 40,
                    "p2_ptcut": 40,
                    "p1_etacut": 2.1,
                    "p2_etacut": 2.1,
                    "p1_filterbit": EraModifier(
                        {
                            "2022preEE": 7,
                            "2022postEE": 7,
                            "2023preBPix": 7,
                            "2023postBPix": 7,
                            "2024": 11,
                        }
                    ),  
                    "p2_filterbit": EraModifier(
                        {
                            "2022preEE": 7,
                            "2022postEE": 7,
                            "2023preBPix": 7,
                            "2023postBPix": 7,
                            "2024": 11,
                        }
                    ),   
                    "p1_trigger_particle_id": 15,
                    "p2_trigger_particle_id": 15,
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    elmu_cross_trigger_defaults = {
        "p1_etacut": 2.1,
        "p1_filterbit": 5,
        "p1_trigger_particle_id": 11,
        "p2_etacut": 2.5,
        "p2_filterbit": 5,
        "p2_trigger_particle_id": 13,
        "max_deltaR_triggermatch": 0.4,
    }
    configuration.add_config_parameters(
        ["em"],
        {
            "elmu_cross_trigger":[
                {
                    "flagname": "trg_cross_mu23ele12",
                    "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                    "p1_ptcut": 12,
                    "p2_ptcut": 24,
                    **elmu_cross_trigger_defaults,
                },
                {
                    "flagname": "trg_cross_mu8ele23",
                    "hlt_path": "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                    "p1_ptcut": 24,
                    "p2_ptcut": 8,
                    **elmu_cross_trigger_defaults,
                },
            ],
        },
    )

    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "singletau_trigger_trailing": 
                [
                    {
                    "flagname": "trg_single_tau180_2",
                    "hlt_path": "HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1",
                    "ptcut": 180,
                    "etacut": 2.1,
                    "filterbit": 9,
                    "trigger_particle_id": 15,
                    "max_deltaR_triggermatch": 0.4,
                    },
                ],
        },
    )

    # doubleelectron trigger  # applying the same defaults as for the singleelectron trigger
    configuration.add_config_parameters(
        ["ee"],
        {
            "doubleelectron_trigger": 
            [
                {
                "flagname": "trg_double_ele23",
                "hlt_path": "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
                "p1_ptcut": 23,
                "p2_ptcut": 12,
                "p1_etacut": 2.1,
                "p1_filterbit": 4,
                "p1_trigger_particle_id": 11,
                "p2_etacut": 2.1,
                "p2_filterbit": 4,
                "p2_trigger_particle_id": 11,
                "max_deltaR_triggermatch": 0.4,
                },
            ],
        },
    )
    #######################
    #trigger scale factors#
    #######################
    configuration.add_config_parameters(
        ["et"],
        {
            "e_trigger_sf_file": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/EGM/2022_Summer22/electronHlt.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electronHlt.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/EGM/2023_Summer23/electronHlt.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electronHlt.json.gz",
                    "2024": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electronHlt.json.gz",
                }
            ),
            "et_trigger_leg1_sf_file": EraModifier(
                {
                    "2022preEE": "data/hleprare/TriggerScaleFactors/2022preEE/CrossEleTauHlt_EleLeg_v1.json",
                    "2022postEE": "data/hleprare/TriggerScaleFactors/2022postEE/CrossEleTauHlt_EleLeg_v1.json",
                    "2023preBPix": "data/hleprare/TriggerScaleFactors/2023preBPix/CrossEleTauHlt_EleLeg_v1.json",
                    "2023postBPix": "data/hleprare/TriggerScaleFactors/2023postBPix/CrossEleTauHlt_EleLeg_v1.json",
                    "2024": "data/hleprare/TriggerScaleFactors/2023postBPix/CrossEleTauHlt_EleLeg_v1.json",
                }
            ),
            "e_trigger_era": EraModifier(
                {
                    "2022preEE": "2022Re-recoBCD",
                    "2022postEE": "2022Re-recoE+PromptFG",
                    "2023preBPix": "2023PromptC",
                    "2023postBPix": "2023PromptD",
                    "2024": "2023PromptD",
                }
            ),
            "single_ele_trigger_sf": [
                {
                    "e_trigger_flagname": "trg_wgt_single_ele30",
                    "e_trigger_flag": "trg_single_ele30",
                    "e_trigger_sf_name": "Electron-HLT-SF",
                    "e_trigger_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                    "e_trigger_variation": "sf",
                },
            ],

            "eletau_trigger_leg1_sf": [
                {
                    "et_trigger_flag": "trg_cross_ele24tau30_hps",
                    "et_trigger_leg1_flagname": "trg_wgt_ele24tau30_leg1",
                    "et_trigger_leg1_sf_name": "Electron-HLT-SF",
                    "et_trigger_leg1_path_id_name": "HLT_SF_Ele24_TightID",
                    "et_trigger_leg1_variation": "sf",
                },
            ],
            "eletau_trigger_leg2_sf": [
                {
                    "et_trigger_leg2_flagname": "trg_wgt_ele24tau30_leg2",
                    "et_trigger_flag": "trg_cross_ele24tau30_hps",
                    "et_trigger_leg2_sf_name": "etau",
                    "et_trigger_leg2_variation": "nom",
                },
            ]
        },
    )

    # single muon trigger scale factors
    configuration.add_config_parameters(
        ["mt"],
        {
            "mt_trigger_leg1_sf_file": EraModifier(
                {
                    "2022preEE": '"data/hleprare/TriggerScaleFactors/2022preEE/CrossMuTauHlt_MuLeg_v1.json"',
                    "2022postEE": '"data/hleprare/TriggerScaleFactors/2022postEE/CrossMuTauHlt_MuLeg_v1.json"',
                    "2023preBPix": '"data/hleprare/TriggerScaleFactors/2023preBPix/CrossMuTauHlt_MuLeg_v1.json"',
                    "2023postBPix": '"data/hleprare/TriggerScaleFactors/2023postBPix/CrossMuTauHlt_MuLeg_v1.json"',
                    "2024":'"data/hleprare/TriggerScaleFactors/2023postBPix/CrossMuTauHlt_MuLeg_v1.json"',
                }
            ),
            "single_mu_trigger_sf": [
                {
                    "m_trigger_flagname": "trg_wgt_single_mu24",
                    "m_trigger_flag": "trg_single_mu24",
                    "m_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                    "m_trigger_variation": "nominal",
                },
            ],

            "mutau_trigger_leg1_sf": [
                {
                    "mt_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                    "mt_trigger_flag": "trg_cross_mu20tau27_hps",
                    "mt_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                    "mt_trigger_leg1_variation": "nominal",
                },
            ],
            "mutau_trigger_leg2_sf": [
                {
                    "mt_trigger_leg2_flagname": "trg_wgt_mu20tau27_leg2",
                    "mt_trigger_flag": "trg_cross_mu20tau27_hps",
                    "mt_trigger_leg2_sf_name": "mutau",
                    "mt_trigger_leg2_variation": "nom",
                },
            ],
        },
    )

    # double tau-tau trigger scale factors
    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger_leg1_sf": [
                {
                    "tt_trigger_leg1_flagname": "trg_wgt_doubletau35_leg1",
                    "tt_trigger_flag": "trg_double_tau35_mediumiso_hps",
                    "tt_trigger_leg1_sf_name": "ditau",
                    "tt_trigger_leg1_variation": "nom",
                },
            ],
            "doubletau_trigger_leg2_sf": [
                {
                    "tt_trigger_leg2_flagname": "trg_wgt_doubletau35_leg2",
                    "tt_trigger_flag": "trg_double_tau35_mediumiso_hps",
                    "tt_trigger_leg2_sf_name": "ditau",
                    "tt_trigger_leg2_variation": "nom",
                },
            ],
        },
    )

    #######################
    # trigger shifts #
    #######################
    for _variation in ["up", "down"]:
        configuration.add_shift(
            SystematicShift(
                name=f"singleEleTriggerSF{_variation.upper()}",
                shift_config={
                    ("et"): {
                        "single_ele_trigger_sf": [
                            {
                                "e_trigger_flagname": "trg_wgt_single_ele30",
                                "e_trigger_flag": "trg_single_ele30",
                                "e_trigger_sf_name": "Electron-HLT-SF",
                                "e_trigger_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                                "e_trigger_variation": f"sf{_variation}",
                            },
                        ],
                    }
                },
                producers={("et"): scalefactors.SingleEleTriggerSF},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"EleTauTriggerSF{_variation.upper()}",
                shift_config={
                    ("et"): {
                        "eletau_trigger_leg1_sf": [
                            {
                                "et_trigger_leg1_flagname": "trg_wgt_ele24tau30_leg1",
                                "et_trigger_flag": "trg_cross_ele24tau30_hps",
                                "et_trigger_leg1_sf_name": "Electron-HLT-SF",
                                "et_trigger_leg1_path_id_name": "HLT_SF_Ele24_TightID",
                                "et_trigger_leg1_variation": f"sf{_variation}",
                            },
                        ],
                        "eletau_trigger_leg2_sf": [
                            {
                                "et_trigger_leg2_flagname": "trg_wgt_ele24tau30_leg2",
                                "et_trigger_flag": "trg_cross_ele24tau30_hps",
                                "et_trigger_leg2_sf_name": "etau",
                                "et_trigger_leg2_variation": _variation,
                            },
                        ]
                    },
                },
                producers={
                    ("et"): [
                        scalefactors.EleTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
                SystematicShift(
                    name=f"singleMuTriggerSF{_variation.upper()}",
                    shift_config={
                        ("mt"): {
                            "single_mu_trigger_sf": [
                                {
                                    "m_trigger_flagname": "trg_wgt_single_mu24",
                                    "m_trigger_flag": "trg_single_mu24",
                                    "m_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "m_trigger_variation": f"syst{_variation}",
                                },
                            ],
                        }
                    },
                    producers={("mt"): scalefactors.SingleMuTriggerSF},
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )
        configuration.add_shift(
            SystematicShift(
                name=f"MuTauTriggerSF{_variation.upper()}",
                shift_config={
                    ("mt"): {
                        "mutau_trigger_leg1_sf": [
                            {
                                "mt_trigger_flag": "trg_cross_mu20tau27_hps",
                                "mt_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                                "mt_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                                "mt_trigger_leg1_variation": f"syst{_variation}",
                            },
                        ],
                        "mutau_trigger_leg2_sf": [
                            {
                                "mt_trigger_flag": "trg_cross_mu20tau27_hps",
                                "mt_trigger_leg2_flagname": "trg_wgt_mu20tau27_leg2",
                                "mt_trigger_leg2_sf_name": "mutau",
                                "mt_trigger_leg2_variation": _variation,
                            },
                        ],
                    },
                },
                producers={
                    ("mt"): [
                        scalefactors.MuTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"DoubleTauTriggerSF{_variation.upper()}",
                shift_config={
                    ("tt"): {
                        "doubletau_trigger_leg1_sf": [
                            {
                                "tt_trigger_leg1_flagname": "trg_wgt_doubletau35_leg1",
                                "tt_trigger_flag": "trg_double_tau35_mediumiso_hps",
                                "tt_trigger_leg1_sf_name": "ditau",
                                "tt_trigger_leg1_variation": _variation,
                            },
                        ],
                        "doubletau_trigger_leg2_sf": [
                            {
                                "tt_trigger_leg2_flagname": "trg_wgt_doubletau35_leg2",
                                "tt_trigger_flag": "trg_double_tau35_mediumiso_hps",
                                "tt_trigger_leg2_sf_name": "ditau",
                                "tt_trigger_leg2_variation": _variation,
                            },
                        ],
                    },
                },
                producers={
                    ("tt"): [
                        scalefactors.DoubleTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )

    return configuration
