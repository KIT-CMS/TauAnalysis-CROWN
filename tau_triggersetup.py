from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier


def add_diTauTriggerSetup(configuration: Configuration):
    ## MT, MM scope trigger setup
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "singlemuon_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_mu50",
                        #     "hlt_path": "HLT_Mu50",
                        #     "ptcut": 55,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 13,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            "boosted_singlemuon_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_single_mu24_boosted",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_mu27_boosted",
                        #     "hlt_path": "HLT_IsoMu27",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 13,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_mu50_boosted",
                            "hlt_path": "HLT_Mu50",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_oldmu100_boosted",
                            "hlt_path": "HLT_OldMu100",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_tkmu100_boosted",
                            "hlt_path": "HLT_TkMu100",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_cross_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 22,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 22,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                }
            ),
        },
    )
    ## ET, EE scope trigger setup
    configuration.add_config_parameters(
        ["et"],
        {
            "singleelectron_trigger": EraModifier(
                {
                    "2018": [
                        # {
                        #     "flagname": "trg_single_ele27",
                        #     "hlt_path": "HLT_Ele27_WPTight_Gsf",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_ele27",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 28,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            "boosted_singleelectron_trigger": EraModifier(
                {
                    "2018": [
                        # {
                        #     "flagname": "trg_single_ele27_boosted",
                        #     "hlt_path": "HLT_Ele27_WPTight_Gsf",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele32_boosted",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_ele35_boosted",
                        #     "hlt_path": "HLT_Ele35_WPTight_Gsf",
                        #     "ptcut": 36,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele115_boosted",
                            "hlt_path": "HLT_Ele115_CaloIdVT_GsfTrkIdT",
                            "ptcut": 115,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_photon200_boosted",
                            "hlt_path": "HLT_Photon200",
                            "ptcut": 115,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )
    # ET scope crosstrigger
    configuration.add_config_parameters(
        ["et"],
        {
            "eltau_cross_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_ele24tau20",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_ele24tau20",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    ## TT scope trigger setup
    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_double_tau35_mediumiso",
                            "hlt_path": "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_double_tau35_mediumiso",
                            "hlt_path": "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            "boosted_ditau_trigger": EraModifier(
                {
                    "2018": [
                        # {
                        #     "flagname": "trg_ak8pfht750_trimmass50",
                        #     "hlt_path": "HLT_AK8PFHT750_TrimMass50",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfht800_trimmass50",
                        #     "hlt_path": "HLT_AK8PFHT800_TrimMass50",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet60",
                        #     "hlt_path": "HLT_AK8PFJet60",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet80",
                        #     "hlt_path": "HLT_AK8PFJet80",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet140",
                        #     "hlt_path": "HLT_AK8PFJet140",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet200",
                        #     "hlt_path": "HLT_AK8PFJet200",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet260",
                        #     "hlt_path": "HLT_AK8PFJet260",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet320",
                        #     "hlt_path": "HLT_AK8PFJet320",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet400",
                        #     "hlt_path": "HLT_AK8PFJet400",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet40",
                        #     "hlt_path": "HLT_AK8PFJet40",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet450",
                        #     "hlt_path": "HLT_AK8PFJet450",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet500",
                        #     "hlt_path": "HLT_AK8PFJet500",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet360_trimmass30",
                        #     "hlt_path": "HLT_AK8PFJet360_TrimMass30",
                        # },
                        {
                            "flagname": "trg_ak8pfjet400_trimmass30",
                            "hlt_path": "HLT_AK8PFJet400_TrimMass30",
                        },
                        # {
                        #     "flagname": "trg_pfht250",
                        #     "hlt_path": "HLT_PFHT250",
                        # },
                        # {
                        #     "flagname": "trg_pfht350",
                        #     "hlt_path": "HLT_PFHT350",
                        # },
                        # {
                        #     "flagname": "trg_pfjet40",
                        #     "hlt_path": "HLT_PFJet40",
                        # },
                        # {
                        #     "flagname": "trg_pfjet60",
                        #     "hlt_path": "HLT_PFJet60",
                        # },
                        # {
                        #     "flagname": "trg_pfjet80",
                        #     "hlt_path": "HLT_PFJet80",
                        # },
                        # {
                        #     "flagname": "trg_pfjet140",
                        #     "hlt_path": "HLT_PFJet140",
                        # },
                        # {
                        #     "flagname": "trg_pfjet200",
                        #     "hlt_path": "HLT_PFJet200",
                        # },
                        # {
                        #     "flagname": "trg_pfjet260",
                        #     "hlt_path": "HLT_PFJet260",
                        # },
                        # {
                        #     "flagname": "trg_pfjet320",
                        #     "hlt_path": "HLT_PFJet320",
                        # },
                        # {
                        #     "flagname": "trg_pfjet400",
                        #     "hlt_path": "HLT_PFJet400",
                        # },
                        # {
                        #     "flagname": "trg_pfjet450",
                        #     "hlt_path": "HLT_PFJet450",
                        # },
                        # {
                        #     "flagname": "trg_pfjet500",
                        #     "hlt_path": "HLT_PFJet500",
                        # },
                        # {
                        #     "flagname": "trg_pfjet550",
                        #     "hlt_path": "HLT_PFJet550",
                        # },
                        {
                            "flagname": "trg_pfht500_pfmet100_pfmht100_idtight",
                            "hlt_path": "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
                        },
                        # {
                        #     "flagname": "trg_pfht500_pfmet110_pfmht110_idtight",
                        #     "hlt_path": "HLT_PFHT500_PFMET110_PFMHT110_IDTight",
                        # },
                        # {
                        #     "flagname": "trg_pfmet110_pfmht110_idtight",
                        #     "hlt_path": "HLT_PFMET110_PFMHT110_IDTight",
                        # },
                        {
                            "flagname": "trg_pfmet120_pfmht120_idtight",
                            "hlt_path": "HLT_PFMET120_PFMHT120_IDTight",
                        },
                        # {
                        #     "flagname": "trg_pfmetnomu110_pfmhtnomu110_idtight",
                        #     "hlt_path": "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
                        # },
                        {
                            "flagname": "trg_pfmetnomu120_pfmhtnomu120_idtight",
                            "hlt_path": "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
                        },
                    ]
                }
            ),
        },
    )

    ## TT singletau trigger
    # configuration.add_config_parameters(
    #     ["tt"],
    #     {
    #         "singletau_trigger_leading": EraModifier(
    #             {
    #                 "2018": [
    #                     {
    #                         "flagname": "trg_single_tau180_1",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2017": [
    #                     {
    #                         "flagname": "trg_single_tau180_1",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2016postVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #                 "2016preVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #             }
    #         )
    #     },
    # )

    ## trailing singletau trigger
    # configuration.add_config_parameters(
    #     ["et", "mt", "tt"],
    #     {
    #         "singletau_trigger_trailing": EraModifier(
    #             {
    #                 "2018": [
    #                     {
    #                         "flagname": "trg_single_tau180_2",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2017": [
    #                     {
    #                         "flagname": "trg_single_tau180_2",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2016postVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #                 "2016preVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #             }
    #         )
    #     },
    # )

    return configuration
