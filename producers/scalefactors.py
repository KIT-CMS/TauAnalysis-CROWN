from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults


############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

with defaults(scopes=["mt", "mm"], input=[q.pt_1, q.eta_1]):
    Muon_1_ID_SF = Producer(
        call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_variation}")',
        output=[q.id_wgt_mu_1],
    )
    Muon_1_Iso_SF = Producer(
        call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_variation}")',
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
        call='physicsobject::muon::scalefactor::Id({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_id_sf_name}", "{muon_sf_variation}")',
        output=[q.id_wgt_mu_2],
    )
    Muon_2_Iso_SF = Producer(
        call='physicsobject::muon::scalefactor::Iso({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{muon_iso_sf_name}", "{muon_sf_variation}")',
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
        call='physicsobject::tau::scalefactor::Id_vsJet({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", {tau_vsjet_sf_dependence}, {tau_sf_vsjet_tauDM0}, {tau_sf_vsjet_tauDM1}, {tau_sf_vsjet_tauDM10}, {tau_sf_vsjet_tauDM11})',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )
    Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", {tau_sf_vsele_barrel}, {tau_sf_vsele_endcap})',
        input=[q.eta_1, q.tau_decaymode_1, q.gen_match_1], #remove DM for run2
        output="tau_1_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{era}", "{vsmu_tau_id_WP}", "{vsele_tau_id_WP}", "{vsjet_tau_id_WP}", {tau_sf_vsmu_wheel1}, {tau_sf_vsmu_wheel2}, {tau_sf_vsmu_wheel3}, {tau_sf_vsmu_wheel4}, {tau_sf_vsmu_wheel5})',
        input=[q.eta_1, q.gen_match_1],
        output="tau_1_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )
    Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsJet({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", {tau_vsjet_sf_dependence}, {tau_sf_vsjet_tauDM0}, {tau_sf_vsjet_tauDM1}, {tau_sf_vsjet_tauDM10}, {tau_sf_vsjet_tauDM11})',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id",
    )

with defaults(
    scopes=["et", "mt"],
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    vec_configs="vsjet_tau_id",
):
    Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
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

    Tau_2_VsJetTauID_lt_SF_dm_binned = ExtendedVectorProducer(
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

    Tau_2_VsJetTauID_lt_SF_dm_pt_binned = ExtendedVectorProducer(
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


with defaults(scopes=["et", "mt", "tt"]):
    Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsEle({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{vsele_tau_id_WP}", {tau_sf_vsele_barrel}, {tau_sf_vsele_endcap})',
        input=[q.eta_2, q.tau_decaymode_2, q.gen_match_2], #remove DM for run2
        output="tau_2_vsele_sf_outputname",
        vec_config="vsele_tau_id",
    )
    Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsMu({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_id_discriminator}", "{era}", "{vsmu_tau_id_WP}", "{vsele_tau_id_WP}", "{vsjet_tau_id_WP}", {tau_sf_vsmu_wheel1}, {tau_sf_vsmu_wheel2}, {tau_sf_vsmu_wheel3}, {tau_sf_vsmu_wheel4}, {tau_sf_vsmu_wheel5})',
        input=[q.eta_2, q.gen_match_2],
        output="tau_2_vsmu_sf_outputname",
        vec_config="vsmu_tau_id",
    )

#########################
# Electron ID/ISO SF with isolation
#########################

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2]):
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
    # --- from our measurement ---
    TauEmbeddingElectronIDSF_1_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_id_sf}", "mc")',
        output=[q.id_wgt_ele_1],
    )
    TauEmbeddingElectronIsoSF_1_MC = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_electron_iso_sf}", "mc")',
        output=[q.iso_wgt_ele_1],
    )

with defaults(scopes=["em", "ee", "et"], input=[q.pt_1, q.eta_1, q.phi_1]):
    Ele_1_IDWP90_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")',
        output=[q.id_wgt_ele_wp90iso_1],
    )
    Ele_1_IDWP80_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")',
        output=[q.id_wgt_ele_wp80iso_1],
    )

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2, q.phi_2]):
    Ele_2_IDWP90_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp90iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")',
        output=[q.id_wgt_ele_wp90iso_2],
    )
    Ele_2_IDWP80_SF = Producer(
        call='physicsobject::electron::scalefactor::Id({df}, correctionManager, {output}, {input}, "{ele_sf_year_id}", "wp80iso", "{ele_sf_file}", "{ele_id_sf_name}", "{ele_sf_variation}")',
        output=[q.id_wgt_ele_wp80iso_2],
    )

ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(  # --- from our measurement ---
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{mc_electron_sf_file}", "{mc_trigger_sf}", "mc", {mc_electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)

######################
# Trigger scale factors Run 3
######################

SingleEleTriggerSF = ExtendedVectorProducer(
    name="SingleEleTriggerSF",
    call='physicsobject::electron::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{singleelectron_trigger_flag}", "{singleelctron_trigger_era}", "{singleelectron_trigger_path_id_name}", "{singleelectron_trigger_sf_file}", "{singleelectron_trigger_sf_name}", "{singleelectron_trigger_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="singleelectron_trigger_flagname",
    scope=["et","em"],
    vec_config="singleelectron_trigger_sf",
)

SingleMuTriggerSF = ExtendedVectorProducer(
    name="SingleMuTriggerSF",
    call='physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{singlemuon_trigger_flag}", "{muon_sf_file}", "{singlemuon_trigger_sf_name}", "{singlemuon_trigger_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="singlemuon_trigger_flagname",
    scope=["mt","em"],
    vec_config="singlemuon_trigger_sf",
)

MuTauTriggerLeg1SF = ExtendedVectorProducer(
    name="MuTauTriggerLeg1SF",
    call='physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{mutau_cross_trigger_flag}", {mutau_cross_trigger_leg1_sf_file}, "{mutau_cross_trigger_leg1_sf_name}", "{mutau_cross_trigger_leg1_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="mutau_cross_trigger_leg1_flagname",
    scope=["mt"],
    vec_config="mutau_trigger_leg1_sf",
)

MuTauTriggerLeg2SF = ExtendedVectorProducer(
    name="GenerateMuTauCrossTriggerLeg2SF",
    call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{mutau_cross_trigger_flag}", "{tau_sf_file}", "tau_trigger", "{mutau_cross_trigger_leg2_sf_name}", "{ditau_trigger_wp}", "{ditau_trigger_corrtype}", "{mutau_cross_trigger_leg2_variation}")',
    input=[
        q.pt_2,
        q.tau_decaymode_2,
    ],
    output="mutau_cross_trigger_leg2_flagname",
    scope=["mt"],
    vec_config="mutau_trigger_leg2_sf",
)

# producer group containing the scale factors for both legs of the double muon-tau trigger
MuTauTriggerSF = ProducerGroup(
    name="MuTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        MuTauTriggerLeg1SF,
        MuTauTriggerLeg2SF,
    ],
)

EleTauTriggerLeg1SF = ExtendedVectorProducer(
    name="EleTauTriggerLeg1SF",
    call='physicsobject::electron::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{eletau_cross_trigger_flag}", "{singleelctron_trigger_era}", "{eletau_cross_trigger_leg1_path_id_name}", "{eletau_cross_trigger_leg1_sf_file}", "{eletau_cross_trigger_leg1_sf_name}", "{eletau_cross_trigger_leg1_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="eletau_cross_trigger_leg1_flagname",
    scope=["et"],
    vec_config="eletau_cross_trigger_leg1_sf",
)

EleTauTriggerLeg2SF = ExtendedVectorProducer(
    name="EleTauTriggerLeg2SF",
    call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{eletau_cross_trigger_flag}", "{tau_sf_file}", "tau_trigger", "{eletau_cross_trigger_leg2_sf_name}", "{ditau_trigger_wp}", "{ditau_trigger_corrtype}", "{eletau_cross_trigger_leg2_variation}")',
    input=[
        q.pt_2,
        q.tau_decaymode_2,
    ],
    output="eletau_cross_trigger_leg2_flagname",
    scope=["et"],
    vec_config="eletau_cross_trigger_leg2_sf",
)

EleTauTriggerSF = ProducerGroup(
    name="EleTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers=[
        EleTauTriggerLeg1SF,
        EleTauTriggerLeg2SF,
    ],
)

DoubleTauTriggerLeg1SF = ExtendedVectorProducer(
    name="DoubleTauTriggerLeg1SF",
    call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{doubletau_trigger_flag}", "{tau_sf_file}", "tau_trigger", "{doubletau_trigger_leg1_sf_name}", "{ditau_trigger_wp}", "{ditau_trigger_corrtype}", "{doubletau_trigger_leg1_variation}")',
    input=[
        q.pt_1,
        q.tau_decaymode_1,
    ],
    output="doubletau_trigger_leg1_flagname",
    scope=["tt"],
    vec_config="doubletau_trigger_leg1_sf",
)

DoubleTauTriggerLeg2SF = ExtendedVectorProducer(
    name="DoubleTauTriggerLeg2SF",
    call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{doubletau_trigger_flag}", "{tau_sf_file}", "tau_trigger", "{doubletau_trigger_leg2_sf_name}", "{ditau_trigger_wp}", "{ditau_trigger_corrtype}", "{doubletau_trigger_leg2_variation}")',
    input=[
        q.pt_2,
        q.tau_decaymode_2,
    ],
    output="doubletau_trigger_leg2_flagname",
    scope=["tt"],
    vec_config="doubletau_trigger_leg2_sf",
)

DoubleTauTriggerSF = ProducerGroup(
    name="DoubleTauTriggerSF",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        DoubleTauTriggerLeg1SF,
        DoubleTauTriggerLeg2SF,
    ],
)

#########################
# b-tagging SF
#########################

btagging_SF = Producer(
    call='physicsobject::jet::scalefactor::BtaggingShape({df}, correctionManager, {output}, {input}, "{btag_sf_file}", "{btag_corr_algo}", "{btag_sf_variation}")',
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_btagPNetB,
        nanoAOD.Jet_hadronFlavour,
        q.good_jets_mask,
        q.good_bjets_mask,
        q.jet_overlap_veto_mask,
    ],
    output=[q.btag_weight],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)

btaggingWP_SF = Producer(
    call='physicsobject::jet::scalefactor::BtaggingWP({df}, correctionManager, {output}, {input}, "{btag_sf_file}", "{btag_corr_algo}", "{btag_sf_variation}", "{btag_wp}")',
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
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
                # Tau_2_VsJetTauID_lt_SF_dm_binned, # only available for Run 2
                # Tau_2_VsJetTauID_lt_SF_dm_pt_binned, # only available for Run 2
                Tau_2_VsEleTauID_SF,
                Tau_2_VsMuTauID_SF,
            ],
            "et": [
                Tau_2_VsJetTauID_lt_SF,
                # Tau_2_VsJetTauID_lt_SF_dm_binned, # only available for Run 2
                # Tau_2_VsJetTauID_lt_SF_dm_pt_binned, # only available for Run 2
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
