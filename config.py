from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

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
#from .producers import triggers as triggers
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
#from .tau_triggersetup import add_diTauTriggerSetup
from .tau_variations import add_tauVariations
from .jet_variations import add_jetVariations
#from .tau_embedding_settings import setup_embedding
from .btag_variations import add_btagVariations
from .jec_data import add_jetCorrectionData
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


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

    ###########################
    ####### Parameters ########
    ###########################

    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            # for LHE weights
            "muR": 1.0,
            "muF": 1.0,
            "isr": 1.0,
            "fsr": 1.0,
            "pdf_variation": "nominal",
            "pdf_alphaS_variation": "nominal",
            "golden_json_file": "data/golden_json/Cert_Collisions2024_378981_386951_Golden.json",
            "met_filters": ["Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",  # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
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
    # electron base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_ele_pt": 10.0,
            "max_ele_eta": 2.5,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "max_ele_iso": 0.3,
            "ele_id": "Electron_mvaNoIso_WP90",
            #"ele_es_era": '"2023_Summer23BPix"',
            #"ele_es_variation": "nom",
            #"ele_es_file": '"data/electron_energy_scale/2018_UL/EGM_ScaleUnc.json.gz"',
        },
    )
    # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 30,
            "max_jet_eta": 4.7,
            "jet_collection_name":'"AK4PUPPI"', #might be redundant with the "jet_jec_algo" parameter, need to check better
            "jet_id_json": '"data/jsonpog-integration/POG/JME/2024_Winter24/jetid.json.gz"', #points back to 2022
            "jet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": "data/jsonpog-integration/POG/JME/2024_Winter24/jet_jerc.json.gz",
            "jet_jer_tag": '"Winter24Prompt24_V3_MC_L1FastJet"', 
            "jet_jes_tag_data": '"Winter24Prompt24_V3_MC_L1FastJet"',
            "jet_jes_tag": '"Winter24Prompt24_V3_MC_L1FastJet"',
            "jet_jec_algo": '"AK4PFPuppi"',
        },
    )
    # bjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_bjet_pt": 20,
            "max_bjet_eta": 2.5,
            "btag_cut": 0.2783,
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
                    "tau_id_discriminator": "DeepTau2018v2p5VSjet",
                    "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(
                        wp=wp
                    ),
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
                    "tau_id_discriminator": "DeepTau2018v2p5VSe",
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
                    "VLoose": 3,
                    "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    "VTight": 7,
                    "VVTight": 8,
                }.items()
            ],
            "vsmu_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2018v2p5VSmu",
                    "tau_1_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_2".format(wp=wp),
                    "vsmu_tau_id_WP": "{wp}".format(wp=wp),
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
            "tau_sf_vsele_barrel": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsele_endcap": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsmu_wheel1": "nom",
            "tau_sf_vsmu_wheel2": "nom",
            "tau_sf_vsmu_wheel3": "nom",
            "tau_sf_vsmu_wheel4": "nom",
            "tau_sf_vsmu_wheel5": "nom",
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
            "tau_vsjet_vseleWP": "VVLoose",
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "tau_vsjet_vseleWP": "VVLoose",
        },
    )
    # MT / ET tau selection
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "min_tau_pt": 20.0,
            "max_tau_eta": 2.3,
            "max_tau_dz": 0.2,
            "vsjet_tau_id_bit": 4, #not a bit mask anymore but id, could rename it for clarity
            "vsele_tau_id_bit": 2,
            "vsmu_tau_id_bit": 1,
        },
    )
    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "tau_dms": "0,1,10,11",
            #"tau_sf_file": "data/jsonpog-integration/POG/TAU/2018_UL/tau.json.gz",
            "tau_ES_json_name": "tau_energy_scale",
            "tau_id_algorithm": "DeepTau2018v2p5",
            "tau_ES_shift_DM0": "nom",
            "tau_ES_shift_DM1": "nom",
            "tau_ES_shift_DM10": "nom",
            "tau_ES_shift_DM11": "nom",
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_mufake_es": "nom",
        },
    )
    # MT/MM scope Muon selection
    configuration.add_config_parameters(
        ["mt", "mm"],
        {
            "muon_index_in_pair": 0,
            "min_muon_pt": 23.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 0.3,
        },
    )
    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "deltaR_jet_veto": 0.5,
            "pairselection_min_dR": 0.1,
        },
    )
    ## all scopes MET selection
    # all scopes MET selection
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
            #"recoil_corrections_file":"data/recoil_corrections/Type1_PuppiMET_2018.root",
            #"recoil_systematics_file": "data/recoil_corrections/PuppiMETSys_2018.root",
            "applyRecoilCorrections": False,
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,
        },
    )

    ############################
    ######## Producers #########
    ############################
    # global producers
    configuration.add_producers(
        "global",
        [
            electrons.RenameElectronPt, # gives as output Electron_pt_corrected but no correction is performed, it's just a rename
            # event.RunLumiEventFilter,
            event.SampleFlags,
            event.Lumi,
            event.npartons,
            event.MetFilter, 
            #event.PUweights,
            event.LHE_Scale_weight,
            event.LHE_PDF_weight,
            event.LHE_alphaS_weight,
            event.PS_weight,
            muons.BaseMuons,
            electrons.BaseElectrons,
            jets.JetEnergyCorrection,
            jets.GoodJets,
            jets.GoodBJets,
            event.DiLeptonVeto,
            met.MetBasics,
            jets.JetID,
        ],
    )
    # common
    configuration.add_producers(
        scopes,
        [
            jets.JetCollection,
            jets.BasicJetQuantities, 
            jets.BJetCollection,
            jets.BasicBJetQuantities,
            #met.MetCorrections, 
            #met.PFMetCorrections,
            #pairquantities.DiTauPairMETQuantities,
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
            #taus.TauEnergyCorrection,
            taus.TauMassCorrection, #usually in the previous producer but here needd since i remove the pt correction file
            taus.RenameTauPt,
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
            #  scalefactors.MuonIDIso_SF,
            # pairquantities.FastMTTQuantities,
            # scalefactors.MuonIDIso_SF,
            #scalefactors.Tau_2_VsJetTauID_lt_SF,
            #scalefactors.Tau_2_VsEleTauID_SF,
            #scalefactors.Tau_2_VsMuTauID_SF,
            #triggers.MTGenerateSingleMuonTriggerFlags,
            #triggers.MTGenerateCrossTriggerFlags,
            #triggers.GenerateSingleTrailingTauTriggerFlags,
            #pairquantities.VsJetTauIDFlagOnly_2,
            # pairquantities.VsEleTauIDFlagOnly_2,
            # pairquantities.VsMuTauIDFlagOnly_2,
        ],
    )

    ################################
    ######### Modifications ########
    ################################
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.npartons],
            exclude_samples=["dyjets", "wjets", "electroweak_boson"],
        ),
    )

    #########################
    ######## OUTPUTS ########
    #########################
    configuration.add_outputs(
        scopes,
        [
            q.is_data,
            #q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_ggh_htautau,
            q.is_vbf_htautau,
            q.is_diboson,
            nanoAOD.run,
            #q.lumi,
            #q.npartons,
            nanoAOD.event,
            #q.puweight,
            #q.lhe_scale_weight,
            #q.ps_weight,
            #q.lhe_pdf_weight,
            #q.lhe_alphaS_weight,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.njets,
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
            #q.met,
            #q.metphi,
            #q.pfmet,
            #q.pfmetphi,
            #q.met_uncorrected,
            #q.metphi_uncorrected,
            #q.pfmet_uncorrected,
            #q.pfmetphi_uncorrected,
            #q.metSumEt,
            #q.metcov00,
            #q.metcov01,
            #q.metcov10,
            #q.metcov11,
            #q.pzetamissvis,
            #q.mTdileptonMET,
            #q.mt_1,
            #q.mt_2,
            #q.pt_tt,
            #q.pt_ttjj,
            #q.mt_tot,
            q.genbosonmass,
            q.gen_match_1,
            q.gen_match_2,
            #q.pzetamissvis_pf,
            #q.mTdileptonMET_pf,
            #q.mt_1_pf,
            #q.mt_2_pf,
            #q.pt_tt_pf,
            #q.pt_ttjj_pf,
            #q.mt_tot_pf,
            #q.pt_dijet,
            #q.jet_hemisphere,
            q.dimuon_veto,
            q.dilepton_veto,
            q.dielectron_veto,
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
            #nanoAOD.Jet_jetId,
        ],
    )
    configuration.add_outputs(
        "global",
        [
            q.Jet_ID,
        ],
    )
    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            #scalefactors.Tau_2_VsJetTauID_lt_SF.output_group,
            #scalefactors.Tau_2_VsEleTauID_SF.output_group,
            #scalefactors.Tau_2_VsMuTauID_SF.output_group,
            #pairquantities.VsJetTauIDFlag_2.output_group,
            #pairquantities.VsEleTauIDFlag_2.output_group,
            #pairquantities.VsMuTauIDFlag_2.output_group,
            #pairquantities.VsJetTauIDFlagOnly_2.output_group,
            # pairquantities.VsEleTauIDFlagOnly_2.output_group,
            # pairquantities.VsMuTauIDFlagOnly_2.output_group,
            #triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            #triggers.MTGenerateCrossTriggerFlags.output_group,
            #triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.extramuon_veto,
            q.dimuon_veto,
            #q.extraelec_veto,
            # q.id_wgt_mu_1,
            # q.iso_wgt_mu_1,
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
    #if "dyjets" in sample or "electroweak_boson" in sample:
    #   with defaults(shift_map={"Down": "down", "Up": "up"}):
    #        add_shift(
    #            name="tauMuFakeEs",
    #            shift_key="tau_mufake_es",
    #            scopes="mt",
    #            producers=[taus.TauPtCorrection_muFake],
    #        )
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
    )
    #########################
    # MET Recoil Shifts
    #########################
    with defaults(
        scopes=("et", "mt", "tt", "em", "ee", "mm"),
        producers=[met.ApplyRecoilCorrections],
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
    #########################
    # Pileup Shifts
    #########################
    add_shift(
        name="PileUp",
        shift_key="PU_reweighting_variation",
        shift_map={"Up": "up", "Down": "down"},
        scopes="global",
        producers=[event.PUweights],
        exclude_samples=["data"],
    )
    #########################
    # Trigger shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            "2024": [
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
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            "2024": [
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
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data"],
    )
    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    configuration = add_tauVariations(configuration, sample)
    #########################
    # Import triggersetup   #
    #########################
    #configuration = add_diTauTriggerSetup(configuration)
    
    #########################
    # Jet energy resolution and jet energy scale
    #########################
    configuration = add_jetVariations(configuration, era)

    #########################
    # btagging scale factor shape variation
    #########################
    configuration = add_btagVariations(configuration)

    #########################
    # Jet energy correction for data
    #########################
    configuration = add_jetCorrectionData(configuration, era)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
