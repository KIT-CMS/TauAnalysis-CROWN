from __future__ import annotations  # needed for type annotations in > python 3.7

from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from .producers import embedding as embedding
from .producers import scalefactors as scalefactors
from .producers import pairquantities as pairquantities
from .producers import genparticles as genparticles
from .producers import taus as taus
from .producers import jets as jets
from .producers import triggers as triggers
from .producers import electrons as electrons
from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift, get_add_shift
from code_generation.modifiers import EraModifier
from code_generation.helpers import defaults

measure_tauES = False
measure_eleES = False
measure_tauID = False


def setup_embedding(configuration: Configuration, scopes: List[str], era: str) -> Configuration:
    #####################
    # gen parameters #
    #####################

    configuration.add_config_parameters(
        ["mt", "et", "tt", "em"],
        {
            "truegen_mother_pdgid": 23,
            "truegen_daughter_1_pdgid": 15,
            "truegen_daugher_2_pdgid": 15,
        },
    )
    configuration.add_config_parameters(
        ["mm"],
        {
            "truegen_mother_pdgid": 23,
            "truegen_daughter_1_pdgid": 13,
            "truegen_daugher_2_pdgid": 13,
        },
    )
    configuration.add_config_parameters(
        ["ee"],
        {
            "truegen_mother_pdgid": 23,
            "truegen_daughter_1_pdgid": 11,
            "truegen_daugher_2_pdgid": 11,
        },
    )

    ######################
    # scale factors #
    ######################

    # add embedding selection scalefactors
    configuration.add_config_parameters(
        scopes,
        {
            "embedding_selection_sf_file": EraModifier(
                {
                    "2016preVFP": "data/embedding/embeddingselection_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/embeddingselection_2016postVFPUL.json.gz",
                    "2017": "data/embedding/embeddingselection_2017UL.json.gz",
                    "2018": "data/embedding/embeddingselection_2018UL.json.gz",
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '"data/embedding/embeddingselection_2024C.json.gz"',
                    "2025": '""',
                }
            ),
            "embedding_selection_trigger_sf": "m_sel_trg_kit_ratio",
            "embedding_selection_id_sf": "EmbID_pt_eta_bins",
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
                    "2022preEE": '""',
                    "2022postEE": '""',
                    "2023preBPix": '""',
                    "2023postBPix": '""',
                    "2024": '"data/embedding/muon_2024C.json.gz"',
                    "2025": '""',
                }
            ),
            "embedding_muon_id_sf": "ID_pt_eta_bins",
            "embedding_muon_iso_sf": "Iso_pt_eta_bins",
        },
    )
    # add electron scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            "embedding_electron_sf_file": EraModifier(
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
            "embedding_electron_id_sf": "ID90_pt_eta_bins",
            "embedding_electron_iso_sf": "Iso_pt_eta_bins",
        },
    )

    ############
    # TRIGGERS #
    ############

    # For the tau related triggers, in embedding, we cannot use a trigger path directly, since they are not
    # correctly represented in embedded samples. Instead, it is possible to match to an earlier filter
    # within the trigger sequence. In order to do this, we have to use another producer
    # and not the regular trigger producer. Also we have to match to special filter bits:
    # tt -> bit 20
    # mt -> bit 21
    configuration.add_config_parameters(
        ["tt"],
        {
            # here we do not match to the hlt path, only the filter
            "doubletau_trigger_embedding": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_double_tau30_mediumiso_pnet",
                            "p1_ptcut": 30,
                            "p2_ptcut": 30,
                            "p1_etacut": 2.3,
                            "p2_etacut": 2.3,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2024": [
                        {
                            "flagname": "trg_double_tau30_mediumiso_pnet",
                            "p1_ptcut": 30,
                            "p2_ptcut": 30,
                            "p1_etacut": 2.3,
                            "p2_etacut": 2.3,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # 13,  # TODO: check this
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # 13,  # TODO: check this
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # 13,  # TODO: check this
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # 13,  # TODO: check this
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # 13,  # TODO: check this
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # 13,  # TODO: check this
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "p1_ptcut": 35,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # 13,  # TODO: check this
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # 13,  # TODO: check this
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
                }
            ),
        },
    )

    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_cross_trigger_embedding": EraModifier(
                {
                    "2025": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2024": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2023postBPix": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2023preBPix": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2022postEE": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2022preEE": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2018": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 20,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
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
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p1_etacut": 2.1,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 25,
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
                            "p2_ptcut": 25,
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

    #####################
    # trigger scale factors #
    #####################

    # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "singlemuon_trigger_sf": EraModifier(
                {
                    "2025": [  # TODO: not implemented yet
                        {
                            "singlemuon_trigger_flagname": '""',
                            "singlemuon_trigger_flag": '""',
                            "singlemuon_trigger_sf_name": '""',
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2024": [
                        {  #  Run3 uses the single muon trigger from scalefactors.SingleMuTriggerSF
                            "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                            "singlemuon_trigger_flag": "trg_single_mu24",
                            "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_???",
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2023postBPix": [  # TODO: not implemented yet
                        {
                            "singlemuon_trigger_flagname": '""',
                            "singlemuon_trigger_flag": '""',
                            "singlemuon_trigger_sf_name": '""',
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2023preBPix": [  # TODO: not implemented yet
                        {
                            "singlemuon_trigger_flagname": '""',
                            "singlemuon_trigger_flag": '""',
                            "singlemuon_trigger_sf_name": '""',
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2022postEE": [  # TODO: not implemented yet
                        {
                            "singlemuon_trigger_flagname": '""',
                            "singlemuon_trigger_flag": '""',
                            "singlemuon_trigger_sf_name": '""',
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2022preEE": [  # TODO: not implemented yet
                        {
                            "singlemuon_trigger_flagname": '""',
                            "singlemuon_trigger_flag": '""',
                            "singlemuon_trigger_sf_name": '""',
                            "singlemuon_trigger_variation": "nominal",
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "embedding_trigger_sf": "Trg_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_wgt_single_mu22",
                            "embedding_trigger_sf": "Trg_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
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
            "singlelectron_trigger_sf": EraModifier(
                {
                    "2025": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2024": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023postBPix": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023preBPix": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022postEE": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022preEE": [  # TODO: not implemented yet
                        {
                            "flagname": '""',
                            "embedding_trigger_sf": '""',
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "embedding_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "embedding_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_wgt_single_ele25",
                            "embedding_trigger_sf": "Trg25_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        }
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_wgt_single_ele25",
                            "embedding_trigger_sf": "Trg25_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.0,  # for nominal case
                        }
                    ],
                }
            )
        },
    )
    # ditau trigger SF settings for embedding
    configuration.add_config_parameters(
        ["tt"],
        {
            "emb_ditau_trigger_wp": "Medium",
            "emb_ditau_trigger_type": "ditau",
            "emb_ditau_trigger_corrtype": "sf",
            "emb_ditau_trigger_syst": "nom",
            "emb_ditau_trigger_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "data/embedding/tau_trigger2018_UL.json.gz",
                    "2022preEE": "",
                    "2022postEE": "",
                    "2023preBPix": "",
                    "2023postBPix": "",
                    "2024": "",
                    "2025": "",
                }
            ),
        },
    )

    #########################
    # Trigger shifts
    #########################

    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFUp",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf": [
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "embedding_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "trg_extrapolation": 1.02,
                        },
                    ]
                }
            },
            producers={("et"): embedding.ETGenerateSingleElectronTriggerSF},
        ),
        samples=["embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFDown",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf": [
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "embedding_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "trg_extrapolation": 0.98,
                        },
                    ]
                }
            },
            producers={("et"): embedding.ETGenerateSingleElectronTriggerSF},
        ),
        samples=["embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt", "mm"): {
                    "singlemuon_trigger_sf": EraModifier(
                        {
                            "2025": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2024": [
                                {  #  Run3 uses the single muon trigger from scalefactors.SingleMuTriggerSF
                                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                                    "singlemuon_trigger_flag": "trg_single_mu24",
                                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_???",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2023postBPix": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2023preBPix": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2022postEE": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2022preEE": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systup",
                                },
                            ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "embedding_trigger_sf": "Trg_pt_eta_bins",
                                    "trg_extrapolation": 1.02,
                                },
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "embedding_trigger_sf": "Trg_pt_eta_bins",
                                    "trg_extrapolation": 1.02,  # for nominal case
                                },
                            ],
                        }
                    )
                }
            },
            producers={
                ("mt"): embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
                ("mm"): embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
            },
        ),
        samples=["embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt", "mm"): {
                    "singlemuon_trigger_sf": EraModifier(
                        {
                            "2025": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2024": [
                                {  #  Run3 uses the single muon trigger from scalefactors.SingleMuTriggerSF
                                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                                    "singlemuon_trigger_flag": "trg_single_mu24",
                                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_???",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2023postBPix": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2023preBPix": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2022postEE": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2022preEE": [  # TODO: not implemented yet
                                {
                                    "singlemuon_trigger_flagname": "",
                                    "singlemuon_trigger_flag": "",
                                    "singlemuon_trigger_sf_name": "",
                                    "singlemuon_trigger_variation": "systdown",
                                },
                            ],
                            "2018": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                            ],
                            "2017": [
                                {
                                    "flagname": "trg_wgt_single_mu24",
                                    "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                                {
                                    "flagname": "trg_wgt_single_mu24ormu27",
                                    "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                            ],
                            "2016postVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "embedding_trigger_sf": "Trg_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                            ],
                            "2016preVFP": [
                                {
                                    "flagname": "trg_wgt_single_mu22",
                                    "embedding_trigger_sf": "Trg_pt_eta_bins",
                                    "trg_extrapolation": 0.98,
                                },
                            ],
                        }
                    )
                }
            },
            producers={
                ("mt"): embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
                ("mm"): embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
            },
        ),
        samples=["embedding", "embedding_mc"],
    )

    #############
    # Producer modifications #
    #############

    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=[embedding.EmbeddingQuantities],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et", "mt", "tt"],
        RemoveProducer(
            producers=[pairquantities.taujet_pt_2, genparticles.gen_taujet_pt_2],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["tt"],
        RemoveProducer(
            producers=[pairquantities.taujet_pt_1, genparticles.gen_taujet_pt_1],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        ReplaceProducer(
            producers=[genparticles.MTGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        ReplaceProducer(
            producers=[genparticles.ETGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["tt"],
        ReplaceProducer(
            producers=[genparticles.TTGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["em"],
        ReplaceProducer(
            producers=[genparticles.EMGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["mm"],
        ReplaceProducer(
            producers=[genparticles.MuMuGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["ee"],
        ReplaceProducer(
            producers=[genparticles.ElElGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )

    if int(era[:4]) < 2022:
        configuration.add_modification_rule(
            scopes,
            AppendProducer(
                producers=[embedding.TauEmbeddingSelectionSF],
                samples=["embedding", "embedding_mc"],
            ),
        )
        configuration.add_modification_rule(
            ["mt"],
            AppendProducer(
                producers=[
                    embedding.TauEmbeddingMuonIDSF_1,
                    embedding.TauEmbeddingMuonIsoSF_1,
                    embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_modification_rule(
            ["et"],
            AppendProducer(
                producers=[
                    embedding.TauEmbeddingElectronIDSF_1,
                    embedding.TauEmbeddingElectronIsoSF_1,
                    embedding.ETGenerateSingleElectronTriggerSF,
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_modification_rule(
            ["tt"],
            AppendProducer(
                producers=[
                    embedding.TTGenerateDoubleTauTriggerSF_1,
                    embedding.TTGenerateDoubleTauTriggerSF_2,
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_modification_rule(
            ["em"],
            AppendProducer(
                producers=[
                    embedding.TauEmbeddingElectronIDSF_1,
                    embedding.TauEmbeddingElectronIsoSF_1,
                    embedding.TauEmbeddingMuonIDSF_2,
                    embedding.TauEmbeddingMuonIsoSF_2,
                ],
                samples=["embedding"],
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
                    embedding.TauEmbeddingSingleMuTriggerSF_Switch.get(era),
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_modification_rule(
            ["ee"],
            AppendProducer(
                producers=[
                    embedding.TauEmbeddingElectronIDSF_1,
                    embedding.TauEmbeddingElectronIsoSF_1,
                    embedding.TauEmbeddingElectronIDSF_2,
                    embedding.TauEmbeddingElectronIsoSF_2,
                    embedding.ETGenerateSingleElectronTriggerSF,
                ],
                samples=["embedding"],
            ),
        )
        # use other trigger flags for embedding samples
        configuration.add_modification_rule(
            "tt",
            ReplaceProducer(
                producers=[
                    triggers.TTGenerateDoubleTauTriggerFlags,
                    triggers.TTGenerateDoubleTauTriggerFlagsEmbedding,
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_outputs("tt", triggers.TTGenerateDoubleTauTriggerFlagsEmbedding.output_group)
        # use other trigger flags for embedding samples
        configuration.add_modification_rule(
            "mt",
            ReplaceProducer(
                producers=[
                    triggers.MTGenerateCrossTriggerFlags,
                    triggers.MTGenerateCrossTriggerFlagsEmbedding,
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_outputs("mt", triggers.MTGenerateCrossTriggerFlagsEmbedding.output_group)

    ######################
    # Tau ID SFs
    ######################

    if not measure_tauID:
        # replace TauID producers for embedding samples
        configuration.add_config_parameters(
            ["mt", "et"],
            {
                "tau_emb_sf_file": EraModifier(
                    {
                        "2016preVFP": "data/embedding/tau_id_es_embedding2016preVFPUL.json.gz",
                        "2016postVFP": "data/embedding/tau_id_es_embedding2016postVFPUL.json.gz",
                        "2017": "data/embedding/tau_id_es_embedding2017UL.json.gz",
                        "2018": "data/embedding/tau_id_es_embedding2018UL.json.gz",
                        "2022preEE": "",
                        "2022postEE": "",
                        "2023preBPix": "",
                        "2023postBPix": "",
                        "2024": "",
                        "2025": "",
                    }
                ),
                "tau_emb_ES_json_name": "tau_energy_scale",
                "tau_emb_sf_vsjet_1prong0pizero": "nom",
                "tau_emb_sf_vsjet_1prong0pizero20to40": "nom",
                "tau_emb_sf_vsjet_1prong0pizero40toInf": "nom",
                "tau_emb_sf_vsjet_1prong1pizero": "nom",
                "tau_emb_sf_vsjet_1prong1pizero20to40": "nom",
                "tau_emb_sf_vsjet_1prong1pizero40toInf": "nom",
                "tau_emb_sf_vsjet_3prong0pizero": "nom",
                "tau_emb_sf_vsjet_3prong0pizero20to40": "nom",
                "tau_emb_sf_vsjet_3prong0pizero40toInf": "nom",
                "tau_emb_sf_vsjet_3prong1pizero": "nom",
                "tau_emb_sf_vsjet_3prong1pizero20to40": "nom",
                "tau_emb_sf_vsjet_3prong1pizero40toInf": "nom",
                "tau_emb_sf_vsjet_variation": "nom",
                "tau_emb_ES_WP": "Tight",  # Do also for more WP (vsjets) if needed !!!
                "tau_emb_id_sf_correctionset": "DeepTau2017v2p1VSjet",
                "tau_emb_vsjet_sf_dependence": "pt",
                "vsjet_tau_id_sf_embedding": [
                    {
                        "tau_1_vsjet_sf_outputname": f"id_wgt_tau_vsJet_{wp}_1",
                        "tau_2_vsjet_sf_outputname": f"id_wgt_tau_vsJet_{wp}_2",
                        "vsjet_tau_id_WP": f"{wp}",
                    }
                    for wp in [
                        # "VVVLoose",
                        # "VVLoose",
                        # "VLoose",
                        # "Loose",
                        "Medium",
                        "Tight",
                        # "VTight",
                        # "VVTight",
                    ]
                ],
            },
        )
        # replace TauID producers for embedding samples
        configuration.add_config_parameters(
            ["tt"],
            {
                "tau_emb_sf_file": EraModifier(
                    {
                        "2016preVFP": "data/embedding/tau_2016preVFPUL.json.gz",
                        "2016postVFP": "data/embedding/tau_2016postVFPUL.json.gz",
                        "2017": "data/embedding/tau_2017UL.json.gz",
                        "2018": "data/jsonpog-integration/POG/TAU/2018_UL/tau_emb_es_2018UL.json.gz",
                        "2022preEE": '""',
                        "2022postEE": '""',
                        "2023preBPix": '""',
                        "2023postBPix": '""',
                        "2024": '""',
                        "2025": '""',
                    }
                ),
                "tau_emb_ES_json_name": "tau_energy_scale",
                "tau_emb_sf_vsjet_1prong0pizero": "nom",
                "tau_emb_sf_vsjet_1prong0pizero20to40": "nom",
                "tau_emb_sf_vsjet_1prong0pizero40toInf": "nom",
                "tau_emb_sf_vsjet_1prong1pizero": "nom",
                "tau_emb_sf_vsjet_1prong1pizero20to40": "nom",
                "tau_emb_sf_vsjet_1prong1pizero40toInf": "nom",
                "tau_emb_sf_vsjet_3prong0pizero": "nom",
                "tau_emb_sf_vsjet_3prong0pizero20to40": "nom",
                "tau_emb_sf_vsjet_3prong0pizero40toInf": "nom",
                "tau_emb_sf_vsjet_3prong1pizero": "nom",
                "tau_emb_sf_vsjet_3prong1pizero20to40": "nom",
                "tau_emb_sf_vsjet_3prong1pizero40toInf": "nom",
                "tau_emb_id_sf_correctionset": "DeepTau2017v2p1VSjet",
                "tau_emb_vsjet_sf_dependence": "pt",
                "vsjet_tau_id_sf_embedding": [
                    {
                        "tau_1_vsjet_sf_outputname": f"id_wgt_tau_vsJet_{wp}_1",
                        "tau_2_vsjet_sf_outputname": f"id_wgt_tau_vsJet_{wp}_2",
                        "vsjet_tau_id_WP": f"{wp}",
                    }
                    for wp in [
                        # "VVVLoose",
                        # "VVLoose",
                        # "VLoose",
                        # "Loose",
                        "Medium",
                        "Tight",
                        # "VTight",
                        # "VVTight",
                    ]
                ],
            },
        )
        if int(era[:4]) < 2022:
            configuration.add_modification_rule(
                ["et", "mt"],
                ReplaceProducer(
                    producers=[
                        scalefactors.TauID_SFSwitch.get(era),
                        embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned,
                    ],
                    samples=["embedding"],
                ),
            )
            configuration.add_modification_rule(
                "tt",
                ReplaceProducer(
                    producers=[
                        scalefactors.Tau_1_VsJetTauID_SF_Run2,
                        embedding.Tau_1_VsJetTauID_tt_SF,
                    ],
                    samples=["embedding"],
                ),
            )
            configuration.add_modification_rule(
                "tt",
                ReplaceProducer(
                    producers=[
                        scalefactors.TauID_SFSwitch.get(era),
                        embedding.Tau_2_VsJetTauID_tt_SF,
                    ],
                    samples=["embedding"],
                ),
            )
            configuration.add_outputs(
                ["et", "mt"],
                embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned.output_group,
            )
            configuration.add_outputs(
                "tt",
                [
                    embedding.Tau_1_VsJetTauID_tt_SF.output_group,
                    embedding.Tau_2_VsJetTauID_tt_SF.output_group,
                ],
            )

        # and add the variations for it
        # !!! The corresponding producer has to be picked in taus.py, either the pt inclusive or exclusive one. They are named the same !!!
        add_shift = get_add_shift(configuration)
        with defaults(shift_map={"Up": "up", "Down": "down"}):
            for var in ["20to40", "40toInf"]:
                for dm in ["1prong0pizero", "1prong1pizero", "3prong0pizero", "3prong1pizero"]:
                    add_shift(
                        name=f"vsJetTau{dm}{var}",
                        shift_key=f"tau_emb_sf_vsjet_{dm}{var}",
                        scopes=("et", "mt"),
                        producers=[embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned],
                    )
                    add_shift(
                        name=f"tauEs{dm}{var}",
                        shift_key=f"tau_ES_shift_{dm}{var}",
                        scopes=("et", "mt"),
                        producers=[taus.TauPtCorrection_emb_genTau_dm_pt_binned],
                    )

                for dm in [0, 1, 10, 11]:
                    add_shift(
                        name=f"vsJetTauDM{dm}{var}",
                        shift_key=f"tau_emb_sf_vsjet_tauDM{dm}{var}",
                        scopes="tt",
                        producers=[embedding.Tau_1_VsJetTauID_tt_SF, embedding.Tau_2_VsJetTauID_tt_SF],
                    )

    if measure_tauES:
        ###################
        # Tau ES variations for measurement
        # first set the initial variation to nominal

        configuration.add_config_parameters(
            "mt",
            {
                "tau_ES_shift_DM0": 1.0,
                "tau_ES_shift_DM1": 1.0,
                "tau_ES_shift_DM10": 1.0,
                "tau_ES_shift_DM11": 1.0,
            },
        )
        configuration.add_modification_rule(
            "mt",
            ReplaceProducer(
                producers=[
                    taus.TauEnergyCorrectionSwitch.get(era),  # taus.TauEnergyCorrection,
                    taus.TauEnergyCorrection_Embedding_ES_dm_pt_binned,  # taus.TauEnergyCorrection_Embedding,
                ],
                samples=["embedding"],
            ),
        )
        tauESvariations = [-8.0 + 0.1 * i for i in range(0, 121)]
        for tauESvariation in tauESvariations:
            name = str(round(tauESvariation, 2)).replace("-", "minus").replace(".", "p")
            configuration.add_shift(
                SystematicShift(
                    name=f"EMBtauESshift_{name}",
                    shift_config={
                        ("mt"): {
                            "tau_ES_shift_DM0": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM1": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM10": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM11": 1.0 + (round(tauESvariation / 100.0, 5)),
                        }
                    },
                    producers={("mt"): taus.TauPtCorrection_byValue},
                ),
                samples=["embedding"],
            )
    else:
        if int(era[:4]) < 2022:
            configuration.add_modification_rule(
                ["mt", "et", "tt"],
                ReplaceProducer(
                    producers=[
                        taus.TauEnergyCorrectionSwitch.get(era),
                        embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned,
                    ],
                    samples=["embedding"],
                ),
            )

    if measure_eleES:
        ###################
        # Ele fake ES variations for measurement
        # first set the initial variation to nominal
        configuration.add_config_parameters(
            "global",
            {
                "ele_energyscale_barrel": 1.0,
                "ele_energyscale_endcap": 1.0,
            },
        )
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[
                    electrons.ElectronPtCorrectionMCSwitch.get(era),
                    electrons.ElectronPtCorrectionEmbedding,
                ],
                samples=["embedding"],
            ),
        )
        elefakeESvariations = [-1.5 + 0.05 * i for i in range(51)]
        for elefakeESvariation in elefakeESvariations:
            name = str(round(elefakeESvariation, 2)).replace("-", "minus").replace(".", "p")
            configuration.add_shift(
                SystematicShift(
                    name=f"EMBelefakeESshift_{name}",
                    shift_config={
                        ("global"): {
                            "ele_energyscale_barrel": 1.0 + (round(elefakeESvariation / 100.0, 5)),
                            "ele_energyscale_endcap": 1.0 + (round(elefakeESvariation / 100.0, 5)),
                        }
                    },
                    producers={("global"): electrons.ElectronPtCorrectionEmbedding},
                ),
                samples=["embedding"],
            )
    else:
        # add embedding electron energy scale scalefactors
        configuration.add_config_parameters(
            "global",
            {
                "embedding_electron_es_sf_file": EraModifier(
                    {
                        "2016preVFP": "data/embedding/eleES_2016preVFPUL.json.gz",
                        "2016postVFP": "data/embedding/eleES_2016postVFPUL.json.gz",
                        "2017": "data/embedding/eleES_2017UL.json.gz",
                        "2018": "data/embedding/eleES_2018UL.json.gz",
                        "2022preEE": "",
                        "2022postEE": "",
                        "2023preBPix": "",
                        "2023postBPix": "",
                        "2024": "",
                        "2025": "",
                    }
                ),
                "ele_ES_json_name": "eleES",
                "ele_energyscale_barrel": "nom",
                "ele_energyscale_endcap": "nom",
            },
        )
        # not yet measured for run 3
        if int(era[:4]) < 2022:
            configuration.add_modification_rule(
                "global",
                ReplaceProducer(
                    producers=[
                        electrons.ElectronPtCorrectionMC_v9,
                        electrons.ElectronPtCorrectionEmbedding,
                    ],
                    samples=["embedding"],
                ),
            )
            configuration.add_shift(
                SystematicShift(
                    name="eleEsBarrelUp",
                    shift_config={("global"): {"ele_energyscale_barrel": "up"}},
                    producers={("global"): electrons.ElectronPtCorrectionEmbedding},
                ),
                samples=["embedding"],
            )
            configuration.add_shift(
                SystematicShift(
                    name="eleEsBarrelDown",
                    shift_config={
                        ("global"): {"ele_energyscale_barrel": "down"},
                    },
                    producers={("global"): electrons.ElectronPtCorrectionEmbedding},
                ),
                samples=["embedding"],
            )
            configuration.add_shift(
                SystematicShift(
                    name="eleEsEndcapUp",
                    shift_config={
                        ("global"): {
                            "ele_energyscale_endcap": "up",
                        }
                    },
                    producers={("global"): electrons.ElectronPtCorrectionEmbedding},
                ),
                samples=["embedding"],
            )
            configuration.add_shift(
                SystematicShift(
                    name="eleEsEndcapDown",
                    shift_config={
                        ("global"): {
                            "ele_energyscale_endcap": "down",
                        }
                    },
                    producers={("global"): electrons.ElectronPtCorrectionEmbedding},
                ),
                samples=["embedding"],
            )

    return configuration
