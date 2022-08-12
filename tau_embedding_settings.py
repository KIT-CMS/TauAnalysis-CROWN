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
from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from code_generation.modifiers import EraModifier

measure_tauES = False


def setup_embedding(configuration: Configuration, scopes: List[str]):

    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=embedding.EmbeddingQuantities,
            samples=["embedding", "embedding_mc"],
        ),
    )

    # add embedding selection scalefactors
    configuration.add_config_parameters(
        scopes,
        {
            "embedding_selection_sf_file": "data/embedding/muon_2018UL.json.gz",
            "embedding_selection_trigger_sf": "m_sel_trg_kit_ratio",
            "embedding_selection_id_sf": "EmbID_pt_eta_bins",
        },
    )
    configuration.add_modification_rule(
        scopes,
        AppendProducer(
            producers=embedding.TauEmbeddingSelectionSF, samples=["embedding"]
        ),
    )
    # add muon scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm", "em"],
        {
            "embedding_muon_sf_file": "data/embedding/muon_2018UL.json.gz",
            "embedding_muon_id_sf": "ID_pt_eta_bins",
            "embedding_muon_iso_sf": "Iso_pt_eta_bins",
        },
    )
    # add electron scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["et", "ee", "em"],
        {
            "embedding_electron_sf_file": "data/embedding/electron_2018UL.json.gz",
            "embedding_electron_id_sf": "ID90_pt_eta_bins",
            "embedding_electron_iso_sf": "Iso_pt_eta_bins",
        },
    )
    # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mt"],
        {
            "singlemuon_trigger_sf": [
                {
                    "flagname": "trg_wgt_single_mu24",
                    "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                    "muon_trg_extrapolation": 1.0,
                },
                {
                    "flagname": "trg_wgt_single_mu27",
                    "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                    "muon_trg_extrapolation": 1.0,
                },
                {
                    "flagname": "trg_wgtsingle_mu24Ormu27",
                    "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                    "muon_trg_extrapolation": 1.0,
                },
            ]
        },
    )
    # electron trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["et"],
        {
            "singlelectron_trigger_sf": [
                {
                    "flagname": "trg_wgt_single_ele32",
                    "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                    "electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele35",
                    "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                    "electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele32orele35",
                    "embedding_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                    "electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele27orele32orele35",
                    "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                    "electron_trg_extrapolation": 1.0,  # for nominal case
                },
            ]
        },
    )
    configuration.add_modification_rule(
        ["mt"],
        AppendProducer(
            producers=[
                embedding.TauEmbeddingMuonIDSF_1,
                embedding.TauEmbeddingMuonIsoSF_1,
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
            ],
            samples=["embedding"],
        ),
    )
    configuration.add_modification_rule(
        ["mt"],
        AppendProducer(
            producers=[
                embedding.MTGenerateSingleMuonTriggerSF,
            ],
            samples=["embedding"],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        AppendProducer(
            producers=[
                embedding.ETGenerateSingleElectronTriggerSF,
            ],
            samples=["embedding"],
        ),
    )
    # remove some gen producers
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
        "global",
        RemoveProducer(
            producers=jets.JetEnergyCorrection, samples=["embedding", "embdding_mc"]
        ),
    )

    # For the tau related triggers, in embedding, we cannot use a trigger path directly, since the are not
    # correctly represented in embedded samples. Instead, it is possible to match to an earier filter
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
                    "2018": [
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
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 20,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 20,
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
                    "2016": [
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
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                    "2016": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 20,
                            "p1_etacut": 2.5,
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

    # use other trigger flags for embedding samples
    configuration.add_modification_rule(
        "tt",
        ReplaceProducer(
            producers=[
                triggers.TTGenerateDoubleTriggerFlags,
                triggers.TTGenerateDoubleTriggerFlagsEmbedding,
            ],
            samples="embedding",
        ),
    )
    configuration.add_outputs(
        "tt", triggers.TTGenerateDoubleTriggerFlagsEmbedding.output_group
    )

    # use other trigger flags for embedding samples
    configuration.add_modification_rule(
        "mt",
        ReplaceProducer(
            producers=[
                triggers.MTGenerateCrossTriggerFlags,
                triggers.MTGenerateCrossTriggerFlagsEmbedding,
            ],
            samples="embedding",
        ),
    )
    configuration.add_outputs(
        "mt", triggers.MTGenerateCrossTriggerFlagsEmbedding.output_group
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
                            "electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 1.02,
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
                            "electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "embedding_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "embedding_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "embedding_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "electron_trg_extrapolation": 0.98,
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
                ("mt"): {
                    "singlemuon_trigger_sf": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "muon_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 1.02,
                        },
                    ],
                }
            },
            producers={("mt"): embedding.MTGenerateSingleMuonTriggerSF},
        ),
        samples=["embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "embedding_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "muon_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "embedding_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "muon_trg_extrapolation": 0.98,
                        },
                    ],
                }
            },
            producers={("mt"): embedding.MTGenerateSingleMuonTriggerSF},
        ),
        samples=["embedding", "embedding_mc"],
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
                    taus.TauEnergyCorrection,
                    taus.TauEnergyCorrection_Embedding,
                ],
                samples=["embedding"],
            ),
        )
        tauESvariations = [-2.4 + 0.05 * i for i in range(0, 96)]
        for tauESvariation in tauESvariations:
            name = str(round(tauESvariation, 2)).replace("-", "minus").replace(".", "p")
            configuration.add_shift(
                SystematicShift(
                    name=f"EMBtauESshift_{name}",
                    shift_config={
                        ("mt"): {
                            "tau_ES_shift_DM0": 1.0
                            + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM1": 1.0
                            + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM10": 1.0
                            + (round(tauESvariation / 100.0, 5)),
                            "tau_ES_shift_DM11": 1.0
                            + (round(tauESvariation / 100.0, 5)),
                        }
                    },
                    producers={("mt"): taus.TauPtCorrection_byValue},
                ),
                samples=["embedding"],
            )
    else:
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
                    taus.TauEnergyCorrection,
                    taus.TauEnergyCorrection_Embedding,
                ],
                samples=["embedding"],
            ),
        )
        # default values until we have the correct measured values
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs1prong0pizeroUp",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM0": 1.012
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs1prong0pizeroDown",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM0": 0.988
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs1prong1pizeroUp",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM1": 1.012
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs1prong1pizeroDown",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM1": 0.988
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs3prong0pizeroUp",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM10": 1.012
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs3prong0pizeroDown",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM10": 0.988
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs3prong1pizeroUp",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM11": 1.012
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"tauEs3prong1pizeroDown",
                shift_config={
                    ("mt"): {
                        "tau_ES_shift_DM11": 0.988
                    }
                },
                producers={("mt"): taus.TauPtCorrection_byValue},
            ),
            samples=["embedding"],
        )


    return configuration
