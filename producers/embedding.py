from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults
from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD


with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    with defaults(call="event::quantity::Rename<Float_t>({df}, {output}, {input})"):
        EmbeddingGenWeight = Producer(input=[nanoAOD.genWeight], output=[q.emb_genweight])
        TauEmbeddingInitialMETEt = Producer(input=[nanoAOD.TauEmbedding_initialMETEt], output=[q.emb_initialMETEt])
        TauEmbeddingInitialMETphi = Producer(input=[nanoAOD.TauEmbedding_initialMETphi], output=[q.emb_initialMETphi])
        TauEmbeddingInitialPuppiMETEt = Producer(input=[nanoAOD.TauEmbedding_initialPuppiMETEt], output=[q.emb_initialPuppiMETEt])
        TauEmbeddingInitialPuppiMETphi = Producer(input=[nanoAOD.TauEmbedding_initialPuppiMETphi], output=[q.emb_initialPuppiMETphi])
        TauEmbeddingnInitialPairCandidates = Producer(input=[nanoAOD.TauEmbedding_nInitialPairCandidates], output=[q.emb_InitialPairCandidates])
        TauEmbeddingSelectionOldMass = Producer(input=[nanoAOD.TauEmbedding_SelectionOldMass], output=[q.emb_SelectionOldMass])
        TauEmbeddingSelectionNewMass = Producer(input=[nanoAOD.TauEmbedding_SelectionNewMass], output=[q.emb_SelectionNewMass])

    with defaults(call="event::quantity::Rename<Bool_t>({df}, {output}, {input})"):
        TauEmbeddingIsMediumLeadingMuon = Producer(input=[nanoAOD.TauEmbedding_isMediumLeadingMuon], output=[q.emb_isMediumLeadingMuon])
        TauEmbeddingIsMediumTrailingMuon = Producer(input=[nanoAOD.TauEmbedding_isMediumTrailingMuon], output=[q.emb_isMediumTrailingMuon])
        TauEmbeddingIsTightLeadingMuon = Producer(input=[nanoAOD.TauEmbedding_isTightLeadingMuon], output=[q.emb_isTightLeadingMuon])
        TauEmbeddingIsTightTrailingMuon = Producer(input=[nanoAOD.TauEmbedding_isTightTrailingMuon], output=[q.emb_isTightTrailingMuon])

    # Selection scalefactor

    TauEmbeddingTriggerSelectionSF = Producer(
        call='embedding::scalefactor::SelectionTrigger({df}, correctionManager, {output}, {input}, "{embedding_selection_sf_file}", "{embedding_selection_trigger_sf}")',
        input=[q.gen_pt_1, q.gen_eta_1, q.gen_pt_2, q.gen_eta_2],
        output=[q.emb_triggersel_wgt],
    )
    TauEmbeddingIDSelectionSF_1 = Producer(
        call='embedding::scalefactor::SelectionId({df}, correctionManager, {output}, {input}, "{embedding_selection_sf_file}", "{embedding_selection_id_sf}")',
        input=[q.gen_pt_1, q.gen_eta_1],
        output=[q.emb_idsel_wgt_1],
    )
    TauEmbeddingIDSelectionSF_2 = Producer(
        call='embedding::scalefactor::SelectionId({df}, correctionManager, {output}, {input}, "{embedding_selection_sf_file}", "{embedding_selection_id_sf}")',
        input=[q.gen_pt_2, q.gen_eta_2],
        output=[q.emb_idsel_wgt_2],
    )

    with defaults(call=None, input=None, output=None):
        EmbeddingQuantities = ProducerGroup(
            subproducers=[
                EmbeddingGenWeight,
                TauEmbeddingInitialMETEt,
                TauEmbeddingInitialMETphi,
                TauEmbeddingInitialPuppiMETEt,
                TauEmbeddingInitialPuppiMETphi,
                TauEmbeddingIsMediumLeadingMuon,
                TauEmbeddingIsMediumTrailingMuon,
                TauEmbeddingIsTightLeadingMuon,
                TauEmbeddingIsTightTrailingMuon,
                TauEmbeddingnInitialPairCandidates,
                TauEmbeddingSelectionOldMass,
                TauEmbeddingSelectionNewMass,
            ],
        )
        TauEmbeddingSelectionSF = ProducerGroup(
            subproducers=[
                TauEmbeddingTriggerSelectionSF,
                TauEmbeddingIDSelectionSF_1,
                TauEmbeddingIDSelectionSF_2,
            ],
        )

# Muon ID/Iso/Trigger SFS

with defaults(scopes=["mt", "mm"], input=[q.pt_1, q.eta_1]):
    TauEmbeddingMuonIDSF_1 = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_muon_sf_file}", "{embedding_muon_id_sf}", "emb")',
        output=[q.id_wgt_mu_1],
    )
    TauEmbeddingMuonIsoSF_1 = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_muon_sf_file}", "{embedding_muon_iso_sf}", "emb")',
        output=[q.iso_wgt_mu_1],
    )
    MTGenerateSingleMuonTriggerSF = ExtendedVectorProducer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_muon_sf_file}", "{embedding_trigger_sf}", "emb", {muon_trg_extrapolation})',
        output="flagname",
        vec_config="singlemuon_trigger_sf",
    )

with defaults(scopes=["mm", "em"], input=[q.pt_2, q.eta_2]):
    TauEmbeddingMuonIDSF_2 = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_muon_sf_file}", "{embedding_muon_id_sf}", "emb")',
        output=[q.id_wgt_mu_2],
    )
    TauEmbeddingMuonIsoSF_2 = Producer(
        call='embedding::muon::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_muon_sf_file}", "{embedding_muon_iso_sf}", "emb")',
        output=[q.iso_wgt_mu_2],
    )

# Electron ID/Iso/Trigger SFS

with defaults(scopes=["et", "ee", "em"], input=[q.pt_1, q.eta_1]):
    TauEmbeddingElectronIDSF_1 = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_electron_sf_file}", "{embedding_electron_id_sf}", "emb")',
        output=[q.id_wgt_ele_1],
    )
    TauEmbeddingElectronIsoSF_1 = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_electron_sf_file}", "{embedding_electron_iso_sf}", "emb")',
        output=[q.iso_wgt_ele_1],
    )

with defaults(scopes=["ee"], input=[q.pt_2, q.eta_2]):
    TauEmbeddingElectronIDSF_2 = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_electron_sf_file}", "{embedding_electron_id_sf}", "emb")',
        output=[q.id_wgt_ele_2],
    )
    TauEmbeddingElectronIsoSF_2 = Producer(
        call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_electron_sf_file}", "{embedding_electron_iso_sf}", "emb")',
        output=[q.iso_wgt_ele_2],
    )

ETGenerateSingleElectronTriggerSF = ExtendedVectorProducer(
    call='embedding::electron::Scalefactor({df}, correctionManager, {output}, {input}, "{embedding_electron_sf_file}", "{embedding_trigger_sf}", "emb", {electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf",
)

# Di-tau trigger SFs

with defaults(scopes=["tt"]):
    with defaults(call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{emb_ditau_trigger_file}", "tauTriggerSF", "{emb_ditau_trigger_type}", "{emb_ditau_trigger_wp}", "{emb_ditau_trigger_corrtype}", "{emb_ditau_trigger_syst}")'):
        TTGenerateDoubleTauTriggerSF_1 = Producer(input=[q.pt_1, q.tau_decaymode_1], output=[q.emb_trg_wgt_1])
        TTGenerateDoubleTauTriggerSF_2 = Producer(input=[q.pt_2, q.tau_decaymode_2], output=[q.emb_trg_wgt_2])

###############################
# Tau ID/Iso/Trigger SFS
###############################

with defaults(vec_configs="vsjet_tau_id_sf_embedding"):
    with defaults(input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2], output="tau_2_vsjet_sf_outputname"):
        with defaults(scopes=["et", "mt"]):
            Tau_2_VsJetTauID_lt_SF_dm_binned = ExtendedVectorProducer(
                call='''physicsobject::tau::scalefactor::Id_vsJet(
                    {df},
                    correctionManager,
                    {output},
                    {input},
                    "{tau_emb_sf_file}",
                    "{tau_emb_id_sf_correctionset}",
                    "{vsjet_tau_id_WP}",
                    "{tau_vsjet_vseleWP}",
                    "{tau_emb_vsjet_sf_dependence}",
                    "{tau_emb_sf_vsjet_1prong0pizero}",
                    "{tau_emb_sf_vsjet_1prong1pizero}",
                    "{tau_emb_sf_vsjet_3prong0pizero}",
                    "{tau_emb_sf_vsjet_3prong1pizero}")''',
            )
            Tau_2_VsJetTauID_lt_SF_dm_pt_binned = ExtendedVectorProducer(
                call='''physicsobject::tau::scalefactor::Id_vsJet(
                    {df},
                    correctionManager,
                    {output},
                    {input},
                    "{tau_emb_sf_file}",
                    "{tau_emb_id_sf_correctionset}",
                    "{vsjet_tau_id_WP}",
                    "{tau_vsjet_vseleWP}",
                    "{tau_emb_vsjet_sf_dependence}",
                    "{tau_emb_sf_vsjet_1prong0pizero20to40}",
                    "{tau_emb_sf_vsjet_1prong0pizero40toInf}",
                    "{tau_emb_sf_vsjet_1prong1pizero20to40}",
                    "{tau_emb_sf_vsjet_1prong1pizero40toInf}",
                    "{tau_emb_sf_vsjet_3prong0pizero20to40}",
                    "{tau_emb_sf_vsjet_3prong0pizero40toInf}",
                    "{tau_emb_sf_vsjet_3prong1pizero20to40}",
                    "{tau_emb_sf_vsjet_3prong1pizero40toInf}")''',
            )
        Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
            call='''physicsobject::tau::scalefactor::Id_vsJet(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_emb_sf_file}",
                "{tau_emb_id_sf_correctionset}",
                "{vsjet_tau_id_WP}",
                "{tau_vsjet_vseleWP}",
                "{tau_emb_vsjet_sf_dependence}",
                "{tau_emb_sf_vsjet_tauDM0}",
                "{tau_emb_sf_vsjet_tauDM1}",
                "{tau_emb_sf_vsjet_tauDM10}",
                "{tau_emb_sf_vsjet_tauDM11}")''',
            scope=["tt"],
        )

    Tau_1_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='physicsobject::tau::scalefactor::Id_vsJet({df}, correctionManager, {output}, {input}, "{tau_emb_sf_file}", "{tau_emb_id_sf_correctionset}", "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_emb_vsjet_sf_dependence}", "{tau_emb_sf_vsjet_tauDM0}", "{tau_emb_sf_vsjet_tauDM1}", "{tau_emb_sf_vsjet_tauDM10}", "{tau_emb_sf_vsjet_tauDM11}")',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        scope=["tt"],
    )
