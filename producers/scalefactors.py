from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
from code_generation.producer import ExtendedVectorProducer


############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

Muon_1_ID_SF = Producer(
    name="MuonID_SF",
    call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_varation}")',
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_mu_1],
    scopes=["mt", "mm"],
)
Muon_1_Iso_SF = Producer(
    name="MuonIso_SF",
    call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_varation}")',
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_mu_1],
    scopes=["mt", "mm"],
)
Muon_2_ID_SF = Producer(
    name="MuonID_SF",
    call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_varation}")',
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_mu_2],
    scopes=["em", "mm"],
)
Muon_2_Iso_SF = Producer(
    name="MuonIso_SF",
    call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_varation}")',
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_mu_2],
    scopes=["em", "mm"],
)
MuonIDIso_SF = ProducerGroup(
    name="MuonIDIso_SF",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "em", "mm"],
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

############################
# Tau ID/ISO SF
# The readout is done via correctionlib
############################
Tau_1_VsJetTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsJetTauID_SF",
    call='physicsobject::tau::scalefactor::Id_vsJet_tt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}")',
    input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
    output="tau_1_vsjet_sf_outputname",
    scope=["tt"],
    vec_config="vsjet_tau_id",
)
Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsEleTauID_SF",
    call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}")',
    input=[q.eta_1, q.gen_match_1],
    output="tau_1_vsele_sf_outputname",
    scope=["tt"],
    vec_config="vsele_tau_id",
)
Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsMuTauID_SF",
    call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}")',
    input=[q.eta_1, q.gen_match_1],
    output="tau_1_vsmu_sf_outputname",
    scope=["tt"],
    vec_config="vsmu_tau_id",
)
Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
    name="Tau_2_VsJetTauID_lt_SF",
    call='physicsobject::tau::scalefactor::Id_vsJet_lt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tau30to35}", "{tau_sf_vsjet_tau35to40}", "{tau_sf_vsjet_tau40to500}", "{tau_sf_vsjet_tau500to1000}", "{tau_sf_vsjet_tau1000toinf}")',
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["et", "mt"],
    vec_config="vsjet_tau_id",
)
Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
    name="Tau_2_VsJetTauID_tt_SF",
    call='physicsobject::tau::scalefactor::Id_vsJet_tt({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_vsjet_sf_dependence}", "{tau_sf_vsjet_tauDM0}", "{tau_sf_vsjet_tauDM1}", "{tau_sf_vsjet_tauDM10}", "{tau_sf_vsjet_tauDM11}")',
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["tt"],
    vec_config="vsjet_tau_id",
)
Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
    name="Tau_2_VsEleTauID_SF",
    call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", "{tau_sf_vsele_barrel}", "{tau_sf_vsele_endcap}")',
    input=[q.eta_2, q.gen_match_2],
    output="tau_2_vsele_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="vsele_tau_id",
)
Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
    name="Tau_2_VsMuTauID_SF",
    call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsmu_tau_id_WP}", "{tau_sf_vsmu_wheel1}", "{tau_sf_vsmu_wheel2}", "{tau_sf_vsmu_wheel3}", "{tau_sf_vsmu_wheel4}", "{tau_sf_vsmu_wheel5}")',
    input=[q.eta_2, q.gen_match_2],
    output="tau_2_vsmu_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="vsmu_tau_id",
)
TauID_SF = ProducerGroup(
    name="TauID_SF",
    call=None,
    input=None,
    output=None,
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

#########################
# Electron ID/ISO SF
#########################
Ele_1_IDWP90_SF = Producer(
    name="Ele_IDWP90_SF",
    call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_ele_wp90nonIso_1],
    scopes=["em", "ee", "et"],
)
Ele_2_IDWP90_SF = Producer(
    name="Ele_IDWP90_SF",
    call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_ele_wp90nonIso_2],
    scopes=["ee"],
)
Ele_1_IDWP80_SF = Producer(
    name="Ele_IDWP80_SF",
    call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_ele_wp80nonIso_1],
    scopes=["em", "ee", "et"],
)
Ele_2_IDWP80_SF = Producer(
    name="Ele_IDWP80_SF",
    call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80noiso", "{ele_sf_varation}", "{ele_sf_file}", "{ele_id_sf_name}, "{ele_sf_varation}")',
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_ele_wp80nonIso_2],
    scopes=["ee"],
)
EleID_SF = ProducerGroup(
    name="EleID_SF",
    call=None,
    input=None,
    output=None,
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

###################################
# Trigger Scalefactors coming from our measurements
###################################
MTGenerateSingleMuonTriggerSF_MC = ExtendedVectorProducer(
    name="MTGenerateSingleMuonTriggerSF_MC",
    call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_trigger_sf}", "mc", {mc_muon_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["mt", "mm"],
    vec_config="singlemuon_trigger_sf_mc",
)

ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(
    name="ETGenerateSingleElectronTriggerSF_MC",
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_trigger_sf}", "mc", {mc_electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)

####################################
# Electron and Muon SFs coming from our measurements
####################################
TauEmbeddingMuonIDSF_1_MC = Producer(
    name="TauEmbeddingMuonIDSF_1_MC",
    call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")',
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_mu_1],
    scopes=["mt", "mm"],
)

TauEmbeddingMuonIDSF_2_MC = Producer(
    name="TauEmbeddingMuonIDSF_2_MC",
    call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")',
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_mu_2],
    scopes=["mm", "em"],
)

TauEmbeddingMuonIsoSF_1_MC = Producer(
    name="TauEmbeddingMuonIsoSF_1_MC",
    call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")',
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_mu_1],
    scopes=["mt", "mm"],
)

TauEmbeddingMuonIsoSF_2_MC = Producer(
    name="TauEmbeddingMuonIsoSF_2_MC",
    call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")',
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_mu_2],
    scopes=["mm", "em"],
)

# Electron ID/Iso/Trigger SFS

TauEmbeddingElectronIDSF_1_MC = Producer(
    name="TauEmbeddingElectronIDSF_1_MC",
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")',
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_ele_1],
    scopes=["et", "ee", "em"],
)

TauEmbeddingElectronIDSF_2_MC = Producer(
    name="TauEmbeddingElectronIDSF_2_MC",
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")',
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_ele_2],
    scopes=["ee"],
)

TauEmbeddingElectronIsoSF_1_MC = Producer(
    name="TauEmbeddingElectronIsoSF_1_MC",
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")',
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_ele_1],
    scopes=["et", "ee", "em"],
)

TauEmbeddingElectronIsoSF_2_MC = Producer(
    name="TauEmbeddingElectronIsoSF_2_MC",
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")',
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_ele_2],
    scopes=["ee"],
)
#########################
# b-tagging SF
#########################
btagging_SF = Producer(
    name="btagging_SF",
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
