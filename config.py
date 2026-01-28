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
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
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
            "met_filters": EraModifier(
                {
                    "2016preVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2016postVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2018": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2022preEE": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2022postEE": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "20223preBPix": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2023postBPix": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2024": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2025": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                }
            ),
            
            # pileup corrections
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
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
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
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
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
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
                    "2016preVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2016postVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
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
            "ele_id": "Electron_mvaFall17V2noIso_WP90",
            "ele_es_name": "UL-EGM_ScaleUnc",
            "ele_es_master_seed": 44,
            "ele_es_mc_name": '"SmearAndSyst"',
            "ele_es_data_name": '"Scale"',
            "ele_es_file": EraModifier(
                {
                    "2016preVFP": "data/electron_energy_scale/2016preVFP_UL/EGM_ScaleUnc.json.gz",
                    "2016postVFP": "data/electron_energy_scale/2016postVFP_UL/EGM_ScaleUnc.json.gz",
                    "2017": "data/electron_energy_scale/2017_UL/EGM_ScaleUnc.json.gz",
                    "2018": "data/electron_energy_scale/2018_UL/EGM_ScaleUnc.json.gz",
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
                    "2016preVFP": 0.2598,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                    "2016postVFP": 0.2489,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                    "2017": 0.3040,
                    "2018": 0.2783,
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
            # jet puID
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2022preEE": 0, #not used
                    "2022postEE": 0, #not used
                    "2023preBPix": 0, #not used
                    "2023postBPix": 0, #not used
                    "2024": 0, #not used
                    "2025": 0, #not used
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            # jet energy calibration 
            "jet_id_json": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""',
                    "2017": '""',
                    "2018": '""',
                    "2022preEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jetid.json.gz"',
                    "2022postEE": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jetid.json.gz"',
                    "2023preBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07jetid.json.gz"',
                    "2023postBPix": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jetid.json.gz"',
                    "2024": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetid.json.gz"',
                    "2025": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetid.json.gz"',
                }
            ),
            "jet_collection_name":'"AK4PUPPI"', #only used for jet ID so not relevant for run 2
            "jer_master_seed": 42,
            "jet_reapplyJES": True,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jes_tag_mc": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
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
                    "2016preVFP": '""',
                    "2016postVFP": '""',
                    "2017": '""',
                    "2018": '""',
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
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
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
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    "2022preEE": '"Summer22_22Sep2023_JRV1_MC"',
                    "2022postEE": '"Summer22EE_22Sep2023_JRV1_MC"',
                    "2023preBPix": '"Summer23Prompt23_RunCv1234_JRV1_MC"',
                    "2023postBPix": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                    "2024": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                    "2025": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                }
            ),
            "jet_jec_algo": EraModifier(
                {
                    "2016preVFP": '"AK4PFchs"',
                    "2016postVFP": '"AK4PFchs"',
                    "2017": '"AK4PFchs"',
                    "2018": '"AK4PFchs"',
                    "2022preEE": '"AK4PFPuppi"',
                    "2022postEE": '"AK4PFPuppi"',
                    "2023preBPix": '"AK4PFPuppi"',
                    "2023postBPix": '"AK4PFPuppi"',
                    "2024": '"AK4PFPuppi"',
                    "2025": '"AK4PFPuppi"',
                }
            ),
            # jet veto configuration
            "jet_veto_map_file": EraModifier(
                {
                    "2016preVFP": '""',
                    "2016postVFP": '""',
                    "2017": '""',
                    "2018": '""',
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
                    "2016preVFP": '""',
                    "2016postVFP": '""',
                    "2017": '""',
                    "2018": '""',
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
                    "2016preVFP": "data/jsonpog-integration/POG/BTV/2016preVFP_UL/btagging.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/BTV/2016postVFP_UL/btagging.json.gz",
                    "2017": "data/jsonpog-integration/POG/BTV/2017_UL/btagging.json.gz",
                    "2018": "data/jsonpog-integration/POG/BTV/2018_UL/btagging.json.gz",
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
                    "2016preVFP": "deepJet_shape",
                    "2016postVFP": "deepJet_shape",
                    "2017": "deepJet_shape",
                    "2018": "deepJet_shape",
                    "2022preEE": "particleNet_shape", 
                    "2022postEE": "particleNet_shape",
                    "2023preBPix": "particleNet_shape",
                    "2023postBPix": "particleNet_shape",
                    "2024": "UParTAK4_kinfit",
                    "2025": "UParTAK4_kinfit",
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
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                    "2022preEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                    "2025": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '""',
                    "2025": '""',
                }
            ),
            "recoil_method": "QuantileMapHist", #other option is pure "Resclaing"
            "recoil_variation": '""',
            "applyRecoilCorrections": SampleModifier( #apply only to single boson processes
                {
                    "dyjets": True,
                    "dyjets_powheg": True,
                    "dyjets_amcatnlo": True,
                    "dyjets_amcatnlo_ll": True,
                    "dyjets_amcatnlo_tt": True,
                    "wjets": True,
                    "wjets_amcatnlo": True,
                    "electroweak_boson": True,
                    "ggh_htautau": True,
                    "vbf_htautau": True,
                    "rem_htautau": True,
                    "ggh_hww": True,
                    "vbf_hww": True,
                    "rem_VH": True,
                },
                default=False,
            ),
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,

            # zpt reweighting for DY samples
            "zpt_file": EraModifier(
                {
                    "2016preVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  # ToDO: Measured in legacy, therefore the same for pre- and postVFP for now
                    "2016postVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  # ToDO: Measured in legacy, therefore the same for pre- and postVFP for now
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                    "2022preEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                    "2025": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
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
                    "2016preVFP": "data/jsonpog-integration/POG/TAU/2016preVFP_UL/tau.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/TAU/2016postVFP_UL/tau.json.gz",
                    "2017": "data/jsonpog-integration/POG/TAU/2017_UL/tau.json.gz",
                    "2018": "data/jsonpog-integration/POG/TAU/2018_UL/tau.json.gz",
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
            "tau_ES_shift_1prong0pizero": "nom",
            "tau_ES_shift_1prong0pizero20to40": "nom",
            "tau_ES_shift_1prong0pizero40toInf": "nom",
            "tau_ES_shift_1prong1pizero": "nom",
            "tau_ES_shift_1prong1pizero20to40": "nom",
            "tau_ES_shift_1prong1pizero40toInf": "nom",
            "tau_ES_shift_3prong0pizero": "nom",
            "tau_ES_shift_3prong0pizero20to40": "nom",
            "tau_ES_shift_3prong0pizero40toInf": "nom",
            "tau_ES_shift_3prong1pizero": "nom",
            "tau_ES_shift_3prong1pizero20to40": "nom",
            "tau_ES_shift_3prong1pizero40toInf": "nom",
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
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_Z.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
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

            #emebdding scale factors
            "mc_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/muon_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/muon_2016postVFPUL.json.gz",
                    "2017": "data/embedding/muon_2017UL.json.gz",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '""',
                    "2025": '""',
                }
            ),
            "mc_muon_id_sf": "ID_pt_eta_bins",
            "mc_muon_iso_sf": "Iso_pt_eta_bins",
            "mc_muon_id_extrapolation": 1.0,  # for nominal case
            "mc_muon_iso_extrapolation": 1.0,  # for nominal case
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
            "tau_sf_vsjet_1prong0pizero20to40": "nom",
            "tau_sf_vsjet_1prong0pizero40toInf": "nom",
            "tau_sf_vsjet_1prong1pizero20to40": "nom",
            "tau_sf_vsjet_1prong1pizero40toInf": "nom",
            "tau_sf_vsjet_3prong0pizero20to40": "nom",
            "tau_sf_vsjet_3prong0pizero40toInf": "nom",
            "tau_sf_vsjet_3prong1pizero20to40": "nom",
            "tau_sf_vsjet_3prong1pizero40toInf": "nom",
            "tau_sf_vsjet_1prong0pizero": "nom",
            "tau_sf_vsjet_1prong1pizero": "nom",
            "tau_sf_vsjet_3prong0pizero": "nom",
            "tau_sf_vsjet_3prong1pizero": "nom",
            "tau_vsjet_sf_dependence": "dm",
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
                    "2016preVFP": "data/jsonpog-integration/POG/EGM/2016preVFP_UL/electron.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/EGM/2016postVFP_UL/electron.json.gz",
                    "2017": "data/jsonpog-integration/POG/EGM/2017_UL/electron.json.gz",
                    "2018": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
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
                    "2016preVFP": "2016preVFP",
                    "2016postVFP": "2016postVFP",
                    "2017": "2017",
                    "2018": "2018",
                    "2022preEE": "2022Re-recoBCD",
                    "2022postEE": "2022Re-recoE+PromptFG",
                    "2023preBPix": "2023PromptC",
                    "2023postBPix": "2023PromptD",
                    "2024": "2024Prompt",
                    "2025": "2024Prompt",
                }
            ),
            "ele_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations

            #embedding scale factors
            "mc_electron_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/electron_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/electron_2016postVFPUL.json.gz",
                    "2017": "data/embedding/electron_2017UL.json.gz",
                    "2018": "data/embedding/electron_2018UL.json.gz",
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '""',
                    "2025": '""',
                }
            ),
            "mc_electron_id_sf": "ID90_pt_eta_bins",
            "mc_electron_iso_sf": "Iso_pt_eta_bins",
            "mc_electron_id_extrapolation": 1.0,  # for nominal case
            "mc_electron_iso_extrapolation": 1.0,  # for nominal case
        },
    )
    configuration.add_config_parameters(
        ["em", "ee"],
        {
            # electron selection
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 0,
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
    
    if int(era[:4]) < 2022:
        configuration.add_config_parameters(
            "global",
            {
                "muon_iso_cut": 0.3,
                "max_ele_iso": 0.3,
                "jet_reapplyJES": False,
            }
        )
        configuration.add_config_parameters(
            scopes,
            {
                "propagateJets": SampleModifier(
                    {"data": False},
                    default=True,
                ),
            }
        )
        configuration.add_config_parameters(
            ["mt", "et", "tt"],
            {
                "tau_id_algorithm": "DeepTau2017v2p1",
                "vsjet_tau_id_wp_bit": [
                        {
                            "vsjet_tau_id_WPbit": bit,
                            "tau_1_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                            "tau_2_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                        }
                        for wp, bit in dict(
                            VVLoose=2,
                            VLoose=3,
                        ).items()
                    ],
                "vsjet_tau_id": [
                        {
                            "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(wp=wp),
                            "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(wp=wp),
                            "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                            "tau_1_vsjet_id_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                            "tau_2_vsjet_id_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                            "vsjet_tau_id_WPbit": bit,
                        }
                        for wp, bit in {
                            "Loose": 4,
                            "Medium": 5,
                            "Tight": 6,
                            "VTight": 7,
                        }.items()
                    ],
                "vsele_tau_id": [
                    {
                        "tau_1_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_1".format(wp=wp),
                        "tau_2_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_2".format(wp=wp),
                        "vsele_tau_id_WP": "{wp}".format(wp=wp),
                        "tau_1_vsele_id_outputname": "id_tau_vsEle_{wp}_1".format(wp=wp),
                        "tau_2_vsele_id_outputname": "id_tau_vsEle_{wp}_2".format(wp=wp),
                        "vsele_tau_id_WPbit": bit,
                    }
                    for wp, bit in {
                        "VVLoose": 2,
                        "VLoose": 3,
                        "Loose": 4,
                        "Medium": 5,
                        "Tight": 6,
                        "VTight": 7,
                        "VVTight": 8,
                    }.items()
                ],
                "max_tau_eta": 2.3,
            }
        )
        configuration.add_config_parameters(
            ["mt", "mm", "em"],
            {
                "muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            }
        )
        configuration.add_config_parameters(
            ["et", "ee", "em"],
            {
                "ele_id_sf_name": "UL-Electron-ID-SF",
            }
        )
        configuration.add_config_parameters(
            ["et", "mt"],
            {
                "vsjet_tau_id_bit": 1,
                "vsele_tau_id_bit": 1,
                "vsmu_tau_id_bit": 1,
            }
        )
        configuration.add_config_parameters(
            ["mt", "mm"],
            {
                "max_muon_eta": 2.1,
                "muon_iso_cut": 0.3,
            }
        )
        configuration.add_config_parameters(
            ["mm"],
            {
                "min_muon_pt": 20.0,
                "max_muon_eta": 2.1,
                "muon_iso_cut": 0.15,
            }
        )
        configuration.add_config_parameters(
            ["et"],
            {
                "max_electron_eta": 2.1,
                "electron_iso_cut": 0.5,
            }
        )
        configuration.add_config_parameters(
            ["tt"],
            {
                "tau_vsjet_sf_dependence": "pt",
                "min_tau_pt": 35.0,
                "vsjet_tau_id_bit": 4,
                "vsele_tau_id_bit": 4,
                "vsmu_tau_id_bit": 1,
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
            electrons.ElectronPtCorrectionMC,
            electrons.BaseElectrons,
            jets.JetBTagUParT,
            jets.JetID, 
            jets.JetVetoMapVeto,
            jets.JetIDCut,
            jets.JetEnergyCorrection,
            jets.JetPtCut_loose,
            jets.JetEtaCut_Max3,
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
            pairquantities.DiObjectAngleQuantities,
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
            scalefactors.MuonIDIso_SF,
            # pairquantities.FastMTTQuantities,
            scalefactors.TauID_SF,
            # scalefactors.Tau_2_VsEleTauID_SF,
            # scalefactors.Tau_2_VsMuTauID_SF,
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
            scalefactors.MuonIDIso_SF,
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
            scalefactors.TauID_SF,
            # scalefactors.Tau_2_VsEleTauID_SF,
            # scalefactors.Tau_2_VsMuTauID_SF,
            scalefactors.EleID_SF,
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
            scalefactors.EleID_SF,
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
            scalefactors.MuonIDIso_SF,
            scalefactors.EleID_SF,
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
            # scalefactors.Tau_1_VsJetTauID_SF,
            # scalefactors.Tau_1_VsEleTauID_SF,
            # scalefactors.Tau_1_VsMuTauID_SF,
            # scalefactors.Tau_2_VsJetTauID_tt_SF,
            # scalefactors.Tau_2_VsEleTauID_SF,
            # scalefactors.Tau_2_VsMuTauID_SF,
            scalefactors.TauID_SF,
            triggers.TTGenerateDoubleTauTriggerFlags,
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

    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[electrons.ElectronPtCorrectionMC, electrons.ElectronPtCorrectionData,],
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
            exclude_samples=["dyjets", "dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "wjets", "wjets_amcatnlo", "electroweak_boson"],
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
        AppendProducer(
            producers=event.JSONFilter, 
            samples=["data", "data_E", "data_F", "data_G", "embedding"]),
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
            producers=[scalefactors.btaggingWP_SF],
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
        ["et", "mt", "tt"],
        RemoveProducer(
            producers=[
                scalefactors.TauID_SF,
            ],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et", "mt"],
        RemoveProducer(
            producers=[
                configuration.ES_ID_SCHEME.mc.producerID,
            ],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[genparticles.MTGenDiTauPairQuantities],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["mt", "em", "mm"],
        RemoveProducer(
            producers=[
                scalefactors.MuonIDIso_SF,
            ],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et", "ee", "em"],
        RemoveProducer(
            producers=[
                scalefactors.EleID_SF,
            ],
            samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mm"],
        RemoveProducer(
            producers=[genparticles.MuMuGenPairQuantities],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        RemoveProducer(
            producers=[genparticles.ETGenDiTauPairQuantities],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["em"],
        RemoveProducer(
            producers=[genparticles.EMGenDiTauPairQuantities],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["ee"],
        RemoveProducer(
            producers=[genparticles.ElElGenPairQuantities],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    )
    configuration.add_modification_rule(
        ["tt"],
        RemoveProducer(
            producers=[
                genparticles.TTGenDiTauPairQuantities
            ],
            samples=["data", "data_E", "data_F", "data_G",],
        ),
    ) 

    if int(era[:4]) < 2022:
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[electrons.BaseElectrons, electrons.BaseElectrons_Run2],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[electrons.ElectronPtCorrectionMC, electrons.ElectronPtCorrectionMC_Run2,],
                exclude_samples=["data", "data_E", "data_F", "data_G",],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[electrons.ElectronPtCorrectionMC, electrons.RenameElectronPt],
                samples="data",
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.JetID, jets.JetID_rename],
                samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc",],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.JetBTagUParT, jets.JetBTagDeep,],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.GoodJets, jets.GoodJets_Run2,],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            "global",
            RemoveProducer(
                producers=[jets.JetVetoMapVeto,],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            scopes,
            ReplaceProducer(
                producers=[met.MetCorrections, met.MetCorrections_Run2],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            scopes,
            ReplaceProducer(
                producers=[met.PFMetCorrections, met.PFMetCorrections_Run2],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            ["mt", "et", "tt"],
            ReplaceProducer(
                producers=[taus.BaseTaus, taus.BaseTaus_Run2],
                exclude_samples=["fake_era",],
            ),
        )
        configuration.add_modification_rule(
            ["mt", "em", "mm"],
            RemoveProducer(
                producers=[
                    scalefactors.MuonIDIso_SF,
                ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["et", "ee", "em"],
            RemoveProducer(
                producers=[
                    scalefactors.EleID_SF,
                ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["mt"],
            AppendProducer(
                producers=[
                    triggers.MTGenerateCrossTriggerFlags,
                    triggers.GenerateSingleTrailingTauTriggerFlags
                    ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["mt"],
            AppendProducer(
                producers=[
                    scalefactors.MTGenerateSingleMuonTriggerSF_MC,
                    scalefactors.TauEmbeddingMuonIDSF_1_MC,
                    scalefactors.TauEmbeddingMuonIsoSF_1_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["mt"],
            RemoveProducer(
                producers=[
                    scalefactors.SingleMuTriggerSF,
                ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["et"],
            AppendProducer(
                producers=[
                    triggers.ETGenerateCrossTriggerFlags,
                    triggers.GenerateSingleTrailingTauTriggerFlags],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["et"],
            AppendProducer(
                producers=[
                    scalefactors.ETGenerateSingleElectronTriggerSF_MC,
                    scalefactors.TauEmbeddingElectronIDSF_1_MC,
                    scalefactors.TauEmbeddingElectronIsoSF_1_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["et"],
            RemoveProducer(
                producers=[
                    scalefactors.SingleEleTriggerSF,
                ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["tt"],
            AppendProducer(
                producers=[
                    triggers.GenerateSingleTrailingTauTriggerFlags,
                    triggers.GenerateSingleLeadingTauTriggerFlags],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["tt"],
            RemoveProducer(
                producers=[
                    scalefactors.DoubleTauTriggerSF,
                ],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["tt"],
            ReplaceProducer(
                producers=[pairquantities.TTDiTauPairQuantities, pairquantities.TTDiTauPairQuantities_Run2],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            ["em"],
            AppendProducer(
                producers=[
                    scalefactors.TauEmbeddingElectronIDSF_1_MC,
                    scalefactors.TauEmbeddingElectronIsoSF_1_MC,
                    scalefactors.TauEmbeddingMuonIDSF_2_MC,
                    scalefactors.TauEmbeddingMuonIsoSF_2_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["mm"],
            AppendProducer(
                producers=[
                    scalefactors.TauEmbeddingMuonIDSF_1_MC,
                    scalefactors.TauEmbeddingMuonIsoSF_1_MC,
                    scalefactors.TauEmbeddingMuonIDSF_2_MC,
                    scalefactors.TauEmbeddingMuonIsoSF_2_MC,
                    scalefactors.MTGenerateSingleMuonTriggerSF_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["ee"],
            AppendProducer(
                producers=[
                    scalefactors.TauEmbeddingElectronIDSF_1_MC,
                    scalefactors.TauEmbeddingElectronIsoSF_1_MC,
                    scalefactors.TauEmbeddingElectronIDSF_2_MC,
                    scalefactors.TauEmbeddingElectronIsoSF_2_MC,
                    scalefactors.ETGenerateSingleElectronTriggerSF_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        if era != "2018":
            configuration.add_modification_rule(
                "global",
                AppendProducer(
                    producers=event.PrefireWeight,
                    exclude_samples=["fake_era"],
                ),
            )
         # Broken sfs file for 2016. If nlo is used, this reweighting is not even needed. !!!
        if "2016" not in era:
            configuration.add_modification_rule(
                scopes,
                AppendProducer(
                    producers=event.ZPtMassReweighting, samples=["dyjets", "electroweak_boson"]
                ),
            )

    elif 2022 <= int(era[:4]) < 2024:
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
    
    if int(era[:4]) < 2024:
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[met.MetBasics, met.MetBasics_v12,],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
            scopes,
            ReplaceProducer(
                producers=[scalefactors.btaggingWP_SF,scalefactors.btagging_SF],
                exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"], 
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
            q.deltaPhi_ditaupair,
            q.deltaEta_ditaupair,
            q.deltaR_1j1,
            q.deltaR_1j2,
            q.deltaR_2j1,
            q.deltaR_2j2,
            q.deltaR_jj,
            q.deltaR_12j1,
            q.deltaR_12j2,
            q.deltaR_12jj,
            q.deltaPhi_1j1,
            q.deltaPhi_1j2,
            q.deltaPhi_2j1,
            q.deltaPhi_2j2,
            q.deltaPhi_jj,
            q.deltaPhi_12j1,
            q.deltaPhi_12j2,
            q.deltaPhi_12jj,
            q.deltaEta_1j1,
            q.deltaEta_1j2,
            q.deltaEta_2j1,
            q.deltaEta_2j2,
            q.deltaEta_jj,
            q.deltaEta_12j1,
            q.deltaEta_12j2,
            q.deltaEta_12jj,
        ],
    )
    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            scopes,
            nanoAOD.genWeight,
        )
        if era != "2018" and int(era[:4]) < 2022:
            configuration.add_outputs(
                scopes,
                q.prefiring_wgt,
            )

    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            configuration.ES_ID_SCHEME.mc.producerID.output_group,
            #scalefactors.TauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            #q.id_wgt_mu_1, #Quantity id_wgt_mu_1 is already defined in mt scope !
            #q.iso_wgt_mu_1,
            #scalefactors.SingleMuTriggerSF.output_group,
            ],
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
            #scalefactors.TauID_SF.output_group, #will need to switch it for the run2???
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            triggers.ETGenerateSingleElectronTriggerFlags.output_group,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            # q.id_wgt_ele_wp90iso_1,
            # q.id_wgt_ele_wp80iso_1,
            #scalefactors.SingleEleTriggerSF.output_group,
            ],
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
            # scalefactors.Tau_1_VsJetTauID_SF.output_group,
            # scalefactors.Tau_1_VsEleTauID_SF.output_group,
            # scalefactors.Tau_1_VsMuTauID_SF.output_group,
            # scalefactors.Tau_2_VsJetTauID_tt_SF.output_group,
            # scalefactors.Tau_2_VsEleTauID_SF.output_group,
            # scalefactors.Tau_2_VsMuTauID_SF.output_group,
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
            triggers.TTGenerateDoubleTauTriggerFlags.output_group,
            q.taujet_pt_1,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ],
    )

    if int(era[:4]) < 2022:
        configuration.add_outputs(
            "mt",
            [
                triggers.MTGenerateCrossTriggerFlags.output_group,
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            ],
        )
        configuration.add_outputs(
            "et",
            [
                triggers.ETGenerateCrossTriggerFlags.output_group,
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            ],
        )
        configuration.add_outputs(
            "tt",
            [
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
                triggers.GenerateSingleLeadingTauTriggerFlags.output_group,
            ],
        )
    else:
        configuration.add_outputs(
            "mt",
            [
                scalefactors.SingleMuTriggerSF.output_group,
                ] + [p for p in scalefactors.MuonIDIso_SF.get_outputs("mt")
                ] + [p for p in scalefactors.TauID_SF.get_outputs("mt")
                #] + [p for p in scalefactors.MuTauTriggerSF.get_outputs("mt")],
            ],
        )
        configuration.add_outputs(
            "et",
            [
                scalefactors.SingleEleTriggerSF.output_group,
                ] + [p for p in scalefactors.EleID_SF.get_outputs("et")
                ] + [p for p in scalefactors.TauID_SF.get_outputs("et")
                #] + [p for p in scalefactors.EleTauTriggerSF.get_outputs("et"),
            ],
        )
        configuration.add_outputs(
            "tt",
            [
                p for p in scalefactors.DoubleTauTriggerSF.get_outputs("tt")  
            ] + [p for p in scalefactors.TauID_SF.get_outputs("tt")
            ],
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
            if int(era[:4]) < 2022:
                add_shift(
                    name="tauMuFakeEs",
                    shift_key="tau_mufake_es",
                    scopes="mt",
                    producers=[taus.TauPtCorrection_muFake],
                )
                with defaults(
                    scopes="et",
                    producers=[taus.TauPtCorrection_eleFake],
                ):
                    add_shift(name="tauEleFakeEs1prongBarrel", shift_key="tau_elefake_es_DM0_barrel")
                    add_shift(name="tauEleFakeEs1prongEndcap", shift_key="tau_elefake_es_DM0_endcap")
                    add_shift(name="tauEleFakeEs1prong1pizeroBarrel", shift_key="tau_elefake_es_DM1_barrel")
                    add_shift(name="tauEleFakeEs1prong1pizeroEndcap", shift_key="tau_elefake_es_DM1_endcap")
            else:
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
    if int(era[:4]) < 2022:
        with defaults(
            scopes="global",
            shift_key="ele_es_variation",
            producers=[electrons.ElectronPtCorrectionMC_Run2],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ):
            add_shift(name="eleEsReso", shift_map={"Up": "resolutionUp", "Down": "resolutionDown"})
            add_shift(name="eleEsScale", shift_map={"Up": "scaleUp", "Down": "scaleDown"})
    else:
        with defaults(
            scopes="global",
            shift_key="ele_es_variation",
            producers=[electrons.ElectronPtCorrectionMC],
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
    if int(era[:4]) < 2022:
        with defaults(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[met.ApplyRecoilCorrections_Run2],
            exclude_samples=["data", "embedding", "embedding_mc"],
            shift_key=[
                "apply_recoil_resolution_systematic",  # set either to True or False
                "apply_recoil_response_systematic",  # set either to True or False
                "recoil_systematic_shift_up",  # set either to True or False upon variation
                "recoil_systematic_shift_down",  # set either to True or False upon variation
            ]
        ):
            add_shift(
                name="metRecoilResponse",
                shift_map={
                    "Up": [False, True, True, False],
                    "Down": [False, True, False, True],
                }
            )
            add_shift(
                name="metRecoilResolution",
                shift_map={
                    "Up": [True, False, True, False],
                    "Down": [True, False, False, True],
                },
            )
    else: 
        with defaults(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[met.ApplyRecoilCorrections],
            exclude_samples=["data", "data_E", "data_F", "data_G", "embedding", "embedding_mc"],
            shift_key=["recoil_method", "recoil_variation",]
        ):
            add_shift(
                name="metRecoilResponse",
                shift_map={"Up": ["Uncertainty", "RespUp"], "Down": ["Uncertainty", "RespDown"]}
            )
            add_shift(
                name="metRecoilResolution",
                shift_map={"Up": ["Uncertainty", "ResolUp"], "Down": ["Uncertainty", "ResolDown"]}
            )

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
    # Prefiring Shifts
    #########################
    if era != "2018" and int(era[:4]) < 2022:
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringDown",
                quantity_change={
                    nanoAODv9.L1PreFiringWeight_Nom: "L1PreFiringWeight_Dn",
                },
                scopes=["global"],
            )
        )
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringUp",
                quantity_change={
                    nanoAODv9.L1PreFiringWeight_Nom: "L1PreFiringWeight_Up",
                },
                scopes=["global"],
            )
        )

    #########################
    # Z pt DY uncertainties
    #########################
    if "dyjets" in sample or "electroweak_boson" in sample and int(era[:4]) >= 2022:
        add_shift(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[event.ZPtReweighting],
            shift_key="zpt_variation",
            name="zPtReweightWeight",
            shift_map={"Up":"up", "Down":"down"},
        )

    #########################
    # Add additional producers and SFs related to embedded samples
    #########################
    if sample == "embedding" or sample == "embedding_mc" and int(era[:4]) < 2022:
        configuration = setup_embedding(configuration, scopes)

    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    configuration = add_tauVariations(configuration, sample)

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
