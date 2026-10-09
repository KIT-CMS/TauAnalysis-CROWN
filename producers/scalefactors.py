from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer, ProducerGroup, ExtendedVectorProducer, SwitchProducer

############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

with defaults(scopes=["mt", "mm"], input=[q.pt_1, q.eta_1]):
    Muon_1_ID_SF = Producer(
        call='''physicsobject::muon::scalefactor::IsoAndID({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_id_variation}")''',
        output=[q.id_wgt_mu_1],
    )
    Muon_1_Iso_SF = Producer(
        call='''physicsobject::muon::scalefactor::IsoAndID({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_iso_variation}")''',
        output=[q.iso_wgt_mu_1],
    )
    # --- from our measurement ---
    PrivateMuonIDSF_1_MC = Producer(
        call='''embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")''',
        output=[q.id_wgt_mu_1],
    )
    PrivateMuonIsoSF_1_MC = Producer(
        call='''embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")''',
        output=[q.iso_wgt_mu_1],
    )
    MTGenerateSingleMuonTriggerSF_MC = ExtendedVectorProducer(
        call='''embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_trigger_sf}", "mc", {mc_trg_extrapolation})''',
        output="flagname",
        vec_config="singlemuon_trigger_sf_mc",
    )

with defaults(scopes=["em", "mm"], input=[q.pt_2, q.eta_2]):
    Muon_2_ID_SF = Producer(
        call='''physicsobject::muon::scalefactor::IsoAndID({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_id_variation}")''',
        output=[q.id_wgt_mu_2],
    )
    Muon_2_Iso_SF = Producer(
        call='''physicsobject::muon::scalefactor::IsoAndID({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_iso_variation}")''',
        output=[q.iso_wgt_mu_2],
    )
    # --- from our measurement ---
    PrivateMuonIDSF_2_MC = Producer(
        call='''embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_id_sf}", "mc")''',
        output=[q.id_wgt_mu_2],
    )
    PrivateMuonIsoSF_2_MC = Producer(
        call='''embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_muon_sf_file}", "{mc_muon_iso_sf}", "mc")''',
        output=[q.iso_wgt_mu_2],
    )

############################
# Tau ID/ISO SF
# The readout is done via correctionlib
############################

with defaults(scopes=["tt"]):
    Tau_1_VsJetTauID_SF_v12 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSjet", 
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_id_vsjet_DM0}", 
            "{tau_id_vsjet_DM1}", 
            "{tau_id_vsjet_DM10}", 
            "{tau_id_vsjet_DM11}")''',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    # duplicate of the one below...
    Tau_1_VsJetTauID_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_discriminator}", 
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_sf_vsjet_DM0}", 
            "{tau_sf_vsjet_DM1}", 
            "{tau_sf_vsjet_DM10}", 
            "{tau_sf_vsjet_DM11}")''',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_1_VsJetTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSjet", 
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_vsmuWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_id_vsjet_DM0_pt20to40}",
            "{tau_id_vsjet_DM0_pt40to60}",
            "{tau_id_vsjet_DM0_pt60toInf}",
            "{tau_id_vsjet_DM1_pt20to40}",
            "{tau_id_vsjet_DM1_pt40to60}",
            "{tau_id_vsjet_DM1_pt60toInf}",
            "{tau_id_vsjet_DM10_pt20to40}",
            "{tau_id_vsjet_DM10_pt40to60}",
            "{tau_id_vsjet_DM10_pt60toInf}",
            "{tau_id_vsjet_DM11_pt20to40}",
            "{tau_id_vsjet_DM11_pt40to60}",
            "{tau_id_vsjet_DM11_pt60toInf}")''',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_1_VsEleTauID_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsEle(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSe",
            "{vsele_tau_id_WP}",
            "{era}",
            "{tau_id_vsele_barrel}", 
            "{tau_id_vsele_endcap}")''',
        input=[q.eta_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsEle(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSe",
            "{vsele_tau_id_WP}",
            "{era}",
            "{tau_id_vsele_DM0_barrel}", 
            "{tau_id_vsele_DM1_barrel}", 
            "{tau_id_vsele_DM10_barrel}", 
            "{tau_id_vsele_DM11_barrel}",
            "{tau_id_vsele_DM0_endcap}", 
            "{tau_id_vsele_DM1_endcap}", 
            "{tau_id_vsele_DM10_endcap}", 
            "{tau_id_vsele_DM11_endcap}")''',
        input=[q.eta_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    # duplicate of the one below...
    Tau_1_VsMuTauID_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsMu(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_discriminator}", 
            "{vsmu_tau_id_WP}", 
            "{vsele_tau_id_WP}", 
            "{vsjet_tau_id_WP}", 
            "{era}", 
            "{tau_sf_vsmu_wheel1}", 
            "{tau_sf_vsmu_wheel2}", 
            "{tau_sf_vsmu_wheel3}", 
            "{tau_sf_vsmu_wheel4}", 
            "{tau_sf_vsmu_wheel5}")''',
        input=[q.eta_1, q.gen_match_1],
        output="tau_1_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsMu(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSmu",
            "{vsmu_tau_id_WP}", 
            "{vsele_tau_id_WP}", 
            "{vsjet_tau_id_WP}", 
            "{era}", 
            "{tau_id_vsmu_wheel1}", 
            "{tau_id_vsmu_wheel2}", 
            "{tau_id_vsmu_wheel3}", 
            "{tau_id_vsmu_wheel4}", 
            "{tau_id_vsmu_wheel5}")''',
        input=[q.eta_1, q.gen_match_1],
        output="tau_1_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSjet",
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_id_vsjet_DM0}", 
            "{tau_id_vsjet_DM1}", 
            "{tau_id_vsjet_DM10}", 
            "{tau_id_vsjet_DM11}")''',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

with defaults(
    scopes=["et", "mt"],
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    vec_config="vsjet_tau_id",
):
    Tau_2_VsJetTauID_lt_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet_lt(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_discriminator}",
            {vec_open}{tau_dms}{vec_close},
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_sf_vsjet_tau30to35}",
            "{tau_sf_vsjet_tau35to40}",
            "{tau_sf_vsjet_tau40to500}",
            "{tau_sf_vsjet_tau500to1000}",
            "{tau_sf_vsjet_tau1000toinf}")''',
    )
    Tau_2_VsJetTauID_lt_SF_dm_binned_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_discriminator}",
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_sf_vsjet_1prong0pizero}",
            "{tau_sf_vsjet_1prong1pizero}",
            "{tau_sf_vsjet_3prong0pizero}",
            "{tau_sf_vsjet_3prong1pizero}")''',
    )
    Tau_2_VsJetTauID_lt_SF_dm_pt_binned_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_discriminator}",
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_sf_vsjet_1prong0pizero20to40}",
            "{tau_sf_vsjet_1prong0pizero40toInf}",
            "{tau_sf_vsjet_1prong1pizero20to40}",
            "{tau_sf_vsjet_1prong1pizero40toInf}",
            "{tau_sf_vsjet_3prong0pizero20to40}",
            "{tau_sf_vsjet_3prong0pizero40toInf}",
            "{tau_sf_vsjet_3prong1pizero20to40}",
            "{tau_sf_vsjet_3prong1pizero40toInf}")''',
    )
    
    Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet_lt(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSjet",
            {vec_open}{tau_dms}{vec_close},
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_id_vsjet_tau30to35}",
            "{tau_id_vsjet_tau35to40}",
            "{tau_id_vsjet_tau40to500}",
            "{tau_id_vsjet_tau500to1000}",
            "{tau_id_vsjet_tau1000toinf}")''',
    )

    Tau_2_VsJetTauID_lt_SF_dm_binned = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSjet",
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_id_vsjet_1prong0pizero}",
            "{tau_id_vsjet_1prong1pizero}",
            "{tau_id_vsjet_3prong0pizero}",
            "{tau_id_vsjet_3prong1pizero}")''',
    )

    Tau_2_VsJetTauID_lt_SF_dm_pt_binned = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSjet",
            "{vsjet_tau_id_WP}",
            "{tau_vsjet_vseleWP}",
            "{tau_vsjet_sf_dependence}",
            "{tau_id_vsjet_1prong0pizero20to40}",
            "{tau_id_vsjet_1prong0pizero40toInf}",
            "{tau_id_vsjet_1prong1pizero20to40}",
            "{tau_id_vsjet_1prong1pizero40toInf}",
            "{tau_id_vsjet_3prong0pizero20to40}",
            "{tau_id_vsjet_3prong0pizero40toInf}",
            "{tau_id_vsjet_3prong1pizero20to40}",
            "{tau_id_vsjet_3prong1pizero40toInf}")''',
    )


with defaults(scopes=["et", "mt", "tt"]):
    Tau_2_VsEleTauID_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsEle(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSe",
            "{vsele_tau_id_WP}",
            "{era}",
            "{tau_id_vsele_barrel}",
            "{tau_id_vsele_endcap}")''',
        input=[q.eta_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsEle(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_id_algorithm}VSe",
            "{vsele_tau_id_WP}",
            "{era}",
            "{tau_id_vsele_DM0_barrel}", 
            "{tau_id_vsele_DM1_barrel}", 
            "{tau_id_vsele_DM10_barrel}", 
            "{tau_id_vsele_DM11_barrel}",
            "{tau_id_vsele_DM0_endcap}", 
            "{tau_id_vsele_DM1_endcap}", 
            "{tau_id_vsele_DM10_endcap}", 
            "{tau_id_vsele_DM11_endcap}")''',
        input=[q.eta_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    # duplicate of the one below...
    Tau_2_VsMuTauID_SF_Run2 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsMu(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_discriminator}", 
            "{vsmu_tau_id_WP}", 
            "{vsele_tau_id_WP}", 
            "{vsjet_tau_id_WP}", 
            "{era}", 
            "{tau_sf_vsmu_wheel1}", 
            "{tau_sf_vsmu_wheel2}", 
            "{tau_sf_vsmu_wheel3}", 
            "{tau_sf_vsmu_wheel4}", 
            "{tau_sf_vsmu_wheel5}")''',
        input=[q.eta_2, q.gen_match_2],
        output="tau_2_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsMu(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSmu", 
            "{vsmu_tau_id_WP}", 
            "{vsele_tau_id_WP}", 
            "{vsjet_tau_id_WP}", 
            "{era}", 
            "{tau_id_vsmu_wheel1}", 
            "{tau_id_vsmu_wheel2}", 
            "{tau_id_vsmu_wheel3}", 
            "{tau_id_vsmu_wheel4}", 
            "{tau_id_vsmu_wheel5}")''',
        input=[q.eta_2, q.gen_match_2],
        output="tau_2_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    # for run 3, same in all channels
    Tau_2_VsJetTauID_SF_v12 = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSjet", 
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_id_vsjet_DM0}", 
            "{tau_id_vsjet_DM1}", 
            "{tau_id_vsjet_DM10}", 
            "{tau_id_vsjet_DM11}")''',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_2_VsJetTauID_SF = ExtendedVectorProducer(
        call='''physicsobject::tau::scalefactor::Id_vsJet(
            {df}, 
            correctionManager, 
            {output}, 
            {input}, 
            "{tau_sf_file}", 
            "{tau_id_algorithm}VSjet", 
            "{vsjet_tau_id_WP}", 
            "{tau_vsjet_vseleWP}", 
            "{tau_vsjet_vsmuWP}", 
            "{tau_vsjet_sf_dependence}", 
            "{tau_id_vsjet_DM0_pt20to40}",
            "{tau_id_vsjet_DM0_pt40to60}",
            "{tau_id_vsjet_DM0_pt60toInf}",
            "{tau_id_vsjet_DM1_pt20to40}",
            "{tau_id_vsjet_DM1_pt40to60}",
            "{tau_id_vsjet_DM1_pt60toInf}",
            "{tau_id_vsjet_DM10_pt20to40}",
            "{tau_id_vsjet_DM10_pt40to60}",
            "{tau_id_vsjet_DM10_pt60toInf}",
            "{tau_id_vsjet_DM11_pt20to40}",
            "{tau_id_vsjet_DM11_pt40to60}",
            "{tau_id_vsjet_DM11_pt60toInf}")''',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

#########################
# Electron ID/ISO SF with isolation
#########################

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2]):
    # --- from our measurement ---
    PrivateElectronIDSF_2_MC = Producer(
        call='''embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")''',
        output=[q.id_wgt_ele_2],
    )
    PrivateElectronIsoSF_2_MC = Producer(
        call='''embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")''',
        output=[q.iso_wgt_ele_2],
    )

with defaults(scopes=["em", "ee", "et"], input=[q.pt_1, q.eta_1]):
    # --- from our measurement ---
    PrivateElectronIDSF_1_MC = Producer(
        call='''embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")''',
        output=[q.id_wgt_ele_1],
    )
    PrivateElectronIsoSF_1_MC = Producer(
        call='''embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")''',
        output=[q.iso_wgt_ele_1],
   )

with defaults(scopes=["em", "ee", "et"], input=[q.pt_1, q.eta_1, q.phi_1]):
    Ele_1_IDWP90_SF = Producer(
        call='''physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")''',
        output=[q.id_wgt_ele_wp90iso_1],
    )
    Ele_1_IDWP80_SF = Producer(
        call='''physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")''',
        output=[q.id_wgt_ele_wp80iso_1],
    )

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2, q.phi_2]):
    Ele_2_IDWP90_SF = Producer(
        call='''physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")''',
        output=[q.id_wgt_ele_wp90iso_2],
    )
    Ele_2_IDWP80_SF = Producer(
        call='''physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")''',
        output=[q.id_wgt_ele_wp80iso_2],
    )

ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(  # --- from our measurement ---
    call='''embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_trigger_sf}", "mc", {mc_trg_extrapolation})''',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scopes=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)

######################
# Trigger scale factors Run 3
######################

with defaults(scopes=["et"], input=[q.pt_1, q.eta_1]):
    SingleElectronTriggerSF = Producer(
        call='''physicsobject::electron::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_single_flag}", "{singleelctron_trigger_era}", "{trigger_electron_single_path}", "{singleelectron_trigger_sf_file}", "Electron-HLT-SF", "{trigger_electron_variation}")''',
        output=[q.trg_sf_single],
    )
    CrossElectronTriggerSF = Producer(
        call='''physicsobject::electron::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_cross_flag}", "{singleelctron_trigger_era}", "{trigger_electron_cross_path}", "{eletau_cross_trigger_leg1_sf_file}", "Electron-HLT-SF", "{trigger_electron_variation}")''',
        output=[q.trg_sf_lepton],
    )

with defaults(scopes=["mt"], input=[q.pt_1, q.eta_1]):
    SingleMuonTriggerSF = Producer(
        call='''physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_single_flag}", "{muon_sf_file}", "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", "{trigger_muon_variation}")''',
        output=[q.trg_sf_single],
    )
    CrossMuonTriggerSF = Producer(
        call='''physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_cross_flag}", "{mutau_cross_trigger_leg1_sf_file}", "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight", "{trigger_muon_variation}")''',
        output=[q.trg_sf_lepton],
    )

# the muon is leg 2 in em (the electron is leg 1), the single muon trigger is the only trigger used
SingleMuonTriggerSF_em = Producer(
    call='''physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_single_flag}", "{muon_sf_file}", "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", "{trigger_muon_variation}")''',
    input=[q.pt_2, q.eta_2],
    output=[q.trg_wgt],
    scopes=["em"],
)

TauCrossTriggerSF_Leg = Producer(
    call='''physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_cross_flag}", "{tau_sf_file}", "tau_trigger", "{trigger_tau_trigger_name}", "{ditau_trigger_wp}", "sf", "{trigger_tau_variation}")''',
    input=[q.pt_2, q.tau_decaymode_2],
    output=[q.trg_sf_tau],
    scopes=["et", "mt"],
)

with defaults(scopes=["tt"]):
    DiTauTriggerSF_1 = Producer(
        call='''physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_ditau_flag}", "{tau_sf_file}", "tau_trigger", "ditau", "{ditau_trigger_wp}", "sf", "{trigger_ditau_variation}")''',
        input=[q.pt_1, q.tau_decaymode_1],
        output=[q.trg_sf_ditau_1],
    )
    DiTauTriggerSF_2 = Producer(
        call='''physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_ditau_flag}", "{tau_sf_file}", "tau_trigger", "ditau", "{ditau_trigger_wp}", "sf", "{trigger_ditau_variation}")''',
        input=[q.pt_2, q.tau_decaymode_2],
        output=[q.trg_sf_ditau_2],
    )
    DiTauJet_TauTriggerSF_1 = Producer(
        call='''physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_ditaujet_flag}", "{tau_sf_file}", "tau_trigger", "ditaujet", "{ditau_trigger_wp}", "sf", "{trigger_ditaujet_variation}")''',
        input=[q.pt_1, q.tau_decaymode_1],
        output=[q.trg_sf_ditaujet_1],
    )
    DiTauJet_TauTriggerSF_2 = Producer(
        call='''physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{trigger_ditaujet_flag}", "{tau_sf_file}", "tau_trigger", "ditaujet", "{ditau_trigger_wp}", "sf", "{trigger_ditaujet_variation}")''',
        input=[q.pt_2, q.tau_decaymode_2],
        output=[q.trg_sf_ditaujet_2],
    )
    # the jet leg has no centrally provided POG SF, it is provided by the HHbbTauTau group
    DiTauJet_JetTriggerSF_Leg = Producer(
        call='''trigger::JetLegScaleFactor({df}, correctionManager, {output}, {input}, "{trigger_ditaujet_flag}", "{trigger_jet_leg_file}", "{trigger_jet_leg_name}", "{trigger_jet_variation}", "{trigger_jet_syst_var}")''',
        input=[q.jet_p4_1],
        output=[q.trg_sf_jet],
    )

SingleOrCrossTriggerSF = Producer(
    call='''trigger::SingleOrCrossScaleFactor({df}, {output}, "{trigger_single_flag}", {input})''',
    input=[q.trg_sf_single, q.trg_sf_lepton, q.trg_sf_tau],
    output=[q.trg_wgt],
    scopes=["et", "mt"],
)

DiTauOrDiTauJetTriggerSF = Producer(
    call='''trigger::DiTauOrDiTauJetScaleFactor({df}, {output}, "{trigger_ditau_flag}", {input})''',
    input=[q.trg_sf_ditau_1, q.trg_sf_ditau_2, q.trg_sf_ditaujet_1, q.trg_sf_ditaujet_2, q.trg_sf_jet],
    output=[q.trg_wgt],
    scopes=["tt"],
)

# producer groups with the scale factors of the legs, one group per source of uncertainty
ElectronTriggerSF = ProducerGroup(
    name="ElectronTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers=[
        SingleElectronTriggerSF,
        CrossElectronTriggerSF,
    ],
)

MuonTriggerSF = ProducerGroup(
    name="MuonTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        SingleMuonTriggerSF,
        CrossMuonTriggerSF,
    ],
)

TauCrossTriggerSF = ProducerGroup(
    name="TauCrossTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt"],
    subproducers=[
        TauCrossTriggerSF_Leg,
    ],
)

DiTauTriggerSF = ProducerGroup(
    name="DiTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        DiTauTriggerSF_1,
        DiTauTriggerSF_2,
    ],
)

DiTauJet_TauTriggerSF = ProducerGroup(
    name="DiTauJet_TauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        DiTauJet_TauTriggerSF_1,
        DiTauJet_TauTriggerSF_2,
    ],
)

DiTauJet_JetTriggerSF = ProducerGroup(
    name="DiTauJet_JetTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        DiTauJet_JetTriggerSF_Leg,
    ],
)

# producer groups with the trigger scale factor of the event
EleTauTriggerSF = ProducerGroup(
    name="EleTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers=[
        ElectronTriggerSF,
        TauCrossTriggerSF,
        SingleOrCrossTriggerSF,
    ],
)

MuTauTriggerSF = ProducerGroup(
    name="MuTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        MuonTriggerSF,
        TauCrossTriggerSF,
        SingleOrCrossTriggerSF,
    ],
)

TauTauTriggerSF = ProducerGroup(
    name="TauTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        DiTauTriggerSF,
        DiTauJet_TauTriggerSF,
        DiTauJet_JetTriggerSF,
        DiTauOrDiTauJetTriggerSF,
    ],
)

#########################
# b-tagging SF
#########################

btagging_SF = Producer(
    call='''physicsobject::jet::scalefactor::BtaggingShape({df}, correctionManager, {output}, {input}, "{btag_sf_file}", "{btag_corr_algo}", "{btag_sf_variation}")''',
    input=[
        q.jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.jet_BTag,
        nanoAOD.Jet_hadronFlavour,
        q.good_jets_mask,
        q.good_bjets_mask,
        q.jet_overlap_veto_mask,
    ],
    output=[q.btag_weight],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)

btaggingWP_SF = Producer(
    call='''physicsobject::jet::scalefactor::BtaggingWP(
        {df},
        correctionManager,
        {output},
        {input},
        "{btag_sf_file}",
        "{btag_corr_algo}",
        "{btag_corr_algo_lf}",
        "{btag_sf_wp_name}",
        "{btag_eff_file}",
        "{btag_eff_name}",
        "{btag_eff_sample_type}",
        "{btag_sf_variation_bc}",
        "{btag_sf_variation_lf}",
        "{btag_wp}")''',
    input=[
        q.jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.jet_BTag,
        nanoAOD.Jet_hadronFlavour,
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
    TauID_SF_v9 = ProducerGroup(
        scopes=["tt", "mt", "et"],
        subproducers={
            "tt": [
                Tau_1_VsJetTauID_SF_v12,
                Tau_1_VsEleTauID_SF_Run2,
                Tau_1_VsMuTauID_SF,
                Tau_2_VsJetTauID_tt_SF,
                Tau_2_VsEleTauID_SF_Run2,
                Tau_2_VsMuTauID_SF,
            ],
            "mt": [
                # Tau_2_VsJetTauID_lt_SF, 
                # Tau_2_VsJetTauID_lt_SF_dm_binned,
                Tau_2_VsJetTauID_lt_SF_dm_pt_binned, 
                Tau_2_VsEleTauID_SF_Run2,
                Tau_2_VsMuTauID_SF,
            ],
            "et": [
                # Tau_2_VsJetTauID_lt_SF, 
                # Tau_2_VsJetTauID_lt_SF_dm_binned, 
                Tau_2_VsJetTauID_lt_SF_dm_pt_binned, 
                Tau_2_VsEleTauID_SF_Run2,
                Tau_2_VsMuTauID_SF,
            ],
        },
    )
    TauID_SF_v12 = ProducerGroup(
        scopes=["tt", "mt", "et"],
        subproducers={
            "tt": [
                Tau_1_VsJetTauID_SF_v12,
                Tau_1_VsEleTauID_SF,
                Tau_1_VsMuTauID_SF,
                Tau_2_VsJetTauID_SF_v12, 
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "mt": [
                Tau_2_VsJetTauID_SF_v12, 
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "et": [
                Tau_2_VsJetTauID_SF_v12,
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
        },
    )
    TauID_SF = ProducerGroup(
        scopes=["tt", "mt", "et"],
        subproducers={
            "tt": [
                Tau_1_VsJetTauID_SF,
                Tau_1_VsEleTauID_SF,
                Tau_1_VsMuTauID_SF,
                Tau_2_VsJetTauID_SF, 
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "mt": [
                Tau_2_VsJetTauID_SF, 
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "et": [
                Tau_2_VsJetTauID_SF,
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

# need to keep the group producers since they are referenced individually too for variations and such
class TauID_SFSwitch(SwitchProducer):
    run2 = TauID_SF_v9
    class run3:
        v12 = TauID_SF_v12
        v15 = TauID_SF

class btaggingWP_SFSwitch(SwitchProducer):
    run2 = btagging_SF
    run3 = btaggingWP_SF