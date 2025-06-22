from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..helper.ProducerWarapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    AutoExtendedVectorProducer as ExtendedVectorProducer,
    scopes,
)

with scopes(["et", "mt", "tt", "em", "mm", "ee"]):
    EmbeddingGenWeight = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.genWeight],
        output=[q.emb_genweight],
    )
    TauEmbeddingInitialMETEt = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_initialMETEt],
        output=[q.emb_initialMETEt],
    )
    TauEmbeddingInitialMETphi = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_initialMETphi],
        output=[q.emb_initialMETphi],
    )
    TauEmbeddingInitialPuppiMETEt = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_initialPuppiMETEt],
        output=[q.emb_initialPuppiMETEt],
    )
    TauEmbeddingInitialPuppiMETphi = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_initialPuppiMETphi],
        output=[q.emb_initialPuppiMETphi],
    )
    TauEmbeddingIsMediumLeadingMuon = Producer(
        call="event::quantity::Rename<Bool_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_isMediumLeadingMuon],
        output=[q.emb_isMediumLeadingMuon],
    )
    TauEmbeddingIsMediumTrailingMuon = Producer(
        call="event::quantity::Rename<Bool_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_isMediumTrailingMuon],
        output=[q.emb_isMediumTrailingMuon],
    )
    TauEmbeddingIsTightLeadingMuon = Producer(
        call="event::quantity::Rename<Bool_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_isTightLeadingMuon],
        output=[q.emb_isTightLeadingMuon],
    )
    TauEmbeddingIsTightTrailingMuon = Producer(
        call="event::quantity::Rename<Bool_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_isTightTrailingMuon],
        output=[q.emb_isTightTrailingMuon],
    )
    TauEmbeddingInitialPairCandidates = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_InitialPairCandidates],
        output=[q.emb_InitialPairCandidates],
    )
    TauEmbeddingSelectionOldMass = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_SelectionOldMass],
        output=[q.emb_SelectionOldMass],
    )
    TauEmbeddingSelectionNewMass = Producer(
        call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
        input=[nanoAOD.TauEmbedding_SelectionNewMass],
        output=[q.emb_SelectionNewMass],
    )
    EmbeddingQuantities = ProducerGroup(
        call=None,
        input=None,
        output=None,
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
            TauEmbeddingInitialPairCandidates,
            TauEmbeddingSelectionOldMass,
            TauEmbeddingSelectionNewMass,
        ],
    )

    # Selection scalefactor

    TauEmbeddingTriggerSelectionSF = Producer(
        call='scalefactor::embedding::selection_trigger({df}, {input}, {output}, "{embedding_selection_sf_file}", "{embedding_selection_trigger_sf}")',
        input=[q.gen_pt_1, q.gen_eta_1, q.gen_pt_2, q.gen_eta_2],
        output=[q.emb_triggersel_wgt],
    )
    TauEmbeddingIDSelectionSF_1 = Producer(
        call='scalefactor::embedding::selection_id({df}, {input}, {output}, "{embedding_selection_sf_file}", "{embedding_selection_id_sf}")',
        input=[q.gen_pt_1, q.gen_eta_1],
        output=[q.emb_idsel_wgt_1],
    )
    TauEmbeddingIDSelectionSF_2 = Producer(
        call='scalefactor::embedding::selection_id({df}, {input}, {output}, "{embedding_selection_sf_file}", "{embedding_selection_id_sf}")',
        input=[q.gen_pt_2, q.gen_eta_2],
        output=[q.emb_idsel_wgt_2],
    )
    TauEmbeddingSelectionSF = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauEmbeddingTriggerSelectionSF,
            TauEmbeddingIDSelectionSF_1,
            TauEmbeddingIDSelectionSF_2,
        ],
    )

# Muon ID/Iso/Trigger SFS

with scopes(["mt", "mm"]):  # muon leading object
    TauEmbeddingMuonIDSF_1 = Producer(
        call='scalefactor::embedding::muon_sf({df}, {input}, {output}, "{embedding_muon_sf_file}", "emb", "{embedding_muon_id_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_mu_1],
    )
    TauEmbeddingMuonIsoSF_1 = Producer(
        call='scalefactor::embedding::muon_sf({df}, {input}, {output}, "{embedding_muon_sf_file}", "emb", "{embedding_muon_iso_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.iso_wgt_mu_1],
    )
    MTGenerateSingleMuonTriggerSF = ExtendedVectorProducer(
        call='scalefactor::embedding::muon_sf({df}, {input}, {output}, "{embedding_muon_sf_file}", "emb", "{embedding_trigger_sf}", {muon_trg_extrapolation})',
        input=[q.pt_1, q.eta_1],
        output="flagname",
        vec_config="singlemuon_trigger_sf",
    )

with scopes(["mm", "em"]):  # muon trailing object
    TauEmbeddingMuonIDSF_2 = Producer(
        call='scalefactor::embedding::muon_sf({df}, {input}, {output}, "{embedding_muon_sf_file}", "emb", "{embedding_muon_id_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_mu_2],
    )
    TauEmbeddingMuonIsoSF_2 = Producer(
        call='scalefactor::embedding::muon_sf({df}, {input}, {output}, "{embedding_muon_sf_file}", "emb", "{embedding_muon_iso_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.iso_wgt_mu_2],
    )

# Electron ID/Iso/Trigger SFS

with scopes(["et", "ee", "em"]):  # electron leading object
    TauEmbeddingElectronIDSF_1 = Producer(
        call='scalefactor::embedding::electron_sf({df}, {input}, {output}, "{embedding_electron_sf_file}", "emb", "{embedding_electron_id_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.id_wgt_ele_1],
    )
    TauEmbeddingElectronIsoSF_1 = Producer(
        call='scalefactor::embedding::electron_sf({df}, {input}, {output}, "{embedding_electron_sf_file}", "emb", "{embedding_electron_iso_sf}")',
        input=[q.pt_1, q.eta_1],
        output=[q.iso_wgt_ele_1],
    )

with scopes(["ee"]):  # electron trailing object
    TauEmbeddingElectronIDSF_2 = Producer(
        call='scalefactor::embedding::electron_sf({df}, {input}, {output}, "{embedding_electron_sf_file}", "emb", "{embedding_electron_id_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.id_wgt_ele_2],
    )
    TauEmbeddingElectronIsoSF_2 = Producer(
        call='scalefactor::embedding::electron_sf({df}, {input}, {output}, "{embedding_electron_sf_file}", "emb", "{embedding_electron_iso_sf}")',
        input=[q.pt_2, q.eta_2],
        output=[q.iso_wgt_ele_2],
    )

ETGenerateSingleElectronTriggerSF = ExtendedVectorProducer(
    call='scalefactor::embedding::electron_sf({df}, {input}, {output}, "{embedding_electron_sf_file}", "emb", "{embedding_trigger_sf}", {electron_trg_extrapolation})',
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf",
)

# Di-tau trigger SFs

with scopes(["tt"]):
    TTGenerateDoubleTauTriggerSF_1 = Producer(
        call='scalefactor::embedding::ditau_trigger_sf({df}, {input}, {output}, "{emb_ditau_trigger_wp}", "{emb_ditau_trigger_file}", "{emb_ditau_trigger_type}", "{emb_ditau_trigger_corrtype}", "{emb_ditau_trigger_syst}")',
        input=[q.pt_1, q.tau_decaymode_1],
        output=[q.emb_trg_wgt_1],
    )
    TTGenerateDoubleTauTriggerSF_2 = Producer(
        call='scalefactor::embedding::ditau_trigger_sf({df}, {input}, {output}, "{emb_ditau_trigger_wp}", "{emb_ditau_trigger_file}", "{emb_ditau_trigger_type}", "{emb_ditau_trigger_corrtype}", "{emb_ditau_trigger_syst}")',
        input=[q.pt_2, q.tau_decaymode_2],
        output=[q.emb_trg_wgt_2],
    )

    ###############################
    # Tau ID/Iso/Trigger SFS
    ###############################

    Tau_1_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsJet_tt({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_emb_sf_vsjet_tauDM0}", "{tau_emb_sf_vsjet_tauDM1}", "{tau_emb_sf_vsjet_tauDM10}", "{tau_emb_sf_vsjet_tauDM11}", "{tau_emb_vsjet_sf_dependence}", "{tau_vsjet_vseleWP}", {output}, "{tau_emb_sf_file}", "{tau_emb_id_sf_correctionset}")',
        input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
        output="tau_1_vsjet_sf_outputname",
        vec_config="vsjet_tau_id_sf_embedding",
    )
    Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
        call='scalefactor::tau::id_vsJet_tt({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_emb_sf_vsjet_tauDM0}", "{tau_emb_sf_vsjet_tauDM1}", "{tau_emb_sf_vsjet_tauDM10}", "{tau_emb_sf_vsjet_tauDM11}", "{tau_emb_vsjet_sf_dependence}", "{tau_vsjet_vseleWP}", {output}, "{tau_emb_sf_file}", "{tau_emb_id_sf_correctionset}")',
        input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
        output="tau_2_vsjet_sf_outputname",
        vec_config="vsjet_tau_id_sf_embedding",
    )

Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
    call='scalefactor::tau::id_vsJet_lt_embedding({df}, correctionManager, {input}, {vec_open}{tau_dms}{vec_close}, "{vsjet_tau_id_WP}", "{tau_vsjet_vseleWP}", "{tau_emb_sf_vsjet_tau20to25}", "{tau_emb_sf_vsjet_tau25to30}", "{tau_emb_sf_vsjet_tau30to35}", "{tau_emb_sf_vsjet_tau35to40}", "{tau_emb_sf_vsjet_tau40toInf}", "{tau_emb_vsjet_sf_dependence}", {output}, "{tau_emb_sf_file}", "{tau_emb_id_sf_correctionset}")',
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["et", "mt"],
    vec_config="vsjet_tau_id_sf_embedding",
)
