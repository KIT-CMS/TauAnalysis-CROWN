from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults


############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

with defaults(scopes=["mt", "mm"], input=[q.pt_1, q.eta_1]):
    Muon_1_ID_SF = Producer(
        call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_varation}")',
        output=[q.id_wgt_mu_1],
    )
    Muon_1_Iso_SF = Producer(
        call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_varation}")',
        output=[q.iso_wgt_mu_1],
    )
    # --- from our measurement ---
    TauEmbeddingMuonIDSF_1_MC = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")',
        output=[q.id_wgt_mu_1],
    )
    TauEmbeddingMuonIsoSF_1_MC = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")',
        output=[q.iso_wgt_mu_1],
    )
    MTGenerateSingleMuonTriggerSF_MC = ExtendedVectorProducer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_trigger_sf}", "mc", {mc_muon_trg_extrapolation})',
        output="flagname",
        vec_config="singlemuon_trigger_sf_mc",
    )

with defaults(scopes=["em", "mm"], input=[q.pt_2, q.eta_2]):
    Muon_2_ID_SF = Producer(
        call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_varation}")',
        output=[q.id_wgt_mu_2],
    )
    Muon_2_Iso_SF = Producer(
        call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_varation}")',
        output=[q.iso_wgt_mu_2],
    )
    # --- from our measurement ---
    TauEmbeddingMuonIDSF_2_MC = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")',
        output=[q.id_wgt_mu_2],
    )
    TauEmbeddingMuonIsoSF_2_MC = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")',
        output=[q.iso_wgt_mu_2],
    )

############################
# Tau ID/ISO SF
# The readout is done via correctionlib
############################

with defaults(scopes=["tt"]):
    Tau_1_VsJetTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsJet_tt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}")',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}")',
        input=[q.eta_1, q.gen_match_1],
        output="tau_1_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}")',
        input=[q.eta_1, q.gen_match_1],
        output="tau_1_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsJet_tt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}")',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
    call='physicsobject::tau::scalefactor::Id_vsJet_lt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tau30to35}", "{tau_sf_vsjet_tau35to40}", "{tau_sf_vsjet_tau40to500}", "{tau_sf_vsjet_tau500to1000}", "{tau_sf_vsjet_tau1000toinf}")',
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["et", "mt"],
    vec_config="vsjet_tau_id",
)

with defaults(scopes=["et", "mt", "tt"], input=[q.eta_2, q.gen_match_2],):
    Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}")',
        output="tau_2_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}")',
        output="tau_2_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )

#########################
# Electron ID/ISO SF
#########################

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2]):
    Ele_2_IDWP90_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
        output=[q.id_wgt_ele_wp90nonIso_2],
    )
    Ele_2_IDWP80_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
        output=[q.id_wgt_ele_wp80nonIso_2],
    )
    # --- from our measurement ---
    TauEmbeddingElectronIDSF_2_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")',
        output=[q.id_wgt_ele_2],
    )
    TauEmbeddingElectronIsoSF_2_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")',
        output=[q.iso_wgt_ele_2],
    )

with defaults(scopes=["em", "ee", "et"], input=[q.pt_1, q.eta_1]):
    Ele_1_IDWP90_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
        output=[q.id_wgt_ele_wp90nonIso_1],
    )
    Ele_1_IDWP80_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
        output=[q.id_wgt_ele_wp80nonIso_1],
    )
    # --- from our measurement ---
    TauEmbeddingElectronIDSF_1_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")',
        output=[q.id_wgt_ele_1],
    )
    TauEmbeddingElectronIsoSF_1_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")',
        output=[q.iso_wgt_ele_1],
    )

ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(  # --- from our measurement ---
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_trigger_sf}", "mc", {mc_electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)

#########################
# b-tagging SF
#########################

btagging_SF = Producer(
    call='physicsobject::jet::scalefactor::Btagging({df}, correctionManager, {output}, {input}, "{btag_sf_file}", "{btag_corr_algo}", "{btag_sf_variation}")',
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

#########################
# Grouped SF
#########################

with defaults(call=None, input=None, output=None):
    MuonIDIso_SF = ProducerGroup(
        scopes=["mt", "em", "mm"],
        subproducers={
            "mt": [Muon_1_ID_SF, Muon_1_Iso_SF],
            "em": [Muon_2_ID_SF, Muon_2_Iso_SF],
            "mm": [Muon_1_ID_SF, Muon_1_Iso_SF, Muon_2_ID_SF, Muon_2_Iso_SF],
        },
    )
    TauID_SF = ProducerGroup(
        scopes=["tt", "mt", "et"],
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

    EleID_SF = ProducerGroup(
        scopes=["em", "ee", "et"],
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
