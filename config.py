from __future__ import annotations

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
from .quantities import nanoAODv15
from .quantities import output as q
from .selection_config import add_selection, restrict_selection_shifts
from .tau_triggersetup import add_diTauTriggerSetup
from .variations import add_Variations
from .tau_embedding_settings import setup_embedding
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer

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

    measure_btag_efficiency = False

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
    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC
    default_met_filters = [
        "Flag_goodVertices",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_BadPFMuonFilter",
        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
        "Flag_eeBadScFilter",
    ]
    if int(era[:4]) < 2022:
        default_met_filters.extend(["Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter"])
        if sample in ["embedding", "embedding_mc"]:
            default_met_filters.remove("Flag_BadPFMuonDzFilter") # not available in nanoAODv9 of embedding
    if int(era[:4]) >= 2017:
        default_met_filters.append("Flag_ecalBadCalibFilter")
    if int(era[:4]) >= 2022:
        default_met_filters.append("Flag_hfNoisyHitsFilter")
        
    configuration.add_config_parameters(
        "global",
        {
            # noise filters
            "met_filters": default_met_filters,
            
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
            
            # golden json https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions2X
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
                    "2025": "data/golden_json/Cert_Collisions2025_391658_398903_Golden.json", 
                    "2026": "data/golden_json/Cert_Collisions2026_401624_403937_golden.json",
                }
            ),
            
            # pileup corrections
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22CDSep23-Summer22-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23CSep23-Summer23-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23DSep23-Summer23BPix-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-04-15/puWeights_CDEFGHI.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-05/puWeights_2025pp_Golden_Summer24_25ns_69200ub.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-05/puWeights_2025pp_Golden_Summer24_25ns_69200ub.json.gz",
                }
            ),
            "PU_reweighting_file_data": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22CDSep23-Summer22-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23CSep23-Summer23-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23DSep23-Summer23BPix-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2024": "data/root_pileup/Data_PileUp_2024_69p2.root",
                    "2025": "data/root_pileup/Data_PileUp_2025_69p2.root",
                    "2026": "data/root_pileup/Data_PileUp_2025_69p2.root",
                }
            ),
            "PU_reweighting_file_mc": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22CDSep23-Summer22-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23CSep23-Summer23-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23DSep23-Summer23BPix-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2024": "data/root_pileup/MC_PileUp_2024.root",
                    "2025": "data/root_pileup/MC_PileUp_2024.root",
                    "2026": "data/root_pileup/MC_PileUp_2024.root",
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
                    "2024": "Collisions24_CDEFGHI_goldenJSON",
                    "2025": "Collisions25_goldenJSON",
                    "2026": "Collisions25_goldenJSON",
                }
            ),
            "PU_reweighting_variation": "nominal",

            # muon base selection
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.4,
            "max_muon_dxy": 0.045,
            "max_muon_dz": 0.2,
            "muon_id": "Muon_mediumId",
            "max_muon_iso": 0.5, 
            # muon scale and resolution
            "muon_sr_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_scalesmearing.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_scalesmearing.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_scalesmearing.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_scalesmearing.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-06-18/muon_scalesmearing.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_scalesmearing.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_scalesmearing.json.gz",
                }
            ),
            "muon_sr_shift": "nom", # or ScaleUp, ScaleDown, ResoUp, ResoDown
            
            # electron base selection
            "min_ele_pt": 10.0,
            "max_ele_eta": 2.5,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "max_ele_iso": 0.5,
            # electron energy scale
            "ele_es_name": "UL-EGM_ScaleUnc",
            "ele_es_master_seed": 44,
            "ele_es_mc_name": "SmearAndSyst",
            "ele_es_data_name": "Scale",
            "ele_es_file": EraModifier(
                {
                    "2016preVFP": "data/electron_energy_scale/2016preVFP_UL/EGM_ScaleUnc.json.gz",
                    "2016postVFP": "data/electron_energy_scale/2016postVFP_UL/EGM_ScaleUnc.json.gz",
                    "2017": "data/electron_energy_scale/2017_UL/EGM_ScaleUnc.json.gz",
                    "2018": "data/electron_energy_scale/2018_UL/EGM_ScaleUnc.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-15/electronSS_EtDependent.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-15/electronSS_EtDependent.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-26/electronSS_EtDependent.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-26Prompt-Summer24-NanoAODv15/2026-06-08/electronSS_EtDependent.json.gz",
                }
            ),
            "ele_es_variation": "nom",

            # jet base selection
            "min_jet_pt_loose": 30,
            "min_jet_pt_tight": 50,
            "jet_eta_1": 2.5,
            "jet_eta_2": EraModifier(
                {
                    "2024": 3,  # jet eta spikes
                    "2025": 3,  # same treatment as 2024 for jet eta spikes
                    "2026": 3,  # same treatment as 2024 for jet eta spikes
                },
                default=4.7,
            ),
            "jet_eta_3": 4.7,
            "jet_id": 2,  #2==pass tight ID and fail tightLepVeto, 6== pass tight and pass tightLepVeto, new minimal selection https://cms-talk.web.cern.ch/t/updated-jet-selection-criterion-for-jet-veto-map/130527
            # bjet selection -> need to be in global
            "min_bjet_pt": 20,
            "max_bjet_eta": 2.5,
            "btag_cut": EraModifier(  ## values from the wiki for a medium wp https://btv-wiki.docs.cern.ch/ScaleFactors
                {
                    # wp for deepJet
                    "2016preVFP": 0.2598,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                    "2016postVFP": 0.2489,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                    "2017": 0.3040,
                    "2018": 0.2783,
                    # wp for particleNet
                    "2022preEE": 0.245,
                    "2022postEE": 0.2605,
                    "2023preBPix": 0.1917,
                    "2023postBPix": 0.1919,
                },
                default=0.1272,  # 2024, 2025, 2026 UParT
            ),
            # jet puID
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                },
                default=0,  # not used from Run 3 onwards
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            # jet energy calibration
            "jet_id_json": EraModifier(
                {
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jetid.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jetid.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-06-05/jetid.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-05/jetid.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-14/jetid.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-14/jetid.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jetid.json.gz",
                },
                default='""',  # not used for Run 2
            ),
            "jet_collection_name": "AK4PUPPI", #only used for jet ID so not relevant for run 2
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jet_jerc.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jet_jerc.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-06-05/jet_jerc.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-05/jet_jerc.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-14/jet_jerc.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-14/jet_jerc.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jet_jerc.json.gz",
                }
            ),
            "jet_jer_master_seed": 42,
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": "Summer20UL16APVNanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL16APVNanoV15_V1_DATA",
                    "2016postVFP": "Summer20UL16NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL16NanoV15_V1_MC",
                    "2017": "Summer20UL17NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL17NanoV15_V1_MC",
                    "2018": "Summer20UL18NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL18NanoV15_V1_MC",
                    "2022preEE": "Summer22_22Sep2023_V4_DATA" if sample in ["embedding", "data"] else "Summer22_22Sep2023_V4_MC",
                    "2022postEE": "Summer22EE_22Sep2023_V4_DATA" if sample in ["embedding", "data"] else "Summer22EE_22Sep2023_V4_MC",
                    "2023preBPix": "Summer23Prompt23_V4_DATA" if sample in ["embedding", "data"] else "Summer23Prompt23_V4_MC",
                    "2023postBPix": "Summer23BPixPrompt23_V4_DATA" if sample in ["embedding", "data"] else "Summer23BPixPrompt23_V4_MC",
                    "2024": "Summer24Prompt24_V4_DATA" if sample in ["embedding", "data"] else "Summer24Prompt24_V4_MC",
                    "2025": "Summer24Prompt25_V2_DATA" if sample in ["embedding", "data"] else "Summer24Prompt25_V2_MC",
                    "2026": "Summer24Prompt26_V1_DATA" if sample in ["embedding", "data"] else "Summer24Prompt26_V1_MC",
                }
            ),
            # jet resolution correction
            "jet_reapplyJES": True,
            "jet_jes_source": "nom",
            "jet_jes_shift": 0,
            "jet_jer_shift": "nom",  # or "up", "down"
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": "Summer20UL16APV_JRV3_MC",
                    "2016postVFP": "Summer20UL16_JRV3_MC",
                    "2017": "Summer19UL17_JRV4_MC",
                    "2018": "Summer19UL18_JRV3_MC",
                    "2022preEE": "Summer22_22Sep2023_JRV2_MC",
                    "2022postEE": "Summer22EE_22Sep2023_JRV2_MC",
                    "2023preBPix": "Summer23Prompt23_RunCv1234_JRV2_MC",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_JRV2_MC",
                    "2024": "Summer24Prompt24_JRV2_MC",
                    "2025": "Summer24Prompt25_JRV2_MC",
                    "2026": "Summer24Prompt26_RunBD_JRV1_MC",
                }
            ),
            "jet_jec_algo": EraModifier(
                {
                    "2016preVFP": "AK4PFchs",
                    "2016postVFP": "AK4PFchs",
                    "2017": "AK4PFchs",
                    "2018": "AK4PFchs",
                },
                default="AK4PFPuppi", # run3
            ),
            # jet veto configuration
            "jet_veto_map_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv15/2026-06-05/jetvetomaps.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv15/2026-06-05/jetvetomaps.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv15/2026-06-05/jetvetomaps.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv15/2026-06-05/jetvetomaps.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-14/jetvetomaps.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-14/jetvetomaps.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jetvetomaps.json.gz",
                }
            ),
            "jet_veto_map_name": EraModifier(
                {
                    "2016preVFP": "Summer19UL16_V1",
                    "2016postVFP": "Summer19UL16_V1",
                    "2017": "Summer19UL17_V1",
                    "2018": "Summer19UL18_V1",
                    "2022preEE": "Summer22_23Sep2023_RunCD_V1",
                    "2022postEE": "Summer22EE_23Sep2023_RunEFG_V1",
                    "2023preBPix": "Summer23Prompt23_RunC_V1",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_V1",
                    "2024": "Summer24Prompt24_RunBCDEFGHI_V1",
                    "2025": "Summer24Prompt25_RunCDEFG_V1",
                    "2026": "Summer24Prompt26_RunBCD_V1",
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

    for ch in ["tt", "mt", "et", "em"]:
        configuration.add_config_parameters(
            ch,
            {
                "btag_eff_file": EraModifier(
                    {
                        "2022preEE": f"payloads/btag_efficiencies/2022preEE/{ch}/btag_efficiency.json.gz",
                        "2022postEE": f"payloads/btag_efficiencies/2022postEE/{ch}/btag_efficiency.json.gz",
                        "2023preBPix": f"payloads/btag_efficiencies/2023preBPix/{ch}/btag_efficiency.json.gz",
                        "2023postBPix": f"payloads/btag_efficiencies/2023postBPix/{ch}/btag_efficiency.json.gz",
                        "2024": f"payloads/btag_efficiencies/2024/{ch}/btag_efficiency.json.gz",
                        "2025": f"payloads/btag_efficiencies/2025/{ch}/btag_efficiency.json.gz",
                        "2026": f"payloads/btag_efficiencies/2025/{ch}/btag_efficiency.json.gz",  # to update later on
                    },
                    default='""',  # Run 2
                ),
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
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-23CSep23-Summer23-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-03-10/btagging.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-25Prompt-Summer24-NanoAODv15/2026-06-26/btagging.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-25Prompt-Summer24-NanoAODv15/2026-06-26/btagging.json.gz",
                }
            ),
            "btag_sf_variation": "central",
            "btag_sf_variation_bc": "central",
            "btag_sf_variation_lf": "central",
            "btag_wp": "M",
            "btag_corr_algo": EraModifier(
                {
                    "2016preVFP": "deepJet_shape",
                    "2016postVFP": "deepJet_shape",
                    "2017": "deepJet_shape",
                    "2018": "deepJet_shape",
                    "2022preEE": "particleNet_comb",
                    "2022postEE": "particleNet_comb",
                    "2023preBPix": "particleNet_comb",
                    "2023postBPix": "particleNet_comb",
                    "2024": "UParTAK4_comb",
                    "2025": "UParTAK4_comb",
                    "2026": "UParTAK4_comb",
                }
            ),
            "btag_corr_algo_lf": EraModifier(
                {
                    "2016preVFP": "deepJet_shape",
                    "2016postVFP": "deepJet_shape",
                    "2017": "deepJet_shape",
                    "2018": "deepJet_shape",
                    "2022preEE": "particleNet_light",
                    "2022postEE": "particleNet_light",
                    "2023preBPix": "particleNet_light",
                    "2023postBPix": "particleNet_light",
                    "2024": "UParTAK4_light",
                    "2025": "UParTAK4_light",
                    "2026": "UParTAK4_light",
                }
            ),
            "btag_sf_wp_name": EraModifier(
                {
                    "2016preVFP": "TO_ADD",
                    "2016postVFP": "TO_ADD",
                    "2017": "TO_ADD",
                    "2018": "TO_ADD",
                    "2022preEE": "particleNet_wp_values",
                    "2022postEE": "particleNet_wp_values",
                    "2023preBPix": "particleNet_wp_values",
                    "2023postBPix": "particleNet_wp_values",
                    "2024": "UParTAK4_wp_values",
                    "2025": "UParTAK4_wp_values",
                    "2026": "UParTAK4_wp_values",
                },
            ),
            "btag_eff_name": "btag_efficiency",
            "btag_eff_sample_type": SampleModifier(
                {
                    **{
                        sample_type: sample_type
                        for sample_type in available_sample_types
                    },
                    **{
                        sample_type: "dyjets"
                        for sample_type in [
                            "dyjets",
                            "dyjets_madgraph",
                            "dyjets_amcatnlo",
                            "dyjets_amcatnlo_ll",
                            "dyjets_amcatnlo_tt",
                            "dyjets_powheg",
                            "electroweak_boson",
                        ]
                    },
                    **{
                        sample_type: "ggh_htautau"
                        for sample_type in [
                            "ggh_htautau",
                            "ggh_hbb",
                            "hh4b",
                            "hh2b2tau",
                            "hh4v",
                            "nmssm_Ybb",
                            "nmssm_Ytautau",
                        ]
                    },
                    **{
                        sample_type: "vbf_htautau"
                        for sample_type in [
                            "vbf_htautau",
                            "vbf_hbb",
                        ]
                    },
                    **{
                        sample_type: "rem_htautau"
                        for sample_type in [
                            "rem_htautau",
                            "rem_hbb",
                            "rem_hww",
                            "rem_hzz",
                            "rem_higgs",
                        ]
                    },
                    **{
                        sample_type: "ttbar"
                        for sample_type in [
                            "ttbar",
                            "rem_ttbar",
                        ]
                    },
                    **{
                        sample_type: "wjets"
                        for sample_type in [
                            "wjets",
                            "wjets_madgraph",
                            "wjets_amcatnlo",
                        ]
                    },
                }
            ),
            # jet selection
            "deltaR_jet_veto": 0.5,
            # pair selection
            "pairselection_min_dR": 0.5,
            # propagate jet and lepton sf correction to the met
            "propagateLeptons": True,
            "propagateJets": True,
            # recoil corrections
            "recoil_corrections_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                    "2022preEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/RecoilCorrlib/Recoil_corrections_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/RecoilCorrlib/Recoil_corrections_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                    "2025": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                    "2026": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '""',
                    "2025": '""',
                    "2026": '""',
                }
            ),
            "recoil_method": "QuantileMapHist", #other option is pure "Resclaing"
            "recoil_variation": "nom",
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
                    "2016preVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  
                    "2016postVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                    "2022preEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022preEE_v5.json.gz",
                    "2022postEE": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2022postEE_v5.json.gz",
                    "2023preBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023preBPix_v5.json.gz",
                    "2023postBPix": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2023postBPix_v5.json.gz",
                    "2024": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                    "2025": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                    "2026": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
            "DY_order": SampleModifier( #mg is LO, amcat is NLO, powheg is NNLO
                {
                    "dyjets_powheg": "NNLO",
                    "ggh_htautau": "NNLO",
                    "ggh_hbb": "NNLO",
                    "vbf_htautau": "NNLO",
                    "vbf_hbb": "NNLO",
                    "rem_htautau": "NNLO",
                    "rem_hbb": "NNLO",
                    "wjets": "NNLO",
                    }, 
                default="NLO",
            ), #from GrASP it looks like the DY powheg samples are also NLO and not NNLO, doesn't matter for the corrections
            "zpt_variation": "nom",

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
            "tau_vsjet_wp": "Medium", ##change again to Loose if it becomes available
            "tau_vsele_wp": "VVLoose",
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
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-01-14/tau.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-01-14/tau.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-01-14/tau.json.gz",
                }
            ),
            "tau_vsjet_sf_dependence": "dm",
            #decay modes
            "tau_dms": "0,1,10,11",
            #energy scale
            "tau_ES_json_name": "tau_energy_scale",
            # genuine tau 
            "tau_es_DM0": "nom",
            "tau_es_DM1": "nom",
            "tau_es_DM10": "nom",
            "tau_es_DM11": "nom",
            # for 2024 and 2025 py pt too 
            "tau_es_DM0_pt20to40": "nom",
            "tau_es_DM0_pt40to60": "nom",
            "tau_es_DM0_pt60toInf": "nom",
            "tau_es_DM1_pt20to40": "nom",
            "tau_es_DM1_pt40to60": "nom",
            "tau_es_DM1_pt60toInf": "nom",
            "tau_es_DM10_pt20to40": "nom",
            "tau_es_DM10_pt40to60": "nom",
            "tau_es_DM10_pt60toInf": "nom",
            "tau_es_DM11_pt20to40": "nom",
            "tau_es_DM11_pt40to60": "nom",
            "tau_es_DM11_pt60toInf": "nom",
            # vs jet id
            "tau_id_vsjet_DM0": "nom",
            "tau_id_vsjet_DM1": "nom",
            "tau_id_vsjet_DM10": "nom",
            "tau_id_vsjet_DM11": "nom",
            # vs jet id
            "tau_id_vsjet_DM0_pt20to40": "nom",
            "tau_id_vsjet_DM0_pt40to60": "nom",
            "tau_id_vsjet_DM0_pt60toInf": "nom",
            "tau_id_vsjet_DM1_pt20to40": "nom",
            "tau_id_vsjet_DM1_pt40to60": "nom",
            "tau_id_vsjet_DM1_pt60toInf": "nom",
            "tau_id_vsjet_DM10_pt20to40": "nom",
            "tau_id_vsjet_DM10_pt40to60": "nom",
            "tau_id_vsjet_DM10_pt60toInf": "nom",
            "tau_id_vsjet_DM11_pt20to40": "nom",
            "tau_id_vsjet_DM11_pt40to60": "nom",
            "tau_id_vsjet_DM11_pt60toInf": "nom",
            # fake ele
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM10_barrel": "nom",
            "tau_elefake_es_DM11_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_elefake_es_DM10_endcap": "nom",
            "tau_elefake_es_DM11_endcap": "nom",
            # vs ele id
            "tau_id_vsele_DM0_barrel": "nom",
            "tau_id_vsele_DM1_barrel": "nom",
            "tau_id_vsele_DM10_barrel": "nom",
            "tau_id_vsele_DM11_barrel": "nom",
            "tau_id_vsele_DM0_endcap": "nom",
            "tau_id_vsele_DM1_endcap": "nom",
            "tau_id_vsele_DM10_endcap": "nom",
            "tau_id_vsele_DM11_endcap": "nom",
            # fake muon
            "tau_mufake_es_DM0": "nom",
            "tau_mufake_es_DM1": "nom",
            "tau_mufake_es_DM10": "nom",
            "tau_mufake_es_DM11": "nom",
            # vs muon id
            "tau_id_vsmu_wheel1": "nom",
            "tau_id_vsmu_wheel2": "nom",
            "tau_id_vsmu_wheel3": "nom",
            "tau_id_vsmu_wheel4": "nom",
            "tau_id_vsmu_wheel5": "nom",
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
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-18/muon_Z.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-18/muon_Z.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2026-06-18/muon_Z.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-18/muon_Z.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-06-18/muon_Z.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_Z.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_Z.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",  # correction for mediumId WP
            "muon_iso_sf_name": "NUM_TightPFIso_DEN_MediumID",  # correction for TightPFIso WP (PF isolation < 0.15)
            "muon_id_variation": "nominal",  # "systup"/"systdown/statup/statdown", user defined
            "muon_iso_variation": "nominal",  # "systup"/"systdown/statup/statdown", user defined

            #run 2 scale factors from embedding framework
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
                    "2026": '""',
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
        },
    )
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            # muon selection
            # here pt cut lower for additional objects, then the main one is managed by the trigger
            "muon_index_in_pair": 0,
            "min_muon_pt": 15.0,
            "max_muon_eta": 2.4,
            "max_muon_iso": 0.5,
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
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-26/electron.json.gz", 
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-26/electron.json.gz",
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
                    "2025": "2025Prompt",
                    "2026": "2025Prompt",
                }
            ),
            "ele_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations

            #run 2 scale factors form embedding framework
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
                    "2026": '""',
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
            # here pt cut lower for additional objects, then the main one is managed by the trigger
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 0,
            "min_ele_pt": 15.0,
            "max_ele_eta": 2.5,
            "max_ele_iso": 0.5,
            "muon_index_in_pair": 1,
            "min_muon_pt": 15.0,
            "max_muon_eta": 2.4,
            "max_muon_iso": 0.5,
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
            "min_ele_pt": 15.0,
            "max_ele_eta": 2.5,
            "max_ele_iso": 0.5,
        },
    )
    
    if int(era[:4]) < 2022:
        configuration.add_config_parameters(
            "global",
            {
                "max_muon_iso": 0.3,
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
                # remove dependency on vs ele wp for consistency since it's not needed in run2
                "vsmu_tau_id": [
                    {
                        "tau_1_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_1".format(wp=wp),
                        "tau_2_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_2".format(wp=wp),
                        "vsmu_tau_id_WP": "{wp}".format(wp=wp),
                        "vsele_tau_id_WP": '""',
                        "vsjet_tau_id_WP": '""', 
                        "tau_1_vsmu_id_outputname": "id_tau_vsMu_{wp}_1".format(wp=wp),
                        "tau_2_vsmu_id_outputname": "id_tau_vsMu_{wp}_2".format(wp=wp),
                        "vsmu_tau_id_WPbit": bit,
                    }
                    for wp, bit in {
                        "VLoose": 1,
                        "Loose": 2,
                        "Medium": 3,
                        "Tight": 4,
                    }.items()
                ],
                "max_tau_eta": 2.3,
                # variations energy scale
                # by dm and pt
                "tau_ES_shift_1prong0pizero20to40": "nom",
                "tau_ES_shift_1prong0pizero40toInf": "nom",
                "tau_ES_shift_1prong1pizero20to40": "nom",
                "tau_ES_shift_1prong1pizero40toInf": "nom",
                "tau_ES_shift_3prong0pizero20to40": "nom",
                "tau_ES_shift_3prong0pizero40toInf": "nom",
                "tau_ES_shift_3prong1pizero20to40": "nom",
                "tau_ES_shift_3prong1pizero40toInf": "nom",
                # by dm
                "tau_ES_shift_1prong1pizero": "nom",
                "tau_ES_shift_1prong0pizero": "nom",
                "tau_ES_shift_3prong0pizero": "nom",
                "tau_ES_shift_3prong1pizero": "nom",
                # muon fakes variation
                "tau_mufake_es": "nom",
                # tau ID sf variation by pt
                "tau_id_vsjet_tau30to35": "nom",
                "tau_id_vsjet_tau35to40": "nom",
                "tau_id_vsjet_tau40to500": "nom",
                "tau_id_vsjet_tau500to1000": "nom",
                "tau_id_vsjet_tau1000toinf": "nom",
                # tau ID sf variation by dm and pt
                "tau_id_vsjet_1prong0pizero20to40": "nom",
                "tau_id_vsjet_1prong0pizero40toInf": "nom",
                "tau_id_vsjet_1prong1pizero20to40": "nom",
                "tau_id_vsjet_1prong1pizero40toInf": "nom",
                "tau_id_vsjet_3prong0pizero20to40": "nom",
                "tau_id_vsjet_3prong0pizero40toInf": "nom",
                "tau_id_vsjet_3prong1pizero20to40": "nom",
                "tau_id_vsjet_3prong1pizero40toInf": "nom",
                # tau ID sf variation by dm
                "tau_id_vsjet_1prong0pizero": "nom",
                "tau_id_vsjet_1prong1pizero": "nom",
                "tau_id_vsjet_3prong0pizero": "nom",
                "tau_id_vsjet_3prong1pizero": "nom",
            }
        )
        for chs, params in [
            (["mt", "mm", "em"], {"muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID"}),
            (["et", "ee", "em"], {"ele_id_sf_name": "UL-Electron-ID-SF"}),
            (["et", "mt"], {"vsjet_tau_id_bit": 1, "vsele_tau_id_bit": 1, "vsmu_tau_id_bit": 1}),
            (["mt"], {"max_muon_eta": 2.1, "max_muon_iso": 0.3}),
            (["em", "ee"], {"max_ele_eta": 2.1, "max_ele_iso": 0.3, "max_muon_eta": 2.1}),
            (["mm"], {"min_muon_pt": 20.0, "max_muon_eta": 2.1, "max_muon_iso": 0.15}),
            (["et"], {"max_electron_eta": 2.1, "max_ele_iso": 0.5}),
            (["tt"], {
                "tau_vsjet_sf_dependence": "pt",
                "min_tau_pt": 35.0,
                "vsjet_tau_id_bit": 4,
                "vsele_tau_id_bit": 4,
                "vsmu_tau_id_bit": 1,
            }),
        ]:
            configuration.add_config_parameters(chs, params)

    ############################
    ######## Producers #########
    ############################
    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.Lumi,
            event.npartons,
            event.MetFilter, 
            event.PUweights,
            event.LHE_Scale_weight,
            event.LHE_PDF_weight,
            event.LHE_alphaS_weight,
            event.PS_weight,
            muons.MuonPtCorrection,
            muons.BaseMuons,
            electrons.ElectronPtCorrectionMC,
            electrons.BaseElectrons,
            jets.GenJet,
            jets.JetSmearingSeed,
            jets.JetBTagUParT,
            jets.JetRho,
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
            event.EvenOddIDFlag,
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
            taus.TauEnergyCorrection,
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
            scalefactors.MuonIDIso_SF,
            scalefactors.TauID_SF,
            triggers.MTGenerateSingleMuonTriggerFlags,
            #triggers.MTGenerateCrossTriggerFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
            scalefactors.SingleMuTriggerSF,
            #scalefactors.MuTauTriggerSF,
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
            taus.TauEnergyCorrection,
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
            scalefactors.TauID_SF,
            scalefactors.EleID_SF,
            triggers.ETGenerateSingleElectronTriggerFlags,
            #triggers.ETGenerateCrossTriggerFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
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
            scalefactors.SingleEleTriggerSF,
            scalefactors.SingleMuTriggerSF,
        ],
    )
    configuration.add_producers(
        "tt",
        [   
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            taus.TauEnergyCorrection,
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
            scalefactors.TauID_SF,
            triggers.TTGenerateDoubleTauTriggerFlags,
            scalefactors.DoubleTauTriggerSF,
        ],
    )
    
    ################################
    ######### Modifications ########
    ################################

    MC_ONLY = ["data", "embedding", "embedding_mc"]
    
    for mod_scopes, rule_cls, producers, sample_filter in [
        ("global", RemoveProducer, [event.npartons], 
            {"exclude_samples": ["dyjets", "dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "wjets", "wjets_amcatnlo", "electroweak_boson"]}),
        ("global", RemoveProducer, [event.PUweights, event.PS_weight], {"samples": MC_ONLY}),
        ("global", RemoveProducer, [event.LHE_Scale_weight, event.LHE_PDF_weight, event.LHE_alphaS_weight], {"samples": MC_ONLY + ["diboson"]}),
        (scopes, RemoveProducer, [scalefactors.btaggingWP_SF], {"samples": MC_ONLY}),
        (scopes, RemoveProducer, [genparticles.GenMatching], {"samples": MC_ONLY}),
        (["et", "mt", "tt"], RemoveProducer, [scalefactors.TauID_SF], {"samples": MC_ONLY}),
        (["mt", "em", "mm"], RemoveProducer, [scalefactors.MuonIDIso_SF], {"samples": MC_ONLY}),
        (["et", "ee", "em"], RemoveProducer, [scalefactors.EleID_SF], {"samples": MC_ONLY}),
        (["mt"], RemoveProducer, [genparticles.MTGenDiTauPairQuantities], {"samples": ["data"]}),
        (["mm"], RemoveProducer, [genparticles.MuMuGenPairQuantities], {"samples": ["data"]}),
        (["et"], RemoveProducer, [genparticles.ETGenDiTauPairQuantities], {"samples": ["data"]}),
        (["em"], RemoveProducer, [genparticles.EMGenDiTauPairQuantities], {"samples": ["data"]}),
        (["ee"], RemoveProducer, [genparticles.ElElGenPairQuantities], {"samples": ["data"]}),
        (["tt"], RemoveProducer, [genparticles.TTGenDiTauPairQuantities], {"samples": ["data"]}),

        ("global", AppendProducer, [event.JSONFilter], {"samples": MC_ONLY}),
        ## producer to add a cut on DYto2L affected by pythia bug where DYto2Tau has been reprocessed
        ("global", AppendProducer, [genparticles.GenDYFlavor, genparticles.GenDYFilter], {"samples": ["dyjets_amcatnlo_ll"]}),
        (scopes, AppendProducer, [event.ZPtReweighting], {"samples": ["dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "electroweak_boson"]}),
        (scopes, AppendProducer, [event.GGH_NNLO_Reweighting, event.GGH_WG1_Uncertainties], {"samples": ["ggh_htautau", "rem_htautau"]}),
        (scopes, AppendProducer, [event.QQH_WG1_Uncertainties], {"samples": ["vbf_htautau", "rem_htautau"]}),
        (scopes, AppendProducer, [event.TopPtReweighting], {"samples": ["ttbar"]}),
                
        ("global", ReplaceProducer, [jets.GenJet, jets.GenJet_data], {"samples": MC_ONLY}),
        (["et", "mt", "tt"], ReplaceProducer, [taus.TauEnergyCorrection, taus.TauEnergyCorrection_data], {"samples": MC_ONLY}),
        
    ]:
        configuration.add_modification_rule(mod_scopes, rule_cls(producers=producers, **sample_filter))

    if int(era[:4]) < 2022:
        for mod_scopes, rule_cls, producers, sample_filter in [
            ("global", RemoveProducer, [jets.JetVetoMapVeto], {"exclude_samples": ["fake_era"]}),
            (["mt", "em", "mm"], RemoveProducer, [scalefactors.MuonIDIso_SF], {"exclude_samples": MC_ONLY}),
            (["et", "ee", "em"], RemoveProducer, [scalefactors.EleID_SF], {"exclude_samples": MC_ONLY}),
            (["mt"], RemoveProducer, [scalefactors.SingleMuTriggerSF], {"exclude_samples": ["fake_era"]}),
            (["et"], RemoveProducer, [scalefactors.SingleEleTriggerSF], {"exclude_samples": ["fake_era"]}),
            (["tt"], RemoveProducer, [scalefactors.DoubleTauTriggerSF], {"exclude_samples": ["fake_era"]}),

            # cross triggers and embedding triggers      
            (["mt"], AppendProducer, [triggers.MTGenerateCrossTriggerFlags, triggers.GenerateSingleTrailingTauTriggerFlags], {"exclude_samples": ["fake_era"]}),
            (["mt"], AppendProducer, [scalefactors.MTGenerateSingleMuonTriggerSF_MC, scalefactors.PrivateMuonIDSF_1_MC, scalefactors.PrivateMuonIsoSF_1_MC], {"exclude_samples": MC_ONLY}),
            (["et"], AppendProducer, [triggers.ETGenerateCrossTriggerFlags, triggers.GenerateSingleTrailingTauTriggerFlags], {"exclude_samples": ["fake_era"]}),
            (["et"], AppendProducer, [scalefactors.ETGenerateSingleElectronTriggerSF_MC, scalefactors.PrivateElectronIDSF_1_MC, scalefactors.PrivateElectronIsoSF_1_MC], {"exclude_samples": MC_ONLY}),
            (["tt"], AppendProducer, [triggers.GenerateSingleTrailingTauTriggerFlags, triggers.GenerateSingleLeadingTauTriggerFlags], {"exclude_samples": ["fake_era"]}),
            (["em"], AppendProducer, [scalefactors.PrivateElectronIDSF_1_MC, scalefactors.PrivateElectronIsoSF_1_MC, scalefactors.PrivateMuonIDSF_2_MC, scalefactors.PrivateMuonIsoSF_2_MC], {"exclude_samples": MC_ONLY}),
            (["mm"], AppendProducer, [scalefactors.PrivateMuonIDSF_1_MC, scalefactors.PrivateMuonIsoSF_1_MC, scalefactors.PrivateMuonIDSF_2_MC, scalefactors.PrivateMuonIsoSF_2_MC, scalefactors.MTGenerateSingleMuonTriggerSF_MC], {"exclude_samples": MC_ONLY}),
            (["ee"], AppendProducer, [scalefactors.PrivateElectronIDSF_1_MC, scalefactors.PrivateElectronIsoSF_1_MC, scalefactors.PrivateElectronIDSF_2_MC, scalefactors.PrivateElectronIsoSF_2_MC, scalefactors.ETGenerateSingleElectronTriggerSF_MC], {"exclude_samples": MC_ONLY}),
                        
            ("global", ReplaceProducer, [electrons.ElectronIDCut, electrons.ElectronIDCut_v9], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [event.TopPtReweighting, event.TopPtReweighting_Run2], {"samples": ["ttbar"]}),
            ("global", ReplaceProducer, [electrons.ElectronPtCorrectionMC, electrons.ElectronPtCorrectionMC_v9], {"exclude_samples": MC_ONLY}),
            ("global", ReplaceProducer, [electrons.ElectronPtCorrectionMC, electrons.RenameElectronPt], {"samples": MC_ONLY}),
            ("global", ReplaceProducer, [event.DiLeptonVeto, event.DiLeptonVeto_v9], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.JetEnergyCorrection, jets.JetEnergyCorrection_Run2], {"exclude_samples": MC_ONLY}),
            ("global", ReplaceProducer, [jets.JetEnergyCorrection, jets.JetEnergyCorrection_data], {"samples": MC_ONLY}),
            ("global", ReplaceProducer, [jets.JetID, jets.JetID_rename], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.JetBTagUParT, jets.JetBTagDeep], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.JetRho, jets.JetRho_v9], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.GoodJets, jets.GoodJets_Run2], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.GoodBJets, jets.GoodBJets_Run2], {"exclude_samples": ["fake_era"]}),
            (scopes, ReplaceProducer, [scalefactors.btaggingWP_SF, scalefactors.btagging_SF], {"exclude_samples": MC_ONLY}),
            (scopes, ReplaceProducer, [met.MetCorrections, met.MetCorrections_Run2], {"exclude_samples": ["fake_era"]}),
            (scopes, ReplaceProducer, [met.PFMetCorrections, met.PFMetCorrections_Run2], {"exclude_samples": ["fake_era"]}),
            (["mt", "et", "tt"], ReplaceProducer, [taus.BaseTaus, taus.BaseTaus_v9], {"exclude_samples": ["fake_era"]}),
            (["mt", "et", "tt"], ReplaceProducer, [taus.GoodTaus, taus.GoodTaus_v9], {"exclude_samples": ["fake_era"]}),
            (["mt", "et", "tt"], ReplaceProducer, [scalefactors.TauID_SF, scalefactors.TauID_SF_v9], {"exclude_samples": MC_ONLY}),
            (["et", "mt", "tt"], ReplaceProducer, [taus.TauEnergyCorrection, taus.TauEnergyCorrection_ES_dm_pt_binned], {"exclude_samples": MC_ONLY}),
            (["tt"], ReplaceProducer, [pairquantities.TTDiTauPairQuantities, pairquantities.TTDiTauPairQuantities_v9], {"exclude_samples": ["fake_era"]}),
            (["mt"], ReplaceProducer, [pairquantities.MTDiTauPairQuantities, pairquantities.MTDiTauPairQuantities_v9], {"exclude_samples": ["fake_era"]}),
            (["et"], ReplaceProducer, [pairquantities.ETDiTauPairQuantities, pairquantities.ETDiTauPairQuantities_v9], {"exclude_samples": ["fake_era"]}),
        ]:
            configuration.add_modification_rule(mod_scopes, rule_cls(producers=producers, **sample_filter))

        if era != "2018":
            configuration.add_modification_rule("global", AppendProducer(producers=event.PrefireWeight, exclude_samples=["fake_era"],),)
        # Broken sfs file for 2016. If nlo is used, this reweighting is not even needed. !!!
        if "2016" not in era:
            configuration.add_modification_rule(scopes, AppendProducer(producers=event.ZPtReweighting_Run2, samples=["dyjets", "electroweak_boson"]),)
    else:
        configuration.add_modification_rule("global", ReplaceProducer(producers=[electrons.ElectronPtCorrectionMC, electrons.ElectronPtCorrectionData], samples=MC_ONLY,),)

    if 2022 <= int(era[:4]) < 2024:
        for mod_scopes, rule_cls, producers, sample_filter in [
            ("global", ReplaceProducer, [jets.JetBTagUParT, jets.JetBTagPNet], {"exclude_samples": ["fake_era"]}),
            ("global", ReplaceProducer, [jets.JetID, jets.JetIDRun3NanoV12Corrected], {"exclude_samples": ["fake_era"]}),
            (scopes, ReplaceProducer, [met.MetCorrections, met.MetCorrections_v12], {"exclude_samples": ["fake_era"]}),
            (["et", "mt", "tt"], ReplaceProducer, [taus.TauEnergyCorrection, taus.TauEnergyCorrection_v12], {"exclude_samples": MC_ONLY}),
            (["mt", "et", "tt"], ReplaceProducer, [scalefactors.TauID_SF, scalefactors.TauID_SF_v12], {"exclude_samples": MC_ONLY}),
        ]:
            configuration.add_modification_rule(mod_scopes, rule_cls(producers=producers, **sample_filter))
    
    if int(era[:4]) < 2024:
        configuration.add_modification_rule("global", ReplaceProducer(producers=[met.MetBasics, met.MetBasics_v12], exclude_samples=["fake_era"],),)

    # separate MC for 2024 and 2025 by even/odd event number
    if era == "2024":
        configuration.add_modification_rule("global", AppendProducer(producers=[event.EvenIDFilter], exclude_samples=MC_ONLY,),)
    if era == "2025" or era == "2026":
        configuration.add_modification_rule("global", AppendProducer(producers=[event.OddIDFilter], exclude_samples=["data", "embedding"],),)
    

    #########################
    ######## OUTPUTS ########
    #########################
    configuration.add_outputs(
        scopes,
        [
            nanoAODv15.PV_npvsGood,
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_ggh_htautau,
            q.is_vbf_htautau,
            q.is_diboson,
            nanoAODv15.run,
            q.lumi,
            q.npartons,
            nanoAODv15.event,
            q.eventCut_mask,
            q.puweight,
            q.lhe_scale_weight,
            q.ps_weight,
            q.lhe_pdf_weight,
            q.lhe_alphaS_weight,
            q.met_mask,
            q.jet_ID,
            q.jet_vetomap,
            ] + [p for scope in scopes for p in genparticles.GenMatching.get_outputs(scope)] + [
            ] + [p for scope in scopes for p in jets.BasicJetQuantities.get_outputs(scope)] + [
            ] + [p for scope in scopes for p in jets.BasicBJetQuantities.get_outputs(scope)] + [
            q.btag_weight,
            ] + [p for scope in scopes for p in pairquantities.DiTauPairMETQuantities.get_outputs(scope)] + [
            q.dimuon_veto,
            q.dilepton_veto,
            q.dielectron_veto,
            ] + [p for scope in scopes for p in pairquantities.DiObjectAngleQuantities.get_outputs(scope)
            ] + [p for scope in scopes for p in met.MetCorrections.get_outputs(scope)
        ],
    )
    # add genWeight for everything but data
    if sample not in ["data"]:
        configuration.add_outputs(
            scopes,
            nanoAODv15.genWeight,
        )
        if int(era[:4]) < 2018:
            configuration.add_outputs(
                scopes,
                q.prefiring_wgt,
            )

    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in genparticles.MTGenDiTauPairQuantities.get_outputs("mt")
            ] + [p for p in scalefactors.TauID_SF.get_outputs("mt")
        ],
    )
    configuration.add_outputs(
        "mm",
        [
            q.nmuons,
            triggers.MuMuGenerateSingleMuonTriggerFlags.output_group,
            ] + [p for p in pairquantities.MuMuPairQuantities.get_outputs("mm")
            ] + [p for p in genparticles.MuMuGenPairQuantities.get_outputs("mm")
        ],
    )
    configuration.add_outputs(
        "et",
        [
            q.nelectrons,
            q.ntaus,
            triggers.ETGenerateSingleElectronTriggerFlags.output_group,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in genparticles.ETGenDiTauPairQuantities.get_outputs("et")
            ] + [p for p in scalefactors.TauID_SF.get_outputs("et")
        ],
    )
    configuration.add_outputs(
        "em",
        [
            q.nelectrons,
            q.nmuons,
            triggers.EMGenerateSingleElectronTriggerFlags.output_group,
            triggers.EMGenerateSingleMuonTriggerFlags.output_group,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in pairquantities.EMDiTauPairQuantities.get_outputs("em")
            ] + [p for p in genparticles.EMGenDiTauPairQuantities.get_outputs("em")
        ],
    )
    configuration.add_outputs(
        "ee",
        [
            q.nelectrons,
            triggers.ElElGenerateSingleElectronTriggerFlags.output_group,
            triggers.ElElGenerateDoubleMuonTriggerFlags.output_group,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in pairquantities.ElElPairQuantities.get_outputs("ee")
            ] + [p for p in genparticles.ElElGenPairQuantities.get_outputs("ee")
        ],
    )
    configuration.add_outputs(
        "tt",
        [
            q.ntaus,
            triggers.TTGenerateDoubleTauTriggerFlags.output_group,
            q.taujet_pt_1,
            q.taujet_pt_2,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in genparticles.TTGenDiTauPairQuantities.get_outputs("tt")
            ] + [p for p in scalefactors.TauID_SF.get_outputs("tt")
        ],
    )

    if int(era[:4]) < 2024:
        configuration.add_outputs("global", [p for p in met.MetBasics_v12.get_outputs("global")],)
    else:
        configuration.add_outputs("global", [p for p in met.MetBasics.get_outputs("global")],)

    if int(era[:4]) < 2022:
        configuration.add_outputs(
            "mt",
            [
                triggers.MTGenerateCrossTriggerFlags.output_group,
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
                ] + [p for p in pairquantities.MTDiTauPairQuantities_v9.get_outputs("mt")
            ],
        )
        configuration.add_outputs(
            "et",
            [
                triggers.ETGenerateCrossTriggerFlags.output_group,
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
                ] + [p for p in pairquantities.ETDiTauPairQuantities_v9.get_outputs("et")
            ],
        )
        configuration.add_outputs(
            "em",
            [
                triggers.EMGenerateCrossTriggerFlags.output_group,
            ],
        )
        configuration.add_outputs(
            "tt",
            [
                triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
                triggers.GenerateSingleLeadingTauTriggerFlags.output_group,
                ] + [p for p in pairquantities.TTDiTauPairQuantities_v9.get_outputs("tt")
            ],
        )
    else:
        configuration.add_outputs(
            "mt",
            [
                scalefactors.SingleMuTriggerSF.output_group,
                ] + [p for p in scalefactors.MuonIDIso_SF.get_outputs("mt")
                ] + [p for p in pairquantities.MTDiTauPairQuantities.get_outputs("mt")
            ],
        )
        configuration.add_outputs(
            "et",
            [
                scalefactors.SingleEleTriggerSF.output_group,
                ] + [p for p in scalefactors.EleID_SF.get_outputs("et")
                ] + [p for p in pairquantities.ETDiTauPairQuantities.get_outputs("et")
            ],
        )
        configuration.add_outputs(
            "tt",
            [
                p for p in scalefactors.DoubleTauTriggerSF.get_outputs("tt")
                ] + [p for p in pairquantities.TTDiTauPairQuantities.get_outputs("tt")
            ],
        )
        configuration.add_outputs(
            "em",
            [
                scalefactors.SingleMuTriggerSF.output_group,
                scalefactors.SingleEleTriggerSF.output_group,
                ] + [p for p in scalefactors.EleID_SF.get_outputs("em")
                ] + [p for p in scalefactors.MuonIDIso_SF.get_outputs("em")
            ],
        )

    if "data" not in sample and "embedding" not in sample:
        configuration.add_outputs(
            scopes,
            [
                nanoAODv15.HTXS_Higgs_pt,
                nanoAODv15.HTXS_Higgs_y,
                nanoAODv15.HTXS_njets25,
                nanoAODv15.HTXS_njets30,
                nanoAODv15.HTXS_stage1_1_cat_pTjet25GeV,
                nanoAODv15.HTXS_stage1_1_cat_pTjet30GeV,
                nanoAODv15.HTXS_stage1_1_fine_cat_pTjet25GeV,
                nanoAODv15.HTXS_stage1_1_fine_cat_pTjet30GeV,
                nanoAODv15.HTXS_stage1_2_cat_pTjet25GeV,
                nanoAODv15.HTXS_stage1_2_cat_pTjet30GeV,
                nanoAODv15.HTXS_stage1_2_fine_cat_pTjet25GeV,
                nanoAODv15.HTXS_stage1_2_fine_cat_pTjet30GeV,
                nanoAODv15.HTXS_stage_0,
                nanoAODv15.HTXS_stage_1_pTjet25,
                nanoAODv15.HTXS_stage_1_pTjet30,
            ],
        )

    if measure_btag_efficiency:
        configuration.add_config_parameters("global", {"min_jet_pt_loose": 20,},)

        if sample not in ["data", "embedding", "embedding_mc"]:
            configuration.add_producers(
                scopes,
                [
                    jets.JetPtVec,
                    jets.JetEtaVec,
                    jets.JetHadFlavVec,
                    jets.JetBTagVec,
                ],
            )
            configuration.add_outputs(
                scopes,
                [
                    q.jet_pt_vec,
                    q.jet_eta_vec,
                    q.jet_hadronflavour_vec,
                    q.jet_btag_value_vec,
                ],
            )
 
    #########################
    # Add additional producers and SFs related to embedded samples
    #########################
    if sample == "embedding" or sample == "embedding_mc":
        configuration = setup_embedding(configuration, scopes, era)

    #########################
    # Import triggersetup and sf 
    #########################
    configuration = add_diTauTriggerSetup(configuration)

    #########################
    # Selection masks
    #########################
    # Run 3 only: the masks are built on the Run 3 producers, in particular on
    # the jet veto map, which is removed above for the nanoAODv9 based Run 2
    # configurations. The selections themselves have never been written down in
    # the form used here for Run 2.
    if int(era[:4]) >= 2022:
        configuration = add_selection(configuration, scopes, era, sample)

    #########################
    # Systematics shifts
    #########################
    configuration = add_Variations(configuration, sample, era)

    # the masks that are only consumed on nominal ntuples do not need a copy
    # per systematic shift, this has to run after the shifts were added
    if int(era[:4]) >= 2022:
        configuration = restrict_selection_shifts(configuration, scopes)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
