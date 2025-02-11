from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import electrons as electrons
from .producers import event as event
from .producers import genparticles as genparticles
from .producers import jets as jets
# from .producers import fatjets as fatjets
from .producers import met as met
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import pairquantities_bbpair as pairquantities_bbpair
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .producers import taus as taus
# from .producers import boostedtaus as boostedtaus
from .producers import triggers as triggers
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from .tau_triggersetup import add_diTauTriggerSetup
from .tau_variations import add_tauVariations
# from .boostedtau_variations import add_boostedtauVariations
from .jet_variations import add_jetVariations
from .tau_embedding_settings import setup_embedding
from .btag_variations import add_btagVariations
# from .jec_data import add_jetCorrectionData
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity


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

    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            # for LHE weights
            "muR": 1.0,
            "muF": 1.0,
            "PU_reweighting_file": EraModifier(
                {
                    "2016": "",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2016": "",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
                }
            ),
            "PU_reweighting_variation": "nominal",
            "golden_json_file": EraModifier(
                {
                    "2016": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                }
            ),
            "met_filters": EraModifier(
                {
                    "2016": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available. So implement ???
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
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
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available, missing in embedding
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                }
            ),
        },
    )
    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "tau_dms": "0,1,10,11",
            "tau_sf_file": EraModifier(
                {
                    "2016": "data/jsonpog-integration/POG/TAU/2016postVFP_UL/tau.json.gz",
                    "2017": "data/jsonpog-integration/POG/TAU/2017_UL/tau.json.gz",
                    "2018": "data/jsonpog-integration/POG/TAU/2018_UL/tau.json.gz",
                }
            ),
            "tau_ES_json_name": "tau_energy_scale",
            "tau_id_algorithm": "DeepTau2017v2p1",
            "tau_ES_shift_DM0": "nom",
            "tau_ES_shift_DM1": "nom",
            "tau_ES_shift_DM10": "nom",
            "tau_ES_shift_DM11": "nom",
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_mufake_es": "nom",
            # boosted taus
            "boostedtau_dms": "0,1,10",
            "boostedtau_sf_file": EraModifier(
                {
                    "2016": "data/jsonpog-integration/POG/TAU/2016_Legacy/tau.json.gz",
                    "2017": "data/jsonpog-integration/POG/TAU/2017_ReReco/tau.json.gz",
                    "2018": "data/jsonpog-integration/POG/TAU/2018_ReReco/tau.json.gz",
                }
            ),
            "boostedtau_ES_json_name": "tau_energy_scale",
            "boostedtau_id_algorithm": "MVAoldDM2017v2",
            "boostedtau_ES_shift_DM0": "nom",
            "boostedtau_ES_shift_DM1": "nom",
            "boostedtau_ES_shift_DM10": "nom",
            "boostedtau_ES_shift_DM11": "nom",
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
            "muon_iso_cut": 4.0,
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
            "max_ele_iso": 4.0,
            "ele_id": "Electron_mvaNoIso_WP90",
            "ele_es_era": EraModifier(
                {
                    "2016preVFP": '"2016preVFP"',
                    "2016postVFP": '"2016postVFP"',
                    "2017": '2017"',
                    "2018": '"2018"',
                }
            ),
            "ele_es_variation": "nom",
            "ele_es_file": EraModifier(
                {
                    "2016preVFP": '"data/electron_energy_scale/2016preVFP_UL/EGM_ScaleUnc.json.gz"',
                    "2016postVFP": '"data/electron_energy_scale/2016postVFP_UL/EGM_ScaleUnc.json.gz"',
                    "2017": '"data/electron_energy_scale/2017_UL/EGM_ScaleUnc.json.gz"',
                    "2018": '"data/electron_energy_scale/2018_UL/EGM_ScaleUnc.json.gz"',
                }
            ),
        },
    )
    # fatjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_fatjet_pt": 250,
            "max_fatjet_eta": 2.5,
            "fatjet_id": 6,
            "fatjet_reapplyJES": False,
            "fatjet_jes_sources": '{""}',
            "fatjet_jes_shift": 0,
            "fatjet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "fatjet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/fatJet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/fatJet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/fatJet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',  # using AK4 file for fatjets because it either was is just copied and the fatjet file has no merged uncertainty scheme
                }
            ),
            "fatjet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                }
            ),
            "fatjet_jes_tag_data": '""',
            "fatjet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                }
            ),
            "fatjet_jec_algo": '"AK4PFchs"',  # normally "AK8PFPuppi" would be used -> change to AK4 naming to get merged uncertainty scheme
        },
    )
    # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 30,
            "max_jet_eta": 2.5,
            "jet_id": 6,
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
                    "2016": 2.4,
                    "2017": 2.5,
                    "2018": 2.5,
                }
            ),
        },
    )
    configuration.add_config_parameters(
        (["global"] + scopes),
        {
            "btag_cut": EraModifier(  # medium
                {
                    "2016": 0.3093,
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
            "pNetXbb_sf_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/particleNet/pNet_Xbb_SF_2018.json.gz",
                }
            ),
            "pNetXbb_sf_variation": "nominal",
        },
    )
    # gen b pair for NMSSM analysis
    configuration.add_config_parameters(
        scopes,
        {
            "bb_truegen_mother_pdgid": SampleModifier(
                {"nmssm_Ybb": 35, "nmssm_Ytautau": 25}, default=-1
            ),
            "bb_truegen_daughter_1_pdgid": 5,
            "bb_truegen_daughter_2_pdgid": 5,
            "gen_bpair_match_deltaR": 0.2,
            "tautau_truegen_mother_pdgid": SampleModifier(
                {"nmssm_Ybb": 25, "nmssm_Ytautau": 35}, default=-1
            ),
            "tautau_truegen_daughter_1_pdgid": 15,
            "tautau_truegen_daughter_2_pdgid": 15,
            "gen_taupair_match_deltaR": 0.2,
        },
    )
    # leptonveto base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_dielectronveto_pt": 15.0,
            "dielectronveto_id": "Electron_cutBased",
            "dielectronveto_id_wp": 1,
            "min_dimuonveto_pt": 15.0,
            "dimuonveto_id": "Muon_looseId",
            "dileptonveto_dR": 0.15,
        },
    )
    ###### scope Specifics ######
    # MT/TT/ET scope tau ID flags and SFs
    configuration.add_config_parameters(
        ["mt", "tt", "et"],
        {
            "vsjet_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSjet",
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsjet_id_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                    "vsjet_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VVVLoose": 1,
                    # "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
            "vsele_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSe",
                    "tau_1_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_2".format(
                        wp=wp
                    ),
                    "vsele_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsele_id_outputname": "id_tau_vsEle_{wp}_1".format(wp=wp),
                    "tau_2_vsele_id_outputname": "id_tau_vsEle_{wp}_2".format(wp=wp),
                    "vsele_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    # "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
            "vsmu_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSmu",
                    "tau_1_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_2".format(wp=wp),
                    "vsmu_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsmu_id_outputname": "id_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_id_outputname": "id_tau_vsMu_{wp}_2".format(wp=wp),
                    "vsmu_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VLoose": 1,
                    # "Loose": 2,
                    # "Medium": 3,
                    "Tight": 4,
                }.items()
            ],
            "tau_sf_vsele_barrel": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsele_endcap": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsmu_wheel1": "nom",
            "tau_sf_vsmu_wheel2": "nom",
            "tau_sf_vsmu_wheel3": "nom",
            "tau_sf_vsmu_wheel4": "nom",
            "tau_sf_vsmu_wheel5": "nom",
            # boosted Tau ID flags
            "iso_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "MVAoldDM2017v2",
                    "boostedtau_1_iso_id_outputname": "id_boostedtau_iso_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_iso_sf_outputname": "id_wgt_boostedtau_iso_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_iso_id_outputname": "id_boostedtau_iso_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_iso_sf_outputname": "id_wgt_boostedtau_iso_{wp}_2".format(
                        wp=wp
                    ),
                    "iso_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "iso_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    # "VVLoose": 1,
                    "VLoose": 2,
                    "Loose": 3,
                    "Medium": 4,
                    # "Tight": 5,
                    # "VTight": 6,
                    # "VVTight": 7,
                }.items()
            ],
            "antiele_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "antiEleMVA6",
                    "boostedtau_1_antiele_id_outputname": "id_boostedtau_antiEle_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_antiele_sf_outputname": "id_wgt_boostedtau_antiEle_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_antiele_id_outputname": "id_boostedtau_antiEle_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_antiele_sf_outputname": "id_wgt_boostedtau_antiEle_{wp}_2".format(
                        wp=wp
                    ),
                    "antiele_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "antiele_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VLoose": 1,
                    "Loose": 2,
                    # "Medium": 3,
                    # "Tight": 4,
                    # "VTight": 5,
                }.items()
            ],
            "antimu_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "antiMu3",
                    "boostedtau_1_antimu_id_outputname": "id_boostedtau_antiMu_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_antimu_sf_outputname": "id_wgt_boostedtau_antiMu_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_antimu_id_outputname": "id_boostedtau_antiMu_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_antimu_sf_outputname": "id_wgt_boostedtau_antiMu_{wp}_2".format(
                        wp=wp
                    ),
                    "antimu_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "antimu_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    "Loose": 1,
                    # "Tight": 2,
                }.items()
            ],
            "boostedtau_sf_antiele_barrel": "nom",  # or "up"/"down" for up/down variation
            "boostedtau_sf_antiele_endcap": "nom",  # or "up"/"down" for up/down variation
            "boostedtau_sf_antimu_wheel1": "nom",
            "boostedtau_sf_antimu_wheel2": "nom",
            "boostedtau_sf_antimu_wheel3": "nom",
            "boostedtau_sf_antimu_wheel4": "nom",
            "boostedtau_sf_antimu_wheel5": "nom",
        },
    )
    configuration.add_config_parameters(
        ["mt", "tt"],
        {
            "vsjet_tau_id_sf": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSjet",
                    "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(
                        wp=wp
                    ),
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_vsjet_vseleWP": "VVLoose",
                }
                for wp, bit in {
                    # "VVVLoose": 1,
                    # "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
        },
    )
    configuration.add_config_parameters(
        ["et"],
        {
            "vsjet_tau_id_sf": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSjet",
                    "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(
                        wp=wp
                    ),
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_vsjet_vseleWP": "Tight",
                }
                for wp, bit in {
                    # "VVVLoose": 1,
                    # "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
        },
    )
    # MT / ET tau id sf variations
    configuration.add_config_parameters(
        ["mt", "et"],
        {
            "tau_sf_vsjet_tau30to35": "nom",
            "tau_sf_vsjet_tau35to40": "nom",
            "tau_sf_vsjet_tau40to500": "nom",
            "tau_sf_vsjet_tau500to1000": "nom",
            "tau_sf_vsjet_tau1000toinf": "nom",
            "tau_vsjet_sf_dependence": "pt",  # or "dm", "eta"
            "boostedtau_sf_iso_tau30to35": "nom",
            "boostedtau_sf_iso_tau35to40": "nom",
            "boostedtau_sf_iso_tau40to500": "nom",
            "boostedtau_sf_iso_tau500to1000": "nom",
            "boostedtau_sf_iso_tau1000toinf": "nom",
            "boostedtau_iso_sf_dependence": "pt",
        },
    )
    # TT tau id sf variations
    configuration.add_config_parameters(
        ["tt"],
        {
            "tau_sf_vsjet_tauDM0": "nom",
            "tau_sf_vsjet_tauDM1": "nom",
            "tau_sf_vsjet_tauDM10": "nom",
            "tau_sf_vsjet_tauDM11": "nom",
            "tau_vsjet_sf_dependence": "dm",  # or "dm", "eta"
            "boostedtau_sf_iso_tauDM0": "nom",
            "boostedtau_sf_iso_tauDM1": "nom",
            "boostedtau_sf_iso_tauDM10": "nom",
            "boostedtau_sf_iso_tauDM11": "nom",
            "boostedtau_iso_sf_dependence": "dm",  # or "dm", "eta"
        },
    )

    # MT / ET tau selection
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "min_tau_pt": 20.0,
            "max_tau_eta": 2.3,
            "max_tau_dz": 0.2,
            "vsjet_tau_id_bit": 1,
            "vsele_tau_id_bit": 2,
            "vsmu_tau_id_bit": 1,
            "min_boostedtau_pt": 30.0,
            "max_boostedtau_eta": 2.3,
            # "iso_boostedtau_id_bit": 1,
            # "antiele_boostedtau_id_bit": 1,
            # "antimu_boostedtau_id_bit": 1,
            "boosted_pairselection_min_dR": 0.1,
            "boosted_pairselection_max_dR": 5.0,
        },
    )
    # TT tau selection:
    configuration.add_config_parameters(
        ["tt"],
        {
            "min_tau_pt": 35.0,
            "max_tau_eta": 2.1,
            "max_tau_dz": 0.2,
            "vsjet_tau_id_bit": 1,
            "vsele_tau_id_bit": 2,
            "vsmu_tau_id_bit": 1,
            "min_boostedtau_pt": 30.0,
            "max_boostedtau_eta": 2.3,
            # "iso_boostedtau_id_bit": 2,
            # "antiele_boostedtau_id_bit": 2,
            # "antimu_boostedtau_id_bit": 1,
            "boosted_pairselection_min_dR": 0.1,
            "boosted_pairselection_max_dR": 5.0,
        },
    )

    # MT/MM scope Muon selection
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "muon_index_in_pair": 0,
            "min_muon_pt": 20.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 5.0,
        },
    )

    # Muon scale factors configuration
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "muon_sf_file": EraModifier(
                {
                    "2016preBFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_Z.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                }
            ),
            "muon_reco_sf_name": "NUM_TrackerMuons_DEN_genTracks",
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",
            "muon_iso_sf_name": "NUM_LooseRelIso_DEN_MediumID",
            "muon_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP_UL",
                    "2016postVFP": "2016postVFP_UL",
                    "2017": "2017_UL",
                    "2018": "2018_UL",
                }
            ),
            "muon_reco_sf_variation": "nominal",  # "nominal" is nominal, "systup"/"systdown" are up/down variations
            "muon_id_sf_variation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
            "muon_iso_sf_variation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
        },
    )
    # electron scale factors configuration
    configuration.add_config_parameters(
        ["et"],
        {
            "ele_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/EGM/2016preVFP_UL/electron.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/EGM/2016postVFP_UL/electron.json.gz",
                    "2017": "data/jsonpog-integration/POG/EGM/2017_UL/electron.json.gz",
                    "2018": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
                }
            ),
            "ele_id_sf_name": "UL-Electron-ID-SF",
            "ele_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP",
                    "2016postVFP": "2016postVFP",
                    "2017": "2017",
                    "2018": "2018",
                }
            ),
            "ele_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
        },
    )
    # ET scope electron selection
    configuration.add_config_parameters(
        ["et"],
        {
            "electron_index_in_pair": 0,
            "min_electron_pt": 25.0,
            "max_electron_eta": 2.1,
            "electron_iso_cut": 5.0,
        },
    )
    configuration.add_config_parameters(
        ["mm"],
        {
            "min_muon_pt": 20.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 0.15,
            "second_muon_index_in_pair": 1,
        },
    )

    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "deltaR_jet_veto": 0.4,
            "deltaR_fatjet_veto": 0.6,
            "pairselection_min_dR": 0.4,
            "bb_pairselection_min_dR": 0.0,
            # "fatjet_bpair_matching_max_dR": 0.2,
        },
    )
    ## all scopes MET selection
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
                    "2016": "data/recoil_corrections/Type1_PuppiMET_2016.root",
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016": "data/recoil_corrections/PuppiMETSys_2016.root",
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                }
            ),
            "applyRecoilCorrections": SampleModifier(
                {
                    "ttbar": False,
                    "singletop": False,
                    "diboson": False,
                    "data": False,
                    "embedding": False,
                    "embedding_mc": False,
                },
                default=True,
            ),
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,
        },
    )

    configuration.add_config_parameters(
        scopes,
        {
            # "ggHNNLOweightsRootfile": "data/htxs/NNLOPS_reweight.root",
            # "ggH_generator": "powheg",
            "zptmass_file": EraModifier(
                {
                    "2016": "data/zpt/htt_scalefactors_legacy_2016.root",
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
        },
    )

    # add muon scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "mc_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "data/embedding/muon_2018UL.json.gz",
                }
            ),
            "mc_muon_id_sf": "ID_pt_eta_bins",
            "mc_muon_iso_sf": "Iso_pt_eta_bins",
            "mc_muon_id_extrapolation": 1.0,  # for nominal case
            "mc_muon_iso_extrapolation": 1.0,  # for nominal case
        },
    )
    # add electron scalefactors from embedding measurements
    configuration.add_config_parameters(
        ["et"],
        {
            "mc_electron_sf_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "data/embedding/electron_2018UL.json.gz",
                }
            ),
            "mc_electron_id_sf": "ID90_pt_eta_bins",
            "mc_electron_iso_sf": "Iso_pt_eta_bins",
            "mc_electron_id_extrapolation": 1.0,  # for nominal case
            "mc_electron_iso_extrapolation": 1.0,  # for nominal case
        },
    )
    # muon trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
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
            ]
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "boosted_singlemuon_trigger_sf_mc": [
                {
                    "flagname": "trg_wgt_single_mu24_boosted",
                    "muon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                    "muon_trg_sf_variation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
                },
                {
                    "flagname": "trg_wgt_single_mu50_boosted",
                    "muon_trigger_sf_name": "NUM_Mu50_or_OldMu100_or_TkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose",
                    "muon_trg_sf_variation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
                },
            ]
        },
    )
    # electron trigger SF settings from embedding measurements
    configuration.add_config_parameters(
        ["et"],
        {
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
    configuration.add_config_parameters(
        ["et"],
        {
            "ele_trg_sf_file": EraModifier(
                {
                    "2016preVFP": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL16preVFP.json.gz",
                    "2016postVFP": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL16postVFP.json.gz",
                    "2017": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL17.json.gz",
                    "2018": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL18.json.gz",
                }
            ),
            "boosted_singleelectron_trigger_sf_mc": [
                {
                    "flagname": "trg_wgt_single_ele_boosted",
                    "ele_trg_sf_name": "ElectronTriggerSF",
                    "ele_trg_sf_variation": "nominal",  # "nominal" is nominal, "up"/"down" are up/down variations
                },
            ]
        },
    )
    # ditau trigger SF settings for embedding
    configuration.add_config_parameters(
        ["tt"],
        {
            "ditau_trigger_wp": "Medium",
            "ditau_trigger_type": "ditau",
            "ditau_trigger_corrtype": "sf",
            "ditau_trigger_syst": "nom",
        },
    )
    # fatjet trigger settings
    configuration.add_config_parameters(
        ["tt"],
        {
            "fatjet_trigger_sf_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fatjet_trigger/scale_factor__AK8PFJet400_TrimMass30__singlemuon.json",
                }
            ),
            "fatjet_trigger_sf_name": "SF_AK8PFJet400_TrimMass30",
            "fatjet_trigger_sf_syst": "nominal",
        },
    )

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
            muons.BaseMuons,
            electrons.ElectronPtCorrectionMC,
            # electrons.RenameElectronPt,
            electrons.BaseElectrons,
            # fatjets.FatJetEnergyCorrection,
            # fatjets.GoodFatJets,
            jets.JetEnergyCorrection,
            jets.BJetEnergyCorrection,
            jets.GoodJets,
            jets.GoodBJets,
            event.DiLeptonVeto,
            met.MetBasics,
        ],
    )
    ## add prefiring
    if era != "2018":
        configuration.add_producers(
            "global",
            [
                event.PrefireWeight,
            ],
        )
    # common
    configuration.add_producers(
        scopes,
        [
            # fatjets.FatJetCollection,
            # fatjets.FatJetCollection_boosted,
            # fatjets.FatJetCollectionWithoutVeto,
            # fatjets.BasicFatJetQuantities,
            jets.JetCollection,
            jets.BasicJetQuantities,
            jets.BJetCollection,
            jets.BasicBJetQuantities,
            # jets.JetCollection_boosted,
            # jets.BJetCollection_boosted,
            pairselection.BBPairSelection,
            # pairselection.BBPairSelection_boosted,
            # pairselection.GoodBBPairFilter,
            pairselection.LVbjet1,
            pairselection.LVbjet2,
            # pairselection.LVbjet1_boosted,
            # pairselection.LVbjet2_boosted,
            pairquantities_bbpair.DiBjetPairQuantities,
            # pairquantities_bbpair.DiBjetPairQuantities_boosted,
            genparticles.GenDiBjetPairQuantities,
            # fatjets.FindFatjetMatchingBjet,
            # fatjets.BasicMatchedFatJetQuantities,
            # fatjets.FindXbbFatjet,
            # fatjets.BasicXbbFatJetQuantities,
            # fatjets.FindXbbFatjet_boosted,
            # fatjets.BasicXbbFatJetQuantities_boosted,
            # fatjets.LeadingFatJetQuantities,
            scalefactors.btagging_SF,
            # scalefactors.btagging_SF_boosted,
            # scalefactors.Xbb_tagging_SF,
            # scalefactors.Xbb_tagging_SF_boosted,
            met.MetCorrections,
            met.PFMetCorrections,
            # met.MetCorrections_boosted,
            # met.PFMetCorrections_boosted,
            pairquantities.DiTauPairMETQuantities,
            genparticles.GenMatching,
            # genparticles.GenMatchingBoosted,
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
        "mt",
        [
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            # muons.VetoMuons_boosted,
            # muons.BoostedExtraMuonsVeto,
            taus.TauEnergyCorrection,
            # taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            # boostedtaus.boostedTauEnergyCorrection,
            # boostedtaus.GoodBoostedTaus,
            # boostedtaus.NumberOfGoodBoostedTaus,
            electrons.ExtraElectronsVeto,
            pairselection.MTPairSelection,
            # pairselection.boostedMTPairSelection,
            pairselection.GoodMTPairFilter,
            pairselection.LVMu1,
            pairselection.LVTau2,
            # pairselection.additionalBoostedTau,
            # pairselection.LVaddBoostedTau,
            # boostedtaus.boostedLVMu1,
            # boostedtaus.boostedLVTau2,
            # boostedtaus.boostedLVMu1_uncorrected,
            # boostedtaus.boostedLVTau2_uncorrected,
            pairselection.LVMu1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.MTDiTauPairQuantities,
            # boostedtaus.boostedMTDiTauPairQuantities,
            genparticles.MTGenDiTauPairQuantities,
            scalefactors.Tau_2_VsJetTauID_lt_SF,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            # scalefactors.Tau_2_oldIsoTauID_lt_SF,
            # scalefactors.Tau_2_antiEleTauID_SF,
            # scalefactors.Tau_2_antiMuTauID_SF,
            triggers.MTGenerateSingleMuonTriggerFlags,
            # triggers.BoostedMTGenerateSingleMuonTriggerFlags,
            # triggers.MTGenerateCrossTriggerFlags,
            # triggers.GenerateSingleTrailingTauTriggerFlags,
        ],
    )
    configuration.add_producers(
        "et",
        [
            electrons.GoodElectrons,
            taus.TauEnergyCorrection,
            # taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            # boostedtaus.boostedTauEnergyCorrection,
            # boostedtaus.GoodBoostedTaus,
            # boostedtaus.NumberOfGoodBoostedTaus,
            electrons.NumberOfGoodElectrons,
            electrons.VetoElectrons,
            # electrons.VetoElectrons_boosted,
            electrons.ExtraElectronsVeto,
            # electrons.BoostedExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            pairselection.ETPairSelection,
            # pairselection.boostedETPairSelection,
            pairselection.GoodETPairFilter,
            pairselection.LVEl1,
            pairselection.LVTau2,
            # pairselection.additionalBoostedTau,
            # pairselection.LVaddBoostedTau,
            # boostedtaus.boostedLVEl1,
            # boostedtaus.boostedLVTau2,
            # boostedtaus.boostedLVEl1_uncorrected,
            # boostedtaus.boostedLVTau2_uncorrected,
            pairselection.LVEl1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.ETDiTauPairQuantities,
            # boostedtaus.boostedETDiTauPairQuantities,
            genparticles.ETGenDiTauPairQuantities,
            scalefactors.Tau_2_VsJetTauID_lt_SF,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            # scalefactors.Tau_2_oldIsoTauID_lt_SF,
            # scalefactors.Tau_2_antiEleTauID_SF,
            # scalefactors.Tau_2_antiMuTauID_SF,
            triggers.ETGenerateSingleElectronTriggerFlags,
            # triggers.BoostedETGenerateSingleElectronTriggerFlags,
            # triggers.ETGenerateCrossTriggerFlags,
            # triggers.GenerateSingleTrailingTauTriggerFlags,
        ],
    )
    configuration.add_producers(
        "tt",
        [
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            taus.TauEnergyCorrection,
            # taus.BaseTaus,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            # boostedtaus.boostedTauEnergyCorrection,
            # boostedtaus.GoodBoostedTaus,
            # boostedtaus.NumberOfGoodBoostedTaus,
            pairselection.TTPairSelection,
            # pairselection.boostedTTPairSelection,
            pairselection.GoodTTPairFilter,
            pairselection.LVTau1,
            pairselection.LVTau2,
            # boostedtaus.boostedLVTau1,
            # boostedtaus.boostedLVTau2,
            # boostedtaus.boostedLVTau1_uncorrected,
            # boostedtaus.boostedLVTau2_uncorrected,
            pairselection.LVTau1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.TTDiTauPairQuantities,
            # boostedtaus.boostedTTDiTauPairQuantities,
            genparticles.TTGenDiTauPairQuantities,
            scalefactors.Tau_1_VsJetTauID_SF,
            scalefactors.Tau_1_VsEleTauID_SF,
            scalefactors.Tau_1_VsMuTauID_SF,
            scalefactors.Tau_2_VsJetTauID_tt_SF,
            scalefactors.Tau_2_VsEleTauID_SF,
            scalefactors.Tau_2_VsMuTauID_SF,
            # scalefactors.Tau_1_oldIsoTauID_tt_SF,
            # scalefactors.Tau_1_antiEleTauID_SF,
            # scalefactors.Tau_1_antiMuTauID_SF,
            # scalefactors.Tau_2_oldIsoTauID_tt_SF,
            # scalefactors.Tau_2_antiEleTauID_SF,
            # scalefactors.Tau_2_antiMuTauID_SF,
            triggers.TTGenerateDoubleTriggerFlags,
            # triggers.BoostedTTGenerateDoubleTriggerFlags,
            # triggers.GenerateSingleTrailingTauTriggerFlags,
            # triggers.GenerateSingleLeadingTauTriggerFlags,
            # triggers.BoostedTTTriggerFlags,
            scalefactors.TTGenerateDoubleTauTriggerSF_MC,
            # scalefactors.BoostedTTGenerateFatjetTriggerSF_MC,
        ],
    )
    configuration.add_modification_rule(
        ["et", "mt"],
        RemoveProducer(
            producers=[
                scalefactors.Tau_2_VsMuTauID_SF,
                scalefactors.Tau_2_VsJetTauID_lt_SF,
                scalefactors.Tau_2_VsEleTauID_SF,
            ],
            samples="data",
        ),
    )
    # configuration.add_modification_rule(
    #     ["et", "mt"],
    #     RemoveProducer(
    #         producers=[
    #             scalefactors.Tau_2_antiMuTauID_SF,
    #             scalefactors.Tau_2_oldIsoTauID_lt_SF,
    #             scalefactors.Tau_2_antiEleTauID_SF,
    #         ],
    #         samples=["data", "embedding"],
    #     ),
    # )
    configuration.add_modification_rule(
        ["et", "mt", "tt"],
        AppendProducer(
            producers=[
                genparticles.GenBPairQuantities,
                genparticles.GenMatchingBPairFlag,
                genparticles.GenTauPairQuantities,
                # genparticles.GenMatchingBoostedTauPairFlag,
            ],
            samples=["nmssm_Ybb", "nmssm_Ytautau"], 
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
            ],
            samples="data",
        ),
    )
    # configuration.add_modification_rule(
    #     ["tt"],
    #     RemoveProducer(
    #         producers=[
    #             scalefactors.Tau_1_oldIsoTauID_tt_SF,
    #             scalefactors.Tau_1_antiEleTauID_SF,
    #             scalefactors.Tau_1_antiMuTauID_SF,
    #             scalefactors.Tau_2_oldIsoTauID_tt_SF,
    #             scalefactors.Tau_2_antiEleTauID_SF,
    #             scalefactors.Tau_2_antiMuTauID_SF,
    #         ],
    #         samples=["data", "embedding"],
    #     ),
    # )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[
                scalefactors.btagging_SF,
                # scalefactors.btagging_SF_boosted,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    # configuration.add_modification_rule(
    #     scopes,
    #     RemoveProducer(
    #         producers=[
    #             fatjets.fj_Xbb_hadflavor,
    #             fatjets.fj_Xbb_nBhad,
    #             fatjets.fj_Xbb_nChad,
    #             fatjets.fj_Xbb_hadflavor_boosted,
    #             fatjets.fj_Xbb_nBhad_boosted,
    #             fatjets.fj_Xbb_nChad_boosted,
    #         ],
    #         samples=["data", "embedding", "embedding_mc"],
    #     ),
    # )
    configuration.add_modification_rule(
        ["et", "mt", "tt"],
        ReplaceProducer(
            producers=[taus.TauEnergyCorrection, taus.TauEnergyCorrection_data],
            samples="data",
        ),
    )
    # configuration.add_modification_rule(
    #     ["et", "mt", "tt"],
    #     ReplaceProducer(
    #         producers=[
    #             boostedtaus.boostedTauEnergyCorrection,
    #             boostedtaus.boostedTauEnergyCorrection_data,
    #         ],
    #         samples="data",
    #     ),
    # )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.JetEnergyCorrection, jets.JetEnergyCorrection_data],
            samples="data",
        ),
    )
    # configuration.add_modification_rule(
    #     "global",
    #     ReplaceProducer(
    #         producers=[
    #             fatjets.FatJetEnergyCorrection,
    #             fatjets.FatJetEnergyCorrection_data,
    #         ],
    #         samples=["data"],
    #     ),
    # )
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[
                electrons.ElectronPtCorrectionMC,
                electrons.RenameElectronPt,
            ],
            samples=["data"],
        ),
    )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.npartons],
            exclude_samples=["dyjets", "wjets", "electroweak_boson"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    # for whatever reason, the diboson samples do not have these weights in the ntuple....
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.LHE_Scale_weight],
            samples=["data", "embedding", "embedding_mc", "diboson"],
        ),
    )
    # for whatever reason, the nmssm samples have one less entry of the weights and therefore need special treatment
    # configuration.add_modification_rule(
    #     "global",
    #     ReplaceProducer(
    #         producers=[event.LHE_Scale_weight, event.NMSSM_LHE_Scale_weight],
    #         samples=["nmssm_Ybb", "nmssm_Ytautau"],
    #     ),
    # )
    # configuration.add_modification_rule(
    #     ["et", "mt"],
    #     RemoveProducer(
    #         producers=[
    #             pairquantities.tau_gen_match_2,
    #             # boostedtaus.boosted_tau_gen_match_2,
    #         ],
    #         samples="data",
    #     ),
    # )
    # configuration.add_modification_rule(
    #     ["tt"],
    #     RemoveProducer(
    #         producers=[
    #             pairquantities.tau_gen_match_1,
    #             pairquantities.tau_gen_match_2,
    #         ],
    #         samples="data",
    #     ),
    # )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[
                genparticles.GenMatching,
                # genparticles.GenMatchingBoosted,
            ],
            samples="data",
        ),
    )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[
                genparticles.GenDiBjetPairQuantities,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    # configuration.add_modification_rule(
    #     scopes,
    #     AppendProducer(
    #         producers=[event.GGH_NNLO_Reweighting, event.GGH_WG1_Uncertainties],
    #         samples=["ggh_htautau", "rem_htautau"],
    #     ),
    # )
    # configuration.add_modification_rule(
    #     scopes,
    #     AppendProducer(
    #         producers=event.QQH_WG1_Uncertainties,
    #         samples=["vbf_htautau", "rem_htautau"],
    #     ),
    # )
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
    # changes needed for data
    # global scope
    configuration.add_modification_rule(
        "global",
        ReplaceProducer(
            producers=[jets.JetEnergyCorrection, jets.RenameJetsData],
            samples=["embedding", "embedding_mc"],
        ),
    )
    # configuration.add_modification_rule(
    #     "global",
    #     ReplaceProducer(
    #         producers=[fatjets.FatJetEnergyCorrection, fatjets.RenameFatJetsData],
    #         samples=["embedding", "embedding_mc"],
    #     ),
    # )

    configuration.add_modification_rule(
        "global",
        AppendProducer(producers=event.JSONFilter, samples=["data", "embedding"]),
    )

    # scope specific
    configuration.add_modification_rule(
        "mt",
        RemoveProducer(
            producers=[genparticles.MTGenDiTauPairQuantities],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "et",
        RemoveProducer(
            producers=[genparticles.ETGenDiTauPairQuantities],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "tt",
        RemoveProducer(
            producers=[genparticles.TTGenDiTauPairQuantities],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "mm",
        RemoveProducer(
            producers=[genparticles.MuMuGenPairQuantities],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "tt",
        RemoveProducer(
            producers=[
                scalefactors.TTGenerateDoubleTauTriggerSF_MC,
                # scalefactors.BoostedTTGenerateFatjetTriggerSF_MC,
            ],
            samples=["data"],
        ),
    )
    # lepton scalefactors from our measurement
    configuration.add_modification_rule(
        ["mt"],
        AppendProducer(
            producers=[
                scalefactors.TauEmbeddingMuonIDSF_1_MC,
                scalefactors.TauEmbeddingMuonIsoSF_1_MC,
                # scalefactors.TauEmbeddingBoostedMuonIDSF_1_MC,
                # scalefactors.TauEmbeddingBoostedMuonIsoSF_1_MC,
                # scalefactors.Muon_SF_boosted,
            ],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        AppendProducer(
            producers=[
                scalefactors.TauEmbeddingElectronIDSF_1_MC,
                scalefactors.TauEmbeddingElectronIsoSF_1_MC,
                # scalefactors.TauEmbeddingBoostedElectronIDSF_1_MC,
                # scalefactors.TauEmbeddingBoostedElectronIsoSF_1_MC,
                # scalefactors.EleID_SF_boosted,
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
        ["mt"],
        AppendProducer(
            producers=[
                scalefactors.MTGenerateSingleMuonTriggerSF_MC,
                # scalefactors.BoostedMTGenerateSingleMuonTriggerSF_MC,
            ],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ["et"],
        AppendProducer(
            producers=[
                scalefactors.ETGenerateSingleElectronTriggerSF_MC,
                # scalefactors.BoostedETGenerateSingleElectronTriggerSF_MC,
            ],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ),
    )

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
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            # q.nfatjets,
            # q.fj_pt_1,
            # q.fj_eta_1,
            # q.fj_phi_1,
            # q.fj_mass_1,
            # q.fj_msoftdrop_1,
            # q.fj_particleNet_XbbvsQCD_1,
            # q.fj_nsubjettiness_2over1_1,
            # q.fj_nsubjettiness_3over2_1,
            # q.fj_pt_2,
            # q.fj_eta_2,
            # q.fj_phi_2,
            # q.fj_mass_2,
            # q.fj_msoftdrop_2,
            # q.fj_particleNet_XbbvsQCD_2,
            # q.fj_nsubjettiness_2over1_2,
            # q.fj_nsubjettiness_3over2_2,
            # q.fj_matched_pt,
            # q.fj_matched_eta,
            # q.fj_matched_phi,
            # q.fj_matched_mass,
            # q.fj_matched_msoftdrop,
            # q.fj_matched_particleNet_XbbvsQCD,
            # q.fj_matched_nsubjettiness_2over1,
            # q.fj_matched_nsubjettiness_3over2,
            # q.fj_Xbb_pt,
            # q.fj_Xbb_eta,
            # q.fj_Xbb_phi,
            # q.fj_Xbb_mass,
            # q.fj_Xbb_msoftdrop,
            # q.fj_Xbb_particleNet_XbbvsQCD,
            # q.fj_Xbb_nsubjettiness_2over1,
            # q.fj_Xbb_nsubjettiness_3over2,
            # q.fj_Xbb_hadflavor,
            # q.fj_Xbb_nBhad,
            # q.fj_Xbb_nChad,
            # q.nfatjets_boosted,
            # q.fj_Xbb_pt_boosted,
            # q.fj_Xbb_eta_boosted,
            # q.fj_Xbb_phi_boosted,
            # q.fj_Xbb_mass_boosted,
            # q.fj_Xbb_msoftdrop_boosted,
            # q.fj_Xbb_particleNet_XbbvsQCD_boosted,
            # q.fj_Xbb_nsubjettiness_2over1_boosted,
            # q.fj_Xbb_nsubjettiness_3over2_boosted,
            # q.fj_Xbb_hadflavor_boosted,
            # q.fj_Xbb_nBhad_boosted,
            # q.fj_Xbb_nChad_boosted,
            q.bpair_pt_1,
            q.bpair_pt_2,
            q.bpair_eta_1,
            q.bpair_eta_2,
            q.bpair_phi_1,
            q.bpair_phi_2,
            q.bpair_mass_1,
            q.bpair_mass_2,
            q.bpair_btag_value_1,
            q.bpair_btag_value_2,
            q.bpair_reg_res_1,
            q.bpair_reg_res_2,
            q.bpair_m_inv,
            q.bpair_deltaR,
            q.bpair_pt_dijet,
            # q.bpair_pt_1_boosted,
            # q.bpair_pt_2_boosted,
            # q.bpair_eta_1_boosted,
            # q.bpair_eta_2_boosted,
            # q.bpair_phi_1_boosted,
            # q.bpair_phi_2_boosted,
            # q.bpair_mass_1_boosted,
            # q.bpair_mass_2_boosted,
            # q.bpair_btag_value_1_boosted,
            # q.bpair_btag_value_2_boosted,
            # q.bpair_reg_res_1_boosted,
            # q.bpair_reg_res_2_boosted,
            # q.bpair_m_inv_boosted,
            # q.bpair_deltaR_boosted,
            # q.bpair_pt_dijet_boosted,
            q.genjet_pt_1,
            q.genjet_eta_1,
            q.genjet_phi_1,
            q.genjet_mass_1,
            q.genjet_hadFlavour_1,
            q.genjet_pt_2,
            q.genjet_eta_2,
            q.genjet_phi_2,
            q.genjet_mass_2,
            q.genjet_hadFlavour_2,
            q.genjet_m_inv,
            q.njets,
            # q.njets_boosted,
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
            q.deltaR_ditaupair,
            q.pt_vis,
            q.nbtag,
            # q.nbtag_boosted,
            # q.bpt_1,
            # q.bpt_2,
            # q.beta_1,
            # q.beta_2,
            # q.bphi_1,
            # q.bphi_2,
            # q.btag_value_1,
            # q.btag_value_2,
            q.btag_weight,
            # q.btag_weight_boosted,
            # q.pNet_Xbb_weight,
            # q.pNet_Xbb_weight_boosted,
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
            # q.met_boosted,
            # q.metphi_boosted,
            # q.pfmet_boosted,
            # q.pfmetphi_boosted,
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
            q.pt_tautau,
            # q.pt_ttjj,
            q.pt_tautaubb,
            q.mass_tautaubb,
            q.mt_tot,
            q.genbosonmass,
            q.gen_match_1,
            q.gen_match_2,
            # q.boosted_gen_match_1,
            # q.boosted_gen_match_2,
            q.pzetamissvis_pf,
            q.mTdileptonMET_pf,
            q.mt_1_pf,
            q.mt_2_pf,
            q.pt_tt_pf,
            # q.pt_ttjj_pf,
            q.pt_ttbb_pf,
            q.mt_tot_pf,
            q.pt_dijet,
            q.jet_hemisphere,
        ],
    )
    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            scopes,
            nanoAOD.genWeight,
        )
    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            # q.nboostedtaus,
            scalefactors.Tau_2_VsJetTauID_lt_SF.output_group,
            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            # scalefactors.Tau_2_oldIsoTauID_lt_SF.output_group,
            # scalefactors.Tau_2_antiEleTauID_SF.output_group,
            # scalefactors.Tau_2_antiMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            # boostedtaus.isoTauIDFlag_2.output_group,
            # boostedtaus.antiEleTauIDFlag_2.output_group,
            # boostedtaus.antiMuTauIDFlag_2.output_group,
            triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            # triggers.BoostedMTGenerateSingleMuonTriggerFlags.output_group,
            # triggers.MTGenerateCrossTriggerFlags.output_group,
            # triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            # q.tau_gen_match_2,
            q.muon_veto_flag,
            # q.boosted_muon_veto_flag,
            q.electron_veto_flag,
            q.dimuon_veto,
            q.dilepton_veto,
            # q.id_wgt_mu_1,
            # q.iso_wgt_mu_1,
            # q.boosted_dxy_1,
            # q.boosted_dz_1,
            # q.boosted_tau_decaymode_1,
            # q.boosted_tau_decaymode_2,
            # q.boosted_tau_gen_match_2,
            # q.boosted_pt_1,
            # q.boosted_pt_2,
            # q.boosted_eta_1,
            # q.boosted_eta_2,
            # q.boosted_phi_1,
            # q.boosted_phi_2,
            # q.boosted_mass_1,
            # q.boosted_mass_2,
            # q.boosted_q_1,
            # q.boosted_q_2,
            # q.boosted_iso_1,
            # q.boosted_iso_2,
            # q.boosted_m_vis,
            # q.boosted_deltaR_ditaupair,
            # q.boosted_pt_vis,
            # q.boosted_mt_1,
            # q.boosted_mt_2,
            # q.boosted_pt_tautaubb,
            # q.boosted_mass_tautaubb,
            # q.boosted_pt_add,
            # q.boosted_eta_add,
            # q.boosted_phi_add,
            # q.boosted_mass_add,
        ],
    )
    configuration.add_outputs(
        "et",
        [
            q.nelectrons,
            q.ntaus,
            # q.nboostedtaus,
            scalefactors.Tau_2_VsJetTauID_lt_SF.output_group,
            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            # scalefactors.Tau_2_oldIsoTauID_lt_SF.output_group,
            # scalefactors.Tau_2_antiEleTauID_SF.output_group,
            # scalefactors.Tau_2_antiMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            # boostedtaus.isoTauIDFlag_2.output_group,
            # boostedtaus.antiEleTauIDFlag_2.output_group,
            # boostedtaus.antiMuTauIDFlag_2.output_group,
            triggers.ETGenerateSingleElectronTriggerFlags.output_group,
            # triggers.BoostedETGenerateSingleElectronTriggerFlags.output_group,
            # triggers.ETGenerateCrossTriggerFlags.output_group,
            # triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            # q.tau_gen_match_2,
            q.muon_veto_flag,
            # q.boosted_electron_veto_flag,
            q.electron_veto_flag,
            q.dielectron_veto,
            q.dilepton_veto,
            # q.id_wgt_ele_wp90nonIso_1,
            # q.id_wgt_ele_wp80nonIso_1,
            # q.boosted_dxy_1,
            # q.boosted_dz_1,
            # q.boosted_tau_decaymode_1,
            # q.boosted_tau_decaymode_2,
            # q.boosted_tau_gen_match_2,
            # q.boosted_pt_1,
            # q.boosted_pt_2,
            # q.boosted_eta_1,
            # q.boosted_eta_2,
            # q.boosted_phi_1,
            # q.boosted_phi_2,
            # q.boosted_mass_1,
            # q.boosted_mass_2,
            # q.boosted_q_1,
            # q.boosted_q_2,
            # q.boosted_iso_1,
            # q.boosted_iso_2,
            # q.boosted_m_vis,
            # q.boosted_deltaR_ditaupair,
            # q.boosted_pt_vis,
            # q.boosted_mt_1,
            # q.boosted_mt_2,
            # q.boosted_pt_tautaubb,
            # q.boosted_mass_tautaubb,
            # q.boosted_pt_add,
            # q.boosted_eta_add,
            # q.boosted_phi_add,
            # q.boosted_mass_add,
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
            # scalefactors.Tau_1_oldIsoTauID_tt_SF.output_group,
            # scalefactors.Tau_1_antiEleTauID_SF.output_group,
            # scalefactors.Tau_1_antiMuTauID_SF.output_group,
            # scalefactors.Tau_2_oldIsoTauID_tt_SF.output_group,
            # scalefactors.Tau_2_antiEleTauID_SF.output_group,
            # scalefactors.Tau_2_antiMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_1.output_group,
            pairquantities.VsEleTauIDFlag_1.output_group,
            pairquantities.VsMuTauIDFlag_1.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            # boostedtaus.isoTauIDFlag_1.output_group,
            # boostedtaus.antiEleTauIDFlag_1.output_group,
            # boostedtaus.antiMuTauIDFlag_1.output_group,
            # boostedtaus.isoTauIDFlag_2.output_group,
            # boostedtaus.antiEleTauIDFlag_2.output_group,
            # boostedtaus.antiMuTauIDFlag_2.output_group,
            # triggers.BoostedTTTriggerFlags.output_group,
            triggers.TTGenerateDoubleTriggerFlags.output_group,
            # triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            # triggers.GenerateSingleLeadingTauTriggerFlags.output_group,
            # q.taujet_pt_1,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            # q.tau_gen_match_1,
            # q.tau_gen_match_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dimuon_veto,
            q.dilepton_veto,
            # q.boosted_tau_decaymode_1,
            # q.boosted_tau_decaymode_2,
            # q.boosted_tau_gen_match_1,
            # q.boosted_tau_gen_match_2,
            # q.boosted_pt_1,
            # q.boosted_pt_2,
            # q.boosted_eta_1,
            # q.boosted_eta_2,
            # q.boosted_phi_1,
            # q.boosted_phi_2,
            # q.boosted_mass_1,
            # q.boosted_mass_2,
            # q.boosted_q_1,
            # q.boosted_q_2,
            # q.boosted_iso_1,
            # q.boosted_iso_2,
            # q.boosted_m_vis,
            # q.boosted_deltaR_ditaupair,
            # q.boosted_pt_vis,
            # q.boosted_mt_1,
            # q.boosted_mt_2,
            # q.boosted_pt_tautaubb,
            # q.boosted_mass_tautaubb,
            # q.fj_leading_pt, 
            # q.fj_leading_msoftdrop,
        ],
    )
    configuration.add_outputs(
        "mm",
        [
            q.nmuons,
            triggers.MuMuGenerateSingleMuonTriggerFlags.output_group,
        ],
    )
    if "data" not in sample:
        configuration.add_outputs(
            "tt",
            [
                q.trg_wgt_double_tau_1,
                q.trg_wgt_double_tau_2,
                # q.trg_wgt_fatjet,
            ],
        )

    if sample in ["nmssm_Ybb", "nmssm_Ytautau"]:
        configuration.add_outputs(
            scopes,
            [
                q.gen_b_pt_1,
                q.gen_b_eta_1,
                q.gen_b_phi_1,
                q.gen_b_mass_1,
                q.gen_b_pt_2,
                q.gen_b_eta_2,
                q.gen_b_phi_2,
                q.gen_b_mass_2,
                q.gen_b_m_inv,
                q.gen_b_deltaR,
                q.gen_bpair_match_flag,
                q.gen_tau_pt_1,
                q.gen_tau_eta_1,
                q.gen_tau_phi_1,
                q.gen_tau_mass_1,
                q.gen_tau_pt_2,
                q.gen_tau_eta_2,
                q.gen_tau_phi_2,
                q.gen_tau_mass_2,
                q.gen_tau_m_inv,
                q.gen_tau_deltaR,
                # q.gen_boostedtaupair_match_flag,
            ],
        )
    #########################
    # LHE Scale Weight variations
    # up is muR=2.0, muF=2.0
    # down is muR=0.5, muF=0.5
    #########################
    if sample in ["ggh", "qqh"]:
        configuration.add_shift(
            SystematicShift(
                "muRWeightUp",
                shift_config={
                    "global": {
                        "muR": 2.0,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muRWeightDown",
                shift_config={
                    "global": {
                        "muR": 0.5,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightUp",
                shift_config={
                    "global": {
                        "muF": 2.0,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightDown",
                shift_config={
                    "global": {
                        "muF": 0.5,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
    # if sample in ["nmssm_Ybb", "nmssm_Ytautau"]:
    #     configuration.add_shift(
    #         SystematicShift(
    #             "muRWeightUp",
    #             shift_config={
    #                 "global": {
    #                     "muR": 2.0,
    #                 }
    #             },
    #             producers={"global": [event.NMSSM_LHE_Scale_weight]},
    #         )
    #     )
    #     configuration.add_shift(
    #         SystematicShift(
    #             "muRWeightDown",
    #             shift_config={
    #                 "global": {
    #                     "muR": 0.5,
    #                 }
    #             },
    #             producers={"global": [event.NMSSM_LHE_Scale_weight]},
    #         )
    #     )
    #     configuration.add_shift(
    #         SystematicShift(
    #             "muFWeightUp",
    #             shift_config={
    #                 "global": {
    #                     "muF": 2.0,
    #                 }
    #             },
    #             producers={"global": [event.NMSSM_LHE_Scale_weight]},
    #         )
    #     )
    #     configuration.add_shift(
    #         SystematicShift(
    #             "muFWeightDown",
    #             shift_config={
    #                 "global": {
    #                     "muF": 0.5,
    #                 }
    #             },
    #             producers={"global": [event.NMSSM_LHE_Scale_weight]},
    #         )
    #     )

    #########################
    # Lepton to tau fakes energy scalefactor shifts  #
    #########################
    if "dyjets" in sample or "electroweak_boson" in sample:
        configuration.add_shift(
            SystematicShift(
                name="tauMuFakeEsDown",
                shift_config={
                    "mt": {
                        "tau_mufake_es": "down",
                    }
                },
                producers={"mt": [taus.TauPtCorrection_muFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauMuFakeEsUp",
                shift_config={
                    "mt": {
                        "tau_mufake_es": "up",
                    }
                },
                producers={"mt": [taus.TauPtCorrection_muFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongBarrelDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_barrel": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongBarrelUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_barrel": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongEndcapDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_endcap": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongEndcapUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_endcap": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroBarrelDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_barrel": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroBarrelUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_barrel": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroEndcapDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_endcap": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroEndcapUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_endcap": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
    
    #########################
    # Electron energy correction shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="eleEsResoUp",
            shift_config={
                ("global"): {"ele_es_variation": "resolutionUp"},
            },
            producers={
                ("global"): [
                    electrons.ElectronPtCorrectionMC,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="eleEsResoDown",
            shift_config={
                ("global"): {"ele_es_variation": "resolutionDown"},
            },
            producers={
                ("global"): [
                    electrons.ElectronPtCorrectionMC,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="eleEsScaleUp",
            shift_config={
                ("global"): {"ele_es_variation": "scaleUp"},
            },
            producers={
                ("global"): [
                    electrons.ElectronPtCorrectionMC,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="eleEsScaleDown",
            shift_config={
                ("global"): {"ele_es_variation": "scaleDown"},
            },
            producers={
                ("global"): [
                    electrons.ElectronPtCorrectionMC,
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
                nanoAOD.MET_pt: "PuppiMET_ptUnclusteredUp",
                nanoAOD.MET_phi: "PuppiMET_phiUnclusteredUp",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnDown",
            quantity_change={
                nanoAOD.MET_pt: "PuppiMET_ptUnclusteredDown",
                nanoAOD.MET_phi: "PuppiMET_phiUnclusteredDown",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    #########################
    # Prefiring Shifts
    #########################
    if era != "2018":
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringDown",
                quantity_change={
                    nanoAOD.prefireWeight: "L1PreFiringWeight_Dn",
                },
                scopes=["global"],
            )
        )
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringUp",
                quantity_change={
                    nanoAOD.prefireWeight: "L1PreFiringWeight_Up",
                },
                scopes=["global"],
            )
        )
    #########################
    # particleNet Xbb scale factor uncertainties
    #########################
    # configuration.add_shift(
    #     SystematicShift(
    #         name="pNetXbbSFUp",
    #         shift_config={
    #             ("mt", "et", "tt"): {"pNetXbb_sf_variation": "up"},
    #         },
    #         producers={
    #             ("mt", "et", "tt"): {
    #                 scalefactors.Xbb_tagging_SF,
    #                 scalefactors.Xbb_tagging_SF_boosted,
    #             }
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="pNetXbbSFDown",
    #         shift_config={
    #             ("mt", "et", "tt"): {"pNetXbb_sf_variation": "down"},
    #         },
    #         producers={
    #             ("mt", "et", "tt"): {
    #                 scalefactors.Xbb_tagging_SF,
    #                 scalefactors.Xbb_tagging_SF_boosted,
    #             }
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    #########################
    # MET Recoil Shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResponseUp",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": False,
                    "apply_recoil_response_systematic": True,
                    "recoil_systematic_shift_up": True,
                    "recoil_systematic_shift_down": False,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                    # met.ApplyRecoilCorrections_boosted,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResponseDown",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": False,
                    "apply_recoil_response_systematic": True,
                    "recoil_systematic_shift_up": False,
                    "recoil_systematic_shift_down": True,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                    # met.ApplyRecoilCorrections_boosted,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResolutionUp",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": True,
                    "apply_recoil_response_systematic": False,
                    "recoil_systematic_shift_up": True,
                    "recoil_systematic_shift_down": False,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                    # met.ApplyRecoilCorrections_boosted,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResolutionDown",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": True,
                    "apply_recoil_response_systematic": False,
                    "recoil_systematic_shift_up": False,
                    "recoil_systematic_shift_down": True,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                    # met.ApplyRecoilCorrections_boosted,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    #########################
    # Pileup Shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="PileUpUp",
            scopes=["global"],
            shift_config={
                ("global"): {"PU_reweighting_variation": "up"},
            },
            producers={
                "global": [
                    event.PUweights,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="PileUpDown",
            scopes=["global"],
            shift_config={
                ("global"): {"PU_reweighting_variation": "down"},
            },
            producers={
                "global": [
                    event.PUweights,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    #########################
    # Electron id/iso sf shifts
    #########################
    
    # configuration.add_shift(
    #     SystematicShift(
    #         name="electronIdSFUp",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"mc_electron_id_extrapolation": 1.02},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.TauEmbeddingElectronIDSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="electronIdSFDown",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"mc_electron_id_extrapolation": 0.98},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.TauEmbeddingElectronIDSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="electronIsoSFUp",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"mc_electron_iso_extrapolation": 1.02},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.TauEmbeddingElectronIsoSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="electronIsoSFDown",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"mc_electron_iso_extrapolation": 0.98},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.TauEmbeddingElectronIsoSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedElectronIdSFUp",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"ele_sf_variation": "sfup"},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.EleID_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedElectronIdSFDown",
    #         scopes=["et"],
    #         shift_config={
    #             ("et"): {"ele_sf_variation": "sfdown"},
    #         },
    #         producers={
    #             ("et"): [
    #                 scalefactors.EleID_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )

    #########################
    # Muon id/iso sf shifts
    #########################
    
    # configuration.add_shift(
    #     SystematicShift(
    #         name="muonIdSFUp",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"mc_muon_id_extrapolation": 1.02},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.TauEmbeddingMuonIDSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="muonIdSFDown",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"mc_muon_id_extrapolation": 0.98},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.TauEmbeddingMuonIDSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="muonIsoSFUp",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"mc_muon_iso_extrapolation": 1.02},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.TauEmbeddingMuonIsoSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="muonIsoSFDown",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"mc_muon_iso_extrapolation": 0.98},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.TauEmbeddingMuonIsoSF_1_MC,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )

    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonRecoSFUp",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_reco_sf_variation": "systup"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_Reco_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonRecoSFDown",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_reco_sf_variation": "systdown"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_Reco_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonIdSFUp",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_id_sf_variation": "systup"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_ID_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonIdSFDown",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_id_sf_variation": "systdown"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_ID_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonIsoSFUp",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_iso_sf_variation": "systup"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_Iso_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedMuonIsoSFDown",
    #         scopes=["mt"],
    #         shift_config={
    #             ("mt"): {"muon_iso_sf_variation": "systdown"},
    #         },
    #         producers={
    #             ("mt"): [
    #                 scalefactors.Muon_1_Iso_SF_boosted,
    #             ],
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )

    #########################
    # Trigger shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFUp",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": [
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 1.02,
                        },
                    ]
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFDown",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": [
                        {
                            "flagname": "trg_wgt_single_ele32orele35",
                            "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele32",
                            "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele35",
                            "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_ele27orele32orele35",
                            "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                            "mc_electron_trg_extrapolation": 0.98,
                        },
                    ]
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.02,
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 1.02,
                        },
                    ],
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": [
                        {
                            "flagname": "trg_wgt_single_mu24",
                            "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_mu27",
                            "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 0.98,
                        },
                        {
                            "flagname": "trg_wgt_single_mu24ormu27",
                            "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                            "mc_muon_trg_extrapolation": 0.98,
                        },
                    ],
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedSingleMuonTriggerSFUp",
    #         shift_config={
    #             ("mt"): {
    #                 "boosted_singlemuon_trigger_sf_mc": [
    #                     {
    #                         "flagname": "trg_wgt_single_mu24_boosted",
    #                         "muon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
    #                         "muon_trg_sf_variation": "systup",  # "sf" is nominal, "systup"/"systdown" are up/down variations
    #                     },
    #                     {
    #                         "flagname": "trg_wgt_single_mu50_boosted",
    #                         "muon_trigger_sf_name": "NUM_Mu50_or_OldMu100_or_TkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose",
    #                         "muon_trg_sf_variation": "systup",  # "sf" is nominal, "systup"/"systdown" are up/down variations
    #                     },
    #                 ],
    #             }
    #         },
    #         producers={("mt"): scalefactors.BoostedMTGenerateSingleMuonTriggerSF_MC},
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedSingleMuonTriggerSFDown",
    #         shift_config={
    #             ("mt"): {
    #                 "boosted_singlemuon_trigger_sf_mc": [
    #                     {
    #                         "flagname": "trg_wgt_single_mu24_boosted",
    #                         "muon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
    #                         "muon_trg_sf_variation": "systdown",  # "sf" is nominal, "systup"/"systdown" are up/down variations
    #                     },
    #                     {
    #                         "flagname": "trg_wgt_single_mu50_boosted",
    #                         "muon_trigger_sf_name": "NUM_Mu50_or_OldMu100_or_TkMu100_DEN_CutBasedIdGlobalHighPt_and_TkIsoLoose",
    #                         "muon_trg_sf_variation": "systdown",  # "sf" is nominal, "systup"/"systdown" are up/down variations
    #                     },
    #                 ],
    #             }
    #         },
    #         producers={("mt"): scalefactors.BoostedMTGenerateSingleMuonTriggerSF_MC},
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedSingleElectronTriggerSFUp",
    #         shift_config={
    #             ("et"): {
    #                 "boosted_singleelectron_trigger_sf_mc": [
    #                     {
    #                         "flagname": "trg_wgt_single_ele_boosted",
    #                         "ele_trg_sf_name": "ElectronTriggerSF",
    #                         "ele_trg_sf_variation": "up",  
    #                     },
    #                 ],
    #             }
    #         },
    #         producers={("et"): scalefactors.BoostedETGenerateSingleElectronTriggerSF_MC},
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="boostedSingleElectronTriggerSFDown",
    #         shift_config={
    #             ("et"): {
    #                 "boosted_singleelectron_trigger_sf_mc": [
    #                     {
    #                         "flagname": "trg_wgt_single_ele_boosted",
    #                         "ele_trg_sf_name": "ElectronTriggerSF",
    #                         "ele_trg_sf_variation": "down",  
    #                     },
    #                 ],
    #             }
    #         },
    #         producers={("et"): scalefactors.BoostedETGenerateSingleElectronTriggerSF_MC},
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )

    configuration.add_shift(
        SystematicShift(
            name="ditauTriggerSFUp",
            shift_config={("tt"): {"ditau_trigger_syst": "up"}},
            producers={
                ("tt"): scalefactors.TTGenerateDoubleTauTriggerSF_MC,
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="ditauTriggerSFDown",
            shift_config={("tt"): {"ditau_trigger_syst": "down"}},
            producers={
                ("tt"): scalefactors.TTGenerateDoubleTauTriggerSF_MC,
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    
    # configuration.add_shift(
    #     SystematicShift(
    #         name="fatjetTriggerSFUp",
    #         shift_config={("tt"): {"fatjet_trigger_sf_syst": "up"}},
    #         producers={
    #             ("tt"): scalefactors.BoostedTTGenerateFatjetTriggerSF_MC,
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="fatjetTriggerSFDown",
    #         shift_config={("tt"): {"fatjet_trigger_sf_syst": "down"}},
    #         producers={
    #             ("tt"): scalefactors.BoostedTTGenerateFatjetTriggerSF_MC,
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )

    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    add_tauVariations(configuration, sample)
    # add_boostedtauVariations(configuration, sample)
    #########################
    # Import triggersetup   #
    #########################
    add_diTauTriggerSetup(configuration)
    #########################
    # Add additional producers and SFs related to embedded samples
    #########################
    if sample == "embedding" or sample == "embedding_mc":
        setup_embedding(configuration, scopes)

    #########################
    # Jet energy resolution and jet energy scale
    #########################
    add_jetVariations(configuration, era)

    #########################
    # btagging scale factor shape variation
    #########################
    add_btagVariations(configuration)

    #########################
    # Jet energy correction for data
    #########################
    # add_jetCorrectionData(configuration, era)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
