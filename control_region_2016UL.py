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

from .btag_variations import add_btagVariations
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

    # bjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_bjet_pt": 20,
            "max_bjet_eta": EraModifier(
                {
                    "2016preVFP": 2.5,
                    "2016postVFP": 2.5,
                    "2017": 2.5,
                    "2018": 2.5,
                }
            ),
            "btag_cut": EraModifier(  # medium
                {
                    "2016preVFP": 0.2598,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
                    "2016postVFP": 0.2489,  # taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                    "2017": 0.3040,
                    "2018": 0.2783,
                }
            ),
        },
    )

    # bjet scale factors
    configuration.add_config_parameters(
        scopes,
        {
            "btag_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/BTV/2016preVFP_UL/btagging.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/BTV/2016postVFP_UL/btagging.json.gz",
                    "2017": "data/jsonpog-integration/POG/BTV/2017_UL/btagging.json.gz",
                    "2018": "data/jsonpog-integration/POG/BTV/2018_UL/btagging.json.gz",
                }
            ),
            "btag_sf_variation": "central",
            "btag_corr_algo": "deepJet_shape",
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

    # # muon base selection:
    # configuration.add_config_parameters(
    #     "global",
    #     {
    #         "min_muon_pt": 10.0,
    #         "max_muon_eta": 2.4,
    #         "max_muon_dxy": 1.00,
    #         "max_muon_dz": 1.00,
    #         "muon_id": "Muon_looseId",
    #         "muon_iso_cut": 1.00,
    #     },
    # )
    # muon base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.4,
            "max_muon_dxy": 1.00,
            "max_muon_dz": 1.00,
            "muon_id": "Muon_mediumId",
            "muon_iso_cut": 1.00,
        },
    )
    # MuMu scope Muon selection
    configuration.add_config_parameters(
        ["mm"],
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            "min_muon_pt": 10.0,
            "max_muon_eta": 2.4,
            "muon_iso_cut": 1.00,
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
    # Muon scale factors configuration
    configuration.add_config_parameters(
        ["mm"],
        {
            "muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_Z.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",
            "muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            "muon_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP_UL",
                    "2016postVFP": "2016postVFP_UL",
                    "2017": "2017_UL",
                    "2018": "2018_UL",
                }
            ),
            "muon_sf_varation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
        },
    )
    # # muon trigger SF settings from embedding measurements NEW THING
    # configuration.add_config_parameters(
    #     ["mm"],
    #     {
    #         "singlemuon_trigger_sf_mc": [
    #             {
    #                 "flagname": "trg_wgt_single_mu24",
    #                 "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
    #                 "mc_muon_trg_extrapolation": 1.0,  # for nominal case
    #             },
    #             {
    #                 "flagname": "trg_wgt_single_mu27",
    #                 "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
    #                 "mc_muon_trg_extrapolation": 1.0,  # for nominal case
    #             },
    #             {
    #                 "flagname": "trg_wgt_single_mu24ormu27",
    #                 "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
    #                 "mc_muon_trg_extrapolation": 1.0,  # for nominal case
    #             },
    #         ]
    #     },
    
    # )

    # # # muon trigger SF settings from embedding measurements
    # configuration.add_config_parameters(
    #     [ "mm"],
    #     {
    #         "singlemuon_trigger_sf": [
    #             {
    #                 "flagname": "trg_wgt_single_mu24",
    #                 "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
    #                 "muon_trg_extrapolation": 1.0,
    #             },
    #             {
    #                 "flagname": "trg_wgt_single_mu27",
    #                 "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
    #                 "muon_trg_extrapolation": 1.0,
    #             },
    #             {
    #                 "flagname": "trg_wgt_single_mu24ormu27",
    #                 "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
    #                 "muon_trg_extrapolation": 1.0,
    #             },
    #         ]
    #     },
    # )


        # muon trigger SF settings from embedding measurements 2016
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemuon_trigger_sf_mc": [
                {
                    "flagname": "trg_wgt_single_mu22",
                    "mc_trigger_sf": "Trg_pt_eta_bins",
                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                },
                # {
                #     "flagname": "trg_wgt_single_mu27",
                #     "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                #     "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                # },
                # {
                #     "flagname": "trg_wgt_single_mu22ormu27",
                #     "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu22_pt_eta_bins",
                #     "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                # },
            ]
        },
    
    )

    # # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        [ "mm"],
        {
            "singlemuon_trigger_sf": [
                {
                    "flagname": "trg_wgt_single_mu22",
                    "embedding_trigger_sf": "Trg_pt_eta_bins",
                    "muon_trg_extrapolation": 1.0,
                },
                # {
                #     "flagname": "trg_wgt_single_mu27",
                #     "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                #     "muon_trg_extrapolation": 1.0,
                # },
                # {
                #     "flagname": "trg_wgt_single_mu24ormu27",
                #     "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu22_pt_eta_bins",
                #     "muon_trg_extrapolation": 1.0,
                # },
            ]
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
                        # {
                        #     "flagname": "trg_double_mu17_mu8_mass8",
                        #     "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                        #     "p1_ptcut": 17,
                        #     "p2_ptcut": 8,
                        #     "p1_etacut": 2.5,
                        #     "p2_etacut": 2.5,
                        #     "p1_filterbit": 4,
                        #     "p1_trigger_particle_id": 13,
                        #     "p2_filterbit": 4,
                        #     "p2_trigger_particle_id": 13,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
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
            "pairselection_min_dR": 0.001,
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
            muons.BaseMuons,
            met.MetBasics,

            jets.GoodJets,
            # jets.JetPtCorrection,
            jets.JetEnergyCorrection, 
            # jets.JetMassCorrection,

            jets.GoodBJets,



            # met.PFMetCorrections,
            # met.MetCorrections,

            event.npartons,
            
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
            triggers.MuMuGenerateSingleMuonTriggerFlags,   # new thing
            # triggers.MuMuGenerateDoubleMuonTriggerFlags,

            jets.JetCollection,
            jets.BasicJetQuantities,
            jets.BasicBJetQuantities,

            jets.BJetCollection,


            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,


            met.ApplyRecoilCorrectionsPFMet,
            met.PropagateJetsToPFMet,
            met.PropagateLeptonsToPFMet,

            
            met.ApplyRecoilCorrections,
            met.PropagateJetsToMet, 
            met.PropagateLeptonsToMet,

            pairquantities.DiTauPairMETQuantities,

  
            scalefactors.btagging_SF,

            electrons.ExtraElectronsVeto,


            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto, 



            
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
            # triggers.MuMuGenerateDoubleMuonTriggerFlags.output_group,

            # q.id_wgt_mu_1,
            # q.iso_wgt_mu_1,

            # q.id_wgt_mu_2,
            # q.iso_wgt_mu_2,

            q.mt_1,
            q.mt_2,
            q.pzetamissvis,

            q.btag_weight,   #check btag imports

            q.deltaR_ditaupair,

             q.muon_veto_flag,
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
    # configuration.add_modification_rule(
    #     "global",
    #     AppendProducer(
    #         producers=[event.npartons],
    #         samples=["dyjets", "wjets"],
    #     ),
    # )
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


    # new thing

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
        RemoveProducer(
            producers=[
                scalefactors.btagging_SF,
            ],
            samples=["data", "embedding", "embedding_mc"],
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

    # if sample == "embedding" or sample == "embedding_mc":
    #     setup_embedding(configuration, "mm")

    

    add_diTauTriggerSetup(configuration)  #new thing

    #########################
    # btagging scale factor shape variation
    #########################
    add_btagVariations(configuration, available_sample_types)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
