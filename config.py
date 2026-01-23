from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List
from itertools import product

from .producers import electrons as electrons
from .producers import event as event
from .producers import genparticles as genparticles
from .producers import jets as jets
from .producers import met as met
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .producers import taus as taus
from .producers import triggers as triggers
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from .tau_triggersetup import add_diTauTriggerSetup
from .tau_variations import add_tauVariations
from .jet_variations import add_jetVariations
#from .tau_embedding_settings import setup_embedding
#from .jec_data import add_jetCorrectionData
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift
from .scripts.SpecialSetups import ES_ID_SCHEME


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
) -> Configuration:
    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    configuration.ES_ID_SCHEME = ES_ID_SCHEME("dm_binned_run3")

    ###########################
    ####### Parameters ########
    ###########################

    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        ["global", "tt", "mt", "et", "ee", "mm", "em"],
        {
            # lhc era parameter
            "era": era,
        }
    )
    configuration.add_config_parameters(
        "global",
        {
            # for LHE weights
            "muR": 1.0,
            "muF": 1.0,
            "isr": 1.0,
            "fsr": 1.0,

            # dy selection for bug samples
            "DY_flavors_list": "11,13",
            
            # pdf variations
            "pdf_variation": "nominal",
            "pdf_alphaS_variation": "nominal",
            
            # golden json
            "golden_json_file": EraModifier(
                {
                    "2022preEE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    "2022postEE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    "2023preBPix": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                    "2023postBPix": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                    "2024": "data/golden_json/Cert_Collisions2024_378981_386951_Golden.json",
                    "2025": "data/golden_json/Cert_Collisions2025_391658_398860_Golden.json", # last Run2025G run is 398903, update golden json when available
                }
            ),
            
            # noise filters
            #https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC
            "met_filters": [
                "Flag_goodVertices",
                "Flag_globalSuperTightHalo2016Filter",
                "Flag_EcalDeadCellTriggerPrimitiveFilter",
                "Flag_BadPFMuonFilter",
                "Flag_BadPFMuonDzFilter",
                "Flag_hfNoisyHitsFilter",
                "Flag_eeBadScFilter",
                "Flag_ecalBadCalibFilter",  
            ],
            
            # pileup corrections
            "PU_reweighting_file": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/LUM/2022_Summer22/puWeights.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/LUM/2022_Summer22EE/puWeights.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23/puWeights.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23BPix/puWeights.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/puWeights_BCDEFGHI.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/puWeights_BCDEFGHI.json.gz",
                }
            ),
            "PU_reweighting_file_data": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/LUM/2022_Summer22/puWeights.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/LUM/2022_Summer22EE/puWeights.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23/puWeights.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23BPix/puWeights.json.gz",
                    "2024": "data/Data_PileUp_2024_69p2.root",
                    "2025": "data/Data_PileUp_2024_69p2.root",
                }
            ),
            "PU_reweighting_file_mc": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/LUM/2022_Summer22/puWeights.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/LUM/2022_Summer22EE/puWeights.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23/puWeights.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/LUM/2023_Summer23BPix/puWeights.json.gz",
                    "2024": "data/MC_PileUp_2024.root",
                    "2025": "data/MC_PileUp_2024.root",
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2022preEE": "Collisions2022_355100_357900_eraBCD_GoldenJson",
                    "2022postEE": "Collisions2022_359022_362760_eraEFG_GoldenJson",
                    "2023preBPix": "Collisions2023_366403_369802_eraBC_GoldenJson",
                    "2023postBPix": "Collisions2023_369803_370790_eraD_GoldenJson",
                    "2024": "Collisions24_BCDEFGHI_goldenJSON",
                    "2025": "Collisions24_BCDEFGHI_goldenJSON",
                }
            ),
            "PU_reweighting_variation": "nominal",

            # muon base selection
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.4,
            "max_muon_dxy": 0.045,
            "max_muon_dz": 0.2,
            "muon_id": "Muon_mediumId",
            "muon_iso_cut": 0.25, ##https://indico.cern.ch/event/1495537/contributions/6359516/attachments/3014424/5315938/HLepRare_25.02.14.pdf add it in the trigger to be 0.15 for signal muons??
            
            # electron base selection
            "min_ele_pt": 10.0,
            "max_ele_eta": 2.5,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "ele_iso_cut": 0.25,
            # electron energy scale
            "ele_es_master_seed": 44,
            "ele_es_mc_name": '"SmearAndSyst"',
            "ele_es_data_name": '"Scale"',
            "ele_es_file": EraModifier(
                {
                    "2022preEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz"',
                    "2022postEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz"',
                    "2023preBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz"',
                    "2023postBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz"',
                    "2024": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-15/electronSS_EtDependent.json.gz"',
                    "2025": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-15/electronSS_EtDependent.json.gz"',
                }
            ),
            "ele_es_variation": "nom",

            # jet base selection
            "min_jet_pt_loose": 30,
            "min_jet_pt_tight": 50,
            "jet_eta_1": 2.5,
            "jet_eta_2": 3,
            "jet_eta_3": 4.7,
            "jet_id": 2,  #2==pass tight ID and fail tightLepVeto, 6== pass tight and pass tightLepVeto, new minimal selection https://cms-talk.web.cern.ch/t/updated-jet-selection-criterion-for-jet-veto-map/130527
            # bjet selection -> need to be in global
            "min_bjet_pt": 20,
            "max_bjet_eta": 2.5,
            "btag_cut": EraModifier( ## values from the wiki for a medium wp https://btv-wiki.docs.cern.ch/ScaleFactors
                {
                    # wp for deepJEt
                    # "2022preEE": 0.3086, 
                    # "2022postEE": 0.3196,
                    # "2023preBPix": 0.2431,
                    # "2023postBPix": 0.2435,
                    # wp for partNet
                    "2022preEE": 0.245, 
                    "2022postEE": 0.2605,
                    "2023preBPix": 0.1917,
                    "2023postBPix": 0.1919,
                    "2024": 0.1272,
                    "2025": 0.1272,
                }
            ),
            # jet energy calibration 
            "jet_id_json": EraModifier(
                {
                    "2022preEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jetid.json.gz"',
                    "2022postEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jetid.json.gz"',
                    "2023preBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07jetid.json.gz"',
                    "2023postBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jetid.json.gz"',
                    "2024": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetid.json.gz"',
                    "2025": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetid.json.gz"',
                }
            ),
            "jet_collection_name":'"AK4PUPPI"',
            "jer_master_seed": 42,
            "jet_reapplyJES": True,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jes_tag_mc": EraModifier(
                {
                    "2022preEE": '"Summer22_22Sep2023_V3_MC"',
                    "2022postEE": '"Summer22EE_22Sep2023_V3_MC"',
                    "2023preBPix": '"Summer23Prompt23_V2_MC"',
                    "2023postBPix": '"Summer23BPixPrompt23_V3_MC"',
                    "2024": '"Summer24Prompt24_V2_MC"',
                    "2025": '"Winter25Prompt25_V2_MC"',
                }
            ),
            "jet_jes_tag_data": EraModifier(
                {
                    "2022preEE": '"Summer22_22Sep2023_RunCD_V3_DATA"',
                    "2022postEE": '""',
                    "2023preBPix": '"Summer23Prompt23_V2_DATA"',
                    "2023postBPix": '"Summer23BPixPrompt23_V3_DATA"',
                    "2024": '"Summer24Prompt24_V2_DATA"',
                    "2025": '"Winter25Prompt25_V2_DATA"',
                }
            ),
            # jet resolution correction
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jer_file": EraModifier(
                {
                    "2022preEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jet_jerc.json.gz"',
                    "2022postEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jet_jerc.json.gz"',
                    "2023preBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07/jet_jerc.json.gz"',
                    "2023postBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jet_jerc.json.gz"',
                    "2024": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jet_jerc.json.gz"',
                    "2025": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Winter25-NanoAODv15/2025-10-27/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2022preEE": '"Summer22_22Sep2023_JRV1_MC"',
                    "2022postEE": '"Summer22EE_22Sep2023_JRV1_MC"',
                    "2023preBPix": '"Summer23Prompt23_RunCv1234_JRV1_MC"',
                    "2023postBPix": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                    "2024": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                    "2025": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                }
            ),
            "jet_jec_algo": '"AK4PFPuppi"',
            # jet veto configuration
            "jet_veto_map_file": EraModifier(
                {
                    "2022preEE":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jetvetomaps.json.gz",
                    "2022postEE":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                    "2023preBPix":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                    "2023postBPix":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                    "2024":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetvetomaps.json.gz",
                    "2025":"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Winter25-NanoAODv15/2025-10-27/jetvetomaps.json.gz",
                }
            ),
            "jet_veto_map_name": EraModifier(
                {
                    "2022preEE": "Summer22_23Sep2023_RunCD_V1",
                    "2022postEE": "Summer22EE_23Sep2023_RunEFG_V1",
                    "2023preBPix": "Summer23Prompt23_RunC_V1",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_V1",
                    "2024": "Summer24Prompt24_RunBCDEFGHI_V1",
                    "2025": "Winter25Prompt25_RunCDE_V1",
                },
            ),
            "jet_veto_map_type": "jetvetomap",
            "jet_veto_min_pt": 15.0,
            "jet_veto_id_wp": 6,  # tightLepVeto
            "jet_veto_max_em_frac": 0.9,

            # lepton veto base selection
            "min_dielectronveto_pt": 15.0,
            "dielectronveto_id": "Electron_cutBased",
            "dielectronveto_id_wp": 1,
            "min_dimuonveto_pt": 15.0,
            "dimuonveto_id": "Muon_looseId",
            "dileptonveto_dR": 0.15,
        },
    )
    configuration.add_config_parameters(
        scopes,
        {
            # bjet scale factors -> needs to be in scopes
            "btag_sf_file": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/BTV/2023_Summer23/btagging.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/BTV/2023_Summer23BPix/btagging.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/btagging_preliminary.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/btagging_preliminary.json.gz",
                }
            ),
            "btag_sf_variation": "central",
            "btag_corr_algo": EraModifier(
                {
                    "2022preEE":"particleNet_shape", 
                    "2022postEE":"particleNet_shape",
                    "2023preBPix":"particleNet_shape",
                    "2023postBPix":"particleNet_shape",
                    "2024":"UParTAK4_kinfit",
                    "2025":"UParTAK4_kinfit",
                }
            ),
            "btag_wp":"M",
            # jet selection
            "deltaR_jet_veto": 0.5,
            # pair selection
            "pairselection_min_dR": 0.5,
            # propagate jet and lepton sf correction to the met
            "propagateLeptons": SampleModifier(
                {"data": False,
                "data_E": False,
                "data_F": False,
                "data_G": False},
                default=True,
            ),
            "propagateJets": True,
            # recoil corrections
            "recoil_corrections_file": EraModifier(
                {
                    "2022preEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                    "2025": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                }
            ),
            "recoil_method": "QuantileMapHist", #other option is pure "Resclaing"
            "recoil_variation": '""',
            "applyRecoilCorrections": SampleModifier( #apply only to single boson processes
                {
                    "dyjets_powheg": True,
                    "dyjets_amcatnlo": True,
                    "dyjets_amcatnlo_ll": True,
                    "dyjets_amcatnlo_tt": True,
                    "wjets": True,
                    "wjets_amcatnlo": True,
                },
                default=False,
            ),
            "min_jetpt_met_propagation": 15,

            # zpt reweighting for DY samples
            "zpt_file": EraModifier(
                {
                    "2022preEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                    "2025": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                }
            ),
            "DY_order": SampleModifier(
                {"dyjets_powheg": "NNLO"}, 
                default="NLO",
            ), #from GrASP it looks like the DY powheg samples are also NLO and not NNLO
            "zpt_variation":"nom",

            # STXS weights
            "ggHNNLOweightsRootfile": "data/htxs/NNLOPS_reweight.root",
            "ggH_generator": "powheg",
        },
    )
    ###### scope Specifics ######
    configuration.add_config_parameters(
        ["mt", "tt", "et"],
        {
            #id flags
            "tau_id_algorithm": "DeepTau2018v2p5",
            "vsjet_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2018v2p5VSjet",
                    "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(wp=wp),
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsjet_id_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                    "vsjet_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    #"Loose": 4, 
                    "Medium": 5,
                    #"Tight": 6,
                    #"VTight": 7,
                    #"VVTight": 8, 
                }.items()
            ],
            "vsele_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2018v2p5VSe",
                    "tau_1_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_1".format(wp=wp),
                    "tau_2_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_2".format(wp=wp),
                    "vsele_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsele_id_outputname": "id_tau_vsEle_{wp}_1".format(wp=wp),
                    "tau_2_vsele_id_outputname": "id_tau_vsEle_{wp}_2".format(wp=wp),
                    "vsele_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VVLoose": 2,
                    #"VLoose": 3,
                    #"Loose": 4,
                    #"Medium": 5,
                    "Tight": 6,
                    #"VTight": 7,
                    #"VVTight": 8,
                }.items()
            ],
            "vsmu_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2018v2p5VSmu",
                    "tau_1_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_{wp_ele}_1".format(wp=wp, wp_ele=wp_ele),
                    "tau_2_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_{wp_ele}_2".format(wp=wp, wp_ele=wp_ele),
                    "vsmu_tau_id_WP": "{wp}".format(wp=wp),
                    "vsele_tau_id_WP": "{wp_ele}".format(wp_ele=wp_ele),
                    "vsjet_tau_id_WP": "Medium", #eventually add more if available and used
                    "tau_1_vsmu_id_outputname": "id_tau_vsMu_{wp}_{wp_ele}_1".format(wp=wp, wp_ele=wp_ele),
                    "tau_2_vsmu_id_outputname": "id_tau_vsMu_{wp}_{wp_ele}_2".format(wp=wp, wp_ele=wp_ele),
                    "vsmu_tau_id_WPbit": bit,
                }
                for (wp, bit), wp_ele in product(
                    {
                        "VLoose": 1,
                        "Loose": 2,
                        "Medium": 3,
                        "Tight": 4,
                    }.items(),
                    [
                        "VVLoose",
                        "Tight",
                    ],
                )
            ],
            # wp for tau pt correction
            "tau_vsjet_wp": '"Medium"', ##change again to Loose if it becomes available
            "tau_vsele_wp": '"VVLoose"',
            # ID flags without where scalefactors does not exist or are requiered withouth them
            # for Run 3 new TAU corrections, only the Medium wp sf are provided
            "vsjet_tau_id_wp_bit": [
                {
                    "vsjet_tau_id_WPbit": bit,
                    "tau_1_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                }
                for wp, bit in dict(
                    VVVLoose = 1,
                    VVLoose = 2,
                    VLoose = 3,
                    Loose = 4, 
                    Tight = 6,
                ).items()
            ],
            #scale factor
            "tau_sf_file": EraModifier(
                {
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-25/tau.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-25/tau.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23CSep23-Summer23-NanoAODv12/2025-12-25/tau.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-25/tau.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-25/tau.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-25/tau.json.gz",
                }
            ),
            "tau_sf_vsele_barrel": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsele_endcap": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsmu_wheel1": "nom",
            "tau_sf_vsmu_wheel2": "nom",
            "tau_sf_vsmu_wheel3": "nom",
            "tau_sf_vsmu_wheel4": "nom",
            "tau_sf_vsmu_wheel5": "nom",
            #decay modes
            "tau_dms": "0,1,10,11",
            #energy scale
            "tau_ES_json_name": "tau_energy_scale",
            "tau_ES_shift_DM0": "nom",
            "tau_ES_shift_DM1": "nom",
            "tau_ES_shift_DM10": "nom",
            "tau_ES_shift_DM11": "nom",
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_mufake_es": "nom",
            # trigger SF
            "ditau_trigger_wp": "Medium",
            "ditau_trigger_corrtype": "sf",
            "ditau_trigger_syst": "nom",
        },
    )
    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            # Muon scale factors configuration
            "muon_sf_file": EraModifier(
                {
                    "2022preEE": "data/jsonpog-integration/POG/MUO/2022_Summer22/muon_Z.json.gz",
                    "2022postEE": "data/jsonpog-integration/POG/MUO/2022_Summer22EE/muon_Z.json.gz",
                    "2023preBPix": "data/jsonpog-integration/POG/MUO/2023_Summer23/muon_Z.json.gz",
                    "2023postBPix": "data/jsonpog-integration/POG/MUO/2023_Summer23BPix/muon_Z.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",  # correction for mediumId WP
            "muon_iso_sf_name": "NUM_TightPFIso_DEN_MediumID",  # correction for TightPFIso WP (PF isolation < 0.15)
            "muon_sf_variation": "nominal",  # "systup"/"systdown" are up/down variations
        },
    )
    configuration.add_config_parameters(
        ["mt", "et"],
        {
            # tau selection 
            "min_tau_pt": 20.0,
            "max_tau_eta": 2.5, ##run 3 recommendation
            "max_tau_dz": 0.2,
            # tau wp selection, set to the first loosest wp
            "vsjet_tau_wp_cut": 1, #change back to 4 if Loose becomes available
            "vsele_tau_wp_cut": 2, 
            "vsmu_tau_wp_cut": 1,
            # tau sf variation
            "tau_sf_vsjet_tau30to35": "nom",
            "tau_sf_vsjet_tau35to40": "nom",
            "tau_sf_vsjet_tau40to500": "nom",
            "tau_sf_vsjet_tau500to1000": "nom",
            "tau_sf_vsjet_tau1000toinf": "nom",
            "tau_vsjet_sf_dependence": "dm",  # "pt in run2 but now "dm to work otherwise pt means only objects with pt>140 gev"
        },
    )
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            #muon selection
            "muon_index_in_pair": 0,
            "min_muon_pt": 23.0,
            "max_muon_eta": 2.4,
            "muon_iso_cut": 0.15,
            "second_muon_index_in_pair": 1,
        },
    )
    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            # electron scale factors
            "ele_sf_file": EraModifier(
                {
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-15/electron.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-15/electron.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-15/electron.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-15/electron.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-15/electron.json.gz", 
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-15/electron.json.gz", 
                }
            ),
            "ele_id_sf_name": "Electron-ID-SF",
            "ele_sf_year_id": EraModifier(
                {
                    "2022preEE": "2022Re-recoBCD",
                    "2022postEE": "2022Re-recoE+PromptFG",
                    "2023preBPix": "2023PromptC",
                    "2023postBPix": "2023PromptD",
                    "2024": "2024Prompt",
                    "2025": "2024Prompt",
                }
            ),
            "ele_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
        },
    )
    configuration.add_config_parameters(
        ["em", "ee"],
        {
            # electron selection
            "electron_index_in_pair": 0,
            "min_ele_pt": 25.0,
            "max_ele_eta": 2.1,
            "ele_iso_cut": 0.3,
            "muon_index_in_pair": 1,
            "min_muon_pt": 23.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 0.15,
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            # tau selection 
            "min_tau_pt": 30.0,
            "max_tau_eta": 2.3,
            "max_tau_dz": 0.2,
            # tau wp selection, set to the first loosest wp
            "vsjet_tau_wp_cut": 1, #change back if loose is available 
            "vsele_tau_wp_cut": 2, 
            "vsmu_tau_wp_cut": 1,
            # tau sf variation
            "tau_sf_vsjet_tauDM0": "nom",
            "tau_sf_vsjet_tauDM1": "nom",
            "tau_sf_vsjet_tauDM10": "nom",
            "tau_sf_vsjet_tauDM11": "nom",
            "tau_vsjet_sf_dependence": "dm",  # or "dm", "eta"
            "tau_vsjet_vseleWP": "VVLoose",
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            # tau vs jet wp
            "tau_vsjet_vseleWP": "VVLoose",
            # muon trigger SF from embedding measurements
            "singlemuon_trigger_sf_mc": [
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
        },
    )
    configuration.add_config_parameters(
        ["et"],
        {
            # tau vs jet wp
            "tau_vsjet_vseleWP": "Tight",

            # electron selection
            "electron_index_in_pair": 0,
            "min_ele_pt": 25.0,
            "max_ele_eta": 2.5,
            "ele_iso_cut": 0.15,

            # electron trigger SF from embedding measurements
            "singlelectron_trigger_sf_mc": [
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
            ]
        },
    )

    if era == "2022postEE":
        configuration.add_config_parameters(
            "global",
            {
                "jet_jes_tag_data": SampleModifier(
                    {
                        "data_E": '"Summer22EE_22Sep2023_RunE_V3_DATA"',
                        "data_F": '"Summer22EE_22Sep2023_RunF_V3_DATA"',
                        "data_G": '"Summer22EE_22Sep2023_RunG_V3_DATA"',
                    },
                    default = '""',
                ),
            }
        )
        
    ############################
    ######## Producers #########
    ############################
    configuration.add_producers(
        "global",
        [
            # event.RunLumiEventFilter,
            event.SampleFlags,
            event.Lumi,
            event.npartons,
            event.MetFilter, 
            event.PUweights,
            event.LHE_Scale_weight,
            event.LHE_PDF_weight,
            event.LHE_alphaS_weight,
            event.PS_weight,
            muons.BaseMuons,
            electrons.ElectronPtCorrectionMC_Run3,
            electrons.BaseElectrons,
            jets.JetBTagUParT,
            jets.JetID, 
            jets.JetVetoMapVeto,
            jets.JetIDCut,
            jets.JetEnergyCorrection,
            jets.JetPtCut_loose,
            jets.LooseJets_LowEta,
            jets.LooseJets_HighEta,
            jets.GoodJets_loose,
            jets.GoodJets_tight,
            jets.GoodJets,
            jets.GoodBJets,
            event.DiLeptonVeto,
            genparticles.CalculateGenBosonVector,
            genparticles.CalculateVisGenBosonVector,
            met.MetBasics,
            met.MetMask,
        ],
    )
    configuration.add_producers(
        scopes,
        [
            jets.JetCollection,
            jets.BasicJetQuantities, 
            jets.BJetCollection,
            jets.BasicBJetQuantities,
            met.MetCorrections, 
            met.PFMetCorrections,
            pairquantities.DiTauPairMETQuantities,
            genparticles.GenMatching,
            scalefactors.btaggingWP_SF,
        ],
    )
    configuration.add_producers(
        "mt",
        [
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            configuration.ES_ID_SCHEME.mc.producerGroupES,
            taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            electrons.ExtraElectronsVeto, 
            pairselection.MTPairSelection,
            pairselection.GoodMTPairFilter,
            pairselection.LVMu1,
            pairselection.LVTau2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.MTDiTauPairQuantities,
            genparticles.MTGenDiTauPairQuantities,
            configuration.ES_ID_SCHEME.mc.producerID,
            # scalefactors.MuonIDIso_SF,
            # pairquantities.FastMTTQuantities,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            triggers.MTGenerateSingleMuonTriggerFlags,
            #triggers.MTGenerateCrossTriggerFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
            scalefactors.SingleMuTriggerSF,
            #scalefactors.MuTauTriggerSF,
            pairquantities.VsJetTauIDFlagOnly_2,
            #pairquantities.VsEleTauIDFlagOnly_2,
            #pairquantities.VsMuTauIDFlagOnly_2,
        ],
    )
    configuration.add_producers(
        "mm",
        [
            muons.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            pairselection.ZMuMuPairSelection,
            pairselection.GoodMuMuPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.MuMuPairQuantities,
            genparticles.MuMuGenPairQuantities,
            # scalefactors.MuonIDIso_SF,
            triggers.MuMuGenerateSingleMuonTriggerFlags,
        ],
    )
    configuration.add_producers(
        "et",
        [
            electrons.GoodElectrons,
            configuration.ES_ID_SCHEME.mc.producerGroupES,
            taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            electrons.NumberOfGoodElectrons,
            electrons.VetoElectrons,
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            pairselection.ETPairSelection,
            pairselection.GoodETPairFilter,
            pairselection.LVEl1,
            pairselection.LVTau2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.ETDiTauPairQuantities,
            genparticles.ETGenDiTauPairQuantities,
            configuration.ES_ID_SCHEME.mc.producerID,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            # scalefactors.EleID_SF,
            triggers.ETGenerateSingleElectronTriggerFlags,
            #triggers.ETGenerateCrossTriggerFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
            pairquantities.VsJetTauIDFlagOnly_2,
            # pairquantities.VsEleTauIDFlagOnly_2,
            # pairquantities.VsMuTauIDFlagOnly_2,
            scalefactors.SingleEleTriggerSF,
            #scalefactors.EleTauTriggerSF,
        ],
    )
    configuration.add_producers(
        "ee",
        [
            electrons.GoodElectrons,
            electrons.VetoElectrons,
            electrons.VetoSecondElectron,
            electrons.ExtraElectronsVeto,
            electrons.NumberOfGoodElectrons,
            pairselection.ElElPairSelection,
            pairselection.GoodElElPairFilter,
            pairselection.LVEl1,
            pairselection.LVEl2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVEl2Uncorrected,
            pairquantities.ElElPairQuantities,
            genparticles.ElElGenPairQuantities,
            triggers.ElElGenerateSingleElectronTriggerFlags,
            triggers.ElElGenerateDoubleMuonTriggerFlags,
        ],
    )
    configuration.add_producers(
        "em",
        [
            electrons.GoodElectrons,
            electrons.NumberOfGoodElectrons,
            electrons.VetoElectrons,
            electrons.ExtraElectronsVeto,
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            pairselection.EMPairSelection,
            pairselection.GoodEMPairFilter,
            pairselection.LVEl1,
            pairselection.LVMu2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.EMDiTauPairQuantities,
            genparticles.EMGenDiTauPairQuantities,
            # scalefactors.MuonIDIso_SF,
            # scalefactors.EleID_SF,
            triggers.EMGenerateSingleElectronTriggerFlags,
            triggers.EMGenerateSingleMuonTriggerFlags,
            triggers.EMGenerateCrossTriggerFlags,
        ],
    )
    configuration.add_producers(
        "tt",
        [   
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            configuration.ES_ID_SCHEME.mc.producerGroupES,
            taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            pairselection.TTPairSelection,
            pairselection.GoodTTPairFilter,
            pairselection.LVTau1,
            pairselection.LVTau2,
            pairselection.LVTau1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.TTDiTauPairQuantities,
            genparticles.TTGenDiTauPairQuantities,
            scalefactors.Tau_1_VsJetTauID_SF,
            scalefactors.Tau_1_VsEleTauID_SF,
            scalefactors.Tau_1_VsMuTauID_SF,
            scalefactors.Tau_2_VsJetTauID_tt_SF,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            triggers.TTGenerateDoubleTauFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
            #triggers.GenerateSingleLeadingTauTriggerFlags,
            pairquantities.VsJetTauIDFlagOnly_1,
            # pairquantities.VsEleTauIDFlagOnly_1,
            # pairquantities.VsMuTauIDFlagOnly_1,
            pairquantities.VsJetTauIDFlagOnly_2,
            # pairquantities.VsEleTauIDFlagOnly_2,
            # pairquantities.VsMuTauIDFlagOnly_2,
            scalefactors.DoubleTauTriggerSF,
        ],
    )
    
    ################################
    ######### Modifications ########
    ################################
    # nanoAOD version dependent producers: discriminating based on the era since for now they are separate like this 
    if era not in ["2024","2025"]:
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.JetBTagUParT, jets.JetBTagPNet],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.JetID, jets.JetIDRun3NanoV12Corrected,],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[met.MetBasics, met.MetBasicsv12,],
                exclude_samples=["fake_era"],
            ),
        )
        #configuration.add_modification_rule(
        #    "global",
        #    ReplaceProducer(
        #        producers=[event.PUweights, event.PUweights_v12,],
        #        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"], #the producer will be removed completely anyway
        #    ),
        #)
        configuration.add_modification_rule(
            scopes,
            ReplaceProducer(
                producers=[scalefactors.btaggingWP_SF,scalefactors.btagging_SF],
                exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"], # will be removed anyway
            ),
        )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[electrons.ElectronPtCorrectionMC_Run3, electrons.ElectronPtCorrectionData,],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.JetEnergyCorrection, jets.JetEnergyCorrection_data],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc",],
        ),
    )
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.npartons],
            exclude_samples=["dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "wjets", "wjets_amcatnlo", "electroweak_boson"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[
                event.PUweights,
                event.PS_weight,
                ],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[
                event.LHE_Scale_weight,
                event.LHE_PDF_weight,
                event.LHE_alphaS_weight,
                ],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc", "diboson"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=jets.RenameJetsData,
            samples=["embedding", "embedding_mc"],
            update_output=False,
        ),
    )
    configuration.add_modification_rule(
        "global",
        AppendProducer(producers=event.JSONFilter, samples=["data", "data_E", "data_F", "data_G", "embedding"]),
    )
    ## producer to add a cut on DYto2L affected by pythia bug where DYto2Tau has been reprocessed
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=[genparticles.GenDYFlavor,genparticles.GenDYFilter],
            samples=["dyjets_amcatnlo_ll"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[genparticles.GenMatching,],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[scalefactors.btaggingWP_SF,],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=event.ZPtReweighting,
            samples=["dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "electroweak_boson"]
        ),
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=[event.GGH_NNLO_Reweighting, event.GGH_WG1_Uncertainties],
            samples=["ggh_htautau", "rem_htautau"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=event.QQH_WG1_Uncertainties,
            samples=["vbf_htautau", "rem_htautau"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=[event.TopPtReweighting], 
            samples="ttbar"
        ),
    )
    configuration.add_modification_rule(
        ["et", "mt", "tt"],
        ReplaceProducer(
            producers=[configuration.ES_ID_SCHEME.mc.producerGroupES, taus.TauEnergyCorrection_data],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["et", "mt"],
        RemoveProducer(
            producers=[
                scalefactors.Tau_2_VsMuTauID_SF,
                configuration.ES_ID_SCHEME.mc.producerID,
                scalefactors.Tau_2_VsEleTauID_SF,
            ],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[genparticles.MTGenDiTauPairQuantities],
            samples=["data","data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        AppendProducer(
            producers=[
                #scalefactors.TauEmbeddingMuonIDSF_1_MC,
                #scalefactors.TauEmbeddingMuonIsoSF_1_MC,
                scalefactors.MuonIDIso_SF,
                #scalefactors.MTGenerateSingleMuonTriggerSF_MC,
            ],
            exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mm"],
        RemoveProducer(
            producers=[genparticles.MuMuGenPairQuantities],
            samples=["data","data_E", "data_F", "data_G",],
        ),
    )
    #configuration.add_modification_rule(
    #   ["mm"],
    #    AppendProducer(
    #        producers=[
    #            scalefactors.TauEmbeddingMuonIDSF_1_MC,
    #            scalefactors.TauEmbeddingMuonIsoSF_1_MC,
    #            scalefactors.TauEmbeddingMuonIDSF_2_MC,
    #            scalefactors.TauEmbeddingMuonIsoSF_2_MC,
    #            scalefactors.MTGenerateSingleMuonTriggerSF_MC,
    #        ],
    #        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    #    ),
    #)
    configuration.add_modification_rule(
        ["et"],
        RemoveProducer(
            producers=[genparticles.ETGenDiTauPairQuantities],
            samples=["data","data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        AppendProducer(
            producers=[
    #            scalefactors.TauEmbeddingElectronIDSF_1_MC,
    #            scalefactors.TauEmbeddingElectronIsoSF_1_MC,
                #scalefactors.ETGenerateSingleElectronTriggerSF_MC,
                 scalefactors.EleID_SF,
            ],
            exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["em"],
        RemoveProducer(
            producers=[genparticles.EMGenDiTauPairQuantities],
            samples=["data","data_E", "data_F", "data_G",],
        ),
    )
    #configuration.add_modification_rule(
    #    ["em"],
    #    AppendProducer(
    #        producers=[
    #            scalefactors.TauEmbeddingElectronIDSF_1_MC,
    #            scalefactors.TauEmbeddingElectronIsoSF_1_MC,
    #            scalefactors.TauEmbeddingMuonIDSF_2_MC,
    #            scalefactors.TauEmbeddingMuonIsoSF_2_MC,
    #        ],
    #        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    #    ),
    #)
    configuration.add_modification_rule(
        ["ee"],
        RemoveProducer(
            producers=[genparticles.ElElGenPairQuantities],
            samples=["data","data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["ee"],
        AppendProducer(
            producers=[
    #            scalefactors.TauEmbeddingElectronIDSF_1_MC,
    #            scalefactors.TauEmbeddingElectronIsoSF_1_MC,
    #            scalefactors.TauEmbeddingElectronIDSF_2_MC,
    #            scalefactors.TauEmbeddingElectronIsoSF_2_MC,
                #scalefactors.ETGenerateSingleElectronTriggerSF_MC,
                scalefactors.EleID_SF,
            ],
            exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["tt"],
        RemoveProducer(
            producers=[
                scalefactors.Tau_1_VsJetTauID_SF,
                scalefactors.Tau_1_VsEleTauID_SF,
                scalefactors.Tau_1_VsMuTauID_SF,
                scalefactors.Tau_2_VsJetTauID_tt_SF,
                scalefactors.Tau_2_VsEleTauID_SF,
                scalefactors.Tau_2_VsMuTauID_SF,
                genparticles.TTGenDiTauPairQuantities
            ],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    ) 

    #########################
    ######## OUTPUTS ########
    #########################
    configuration.add_outputs(
        scopes,
        [
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_ggh_htautau,
            q.is_vbf_htautau,
            q.is_diboson,
            nanoAOD.run,
            q.lumi,
            q.npartons,
            nanoAOD.event,
            q.puweight,
            q.lhe_scale_weight,
            q.ps_weight,
            q.lhe_pdf_weight,
            q.lhe_alphaS_weight,
            q.met_mask,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.njets,
            q.Jet_ID,
            q.Jet_vetomap,
            q.jpt_1,
            q.jpt_2,
            q.jeta_1,
            q.jeta_2,
            q.jphi_1,
            q.jphi_2,
            q.jtag_value_1,
            q.jtag_value_2,
            q.mjj,
            q.m_vis,
            # q.m_fastmtt,
            # q.pt_fastmtt,
            # q.eta_fastmtt,
            # q.phi_fastmtt,
            q.deltaR_ditaupair,
            q.pt_vis,
            q.nbtag,
            q.bpt_1,
            q.bpt_2,
            q.beta_1,
            q.beta_2,
            q.bphi_1,
            q.bphi_2,
            q.btag_value_1,
            q.btag_value_2,
            q.btag_weight,
            q.mass_1,
            q.mass_2,
            q.dxy_1,
            q.dxy_2,
            q.dz_1,
            q.dz_2,
            q.q_1,
            q.q_2,
            q.iso_1,
            q.iso_2,
            q.gen_pt_1,
            q.gen_eta_1,
            q.gen_phi_1,
            q.gen_mass_1,
            q.gen_pdgid_1,
            q.gen_pt_2,
            q.gen_eta_2,
            q.gen_phi_2,
            q.gen_mass_2,
            q.gen_pdgid_2,
            q.gen_m_vis,
            q.met,
            q.metphi,
            q.pfmet,
            q.pfmetphi,
            q.met_uncorrected,
            q.metphi_uncorrected,
            q.pfmet_uncorrected,
            q.pfmetphi_uncorrected,
            q.metSumEt,
            q.metcov00,
            q.metcov01,
            q.metcov10,
            q.metcov11,
            q.pzetamissvis,
            q.mTdileptonMET,
            q.mt_1,
            q.mt_2,
            q.pt_tt,
            q.pt_ttjj,
            q.mt_tot,
            #q.genbosonmass,
            q.gen_match_1,
            q.gen_match_2,
            q.pzetamissvis_pf,
            q.mTdileptonMET_pf,
            q.mt_1_pf,
            q.mt_2_pf,
            q.pt_tt_pf,
            q.pt_ttjj_pf,
            q.mt_tot_pf,
            q.pt_dijet,
            q.jet_hemisphere,
            q.dimuon_veto,
            q.dilepton_veto,
            q.dielectron_veto,
        ],
    )
    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            configuration.ES_ID_SCHEME.mc.producerID.output_group,
            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            #triggers.MTGenerateCrossTriggerFlags.output_group,
            #triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            #q.id_wgt_mu_1, #Quantity id_wgt_mu_1 is already defined in mt scope !
            #q.iso_wgt_mu_1,
            scalefactors.SingleMuTriggerSF.output_group,] 
        #] + [p for p in scalefactors.MuTauTriggerSF.get_outputs("mt")],
    )
    configuration.add_outputs(
        "mm",
        [
            q.nmuons,
            triggers.MuMuGenerateSingleMuonTriggerFlags.output_group,
        ],
    )
    configuration.add_outputs(
        "et",
        [
            q.nelectrons,
            q.ntaus,
            configuration.ES_ID_SCHEME.mc.producerID.output_group,
            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            triggers.ETGenerateSingleElectronTriggerFlags.output_group,
            #triggers.ETGenerateCrossTriggerFlags.output_group,
            #triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            # q.id_wgt_ele_wp90iso_1,
            # q.id_wgt_ele_wp80iso_1,
            scalefactors.SingleEleTriggerSF.output_group,]
        #] + [p for p in scalefactors.EleTauTriggerSF.get_outputs("et")],
    )
    configuration.add_outputs(
        "em",
        [
            q.nelectrons,
            q.nmuons,
            triggers.EMGenerateSingleElectronTriggerFlags.output_group,
            triggers.EMGenerateSingleMuonTriggerFlags.output_group,
            triggers.EMGenerateCrossTriggerFlags.output_group,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
        ],
    )
    configuration.add_outputs(
        "ee",
        [
            q.nelectrons,
            triggers.ElElGenerateSingleElectronTriggerFlags.output_group,
            triggers.ElElGenerateDoubleMuonTriggerFlags.output_group,
            q.dimuon_veto,
            q.dielectron_veto,
            q.extraelec_veto,
        ],
    )
    configuration.add_outputs(
        "tt",
        [
            q.ntaus,
            scalefactors.Tau_1_VsJetTauID_SF.output_group,
            scalefactors.Tau_1_VsEleTauID_SF.output_group,
            scalefactors.Tau_1_VsMuTauID_SF.output_group,
            scalefactors.Tau_2_VsJetTauID_tt_SF.output_group,
            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_1.output_group,
            pairquantities.VsEleTauIDFlag_1.output_group,
            pairquantities.VsMuTauIDFlag_1.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_1.output_group,
            # pairquantities.VsEleTauIDFlagOnly_1.output_group,
            # pairquantities.VsMuTauIDFlagOnly_1.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            triggers.TTGenerateDoubleTauFlags.output_group,
            #triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            #triggers.GenerateSingleLeadingTauTriggerFlags.output_group,
            q.taujet_pt_1,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
        ] + [p for p in scalefactors.DoubleTauTriggerSF.get_outputs("tt")],
    )
    
    if "data" not in sample:
        configuration.add_outputs(
            scopes,
            nanoAOD.genWeight,
        )
    if "data" not in sample and "embedding" not in sample:
        configuration.add_outputs(
            scopes,
            [
                nanoAOD.HTXS_Higgs_pt,
                nanoAOD.HTXS_Higgs_y,
                nanoAOD.HTXS_njets25,
                nanoAOD.HTXS_njets30,
                nanoAOD.HTXS_stage1_1_cat_pTjet25GeV,
                nanoAOD.HTXS_stage1_1_cat_pTjet30GeV,
                nanoAOD.HTXS_stage1_1_fine_cat_pTjet25GeV,
                nanoAOD.HTXS_stage1_1_fine_cat_pTjet30GeV,
                nanoAOD.HTXS_stage1_2_cat_pTjet25GeV,
                nanoAOD.HTXS_stage1_2_cat_pTjet30GeV,
                nanoAOD.HTXS_stage1_2_fine_cat_pTjet25GeV,
                nanoAOD.HTXS_stage1_2_fine_cat_pTjet30GeV,
                nanoAOD.HTXS_stage_0,
                nanoAOD.HTXS_stage_1_pTjet25,
                nanoAOD.HTXS_stage_1_pTjet30,
            ],
        )
    
    #########################
    # LHE Scale Weight variations
    #########################
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)
    if "ggh" in sample or "qqh" in sample:
        with defaults(scopes="global"):
            with defaults(shift_map={"Up": 2.0, "Down": 0.5}):
                add_shift(name="muRWeight", shift_key="muR", producers=[event.LHE_Scale_weight])
                add_shift(name="muFWeight", shift_key="muF", producers=[event.LHE_Scale_weight])
                add_shift(name="FsrWeight", shift_key="fsr", producers=[event.PS_weight])
                add_shift(name="IsrWeight", shift_key="isr", producers=[event.PS_weight])
            with defaults(shift_map={"Up": "up", "Down": "down"}):
                add_shift(name="PdfWeight", shift_key="pdf_variation", producers=[event.LHE_PDF_weight])
                add_shift(name="AlphaSWeight", shift_key="pdf_alphaS_variation", producers=[event.LHE_alphaS_weight])

    #########################
    # Lepton to tau fakes energy scalefactor shifts  #
    #########################
    if "dyjets" in sample or "electroweak_boson" in sample:
        with defaults(shift_map={"Down": "down", "Up": "up"}):
            add_shift(
                name="tauMuFakeEs",
                shift_key="tau_mufake_es",
                scopes="mt",
                producers=[taus.TauPtCorrection_MC],
            )
            with defaults(
                scopes="et",
                producers=[taus.TauPtCorrection_MC],
            ):
                add_shift(name="tauEleFakeEs1prongBarrel", shift_key="tau_elefake_es_DM0_barrel")
                add_shift(name="tauEleFakeEs1prongEndcap", shift_key="tau_elefake_es_DM0_endcap")
                add_shift(name="tauEleFakeEs1prong1pizeroBarrel", shift_key="tau_elefake_es_DM1_barrel")
                add_shift(name="tauEleFakeEs1prong1pizeroEndcap", shift_key="tau_elefake_es_DM1_endcap")

    #########################
    # Electron energy correction shifts
    #########################
    with defaults(
        scopes="global",
        shift_key="ele_es_variation",
        producers=[electrons.ElectronPtCorrectionMC_Run3],
        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    ):
        add_shift(name="eleEsReso", shift_map={"Up": "resolutionUp", "Down": "resolutionDown"})
        add_shift(name="eleEsScale", shift_map={"Up": "scaleUp", "Down": "scaleDown"})

    configuration.add_shift(
        SystematicShift(
            name="electronIdSFUp",
            scopes=["et"],
            shift_config={
                ("et"): {"ele_sf_variation": "sfup"},
            },
            producers={
                ("et"): [
                    scalefactors.EleID_SF,
                ],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="electronIdSFDown",
            scopes=["et"],
            shift_config={
                ("et"): {"ele_sf_variation": "sfdown"},
            },
            producers={
                ("et"): [
                    scalefactors.EleID_SF,
                ],
            },
        )
    )

    #########################
    # MET Shifts
    #########################
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnUp",
            quantity_change={
                nanoAOD.PuppiMET_pt: "PuppiMET_ptUnclusteredUp",
                nanoAOD.PuppiMET_phi: "PuppiMET_phiUnclusteredUp",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnDown",
            quantity_change={
                nanoAOD.PuppiMET_pt: "PuppiMET_ptUnclusteredDown",
                nanoAOD.PuppiMET_phi: "PuppiMET_phiUnclusteredDown",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    )

    #########################
    # MET Recoil Shifts
    #########################
    # with defaults(
    #     scopes=("et", "mt", "tt", "em", "ee", "mm"),
    #     producers=[met.ApplyRecoilCorrections],
    #     exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    #     shift_key=["recoil_method", "recoil_variation",]
    # ):
    #     add_shift(
    #         name="metRecoilResponse",
    #         shift_map={"Up": ["Uncertainty", "RespUp"], "Down": ["Uncertainty", "RespDown"]}
    #     )
    #     add_shift(
    #         name="metRecoilResolution",
    #         shift_map={"Up": ["Uncertainty", "ResolUp"], "Down": ["Uncertainty", "ResolDown"]}
    #     )

    #########################
    # Pileup Shifts
    #########################
    add_shift(
        name="PileUp",
        shift_key="PU_reweighting_variation",
        shift_map={"Up": "up", "Down": "down"},
        scopes="global",
        producers=[event.PUweights],
        exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
    )

    #########################
    # Z pt DY uncertainties
    #########################
    if "dyjets" in sample or "electroweak_boson" in sample:
        add_shift(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[event.ZPtReweighting],
            shift_key="zpt_variation",
            name="zPtReweightWeight",
            shift_map={
                        # "Up1": "up1",
                        # "Up2": "up2",
                        # "Up3": "up3",
                        # "Up4": "up4",
                        # "Up5": "up5",
                        # "Up6": "up6",
                        # "Up7": "up7",
                        # "Up8": "up8",
                        # "Up9": "up9",
                        # "Down1": "down1",
                        # "Down2": "down2",
                        # "Down3": "down3",
                        # "Down4": "down4",
                        # "Down5": "down5",
                        # "Down6": "down6",
                        # "Down7": "down7",
                        # "Down8": "down8",
                        # "Down9": "down9",
                        "Up":"up", "Down":"down",
                        },
        )

    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    configuration = add_tauVariations(configuration, sample, era)

    #########################
    # Import triggersetup and sf 
    #########################
    configuration = add_diTauTriggerSetup(configuration)

    #########################
    # Jet energy resolution and jet energy scale and btag uncertainties
    #########################
    configuration = add_jetVariations(configuration, era)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
