from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List
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
from code_generation.systematics import SystematicShift
from code_generation.modifiers import EraModifier
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift
from .scripts.SpecialSetups import ES_ID_SCHEME
import numpy as np

measure_tauES = True
measure_eleES = False
measure_tauID = True


def setup_embedding(configuration: Configuration, scopes: List[str], era: str) -> Configuration:
    #####################
    # gen parameters #
    #####################

    configuration.add_config_parameters(
        ["mt"],
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

    ######################
    # scale factors #
    ######################

    # add embedding selection scalefactors
    configuration.add_config_parameters(
        scopes,
        {
            "embedding_selection_sf_file": EraModifier( ### ToDo: up to date?
                {
                    "2016preVFP": "data/embedding/embeddingselection_2016preVFPUL.json.gz",
                    "2016postVFP": "data/embedding/embeddingselection_2016postVFPUL.json.gz",
                    "2017": "data/embedding/embeddingselection_2017UL.json.gz",
                    "2018": "data/embedding/embeddingselection_2018UL.json.gz",
                    "2022preEE": "Missing or non existent",
                    "2022postEE": "Missing or non existent",
                    "2023preBPix": "Missing or non existent",
                    "2023postBPix": "Missing or non existent",
                    "2024": "Missing or non existent",
                    "2025": "Missing or non existent",
                }
            ),
            "embedding_selection_trigger_sf": "m_sel_trg_kit_ratio",
            "embedding_selection_id_sf": "EmbID_pt_eta_bins",
        },
    )

    # add muon scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "embedding_muon_sf_file": EraModifier(
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
            "embedding_muon_id_sf": "ID_pt_eta_bins",
            "embedding_muon_id_extrapolation": 1.0,
            "embedding_muon_iso_sf": "Iso_pt_eta_bins",
            "embedding_muon_iso_extrapolation": 1.0,
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
            "singlemuon_trigger_sf_emb": EraModifier(
                {
                    "2025": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2024": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023postBPix": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2023preBPix": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022postEE": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
                        },
                    ],
                    "2022preEE": [ # TODO: not implemented yet
                        {
                            "flagname": "Missing or non existent",
                            "embedding_trigger_sf": "Missing or non existent",
                            "trg_extrapolation": 1.0,  # for nominal case
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

    #########################
    # Trigger shifts
    #########################

    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt", "mm"): {
                    "singlemuon_trigger_sf_emb": EraModifier(
                        {
                            "2025": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2024": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023postBPix": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023preBPix": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022postEE": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022preEE": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
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
                ("mt"): embedding.MTGenerateSingleMuonTriggerSF,
                ("mm"): embedding.MTGenerateSingleMuonTriggerSF,
            },
        ),
        samples=["embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt", "mm"): {
                    "singlemuon_trigger_sf_emb": EraModifier(
                        {
                            "2025": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2024": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023postBPix": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2023preBPix": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022postEE": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
                                },
                            ],
                            "2022preEE": [ # TODO: not implemented yet
                                {
                                    "flagname": "",
                                    "embedding_trigger_sf": "",
                                    "trg_extrapolation": 1.0,  # for nominal case
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
                ("mt"): embedding.MTGenerateSingleMuonTriggerSF,
                ("mm"): embedding.MTGenerateSingleMuonTriggerSF,
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
        ["mt"],
        RemoveProducer(
            producers=[pairquantities.taujet_pt_2, genparticles.gen_taujet_pt_2],
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
        ["mm"],
        ReplaceProducer(
            producers=[genparticles.MuMuGenPair, genparticles.EmbeddingGenPair],
            samples=["embedding", "embedding_mc"],
        ),
    )

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
                embedding.MTGenerateSingleMuonTriggerSF,
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
                embedding.MTGenerateSingleMuonTriggerSF,
            ],
            samples=["embedding"],
        ),
    )

    ######################
    # Tau ID/ISO Variations
    ######################
    # ID
    configuration.add_shift(
         SystematicShift(
             name="muonIdSFUp",
             scopes=["mt", "mm"],
             shift_config={
                 ("mt"): {"embedding_muon_id_extrapolation": 1.02},
                 ("mm"): {"embedding_muon_id_extrapolation": 1.02},
             },
             producers={
                 ("mt"): [
                     embedding.TauEmbeddingMuonIDSF_1,
                 ],
                 ("mm"): [
                     embedding.TauEmbeddingMuonIDSF_1,
                     embedding.TauEmbeddingMuonIDSF_2,
                 ],
             },
         ),
         samples=["embedding", "embedding_mc"],
     )
    configuration.add_shift(
        SystematicShift(
            name="muonIdSFDown",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"embedding_muon_id_extrapolation": 0.98},
                ("mm"): {"embedding_muon_id_extrapolation": 0.98},
            },
            producers={
                ("mt"): [
                    embedding.TauEmbeddingMuonIDSF_1,
                ],
                ("mm"): [
                    embedding.TauEmbeddingMuonIDSF_1,
                    embedding.TauEmbeddingMuonIDSF_2,
                ],
            },
        ),
        samples=["embedding", "embedding_mc"],
    )
    # ISO
    configuration.add_shift(
         SystematicShift(
             name="muonIsoSFUp",
             scopes=["mt", "mm"],
             shift_config={
                 ("mt"): {"embedding_muon_iso_extrapolation": 1.02},
                 ("mm"): {"embedding_muon_iso_extrapolation": 1.02},
             },
             producers={
                 ("mt"): [
                     embedding.TauEmbeddingMuonIsoSF_1,
                 ],
                 ("mm"): [
                     embedding.TauEmbeddingMuonIsoSF_1,
                     embedding.TauEmbeddingMuonIsoSF_2,
                 ],
             },
         ),
         samples=["embedding", "embedding_mc"],
     )
    configuration.add_shift(
        SystematicShift(
            name="muonIsoSFDown",
            scopes=["mt", "mm"],
            shift_config={
                ("mt"): {"embedding_muon_iso_extrapolation": 0.98},
                ("mm"): {"embedding_muon_iso_extrapolation": 0.98},
            },
            producers={
                ("mt"): [
                    embedding.TauEmbeddingMuonIsoSF_1,
                ],
                ("mm"): [
                    embedding.TauEmbeddingMuonIsoSF_1,
                    embedding.TauEmbeddingMuonIsoSF_2,
                ],
            },
        ),
        samples=["embedding", "embedding_mc"],
    )
    
    ######################
    # Tau ID SFs
    ######################

    if not measure_tauID:
        
        # replace TauID producers for embedding samples
        configuration.add_config_parameters(
            ["mt"],
            {
                "tau_emb_sf_file": EraModifier(
                    {
                        # "2016preVFP": "data/embedding/tau_id_es_embedding2016preVFPUL.json.gz",
                        # "2016postVFP": "data/embedding/tau_id_es_embedding2016postVFPUL.json.gz",
                        # "2017": "data/embedding/tau_id_es_embedding2017UL.json.gz",
                        # "2018": "data/embedding/tau_id_es_embedding2018UL.json.gz",
                        "2016preVFP": "payloads/Tau_ID_ES/embedding/DeepTau2018v2p5_id_es_embedding2016preVFPUL.json.gz",
                        "2016postVFP": "payloads/Tau_ID_ES/embedding/DeepTau2018v2p5_id_es_embedding2016postVFPUL.json.gz",
                        "2017": "payloads/Tau_ID_ES/embedding/DeepTau2018v2p5_id_es_embedding2017UL.json.gz",
                        "2018": "payloads/Tau_ID_ES/embedding/DeepTau2018v2p5_id_es_embedding2018UL.json.gz",
                        "2022preEE": "",
                        "2022postEE": "",
                        "2023preBPix": "",
                        "2023postBPix": "",
                        "2024": "",
                        "2025": "",
                    }
                ),
                "tau_emb_ES_json_name": configuration.ES_ID_SCHEME.embedding.tau_emb_ES_json_name,
                "tau_emb_sf_vsjet_DM0": "nom",
                "tau_emb_sf_vsjet_DM0_20to40": "nom",
                "tau_emb_sf_vsjet_DM0_40toInf": "nom",
                "tau_emb_sf_vsjet_DM1": "nom",
                "tau_emb_sf_vsjet_DM1_20to40": "nom",
                "tau_emb_sf_vsjet_DM1_40toInf": "nom",
                "tau_emb_sf_vsjet_DM10": "nom",
                "tau_emb_sf_vsjet_DM10_20to40": "nom",
                "tau_emb_sf_vsjet_DM10_40toInf": "nom",
                "tau_emb_sf_vsjet_DM11": "nom",
                "tau_emb_sf_vsjet_DM11_20to40": "nom",
                "tau_emb_sf_vsjet_DM11_40toInf": "nom",
                "tau_emb_sf_vsjet_variation": "nom",
                "tau_emb_ES_WP": "Medium",  # Do also for more WP (vsjets) if needed !!!
                "tau_vsjet_vseleWP": "VVLoose",
                "tau_emb_id_sf_correctionset": "DeepTau2018v2p5VSjet",
                "tau_emb_vsjet_sf_dependence": configuration.ES_ID_SCHEME.embedding.tau_emb_vsjet_sf_dependence,
                "vsjet_tau_id_sf_embedding": [
                    {
                        "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(
                            wp=wp
                        ),
                        "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(
                            wp=wp
                        ),
                        "vsjet_tau_id_WP": "{wp}".format(wp=wp),
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
        configuration.add_modification_rule(
            ["mt"],
            ReplaceProducer(
                producers=[
                    configuration.ES_ID_SCHEME.mc.producerGroupES,
                    configuration.ES_ID_SCHEME.embedding.producerGroupES,
                ],
                samples=["embedding"],
            ),
        )
        configuration.add_modification_rule(
            ["mt"],
            AppendProducer(
                producers=[configuration.ES_ID_SCHEME.embedding.producerID],
                samples=["embedding"],
            ),
        )
        configuration.add_outputs(
            ["mt"],
            configuration.ES_ID_SCHEME.embedding.producerID.output_group,
        )

        # and add the variations for it
        # !!! The corresponding producer has to be picked in taus.py, either the pt inclusive or exclusive one. They are named the same !!!
        add_shift = get_adjusted_add_shift_SystematicShift(configuration)
        with defaults(shift_map={"Up": "up", "Down": "down"}):
            with defaults(scopes=("et", "mt")):
                with defaults(producers=[configuration.ES_ID_SCHEME.embedding.producerID]):
                    for dm in ["DM0", "DM1", "DM10", "DM11"]:
                        for var in configuration.ES_ID_SCHEME.pt_binning:
                            add_shift(name=f"vsJetTau{dm}{var}", shift_key=f"tau_emb_sf_vsjet_{dm}{var}")

            with defaults(scopes="tt", producers=[embedding.Tau_1_VsJetTauID_tt_SF, embedding.Tau_2_VsJetTauID_tt_SF]):
                for dm in [0, 1, 10, 11]:
                    for var in configuration.ES_ID_SCHEME.pt_binning:
                        add_shift(name=f"vsJetTauDM{dm}{var}", shift_key=f"tau_emb_sf_vsjet_tauDM{dm}{var}") 
    
    if measure_tauES:
        ###################
        # Tau ES variations for measurement
        # first exchange the producer to shift raw/uncorrected pt and set the initial variation to nominal
        configuration.add_modification_rule(
                ["mt"],
                ReplaceProducer(
                    producers=[
                        configuration.ES_ID_SCHEME.mc.producerGroupES,
                        taus.TauEnergyCorrection_Embedding
                    ],
                    samples=["embedding"],
                ),
            )
        configuration.add_config_parameters(
            "mt",
            {
                "shift_tau_ES_DM0_byValue": 1.0,
                "shift_tau_ES_DM1_byValue": 1.0,
                "shift_tau_ES_DM10_byValue": 1.0,
                "shift_tau_ES_DM11_byValue": 1.0,
            },
        )
        # tauESvariations = [x for x in np.arange(20.0, -20.0 - 0.1, -0.1).round(2).tolist() if x != 0 and x>=-20.0]
        # tauESvariations = [x for x in np.arange(20.0, -20.0 - 0.2, -0.2).round(2).tolist() if x < -12.0 or x > 8.0] # even 
        # tauESvariations = [x for x in np.arange(19.9, -20.0, -0.2).round(2).tolist()] # odd
        tauESvariations = []
        for tauESvariation in tauESvariations:
            name = str(round(tauESvariation, 2)).replace("-", "minus").replace(".", "p")
            configuration.add_shift(
                SystematicShift(
                    name=f"EMBtauESshift_{name}",
                    shift_config={
                        ("mt"): {
                            "shift_tau_ES_DM0_byValue": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "shift_tau_ES_DM1_byValue": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "shift_tau_ES_DM10_byValue": 1.0 + (round(tauESvariation / 100.0, 5)),
                            "shift_tau_ES_DM11_byValue": 1.0 + (round(tauESvariation / 100.0, 5)),
                        }
                    },
                    producers={("mt"): taus.TauPtCorrection_byValue},
                ),
                samples=["embedding"],
            )
    else:
        add_shift = get_adjusted_add_shift_SystematicShift(configuration)
        with defaults(shift_map={"Up": "up", "Down": "down"}):
            with defaults(scopes=("et", "mt", "tt")):
                with defaults(producers=[configuration.ES_ID_SCHEME.embedding.producerGroupES],
                              exclude_samples=["data"]):
                            for dm in ["DM0", "DM1", "DM10", "DM11"]:
                                for var in configuration.ES_ID_SCHEME.pt_binning:
                                    add_shift(name=f"tauEs{dm}{var}", shift_key=f"tau_ES_shift_{dm}{var}")

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
                    electrons.ElectronPtCorrectionMC,
                    electrons.ElectronPtCorrectionEmbedding,
                ],
                samples=["embedding"],
            ),
        )
        elefakeESvariations = [-1.5 + 0.05 * i for i in range(0, 51)]
        for elefakeESvariation in elefakeESvariations:
            name = (
                str(round(elefakeESvariation, 2))
                .replace("-", "minus")
                .replace(".", "p")
            )
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
                        "2022preEE": "Missing or non existent",
                        "2022postEE": "Missing or non existent",
                        "2023preBPix": "Missing or non existent",
                        "2023postBPix": "Missing or non existent",
                        "2024": "Missing or non existent",
                        "2025": "Missing or non existent",
                    }
                ),
                "ele_ES_json_name": "eleES",
                "ele_energyscale_barrel": "nom",
                "ele_energyscale_endcap": "nom",
            },
        )
        # not yet measured for run 3
        configuration.add_modification_rule(
            "global",
            ReplaceProducer(
                producers=[
                    electrons.ElectronPtCorrectionMC,
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
