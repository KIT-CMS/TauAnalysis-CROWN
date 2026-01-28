from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift
from .producers import scalefactors as scalefactors


def add_diTauTriggerSetup(configuration: Configuration) -> Configuration:

    #######################
    #trigger definitions  #
    #######################

    # single muon
    singlemuon_trigger_defaults = {
        "trigger_particle_id": 13,
        "max_deltaR_triggermatch": 0.4,
    }
    
    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            "singlemuon_trigger": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.4,
                            "filterbit": 1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": -1,
                            **singlemuon_trigger_defaults,
                        },
                    ],
                }
            ),
        },
    )

    # mu tau cross trigger
    mutau_cross_trigger_defaults = {
        "p1_etacut": 2.1,
        "p2_etacut": 2.1,
        "p1_trigger_particle_id": 13,
        "p2_trigger_particle_id": 15,
        "max_deltaR_triggermatch": 0.4,
    }
    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_cross_trigger": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 32,
                            "p1_filterbit": 1,
                            "p2_filterbit": 9,  
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p2_ptcut": 32,
                            "p1_filterbit": 3,
                            "p2_filterbit": 4, 
                            **mutau_cross_trigger_defaults,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p2_ptcut": 32,
                            "p1_filterbit": 3,
                            "p2_filterbit": 4, 
                            **mutau_cross_trigger_defaults,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p2_ptcut": 32,
                            "p1_filterbit": 3,
                            "p2_filterbit": 4, 
                            **mutau_cross_trigger_defaults,
                        }
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 22,
                            "p1_filterbit": 3,
                            "p2_filterbit": 4, 
                            **mutau_cross_trigger_defaults,
                        }
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p2_ptcut": 22,
                            "p1_filterbit": 3,
                            "p2_filterbit": 4, 
                            **mutau_cross_trigger_defaults,
                        }
                    ],
                }
            ),
        },
    )

    # single electron
    singleelectron_trigger_defaults = {
        "filterbit": 1, 
        "trigger_particle_id": 11,
        "max_deltaR_triggermatch": 0.4,
    }

    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            "singleelectron_trigger": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_single_ele30",
                            "hlt_path": "HLT_Ele30_WPTight_Gsf",
                            "ptcut": 32,
                            "etacut": 2.5,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_single_ele27",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 28,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_ele27",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 28,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            **singleelectron_trigger_defaults,
                        },
                    ],
                }
            ),
        },
    )

    # e tau cross trigger
    electron_tau_cross_trigger_defaults = {
        "p1_trigger_particle_id": 11,
        "p2_trigger_particle_id": 15,
        "max_deltaR_triggermatch": 0.4,
    }

    configuration.add_config_parameters(
        ["et"],
        {
            "eltau_cross_trigger": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1, 
                            "p1_filterbit": 2, 
                            "p2_filterbit": 3,  
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO check if the filter bit is correct
                            "p2_filterbit": 4,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            **electron_tau_cross_trigger_defaults,
                        },
                    ],
                }
            ),
        },
    )

    # di tau trigger
    doubletau_trigger_defaults = {
        "p1_trigger_particle_id": 15,
        "p2_trigger_particle_id": 15,
        "max_deltaR_triggermatch": 0.4,
    }
    
    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_double_tau30_mediumiso_pnet",
                            "hlt_path": "HLT_DoublePNetTauhPFJet30_Medium_L2NN_eta2p3",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.3,
                            "p2_etacut": 2.3,
                            "p1_filterbit": 11,
                            "p2_filterbit": 11,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_double_tau30_mediumiso_pnet",
                            "hlt_path": "HLT_DoublePNetTauhPFJet30_Medium_L2NN_eta2p3",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.3,
                            "p2_etacut": 2.3,
                            "p1_filterbit": 11,
                            "p2_filterbit": 11,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 7,
                            "p2_filterbit": 7,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 7,
                            "p2_filterbit": 7,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 7,
                            "p2_filterbit": 7,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumDeepTauPFTauHPS35_L2NN_eta2p1",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 7,
                            "p2_filterbit": 7,
                            **doubletau_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
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
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
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
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            **doubletau_trigger_defaults,
                        },
                    ],
                }
            ),
        },
    )

    # e mu cross trigger
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
            "elmu_cross_trigger": EraModifier(
                {
                    "2025": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2024": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2022postEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2022preEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 12,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2018": [
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
                    "2017": [
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
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_mu23ele12_dz",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 13,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu8ele23_dz",
                            "hlt_path": "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 24,
                            "p2_ptcut": 9,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                            "p1_ptcut": 13,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu8ele23",
                            "hlt_path": "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
                            "p1_ptcut": 24,
                            "p2_ptcut": 9,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_mu23ele12_dz",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 13,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu8ele23_dz",
                            "hlt_path": "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                            "p1_ptcut": 24,
                            "p2_ptcut": 9,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu23ele12",
                            "hlt_path": "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                            "p1_ptcut": 13,
                            "p2_ptcut": 24,
                            **elmu_cross_trigger_defaults,
                        },
                        {
                            "flagname": "trg_cross_mu8ele23",
                            "hlt_path": "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
                            "p1_ptcut": 24,
                            "p2_ptcut": 9,
                            **elmu_cross_trigger_defaults,
                        },
                    ],
                }
            ),
        },
    )

    # leading single tau triggers
    singletau_trigger_defaults = {
        "etacut": 2.1,
        "filterbit": 5,
        "trigger_particle_id": 15,
        "max_deltaR_triggermatch": 0.4,
    }

    configuration.add_config_parameters(
        ["tt"],
        {
            "singletau_trigger_leading": EraModifier(
                {
                    "2025": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2024": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2022postEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2022preEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        }
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_tau180_1",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_defaults,
                        }
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_tau120_1",
                            "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
                            "ptcut": 120,
                            **singletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_tau140_1",
                            "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
                            "ptcut": 140,
                            **singletau_trigger_defaults,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_tau120_1",
                            "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
                            "ptcut": 120,
                            **singletau_trigger_defaults,
                        },
                        {
                            "flagname": "trg_single_tau140_1",
                            "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
                            "ptcut": 140,
                            **singletau_trigger_defaults,
                        },
                    ],
                }
            )
        },
    )

    # trailing singletau trigger
    singletau_trigger_trailing_defaults = {
        "etacut": 2.1,
        "filterbit": 5,
        "trigger_particle_id": 15,
        "max_deltaR_triggermatch": 0.4,
    }

    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "singletau_trigger_trailing": EraModifier(
                {
                    "2025": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2024": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2022postEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2022preEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        }
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            **singletau_trigger_trailing_defaults,
                        }
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_tau120_2",
                            "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
                            "ptcut": 120,
                            **singletau_trigger_trailing_defaults,
                        },
                        {
                            "flagname": "trg_single_tau140_2",
                            "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
                            "ptcut": 140,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_tau120_2",
                            "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
                            "ptcut": 120,
                            **singletau_trigger_trailing_defaults,
                        },
                        {
                            "flagname": "trg_single_tau140_2",
                            "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
                            "ptcut": 140,
                            **singletau_trigger_trailing_defaults,
                        },
                    ],
                }
            )
        },
    )

    # doubleelectron trigger  # applying the same defaults as for the singleelectron trigger
    doubleelectron_trigger_defaults = {  # TODO check if (even?) this is (still) correct
        "flagname": "trg_double_ele24",
        "hlt_path": "HLT_DoubleEle24_eta2p1_WPTight_Gsf",
        "p1_ptcut": 24,
        "p2_ptcut": 24,
        "p1_ptcut": 24,
        "p2_ptcut": 24,
        "p1_etacut": 2.1,
        "p1_filterbit": 4,
        "p1_trigger_particle_id": 11,
        "p2_etacut": 2.1,
        "p2_filterbit": 4,
        "p2_trigger_particle_id": 11,
        "max_deltaR_triggermatch": 0.4,
    }
    configuration.add_config_parameters(
        ["ee"],
        {
            "doubleelectron_trigger": doubleelectron_trigger_defaults,
        },
    )


    #######################
    #trigger scale factors#
    #######################

    # muon trigger scale factors
    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            "mutau_cross_trigger_leg1_sf_file": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""', 
                    "2017": '""',
                    "2018": '""',
                    "2022preEE": '"data/hleprare/TriggerScaleFactors/2022preEE/CrossMuTauHlt_MuLeg_v1.json"',
                    "2022postEE": '"data/hleprare/TriggerScaleFactors/2022postEE/CrossMuTauHlt_MuLeg_v1.json"',
                    "2023preBPix": '"data/hleprare/TriggerScaleFactors/2023preBPix/CrossMuTauHlt_MuLeg_v1.json"',
                    "2023postBPix": '"data/hleprare/TriggerScaleFactors/2023postBPix/CrossMuTauHlt_MuLeg_v1.json"',
                    "2024":'"data/hleprare/TriggerScaleFactors/2023postBPix/CrossMuTauHlt_MuLeg_v1.json"',
                    "2025":'"data/hleprare/TriggerScaleFactors/2023postBPix/CrossMuTauHlt_MuLeg_v1.json"',
                }
            ),
            "singlemuon_trigger_sf": [
                {
                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                    "singlemuon_trigger_flag": "trg_single_mu24",
                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                    "singlemuon_trigger_variation": "nominal",
                },
            ],

            "mutau_trigger_leg1_sf": [
                {
                    "mutau_cross_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                    "mutau_cross_trigger_flag": "trg_cross_mu20tau27_hps",
                    "mutau_cross_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                    "mutau_cross_trigger_leg1_variation": "nominal",
                },
            ],
            "mutau_trigger_leg2_sf": [
                {
                    "mutau_cross_trigger_leg2_flagname": "trg_wgt_mu20tau27_leg2",
                    "mutau_cross_trigger_flag": "trg_cross_mu20tau27_hps",
                    "mutau_cross_trigger_leg2_sf_name": "mutau",
                    "mutau_cross_trigger_leg2_variation": "nom",
                },
            ],
        },
    )

    # electron scale factors
    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            "singleelectron_trigger_sf_file": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""', 
                    "2017": '""',
                    "2018": '""',
                    "2022preEE": "data/jsonpog-integration/POG/EGM/2022_Summer22/electronHlt.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electronHlt.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/EGM/2023_Summer23/electronHlt.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electronHlt.json.gz",
                    "2024": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electronHlt.json.gz",
                    "2025": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electronHlt.json.gz",
                }
            ),
            "singleelctron_trigger_era": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""', 
                    "2017": '""',
                    "2018": '""',
                    "2022preEE": "2022Re-recoBCD",
                    "2022postEE": "2022Re-recoE+PromptFG",
                    "2023preBPix": "2023PromptC",
                    "2023postBPix": "2023PromptD",
                    "2024": "2023PromptD",
                    "2025": "2023PromptD",
                }
            ),
            "singleelectron_trigger_sf": [
                {
                    "singleelectron_trigger_flagname": "trg_wgt_single_ele30",
                    "singleelectron_trigger_flag": "trg_single_ele30",
                    "singleelectron_trigger_sf_name": "Electron-HLT-SF",
                    "singleelectron_trigger_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                    "singleelectron_trigger_variation": "sf",
                },
            ],

            "eletau_cross_trigger_leg1_sf_file": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""', 
                    "2017": '""',
                    "2018": '""',
                    "2022preEE": "data/hleprare/TriggerScaleFactors/2022preEE/CrossEleTauHlt_EleLeg_v1.json",
                    "2022postEE": "data/hleprare/TriggerScaleFactors/2022postEE/CrossEleTauHlt_EleLeg_v1.json",
                    "2023preBPix": "data/hleprare/TriggerScaleFactors/2023preBPix/CrossEleTauHlt_EleLeg_v1.json",
                    "2023postBPix": "data/hleprare/TriggerScaleFactors/2023postBPix/CrossEleTauHlt_EleLeg_v1.json",
                    "2024": "data/hleprare/TriggerScaleFactors/2023postBPix/CrossEleTauHlt_EleLeg_v1.json",
                    "2025": "data/hleprare/TriggerScaleFactors/2023postBPix/CrossEleTauHlt_EleLeg_v1.json",
                }
            ),
            "eletau_cross_trigger_leg1_sf": [
                {
                    "eletau_cross_trigger_flag": "trg_cross_ele24tau30_hps",
                    "eletau_cross_trigger_leg1_flagname": "trg_wgt_ele24tau30_leg1",
                    "eletau_cross_trigger_leg1_sf_name": "Electron-HLT-SF",
                    "eletau_cross_trigger_leg1_path_id_name": "HLT_SF_Ele24_TightID",
                    "eletau_cross_trigger_leg1_variation": "sf",
                },
            ],
            "eletau_cross_trigger_leg2_sf": [
                {
                    "eletau_cross_trigger_leg2_flagname": "trg_wgt_ele24tau30_leg2",
                    "eletau_cross_trigger_flag": "trg_cross_ele24tau30_hps",
                    "eletau_cross_trigger_leg2_sf_name": "etau",
                    "eletau_cross_trigger_leg2_variation": "nom",
                },
            ]
        },
    )

    # double tau-tau trigger scale factors
    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger_leg1_sf": [
                {
                    "doubletau_trigger_leg1_flagname": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE": "trg_wgt_doubletau35_leg1",
                            "2022postEE": "trg_wgt_doubletau35_leg1",
                            "2023preBPix": "trg_wgt_doubletau35_leg1",
                            "2023postBPix": "trg_wgt_doubletau35_leg1",
                            "2024": "trg_wgt_doubletau30_leg1",
                            "2025": "trg_wgt_doubletau30_leg1",
                        }
                    ),
                    "doubletau_trigger_flag": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE": "trg_double_tau35_mediumiso_hps",
                            "2022postEE": "trg_double_tau35_mediumiso_hps",
                            "2023preBPix": "trg_double_tau35_mediumiso_hps",
                            "2023postBPix": "trg_double_tau35_mediumiso_hps",
                            "2024": "trg_double_tau30_mediumiso_pnet",
                            "2025": "trg_double_tau30_mediumiso_pnet",
                        }
                    ),
                    "doubletau_trigger_leg1_sf_name": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE":"ditau",
                            "2022postEE":"ditau",
                            "2023preBPix":"ditau",
                            "2023postBPix":"ditau",
                            "2024":"ditau_pnet_medium",
                            "2025":"ditau_pnet_medium"
                        }
                    ),
                    "doubletau_trigger_leg1_variation": "nom",
                },
            ],
            "doubletau_trigger_leg2_sf": [
                {
                    "doubletau_trigger_leg2_flagname": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE": "trg_wgt_doubletau35_leg2",
                            "2022postEE": "trg_wgt_doubletau35_leg2",
                            "2023preBPix": "trg_wgt_doubletau35_leg2",
                            "2023postBPix": "trg_wgt_doubletau35_leg2",
                            "2024": "trg_wgt_doubletau30_leg2",
                            "2025": "trg_wgt_doubletau30_leg2",
                        }
                    ),
                    "doubletau_trigger_flag": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE": "trg_double_tau35_mediumiso_hps",
                            "2022postEE": "trg_double_tau35_mediumiso_hps",
                            "2023preBPix": "trg_double_tau35_mediumiso_hps",
                            "2023postBPix": "trg_double_tau35_mediumiso_hps",
                            "2024": "trg_double_tau30_mediumiso_pnet",
                            "2025": "trg_double_tau30_mediumiso_pnet",
                        }
                    ),
                    "doubletau_trigger_leg2_sf_name": EraModifier(
                        {
                            "2016preVFP": '""',
                            "2016postVFP": '""', 
                            "2017": '""',
                            "2018": '""',
                            "2022preEE":"ditau",
                            "2022postEE":"ditau",
                            "2023preBPix":"ditau",
                            "2023postBPix":"ditau",
                            "2024":"ditau_pnet_medium",
                            "2025":"ditau_pnet_medium"
                        }
                    ),
                    "doubletau_trigger_leg2_variation": "nom",
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
                        "singleelectron_trigger_sf": [
                            {
                                "singleelectron_trigger_flagname": "trg_wgt_single_ele30",
                                "singleelectron_trigger_flag": "trg_single_ele30",
                                "singleelectron_trigger_sf_name": "Electron-HLT-SF",
                                "singleelectron_trigger_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                                "singleelectron_trigger_variation": f"sf{_variation}",
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
                        "eletau_cross_trigger_leg1_sf": [
                            {
                                "eletau_cross_trigger_leg1_flagname": "trg_wgt_ele24tau30_leg1",
                                "eletau_cross_trigger_flag": "trg_cross_ele24tau30_hps",
                                "eletau_cross_trigger_leg1_sf_name": "Electron-HLT-SF",
                                "eletau_cross_trigger_leg1_path_id_name": "HLT_SF_Ele24_TightID",
                                "eletau_cross_trigger_leg1_variation": f"sf{_variation}",
                            },
                        ],
                        "eletau_cross_trigger_leg2_sf": [
                            {
                                "eletau_cross_trigger_leg2_flagname": "trg_wgt_ele24tau30_leg2",
                                "eletau_cross_trigger_flag": "trg_cross_ele24tau30_hps",
                                "eletau_cross_trigger_leg2_sf_name": "etau",
                                "eletau_cross_trigger_leg2_variation": _variation,
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
                            "singlemuon_trigger_sf": [
                                {
                                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                                    "singlemuon_trigger_flag": "trg_single_mu24",
                                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "singlemuon_trigger_variation": f"syst{_variation}",
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
                                "mutau_cross_trigger_flag": "trg_cross_mu20tau27_hps",
                                "mutau_cross_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                                "mutau_cross_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                                "mutau_cross_trigger_leg1_variation": f"syst{_variation}",
                            },
                        ],
                        "mutau_trigger_leg2_sf": [
                            {
                                "mutau_cross_trigger_flag": "trg_cross_mu20tau27_hps",
                                "mutau_cross_trigger_leg2_flagname": "trg_wgt_mu20tau27_leg2",
                                "mutau_cross_trigger_leg2_sf_name": "mutau",
                                "mutau_cross_trigger_leg2_variation": _variation,
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
                                "doubletau_trigger_leg1_flagname": EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE": "trg_wgt_doubletau35_leg1",
                                        "2022postEE": "trg_wgt_doubletau35_leg1",
                                        "2023preBPix": "trg_wgt_doubletau35_leg1",
                                        "2023postBPix": "trg_wgt_doubletau35_leg1",
                                        "2024": "trg_wgt_doubletau30_leg1",
                                        "2025": "trg_wgt_doubletau30_leg1",
                                    }
                                ),
                                "doubletau_trigger_flag":  EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE": "trg_double_tau35_mediumiso_hps",
                                        "2022postEE": "trg_double_tau35_mediumiso_hps",
                                        "2023preBPix": "trg_double_tau35_mediumiso_hps",
                                        "2023postBPix": "trg_double_tau35_mediumiso_hps",
                                        "2024": "trg_double_tau30_mediumiso_pnet",
                                        "2025": "trg_double_tau30_mediumiso_pnet",
                                    }
                                ),
                                "doubletau_trigger_leg1_sf_name": EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE":"ditau",
                                        "2022postEE":"ditau",
                                        "2023preBPix":"ditau",
                                        "2023postBPix":"ditau",
                                        "2024":"ditau_pnet_medium",
                                        "2025":"ditau_pnet_medium"
                                    }
                                ),
                                "doubletau_trigger_leg1_variation": _variation,
                            },
                        ],
                        "doubletau_trigger_leg2_sf": [
                            {
                                "doubletau_trigger_leg2_flagname": EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE": "trg_wgt_doubletau35_leg2",
                                        "2022postEE": "trg_wgt_doubletau35_leg2",
                                        "2023preBPix": "trg_wgt_doubletau35_leg2",
                                        "2023postBPix": "trg_wgt_doubletau35_leg2",
                                        "2024": "trg_wgt_doubletau30_leg2",
                                        "2025": "trg_wgt_doubletau30_leg2",
                                    }
                                ),
                                "doubletau_trigger_flag":  EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE": "trg_double_tau35_mediumiso_hps",
                                        "2022postEE": "trg_double_tau35_mediumiso_hps",
                                        "2023preBPix": "trg_double_tau35_mediumiso_hps",
                                        "2023postBPix": "trg_double_tau35_mediumiso_hps",
                                        "2024": "trg_double_tau30_mediumiso_pnet",
                                        "2025": "trg_double_tau30_mediumiso_pnet",
                                    }
                                ),
                                "doubletau_trigger_leg2_sf_name": EraModifier(
                                    {
                                        "2016preVFP": '""',
                                        "2016postVFP": '""', 
                                        "2017": '""',
                                        "2018": '""',
                                        "2022preEE":"ditau",
                                        "2022postEE":"ditau",
                                        "2023preBPix":"ditau",
                                        "2023postBPix":"ditau",
                                        "2024":"ditau_pnet_medium",
                                        "2025":"ditau_pnet_medium"
                                    }
                                ),
                                "doubletau_trigger_leg2_variation": _variation,
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

        # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "singlemuon_trigger_sf_mc": EraModifier(
                {
                    "2025": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2024": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022postEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022preEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "mc_trigger_sf": "Trg_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "mc_trigger_sf": "Trg_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                }
            )
        },
    )
    # electron trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["et", "ee"],
        {
            "singlelectron_trigger_sf_mc": EraModifier(
                {
                    "2025": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2024": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022postEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022preEE": [ ## TODO: not implemented, here as a placeholder
                        {
                            "flagname": '""',
                            "mc_trigger_sf": '""',
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_wgt_single_ele25",
                            "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        }
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_wgt_single_ele25",
                            "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                        }
                    ],
                }
            )
        },
    )
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFUp",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": EraModifier(
                        {
                            "2025": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2024": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022postEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022preEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_ele32orele35",
                                    "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele32",
                                    "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele35",
                                    "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele27orele32orele35",
                                    "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_ele32orele35",
                                    "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele32",
                                    "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele35",
                                    "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele27orele32orele35",
                                    "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_ele25",
                                    "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                }
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_ele25",
                                    "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 1.02,
                                }
                            ],
                        }
                    )
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFDown",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": EraModifier(
                        {
                            "2025": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                                "2024": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                                "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                                "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                                "2022postEE": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                                "2022preEE": [ ## TODO: not implemented, here as a placeholder
                                    {
                                        "flagname": '""',
                                        "mc_trigger_sf": '""',
                                        "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                                    },
                                ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_ele32orele35",
                                    "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele32",
                                    "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele35",
                                    "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele27orele32orele35",
                                    "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_ele32orele35",
                                    "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele32",
                                    "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele35",
                                    "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_ele27orele32orele35",
                                    "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_ele25",
                                    "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                }
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_ele25",
                                    "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                    "mc_electron_trg_extrapolation": 0.98,
                                }
                            ],
                        }
                    )
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            "2025": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2024": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022postEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022preEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "mc_trigger_sf": "Trg_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "mc_trigger_sf": "Trg_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 1.02,
                                },
                            ],
                        }
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            "2025": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2024": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023postBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023preBPix": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022postEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022preEE": [ ## TODO: not implemented, here as a placeholder
                                {
                                    "flagname": '""',
                                    "mc_trigger_sf": '""',
                                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "mc_trigger_sf": "Trg_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "mc_trigger_sf": "Trg_pt_eta_bins",
                                    "mc_muon_trg_extrapolation": 0.98,
                                },
                            ],
                        }
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    return configuration