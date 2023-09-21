from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import muons as muons
from .producers import electrons as electrons
from .producers import photons as photons
from .producers import met as met
from .producers import jets as jets
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import embedding as emb
from .producers import tagandprobe as tagandprobe
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from .quantities import tagandprobe_output as tp_q
from code_generation.configuration import Configuration
from code_generation.rules import AppendProducer
from code_generation.modifiers import EraModifier, SampleModifier


def build_config(
    era: str,
    sample: str,
    channels: List[str],
    scopes: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_channels: List[str],
):
    if sample != "data" and sample != "embedding" and sample != "dyjets":
        print(
            "WARNING: TagandProbe measurement uses only data, dyjets and embedding samples"
        )
        exit()
    configuration = Configuration(
        era,
        sample,
        channels,
        scopes,
        available_sample_types,
        available_eras,
        available_channels,
    )
    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
            "min_ele_pt": 7.0,
            "max_ele_eta": 2.5,
            "min_photon_pt": 10.0,
            "max_photon_eta": 2.5,
            "met_filters": [
                "Flag_BadPFMuonFilter",
                "Flag_METFilters",
                "Flag_muonBadTrackFilter",
            ],
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
    ###############################
    # FSR Veto flags
    ###############################
    configuration.add_config_parameters(["mm", "ee"], {"fsr_delta_r": 0.4})
    ###### Channel Specifics ######
    # MuMu channel Muon selection
    configuration.add_config_parameters(
        ["mm"],
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
            "pairselection_min_dR": 0.5,
        },
    )
    # ElEl channel Electron selection
    configuration.add_config_parameters(
        ["ee"],
        {
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 1,
            "min_electron_pt": 7.0,
            "max_electron_eta": 2.5,
            "pairselection_min_dR": 0.5,
        },
    )
    # MuMu Channel Trigger setup
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemuon_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoMu27_1",
                            "flagname_2": "trg_IsoMu27_2",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 27.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                    ],
                    "2017": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoMu27_1",
                            "flagname_2": "trg_IsoMu27_2",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 27.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu24_1",
                            "flagname_2": "trg_IsoTkMu24_2",
                            "hlt_path": "HLT_IsoTkMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoMu22_1",
                            "flagname_2": "trg_IsoMu22_2",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu22_1",
                            "flagname_2": "trg_IsoTkMu22_2",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_IsoMu22_eta2p1_1",
                            "flagname_2": "trg_IsoMu22_eta2p1_2",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu22_eta2p1_1",
                            "flagname_2": "trg_IsoTkMu22_eta2p1_2",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu24_1",
                            "flagname_2": "trg_IsoTkMu24_2",
                            "hlt_path": "HLT_IsoTkMu24",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 24.0,
                        },
                        {
                            "flagname_1": "trg_IsoMu22_1",
                            "flagname_2": "trg_IsoMu22_2",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu22_1",
                            "flagname_2": "trg_IsoTkMu22_2",
                            "hlt_path": "HLT_IsoTkMu22",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            # HLT_Iso(Tk)Mu22_eta2p1 added in the menu in Run2016B-ver2
                            # Need to process a single file per job
                            "flagname_1": "trg_IsoMu22_eta2p1_1",
                            "flagname_2": "trg_IsoMu22_eta2p1_2",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_IsoTkMu22_eta2p1_1",
                            "flagname_2": "trg_IsoTkMu22_eta2p1_2",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 22.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17.0,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8.0,
                        },
                    ],
                }
            ),
            "singlemuon_trigger_bit": EraModifier(
                {
                    "2016preVFP": [
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_2",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": -1,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_2",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": -1,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_with_trg_ptcut_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_with_trg_ptcut_2",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_with_trg_ptcut_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_with_trg_ptcut_2",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_2",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": -1,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_2",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": -1,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_with_trg_ptcut_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu17_with_trg_ptcut_2",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 17,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_with_trg_ptcut_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_bit_12_Mu8_with_trg_ptcut_2",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 12,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.1,
                            "triggerobject_ptcut": 8,
                        },
                    ],
                }
            ),
        },
    )
    # ElEl Channel Trigger setup
    configuration.add_config_parameters(
        ["ee"],
        {
            "singleelectron_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_single_ele27_1",
                            "flagname_2": "trg_single_ele27_2",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 27.0,
                        },
                        {
                            "flagname_1": "trg_single_ele32_1",
                            "flagname_2": "trg_single_ele32_2",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 32.0,
                        },
                        {
                            "flagname_1": "trg_single_ele35_1",
                            "flagname_2": "trg_single_ele35_2",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 35.0,
                        },
                    ],
                    "2017": [
                        {
                            "flagname_1": "trg_single_ele27_1",
                            "flagname_2": "trg_single_ele27_2",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 27.0,
                        },
                        {
                            # Trigger not enabled over the full year.
                            # Should have been enabled starting in Run2017D
                            # Already included in the menu starting from the last three runs
                            # contained in Run2017C which leads to problems when processing multiple files
                            # The solution for now is to run Run2017C with a single input file
                            # per job
                            "flagname_1": "trg_single_ele32_1",
                            "flagname_2": "trg_single_ele32_2",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 32.0,
                        },
                        {
                            "flagname_1": "trg_single_ele32_fb_1",
                            "flagname_2": "trg_single_ele32_fb_2",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf_L1DoubleEG",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 10,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 32.0,
                        },
                        {
                            "flagname_1": "trg_single_ele35_1",
                            "flagname_2": "trg_single_ele35_2",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 35.0,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname_1": "trg_single_ele25_1",
                            "flagname_2": "trg_single_ele25_2",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 25.0,
                        },
                        {
                            "flagname_1": "trg_single_ele27_1",
                            "flagname_2": "trg_single_ele27_2",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 27.0,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname_1": "trg_single_ele25_1",
                            "flagname_2": "trg_single_ele25_2",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 25.0,
                        },
                        {
                            "flagname_1": "trg_single_ele27_1",
                            "flagname_2": "trg_single_ele27_2",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 20,
                            "etacut": 2.5,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                            "triggerobject_ptcut": 27.0,
                        },
                    ],
                }
            ),
        },
    )

    configuration.add_config_parameters(
        ["mm"],
        {
            "propagateLeptons": False,
            "propagateJets": False,
            "recoil_corrections_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                }
            ),
            "applyRecoilCorrections": False,
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,
        },
    )

    configuration.add_producers(
        "global",
        [
            event.Lumi,
            # event.MetFilter,
            electrons.RenameElectronPt,
            tagandprobe.BaseMuons,
            tagandprobe.BaseElectrons,
            tagandprobe.BasePhotons,
            met.MetBasics,
            jets.RenameJetsData,
        ],
    )
    configuration.add_producers(
        "mm",
        [
            tagandprobe.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            met.MetCorrections,
            met.PFMetCorrections,
            electrons.ExtraElectronsVeto,
            pairselection.ZMuMuPairSelection,
            pairselection.GoodMuMuPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.MuMuPairQuantities,
            tagandprobe.MuonIDs,
            tagandprobe.MuMuSingleMuonTriggerFlags_1,
            tagandprobe.MuMuSingleMuonTriggerFlags_2,
            tagandprobe.FSR_Veto,
            tagandprobe.MuMuSingleMuonTriggerBitFlags_1,
            tagandprobe.MuMuSingleMuonTriggerBitFlags_2,
            pairquantities.muon_nstations_1,
            pairquantities.muon_nstations_2,
            pairquantities.muon_ntrackerlayers_1,
            pairquantities.muon_ntrackerlayers_2,
            pairquantities.muon_pterr_1,
            pairquantities.muon_pterr_2,
        ],
    )

    configuration.add_producers(
        "ee",
        [
            tagandprobe.GoodElectrons,
            electrons.VetoElectrons,
            electrons.VetoSecondElectron,
            electrons.ExtraElectronsVeto,
            electrons.NumberOfGoodElectrons,
            pairselection.ZElElPairSelection,
            pairselection.GoodElElPairFilter,
            pairselection.LVEl1,
            pairselection.LVEl2,
            pairquantities.ElElPairQuantities,
            tagandprobe.ElectronIDs,
            tagandprobe.ElElSingleElectronTriggerFlags_1,
            tagandprobe.ElElSingleElectronTriggerFlags_2,
            tagandprobe.FSR_Veto,
        ],
    )

    configuration.add_outputs(
        ["mm"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            tp_q.id_medium_1,
            tp_q.id_medium_2,
            tp_q.id_loose_1,
            tp_q.id_loose_2,
            tp_q.id_tight_1,
            tp_q.id_tight_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.dz_1,
            q.dz_2,
            q.dxy_1,
            q.dxy_2,
            q.nmuons,
            q.is_global_1,
            q.is_global_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            tagandprobe.MuMuSingleMuonTriggerFlags_1.output_group,
            tagandprobe.MuMuSingleMuonTriggerFlags_2.output_group,
            tp_q.fsr_photon_veto_1,
            tp_q.fsr_photon_veto_2,
            tagandprobe.MuMuSingleMuonTriggerBitFlags_1.output_group,
            tagandprobe.MuMuSingleMuonTriggerBitFlags_2.output_group,
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
            q.muon_nstations_1,
            q.muon_nstations_2,
            q.muon_ntrackerlayers_1,
            q.muon_ntrackerlayers_2,
            q.muon_pterr_1,
            q.muon_pterr_2,
            nanoAOD.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,
        ],
    )

    configuration.add_outputs(
        ["ee"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.dz_1,
            q.dz_2,
            q.dxy_1,
            q.dxy_2,
            q.electron_veto_flag,
            tp_q.id_wp90_1,
            tp_q.id_wp90_2,
            tp_q.id_wp80_1,
            tp_q.id_wp80_2,
            q.nelectrons,
            tagandprobe.ElElSingleElectronTriggerFlags_1.output_group,
            tagandprobe.ElElSingleElectronTriggerFlags_2.output_group,
            tp_q.fsr_photon_veto_1,
            tp_q.fsr_photon_veto_2,
        ],
    )

    configuration.add_modification_rule(
        ["ee", "mm"],
        AppendProducer(
            producers=emb.EmbeddingQuantities, samples=["embedding", "embedding_mc"]
        ),
    )
    configuration.add_modification_rule(
        "global",
        AppendProducer(producers=event.JSONFilter, samples=["data", "embedding"]),
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
