from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import genparticles as genparticles
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import triggers as triggers
from .producers import scalefactors as scalefactors
from .producers import tagandprobe as tagandprobe
from .producers import embedding as embedding
from .producers import electrons as electrons
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from .quantities import tagandprobe_output as qt
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import RemoveProducer, AppendProducer, ReplaceProducer
from code_generation.systematics import SystematicShift

from .tau_triggersetup import add_diTauTriggerSetup
from .producers import met as met
from code_generation.modifiers import EraModifier, SampleModifier
from .producers import jets as jets

# from .btag_variations import add_btagVariations
from .tau_embedding_settings import setup_embedding



def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):
    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    configuration.add_config_parameters(
        "global",
        {
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2016preVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2016postVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
                }
            ),
            "PU_reweighting_variation": "nominal",
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                }
            ),
            "met_filters": EraModifier(
                {
                    "2016preVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_eeBadScFilter",
                    ],
                    "2016postVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
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
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                }
            ),
        },
    )

    configuration.add_config_parameters(
        scopes,
        {
            "propagateLeptons": SampleModifier(
                {"data": False},
                default=True,
            ),
            "propagateJets": SampleModifier(
                {"data": False},
                default=True,
            ),
            "recoil_corrections_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",  # These are likely from Legacy data sets, therefore no difference in pre and postVFP
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                }
            ),
            "applyRecoilCorrections": SampleModifier(
                {
                    "wjets": False,
                    "dyjets": False,
                    "electroweak_boson": False,
                    "ggh_htautau": False,
                    "vbf_htautau": False,
                    "rem_htautau": False,
                    "ggh_hww": False,
                    "vbf_hww": False,
                    "rem_VH": False,
                },
                default=False,
            ),
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,
        },
    )
        # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 30,
            "max_jet_eta": 4.7,
            "jet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                }
            ),
            "jet_jes_tag_data": '""',
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                }
            ),
            "jet_jec_algo": '"AK4PFchs"',
        },
    )

    configuration.add_config_parameters(
        scopes,
        {
            "ggHNNLOweightsRootfile": "data/htxs/NNLOPS_reweight.root",
            "ggH_generator": "powheg",
            "zptmass_file": EraModifier(
                {
                    "2016preVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  # ToDO: Measured in legacy, therefore the same for pre- and postVFP for now
                    "2016postVFP": "data/zpt/htt_scalefactors_legacy_2016.root",  # ToDO: Measured in legacy, therefore the same for pre- and postVFP for now
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
        },
    )

    # muon base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.4,
            "max_muon_dxy": 0.045,
            "max_muon_dz": 0.2,
            "muon_id": "Muon_mediumId",
            "muon_iso_cut": 0.3,
        },
    )
    # MuMu scope Muon selection
    configuration.add_config_parameters(
        ["mm"],
        {
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 0.15,
            "second_muon_index_in_pair": 1,
            "muon_index_in_pair": 0,
        },
    )

    # add embedding selection scalefactors
    configuration.add_config_parameters(
        scopes,
        {
            "embedding_selection_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/muon_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/muon_2016postVFPUL.json.gz",
                    "2017": "data/embedding/muon_2017UL.json.gz",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                }
            ),
            "embedding_selection_trigger_sf": "m_sel_trg_kit_ratio",
            "embedding_selection_id_sf": "EmbID_pt_eta_bins",
        },
    )

    # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemuon_trigger_sf_mc": EraModifier(
                {
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
        # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemuon_trigger_sf": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "embedding_trigger_sf": "Trg_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "embedding_trigger_sf": "Trg_pt_eta_bins",
                            "muon_trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                }
            )
        },
    )

    

    # add muon scalefactors from embedding measurements
    configuration.add_config_parameters(
        [ "mm"],
        {
            "mc_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/muon_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/muon_2016postVFPUL.json.gz",
                    "2017": "data/embedding/muon_2017UL.json.gz",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                }
            ),
            "mc_muon_id_sf": "ID_pt_eta_bins",
            "mc_muon_iso_sf": "Iso_pt_eta_bins",
            "mc_muon_id_extrapolation": 1.0,  # for nominal case
            "mc_muon_iso_extrapolation": 1.0,  # for nominal case
        },
    )

    # add muon scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            "embedding_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/muon_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/muon_2016postVFPUL.json.gz",
                    "2017": "data/embedding/muon_2017UL.json.gz",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                }
            ),
            "embedding_muon_id_sf": "ID_pt_eta_bins",
            "embedding_muon_iso_sf": "Iso_pt_eta_bins",
        },
    )

    configuration.add_config_parameters(
        ["mm"],
        {
            "doublemuon_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_double_mu17_mu8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu17_mu8_mass8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_double_mu17_mu8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu17_mu8_mass8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_double_mu17_mu8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_double_mu17_mu8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "p1_ptcut": 17,
                            "p2_ptcut": 8,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.5,
                            "p1_filterbit": 4,
                            "p1_trigger_particle_id": 13,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    # electron base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_ele_pt": 10.0,
            "max_ele_eta": 2.5,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "max_ele_iso": 0.3,
            "ele_id": "Electron_mvaFall17V2noIso_WP90",
        },
    )

    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "deltaR_jet_veto": 0.5,
            "pairselection_min_dR": 0.5,  
        },
    )

    configuration.add_config_parameters(
        "global",
        {
            "ele_energyscale_barrel": 1.0,
            "ele_energyscale_endcap": 1.0,
        },
    )

    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            event.Lumi,
            event.npartons,
            event.MetFilter,

            muons.BaseMuons,
            met.MetBasics,

            jets.GoodJets,
            jets.JetEnergyCorrection, 
        

            event.PrefireWeight,

            electrons.ElectronPtCorrectionEmbedding,
            electrons.BaseElectrons,
    
        ],
    )
    configuration.add_producers(
        "mm",
        [
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            pairselection.MuMuPairSelection,
            pairselection.GoodMuMuPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairquantities.MuMuPairQuantities,
            tagandprobe.MuonID_Medium_1,
            tagandprobe.MuonID_Medium_2,
            genparticles.GenMatching,
            genparticles.MuMuGenPairQuantities,
            triggers.MuMuGenerateSingleMuonTriggerFlags,   
           

            jets.JetCollection,
            jets.BasicJetQuantities,


            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,


            met.ApplyRecoilCorrectionsPFMet,
            met.PropagateJetsToPFMet,
            met.PropagateLeptonsToPFMet,

            
            met.ApplyRecoilCorrections,
            met.PropagateJetsToMet, 
            met.PropagateLeptonsToMet,

            pairquantities.DiTauPairMETQuantities,


            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto, 

            electrons.ExtraElectronsVeto,


            
        ],
    )

    configuration.add_outputs(
        "mm",
        [
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_diboson,
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.puweight,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.q_1,
            q.q_2,
            q.dxy_1,
            q.dxy_2,
            q.dz_1,
            q.dz_2,
            q.iso_1,
            q.iso_2,
            q.m_vis,
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
            
            q.is_global_1,
            q.is_global_2,
            q.gen_match_1,
            q.gen_match_2,
            qt.id_medium_1,
            qt.id_medium_2,

            q.nmuons,

            
            q.npartons,
            q.genbosonmass,

            triggers.MuMuGenerateSingleMuonTriggerFlags.output_group,


            q.mt_1,
            q.mt_2,
            q.pzetamissvis,
  

            q.deltaR_ditaupair,
            q.pt_vis,

            q.muon_veto_flag,
            q.prefireweight,
           
            q.electron_veto_flag,

        ],
    )

    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            scopes,
            nanoAOD.genWeight,
        )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data", "embedding"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=[event.JSONFilter],
            samples=["data,embedding"],
        ),
    )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.npartons],
            samples=[
                sample
                for sample in available_sample_types
                if sample not in ["dyjets", "wjets", "electroweak_boson"]
            ],
        ),
    )
    configuration.add_modification_rule(
        "mm",
        RemoveProducer(
            producers=[
                genparticles.MuMuGenPairQuantities,
            ],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "mm",
        RemoveProducer(
            producers=[
                genparticles.GenMatching,
            ],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=embedding.TauEmbeddingSelectionSF, samples=["embedding"]
        ),
    )

    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.JetEnergyCorrection, jets.JetEnergyCorrection_data],
            samples="data",
        ),
    )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.JetEnergyCorrection, jets.RenameJetsData],
            samples=["embedding", "embedding_mc"],
        ),
    )

    configuration.add_modification_rule(
        ["mm"],
        AppendProducer(
            producers=[
                embedding.EmbeddingGenWeight,
            ],
            samples=["embedding"],
        )
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
            samples=[
                sample
                for sample in available_sample_types
                if sample not in ["data", "embedding", "embedding_mc"]
            ],
        ),
    )

    configuration.add_modification_rule(
        ["mm"],
        AppendProducer(
            producers=[
                embedding.TauEmbeddingMuonIDSF_1,
                embedding.TauEmbeddingMuonIsoSF_1,
                embedding.TauEmbeddingMuonIDSF_2,
                embedding.TauEmbeddingMuonIsoSF_2,
                embedding.MTGenerateSingleMuonTriggerSF,
            ],
            samples=["embedding"],
        ),
    )


    configuration.add_modification_rule(
        scopes,
        AppendProducer(producers=event.TopPtReweighting, samples="ttbar"),
    )

    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=event.ZPtMassReweighting, samples=["dyjets", "electroweak_boson"]
        ),
    )

    

    add_diTauTriggerSetup(configuration)  


    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()