from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..scripts.ProducerWrapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    AutoExtendedVectorProducer as ExtendedVectorProducer,
    scopes,
)

############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

with scopes(["mt", "mm"]):
    Muon_1_ID_SF_RooWorkspace = Producer(
        call='scalefactor::muon::id_rooworkspace({df}, {input}, {output}, "{muon_sf_workspace}", "{muon_sf_id_name}", "{muon_sf_id_args}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_mu_1],
    )
    Muon_1_Iso_SF_RooWorkspace = Producer(
        call='scalefactor::muon::iso_rooworkspace({df}, {input}, {output}, "{muon_sf_workspace}", "{muon_sf_iso_name}", "{muon_sf_iso_args}")',
        input=[q.pt_1, q.eta_1, q.iso_1],
        output=[q.iso_wgt_mu_1],
    )
    Muon_1_ID_SF = Producer(
        call='scalefactor::muon::id({df}, correctionManager, {input}, "{muon_sf_year_id}", "{muon_sf_varation}", {output}, "{muon_sf_file}", "{muon_id_sf_name}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_mu_1],
    )
    Muon_1_Iso_SF = Producer(
        call='scalefactor::muon::iso({df}, correctionManager, {input}, "{muon_sf_year_id}", "{muon_sf_varation}", {output}, "{muon_sf_file}", "{muon_iso_sf_name}")',
        input=[q.pt_1, q.eta_1],
        output=[q.iso_wgt_mu_1],
    )

with scopes(["em", "mm"]):
    Muon_2_ID_SF_RooWorkspace = Producer(
        call='scalefactor::muon::id_rooworkspace({df}, {input}, {output}, "{muon_sf_workspace}", "{muon_sf_id_name}", "{muon_sf_id_args}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_mu_2],
    )
    Muon_2_Iso_SF_RooWorkspace = Producer(
        call='scalefactor::muon::iso_rooworkspace({df}, {input}, {output}, "{muon_sf_workspace}", "{muon_sf_iso_name}", "{muon_sf_iso_args}")',
        input=[q.pt_2, q.eta_2, q.iso_2],
        output=[q.iso_wgt_mu_2],
    )
    Muon_2_ID_SF = Producer(
        call='scalefactor::muon::id({df}, correctionManager, {input}, "{muon_sf_year_id}", "{muon_sf_varation}", {output}, "{muon_sf_file}", "{muon_id_sf_name}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_mu_2],
    )
    Muon_2_Iso_SF = Producer(
        call='scalefactor::muon::iso({df}, correctionManager, {input}, "{muon_sf_year_id}", "{muon_sf_varation}", {output}, "{muon_sf_file}", "{muon_iso_sf_name}")',
        input=[q.pt_2, q.eta_2],
        output=[q.iso_wgt_mu_2],
    )

with scopes(["mt", "em", "mm"]):
    MuonIDIso_SF = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers={
            "mt": [
                Muon_1_ID_SF,
                Muon_1_Iso_SF,
            ],
            "em": [
                Muon_2_ID_SF,
                Muon_2_Iso_SF,
            ],
            "mm": [
                Muon_1_ID_SF,
                Muon_1_Iso_SF,
                Muon_2_ID_SF,
                Muon_2_Iso_SF,
            ],
        },
    )
    MuonIDIso_SF_RooWorkspace = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers={
            "mt": [
                Muon_1_ID_SF_RooWorkspace,
                Muon_1_Iso_SF_RooWorkspace,
            ],
            "em": [
                Muon_2_ID_SF_RooWorkspace,
                Muon_2_Iso_SF_RooWorkspace,
            ],
            "mm": [
                Muon_1_ID_SF_RooWorkspace,
                Muon_1_Iso_SF_RooWorkspace,
                Muon_2_ID_SF_RooWorkspace,
                Muon_2_Iso_SF_RooWorkspace,
            ],
        },
    )

############################
# Tau ID/ISO SF
# The readout is done via correctionlib
############################

with scopes(["tt"]):
    Tau_1_VsJetTauID_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsJet_tt({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}", "{tau_vsjet_sf_dependence}", "{tau_vsjet_vseleWP}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsEle({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.eta_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsMu({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.eta_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsJet_tt({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}", "{tau_vsjet_sf_dependence}", "{tau_vsjet_vseleWP}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

with scopes(["et", "mt"]):
    Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsJet_lt({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_sf_vsjet_tau30to35}", "{tau_sf_vsjet_tau35to40}", "{tau_sf_vsjet_tau40to500}", "{tau_sf_vsjet_tau500to1000}", "{tau_sf_vsjet_tau1000toinf}", "{tau_vsjet_sf_dependence}","{tau_vsjet_vseleWP}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

with scopes(["tt", "mt", "et"]):
    Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsEle({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.eta_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsMu({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}", {output}, "{tau_sf_file}", "{tau_id_discriminator}")',
        input=[q.eta_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    TauID_SF = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers={
            "tt": [
                Tau_1_VsJetTauID_SF,
                Tau_1_VsEleTauID_SF,
                Tau_1_VsMuTauID_SF,
                Tau_2_VsJetTauID_tt_SF,
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "mt": [
                Tau_2_VsJetTauID_lt_SF,
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "et": [
                Tau_2_VsJetTauID_lt_SF,
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
        },
    )

#########################
# Electron ID/ISO SF
#########################

with scopes(["ee"]):
    Ele_2_IDWP90_SF = Producer(
        call='scalefactor::electron::id({df}, correctionManager, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", {output}, "{ele_sf_file}", "{ele_id_sf_name}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_ele_wp90nonIso_2],
    )
    Ele_2_IDWP80_SF = Producer(
        call='scalefactor::electron::id({df}, correctionManager, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", {output}, "{ele_sf_file}", "{ele_id_sf_name}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_ele_wp80nonIso_2],
    )

with scopes(["em", "ee", "et"]):
    Ele_1_IDWP90_SF = Producer(
        call='scalefactor::electron::id({df}, correctionManager, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", {output}, "{ele_sf_file}", "{ele_id_sf_name}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_ele_wp90nonIso_1],
    )
    Ele_1_IDWP80_SF = Producer(
        call='scalefactor::electron::id({df}, correctionManager, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", {output}, "{ele_sf_file}", "{ele_id_sf_name}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_ele_wp80nonIso_1],
    )
    EleID_SF = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers={
            "em": [Ele_1_IDWP90_SF, Ele_1_IDWP80_SF],
            "ee": [
                Ele_1_IDWP90_SF,
                Ele_1_IDWP80_SF,
                Ele_2_IDWP90_SF,
                Ele_2_IDWP80_SF,
            ],
            "et": [Ele_1_IDWP90_SF, Ele_1_IDWP80_SF],
        },
    )

###################################
# Trigger Scalefactors coming from our measurements
###################################

MTGenerateSingleMuonTriggerSF_MC = ExtendedVectorProducer(
    call='scalefactor::embedding::muon_sf({df}, correctionManager, {input}, {output}, "{mc_muon_sf_file}", "mc", "{mc_trigger_sf}", {mc_muon_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["mt", "mm"],
    vec_config="singlemuon_trigger_sf_mc",
)
ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(
    call='scalefactor::embedding::electron_sf({df}, correctionManager, {input}, {output}, "{mc_electron_sf_file}", "mc", "{mc_trigger_sf}" , {mc_electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)

####################################
# Electron and Muon SFs coming from our measurements
####################################

with scopes(["mt", "mm"]):
    TauEmbeddingMuonIDSF_1_MC = Producer(
        call='scalefactor::embedding::muon_sf({df}, correctionManager, {input}, {output}, "{mc_muon_sf_file}", "mc", "{mc_muon_id_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_mu_1],
    )
    TauEmbeddingMuonIsoSF_1_MC = Producer(
        call='scalefactor::embedding::muon_sf({df}, correctionManager, {input}, {output}, "{mc_muon_sf_file}", "mc", "{mc_muon_iso_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.iso_wgt_mu_1],
    )

with scopes(["mm", "em"]):
    TauEmbeddingMuonIDSF_2_MC = Producer(
        call='scalefactor::embedding::muon_sf({df}, correctionManager, {input}, {output}, "{mc_muon_sf_file}", "mc", "{mc_muon_id_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_mu_2],
    )
    TauEmbeddingMuonIsoSF_2_MC = Producer(
        call='scalefactor::embedding::muon_sf({df}, correctionManager, {input}, {output}, "{mc_muon_sf_file}", "mc", "{mc_muon_iso_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.iso_wgt_mu_2],
    )

# Electron ID/Iso/Trigger SFS

with scopes(["et", "ee", "em"]):
    TauEmbeddingElectronIDSF_1_MC = Producer(
        call='scalefactor::embedding::electron_sf({df}, correctionManager, {input}, {output}, "{mc_electron_sf_file}", "mc", "{mc_electron_id_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_ele_1],
    )
    TauEmbeddingElectronIsoSF_1_MC = Producer(
        call='scalefactor::embedding::electron_sf({df}, correctionManager, {input}, {output}, "{mc_electron_sf_file}", "mc", "{mc_electron_iso_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.iso_wgt_ele_1],
    )

with scopes(["ee"]):
    TauEmbeddingElectronIDSF_2_MC = Producer(
        call='scalefactor::embedding::electron_sf({df}, correctionManager, {input}, {output}, "{mc_electron_sf_file}", "mc", "{mc_electron_id_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_ele_2],
    )
    TauEmbeddingElectronIsoSF_2_MC = Producer(
        call='scalefactor::embedding::electron_sf({df}, correctionManager, {input}, {output}, "{mc_electron_sf_file}", "mc", "{mc_electron_iso_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.iso_wgt_ele_2],
    )

#########################
# b-tagging SF
#########################

btagging_SF = Producer(
    call='scalefactor::jet::btagSF({df}, correctionManager, {input}, "{btag_sf_variation}", {output}, "{btag_sf_file}", "{btag_corr_algo}")',
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.BJet_discriminator,
        nanoAOD.Jet_flavor,
        q.good_jets_mask,
        q.good_bjets_mask,
        q.jet_overlap_veto_mask,
    ],
    output=[q.btag_weight],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)
