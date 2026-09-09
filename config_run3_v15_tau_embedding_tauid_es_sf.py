from __future__ import annotations  # needed for type annotations in > python 3.7

from itertools import product

from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity

from .producers import (
    electrons,
    event,
    genparticles,
    jets,
    met,
    muons,
    pairquantities,
    pairselection,
    scalefactors,
    taus,
    triggers,
)
from .quantities import nanoAODv9, nanoAODv15
from .quantities import output as q
from code_generation.helpers import defaults
from code_generation.systematics import get_add_shift
from .scripts.SpecialSetups import ES_ID_SCHEME
from .tau_embedding_settings import setup_embedding
from .tau_triggersetup import add_diTauTriggerSetup
from .variations import add_Variations
from .tau_variations import add_tauVariations

def build_config(
    era: str,
    sample: str,
    scopes: list[str],
    shifts: list[str],
    available_sample_types: list[str],
    available_eras: list[str],
    available_scopes: list[str],
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
    
    run2_v15 = False #für Run3_v15
    # define Tau energy correction producers, id, and variation scheme
    configuration.ES_ID_SCHEME = ES_ID_SCHEME("dm_binned_run3")# wie in config_run3 , nicht mehr p_T getrennt 

    ###########################
    ####### Parameters ########
    ###########################

    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        ["global", "mt", "mm"],
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
    "Flag_BadPFMuonDzFilter",
    "Flag_eeBadScFilter",
    "Flag_ecalBadCalibFilter",
    "Flag_hfNoisyHitsFilter",
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
            
            # golden json
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                    "2024": "data/golden_json/Cert_Collisions2024_378981_386951_Golden.json",
                    "2025": "data/golden_json/Cert_Collisions2025_391658_398903_Golden.json", 
                    "2026": "data/golden_json/Cert_Collisions2026_401624_403937_golden.json",
                }
            ),
            
            # pileup corrections
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2016preVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2016postVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2017-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2018-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/puWeights_BCDEFGHI.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-05/puWeights_2025pp_Golden_Summer24_25ns_69200ub.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-25Prompt-Summer24-NanoAODv15/2026-06-05/puWeights_2025pp_Golden_Summer24_25ns_69200ub.json.gz",
                }
            ),
            "PU_reweighting_file_data": EraModifier(
                {
                    "2016preVFP": "Missing or non existent",
                    "2016postVFP": "Missing or non existent",
                    "2017": "Missing or non existent",
                    "2018": "Missing or non existent",
                    "2024": "data/root_pileup/Data_PileUp_2024_69p2.root",
                    "2025": "data/root_pileup/Data_PileUp_2025_69p2.root",
                    "2026": "data/root_pileup/Data_PileUp_2025_69p2.root",
                }
            ),
            "PU_reweighting_file_mc": EraModifier(
                {
                    "2016preVFP": "Missing or non existent",
                    "2016postVFP": "Missing or non existent",
                    "2017": "Missing or non existent",
                    "2018": "Missing or non existent",
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
                    "2024": "Collisions24_BCDEFGHI_goldenJSON",
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
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-06-18/muon_scalesmearing.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-06-18/muon_scalesmearing.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_scalesmearing.json.gz",
                    "2026": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-25Prompt-Summer24-NanoAODv15/2026-04-28/muon_scalesmearing.json.gz",
                },
                default='""',  # not used for Run 2
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
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2016preVFP-UL-NanoAODv15/2025-12-05/electronSS_EtDependent.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2016postVFP-UL-NanoAODv15/2025-12-05/electronSS_EtDependent.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2017-UL-NanoAODv15/2025-12-05/electronSS_EtDependent.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2018-UL-NanoAODv15/2025-12-05/electronSS_EtDependent.json.gz",
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
            "min_jet_pt_loose": 30, # This is used for JetPtCut producer for run2 now !!
            "min_jet_pt_tight": 50,
            "jet_eta_1": 2.5,
            "jet_eta_2": EraModifier(
                {
                    "2016preVFP": 4.7,
                    "2016postVFP": 4.7,
                    "2017": 4.7,
                    "2018": 4.7,
                    "2024": 3.0, #aus config_run3.py
                }
            ),
            "jet_eta_3": 4.7, # This is used for JetEtaCut producer for run2 now !!
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
                    "2024": 0.1272,  # UParT Medium, aus config_run3.py
                }
            ),
            # jet puID
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2024": 0,  # in der Run-3-Referenz nicht verwendet
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            # jet energy calibration 
            "jet_id_json": EraModifier(
                {
                    "2016preVFP": "Missing or non existent", ### ToDo: Is currently being prepared forRun2_v15 !
                    "2016postVFP": "Missing or non existent",
                    "2017": "Missing or non existent",
                    "2018": "Missing or non existent",
                    "2024": '"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetid.json.gz"',
                }
            ),
            "jet_collection_name":'"AK4PUPPI"', #only used for jet ID so not relevant for run 2
            "jet_jec_file": EraModifier( 
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv15/2026-06-05/jet_jerc.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jet_jerc.json.gz",
                }
            ),
            "jet_jer_master_seed": 42,
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": "Summer20UL16APVNanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL16APVNanoV15_V1_MC",
                    "2016postVFP": "Summer20UL16NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL16NanoV15_V1_MC",
                    "2017": "Summer20UL17NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL17NanoV15_V1_MC",
                    "2018": "Summer20UL18NanoV15_V1_DATA" if sample in ["embedding", "data"] else "Summer20UL18NanoV15_V1_MC",
                    "2024": "Summer24Prompt24_V2_DATA" if sample in ["embedding", "data"] else "Summer24Prompt24_V2_MC",
                }
            ),
            # jet resolution correction
            "jet_reapplyJES": True,
            "jet_jes_source": "nom",
            "jet_jes_shift": 0,
            "jet_jer_shift": "nom",  # or "up", "down"
            "jet_jer_tag": EraModifier( # TODO
                {
                    "2016preVFP": "Summer20UL16APV_JRV5_MC",
                    "2016postVFP": "Summer20UL16_JRV5_MC",
                    "2017": "Summer19UL17_JRV4_MC",
                    "2018": "Summer19UL18_JRV3_MC",
                    "2024": "Summer24Prompt24_JRV2_MC", #steht so in configrun3 aber eig 23..
                }
            ),
            "jet_jec_algo": EraModifier(
                {
                    "2016preVFP": "AK4PFPuppi",
                    "2016postVFP": "AK4PFPuppi",
                    "2017": "AK4PFPuppi",
                    "2018": "AK4PFPuppi",
                    "2024": "AK4PFPuppi",
                }
            ),
            # jet veto configuration
            "jet_veto_map_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv15/2026-04-13/jetvetomaps.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv15/2026-04-13/jetvetomaps.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv15/2026-04-13/jetvetomaps.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv15/2026-04-13/jetvetomaps.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/jetvetomaps.json.gz",
                }
            ),
            "jet_veto_map_name": EraModifier(
                {
                    "2016preVFP": "Summer19UL16_V1",
                    "2016postVFP": "Summer19UL16_V1",
                    "2017": "Summer19UL17_V1",
                    "2018": "Summer19UL18_V1",
                    "2024": "Summer24Prompt24_RunBCDEFGHI_V1",
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
        ["mt"],
        {
        "btag_eff_file": EraModifier(
                {
                    "2022preEE": f"payloads/btag_efficiencies/2022preEE/mt/btag_efficiency.json.gz",
                    "2022postEE": f"payloads/btag_efficiencies/2022postEE/mt/btag_efficiency.json.gz",
                    "2023preBPix": f"payloads/btag_efficiencies/2023preBPix/mt/btag_efficiency.json.gz",
                    "2023postBPix": f"payloads/btag_efficiencies/2023postBPix/mt/btag_efficiency.json.gz",
                    "2024": f"payloads/btag_efficiencies/2024/mt/btag_efficiency.json.gz",
                    "2025": f"payloads/btag_efficiencies/2025/mt/btag_efficiency.json.gz",
                    "2026": f"payloads/btag_efficiencies/2025/mt/btag_efficiency.json.gz",  # to update later on
                },
                default='""',  # Run 2
            ),
        },
    )
    configuration.add_config_parameters(
        scopes,
        {
            # bjet scale factors -> needs to be in scopes
            "btag_sf_file": EraModifier( # TODO Update run2 when btag efficiency is measured (needed for new SFs producers)
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
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                    "2024": "data/hleprare/RecoilCorrlib/Recoil_corrections_2024_v5.json.gz",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                    "2024": '""',
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
            "zpt_file": EraModifier( #Run3
                {
                    "2016preVFP": "data/zpt/htt_scalefactors_legacy_2017.root",  # ToDO: 2016 Broken. Measured in legacy, therefore the same for pre- and postVFP for now
                    "2016postVFP": "data/zpt/htt_scalefactors_legacy_2017.root",  # ToDO: Measured in legacy, therefore the same for pre- and postVFP for now
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                    "2024": "data/hleprare/DYweightCorrlib/DY_pTll_weights_2024_v5.json.gz",
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
            "DY_order": SampleModifier(
                {
                                    "dyjets_powheg": "NNLO",
                                    "ggh_htautau": "NNLO",#### wahrschienlich niht nötig
                                    "ggh_hbb": "NNLO",#####
                                    "vbf_htautau": "NNLO",####
                                    "vbf_hbb": "NNLO", #####
                                    "rem_htautau": "NNLO",#####
                                    "rem_hbb": "NNLO",####
                                    "wjets": "NNLO",#####
                                    }, 
                                default="NLO",
            ), #from GrASP it looks like the DY powheg samples are also NLO and not NNLO
            "zpt_variation": "nom",
            # STXS weights
            "ggHNNLOweightsRootfile": "data/htxs/NNLOPS_reweight.root",
            "ggH_generator": "powheg",
        },
    )
    ####################bis hier hin alles easy #################################
    ###### scope Specifics ######
    configuration.add_config_parameters(
        ["mt"],
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
                    "Loose": 4, 
                    "Medium": 5,
                    "Tight": 6,
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
                        # "VLoose": 1,
                        # "Loose": 2,
                        # "Medium": 3,
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
            # ID flags where scalefactors do not exist or are requiered withouth them
            # for Run 3 new TAU corrections, only the Medium wp sf are provided
            "vsjet_tau_id_wp_bit": [
                {
                    "vsjet_tau_id_WPbit": bit,
                    "tau_1_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_WPbit_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                }
                for wp, bit in dict(
                    # VVVLoose = 1,
                    VVLoose = 2,
                    VLoose = 3,
                    # Loose = 4, 
                    # Tight = 6,
                ).items()
            ],
            #scale factor
            "tau_sf_file": EraModifier( # ToDo: run2 is all from 2018, will be updated!
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016preVFP-UL-NanoAODv15/2025-11-27/tau.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016postVFP-UL-NanoAODv15/2025-11-27/tau.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2017-UL-NanoAODv15/2025-11-27/tau.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2018-UL-NanoAODv15/2025-11-27/tau.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-25/tau.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-25/tau.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23CSep23-Summer23-NanoAODv12/2025-12-25/tau.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-25/tau.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-25/tau.json.gz",
                    "2025": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-25/tau.json.gz",
                }
            ),
            "tau_id_vsele_DM0_barrel": "nom",
            "tau_id_vsele_DM1_barrel": "nom",
            "tau_id_vsele_DM10_barrel": "nom",
            "tau_id_vsele_DM11_barrel": "nom",
            "tau_id_vsele_DM0_endcap": "nom",
            "tau_id_vsele_DM1_endcap": "nom",
            "tau_id_vsele_DM10_endcap": "nom",
            "tau_id_vsele_DM11_endcap": "nom",
            "tau_id_vsmu_wheel1": "nom",
            "tau_id_vsmu_wheel2": "nom",
            "tau_id_vsmu_wheel3": "nom",
            "tau_id_vsmu_wheel4": "nom",
            "tau_id_vsmu_wheel5": "nom",
            #decay modes
            "tau_dms": "0,1,10,11",
            #energy scale
            "tau_ES_json_name": "tau_energy_scale",
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
            # fake ele
            "tau_elefake_es_DM0": "nom",
            "tau_elefake_es_DM1": "nom",
            "tau_elefake_es_DM10": "nom",
            "tau_elefake_es_DM11": "nom",
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_mufake_es": "nom",
            # new ES variation (will replace above):
            "tau_es_variation": "nom",
            # variations vs jet
            "tau_sf_vsjet_variation": "nom",
            # trigger SF
            "ditau_trigger_wp": "Medium",
            "ditau_trigger_corrtype": "sf",
            "ditau_trigger_syst": "nom",
        },
    )
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            # Muon scale factors configuration
            "muon_sf_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2016preVFP-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2016postVFP-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2017-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2018-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
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
            "muon_id_sf_variation": "nominal",# "systup"/"systdown" are up/down variations
            "muon_iso_sf_variation": "nominal",

            #run 2 scale factors from embedding framework
            "mc_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/muon_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/muon_2016postVFPUL.json.gz",
                    "2017": "data/embedding/muon_2017UL.json.gz",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                    "2022preEE": "Missing or non existent",
                    "2022postEE": "Missing or non existent",
                    "2023preBPix": "Missing or non existent",
                    "2023postBPix": "Missing or non existent",
                    "2024": "Missing or non existent",
                    "2025": "Missing or non existent",
                }
            ),
            "mc_muon_id_sf": "ID_pt_eta_bins",
            "mc_muon_iso_sf": "Iso_pt_eta_bins",
            "mc_muon_id_extrapolation": 1.0,  # for nominal case
            "mc_muon_iso_extrapolation": 1.0,  # for nominal case
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            # tau selection 
            "min_tau_pt": 20.0,
            "max_tau_eta": 2.5, ## DeepTau2p5 recommendation Run-2(UL) and Run-3
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
            "tau_sf_vsjet_DM0": "nom",
            "tau_sf_vsjet_DM0_20to40": "nom",
            "tau_sf_vsjet_DM0_40toInf": "nom",
            "tau_sf_vsjet_DM1": "nom",
            "tau_sf_vsjet_DM1_20to40": "nom",
            "tau_sf_vsjet_DM1_40toInf": "nom",
            "tau_sf_vsjet_DM10": "nom",
            "tau_sf_vsjet_DM10_20to40": "nom",
            "tau_sf_vsjet_DM10_40toInf": "nom",
            "tau_sf_vsjet_DM11": "nom",
            "tau_sf_vsjet_DM11_20to40": "nom",
            "tau_sf_vsjet_DM11_40toInf": "nom",
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
            # muon selection
            # here pt cut lower for additional objects, then the main one is managed by the trigger
            "muon_index_in_pair": 0,
            "min_muon_pt": 15.0,
            "max_muon_eta": 2.4,
            "max_muon_iso": 0.15,
            "second_muon_index_in_pair": 1,
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            # tau vs jet wp
            "tau_vsjet_vseleWP": "VVLoose",
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
            ["mt", "mm"],
            {
                "muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            }
        )
        configuration.add_config_parameters(
            ["mt"],
            {
                "max_muon_eta": 2.1,
                "max_muon_iso": 0.3,
            }
        )
        configuration.add_config_parameters(
            ["mm"],
            {
                "min_muon_pt": 20.0,
                "max_muon_eta": 2.1,
                "max_muon_iso": 0.15,
            }
        )

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
            # jets.JetIDCut, For run2_v15 in GoodJets_Run2_v15
            jets.JetEnergyCorrection_Run3,
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
            met.BuildRawMetVector,
            met.MetBasics_v15,
            met.MetMask,
            event.EvenOddIDFlag,
        ],
    )
    configuration.add_producers(
        scopes,
        [
            jets.JetCollection,
            jets.BasicJetQuantities,
            met.MetCorrections, 
            pairquantities.DiTauPairMETQuantities,
            genparticles.GenMatching,
        ],
    )
    configuration.add_producers(
        "mt",
        [
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            configuration.ES_ID_SCHEME.mc.producerID,
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
            scalefactors.TauID_SF,
            triggers.MTGenerateSingleMuonTriggerFlags,
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
            triggers.MuMuGenerateSingleMuonTriggerFlags,
        ],
    )
    
    ################################
    ######### Modifications ########
    ################################
    if era == "2024":
        # separate MC for 2024 and 2025 by even/odd event number
        configuration.add_modification_rule(
            "global",
            AppendProducer(
                producers=[event.EvenIDFilter],
                exclude_samples=["data", "embedding"],
            ),
        )
    if era == "2025":
        # temporary root pileup for data 2025 by tau fw group, 23/03/2026
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[event.PUweights, event.PUweights_root],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        # separate MC for 2024 and 2025 by even/odd event number
        configuration.add_modification_rule(
            "global",
            AppendProducer(
                producers=[event.OddIDFilter],
                exclude_samples=["data", "embedding"],
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
            samples=["data", "embedding", "embedding_mc"],
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
            samples=["data", "embedding", "embedding_mc", "diboson", "ggZZ"], # ToDO: scale weights to be provided in nanoAODs for VV at some point!!!
        ),
    )
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=event.JSONFilter, 
            samples=["data", "embedding", "embedding_mc"]),
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
            producers=[genparticles.GenMatching],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.GenJet, jets.GenJet_data],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    configuration.add_modification_rule(
            scopes,
            AppendProducer(
                producers=event.ZPtMassReweighting, samples=["dyjets", "electroweak_boson"]
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
        ["mt"],
        ReplaceProducer(
            producers=[configuration.ES_ID_SCHEME.mc.producerGroupES, taus.TauEnergyCorrection_data],
            samples=["data", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[
                scalefactors.TauID_SF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[
                configuration.ES_ID_SCHEME.mc.producerID,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[genparticles.MTGenDiTauPairQuantities],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        ["mm"],
        RemoveProducer(
            producers=[genparticles.MuMuGenPairQuantities],
            samples=["data"],
        ),
    )
    if int(era[:4]) < 2022:
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[jets.GoodJets, jets.GoodJets_Run2_v15],
                exclude_samples=["fake_era"],
            ),
        )
        configuration.add_modification_rule(
                scopes,
                ReplaceProducer(
                    producers=[met.MetCorrections, met.MetCorrections_Run2],
                    exclude_samples=["fake_era"],
                ),
        )
        configuration.add_modification_rule(
            ["mt"],
            AppendProducer(
                producers=[
                    scalefactors.MTGenerateSingleMuonTriggerSF_MC,
                    scalefactors.PrivateMuonIDSF_1_MC,
                    scalefactors.PrivateMuonIsoSF_1_MC,
                ],
                exclude_samples=["data", "embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["mm"],
            AppendProducer(
                producers=[
                    scalefactors.PrivateMuonIDSF_1_MC,
                    scalefactors.PrivateMuonIsoSF_1_MC,
                    scalefactors.PrivateMuonIDSF_2_MC,
                    scalefactors.PrivateMuonIsoSF_2_MC,
                    scalefactors.MTGenerateSingleMuonTriggerSF_MC,
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
            ] 
            + [p for scope in scopes for p in genparticles.GenMatching.get_outputs(scope)]
            + [p for scope in scopes for p in pairquantities.DiTauPairMETQuantities.get_outputs(scope)] + [
            q.dimuon_veto,
            q.dilepton_veto,
            q.dielectron_veto,
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
            configuration.ES_ID_SCHEME.mc.producerID.output_group,
            triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            q.extramuon_veto,
            q.dimuon_veto,
            q.extraelec_veto,
            ] + [p for p in scalefactors.TauID_SF.get_outputs("mt")
            ]
            ,
    )
    configuration.add_outputs(
        "mm",
        [
            q.nmuons,
            triggers.MuMuGenerateSingleMuonTriggerFlags.output_group,
            ] + [p for p in pairquantities.MuMuPairQuantities.get_outputs("mm")
            ]
            ,
    )

    configuration.add_outputs(
        "global",
        [
            p for p in met.MetBasics_v15.get_outputs("global")
        ],
    )
    configuration.add_outputs(
        "mt",
        [p for p in pairquantities.MTDiTauPairQuantities.get_outputs("mt")
        ],
    )
    
    add_shift = get_add_shift(configuration)

    #########################
    # Electron energy correction shifts
    #########################
    with defaults(
        scopes="global",
        shift_key="ele_es_variation",
        producers=[electrons.ElectronPtCorrectionMC],
        exclude_samples=["data", "embedding", "embedding_mc"],
    ):
        add_shift(name="eleEsReso", shift_map={"Up": "resolutionUp", "Down": "resolutionDown"})
        add_shift(name="eleEsScale", shift_map={"Up": "scaleUp", "Down": "scaleDown"})
    #########################
    # Muon id/iso sf shifts
    #########################

    configuration.add_shift(
        SystematicShift(
            name="muonIdSFUp",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"muon_id_sf_variation": "systup"},
                ("mm"): {"muon_id_sf_variation": "systup"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
                ("mm"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIdSFDown",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"muon_id_sf_variation": "systdown"},
                ("mm"): {"muon_id_sf_variation": "systdown"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
                ("mm"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIsoSFUp",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"muon_iso_sf_variation": "syst_up"},
                ("mm"): {"muon_iso_sf_variation": "syst_up"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
                ("mm"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIsoSFDown",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"muon_iso_sf_variation": "syst_down"},
                ("mm"): {"muon_iso_sf_variation": "syst_down"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
                ("mm"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )   
    
    #########################
    # MET Shifts
    #########################
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnUp",
            quantity_change={
                nanoAODv15.PuppiMET_pt: "PuppiMET_ptUnclusteredUp",
                nanoAODv15.PuppiMET_phi: "PuppiMET_phiUnclusteredUp",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnDown",
            quantity_change={
                nanoAODv15.PuppiMET_pt: "PuppiMET_ptUnclusteredDown",
                nanoAODv15.PuppiMET_phi: "PuppiMET_phiUnclusteredDown",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
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
            exclude_samples=["data", "embedding", "embedding_mc"],
            shift_key=["recoil_method", "recoil_variation"]
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
        exclude_samples=["data", "embedding", "embedding_mc"],
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

    #########################
    # Add additional producers and SFs related to embedded samples
    #########################
    if sample == "embedding" or sample == "embedding_mc":
        configuration = setup_embedding(configuration, scopes, era)

    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    configuration = add_tauVariations(configuration, sample, era, run2_v15)

    #########################
    # Import triggersetup and sf 
    #########################
    configuration = add_diTauTriggerSetup(configuration)

    #########################
    # Jet energy resolution and jet energy scale and btag uncertainties
    #########################
    # configuration = add_jetVariations(configuration, era, run2_v15)
    configuration = add_Variations(configuration, sample, era)
    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
