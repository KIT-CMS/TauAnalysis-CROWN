from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..helper.ProducerWarapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    AutoExtendedVectorProducer as ExtendedVectorProducer,
    scopes,
)

####################
# Set of general producers for DiTauPair Quantities
####################

with scopes(["mt", "et", "tt", "em", "ee", "mm"]):
    pt_1 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.p4_1],
        output=[q.pt_1],
    )
    pt_2 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.p4_2],
        output=[q.pt_2],
    )
    eta_1 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.p4_1],
        output=[q.eta_1],
    )
    eta_2 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.p4_2],
        output=[q.eta_2],
    )
    phi_1 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.p4_1],
        output=[q.phi_1],
    )
    phi_2 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.p4_2],
        output=[q.phi_2],
    )
    mass_1 = Producer(
        call="quantities::mass({df}, {output}, {input})",
        input=[q.p4_1],
        output=[q.mass_1],
    )
    mass_2 = Producer(
        call="quantities::mass({df}, {output}, {input})",
        input=[q.p4_2],
        output=[q.mass_2],
    )
    m_vis = Producer(
        call="quantities::m_vis({df}, {output}, {input_vec})",
        input=[q.p4_1, q.p4_2],
        output=[q.m_vis],
    )
    deltaR_ditaupair = Producer(
        call="quantities::deltaR({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2],
        output=[q.deltaR_ditaupair],
    )
    pt_vis = Producer(
        call="quantities::pt_vis({df}, {output}, {input_vec})",
        input=[q.p4_1, q.p4_2],
        output=[q.pt_vis],
    )

####################
# Set of channel specific producers
####################

with scopes(["mt", "mm"]):  # muon as leading object
    muon_dxy_1 = Producer(
        call="quantities::dxy({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_dxy],
        output=[q.dxy_1],
    )
    muon_is_global_1 = Producer(
        call="quantities::muon::is_global({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_isGlobal],
        output=[q.is_global_1],
    )
    muon_nstations_1 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 0)",
        input=[nanoAOD.Muon_nStations, q.dileptonpair],
        output=[q.muon_nstations_1],
    )
    muon_ntrackerlayers_1 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 0)",
        input=[nanoAOD.Muon_nTrackerLayers, q.dileptonpair],
        output=[q.muon_ntrackerlayers_1],
    )
    muon_pterr_1 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
        input=[nanoAOD.Muon_ptErr, q.dileptonpair],
        output=[q.muon_pterr_1],
    )
    muon_dz_1 = Producer(
        call="quantities::dz({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_dz],
        output=[q.dz_1],
    )
    muon_q_1 = Producer(
        call="quantities::charge({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_charge],
        output=[q.q_1],
    )
    muon_iso_1 = Producer(
        call="quantities::isolation({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_iso],
        output=[q.iso_1],
    )

with scopes(["em", "mm"]):  # muon as subleading object
    muon_dxy_2 = Producer(
        call="quantities::dxy({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_dxy],
        output=[q.dxy_2],
    )
    muon_is_global_2 = Producer(
        call="quantities::muon::is_global({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_isGlobal],
        output=[q.is_global_2],
    )
    muon_nstations_2 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 1)",
        input=[nanoAOD.Muon_nStations, q.dileptonpair],
        output=[q.muon_nstations_2],
    )
    muon_ntrackerlayers_2 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 1)",
        input=[nanoAOD.Muon_nTrackerLayers, q.dileptonpair],
        output=[q.muon_ntrackerlayers_2],
    )
    muon_pterr_2 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
        input=[nanoAOD.Muon_ptErr, q.dileptonpair],
        output=[q.muon_pterr_2],
    )
    muon_dz_2 = Producer(
        call="quantities::dz({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_dz],
        output=[q.dz_2],
    )
    muon_q_2 = Producer(
        call="quantities::charge({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_charge],
        output=[q.q_2],
    )
    muon_iso_2 = Producer(
        call="quantities::isolation({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_iso],
        output=[q.iso_2],
    )

with scopes(["et", "ee", "em"]):  # electron as leading object
    electron_dxy_1 = Producer(
        call="quantities::dxy({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_dxy],
        output=[q.dxy_1],
    )
    electron_dz_1 = Producer(
        call="quantities::dz({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_dz],
        output=[q.dz_1],
    )
    electron_q_1 = Producer(
        call="quantities::charge({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_charge],
        output=[q.q_1],
    )
    electron_iso_1 = Producer(
        call="quantities::isolation({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_iso],
        output=[q.iso_1],
    )

with scopes(["ee"]):  # electron as subleading object
    electron_dxy_2 = Producer(
        call="quantities::dxy({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_dxy],
        output=[q.dxy_2],
    )
    electron_dz_2 = Producer(
        call="quantities::dz({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_dz],
        output=[q.dz_2],
    )
    electron_q_2 = Producer(
        call="quantities::charge({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_charge],
        output=[q.q_2],
    )
    electron_iso_2 = Producer(
        call="quantities::isolation({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_iso],
        output=[q.iso_2],
    )

with scopes(["tt"]):  # tau as leading object
    tau_dxy_1 = Producer(
        call="quantities::dxy({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_dxy],
        output=[q.dxy_1],
    )
    tau_dz_1 = Producer(
        call="quantities::dz({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_dz],
        output=[q.dz_1],
    )
    tau_q_1 = Producer(
        call="quantities::charge({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_charge],
        output=[q.q_1],
    )
    tau_iso_1 = Producer(
        call="quantities::isolation({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_IDraw],
        output=[q.iso_1],
    )
    tau_decaymode_1 = Producer(
        call="quantities::tau::decaymode({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_decayMode],
        output=[q.tau_decaymode_1],
    )
    tau_gen_match_1 = Producer(
        call="quantities::tau::genmatch({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_genMatch],
        output=[q.tau_gen_match_1],
    )
    taujet_pt_1 = Producer(
        call="quantities::tau::matching_jet_pt({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_associatedJet, nanoAOD.Jet_pt],
        output=[q.taujet_pt_1],
    )
    VsJetTauIDFlag_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsjet_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsJet],
        output="tau_1_vsjet_id_outputname",
        vec_config="vsjet_tau_id",
    )
    VsJetTauIDFlagOnly_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsjet_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsJet],
        output="tau_1_vsjet_id_WPbit_outputname",
        vec_config="vsjet_tau_id_wp_bit",
    )
    VsEleTauIDFlag_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsele_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsEle],
        output="tau_1_vsele_id_outputname",
        vec_config="vsele_tau_id",
    )
    VsEleTauIDFlagOnly_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsele_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsEle],
        output="tau_1_vsele_id_WPbit_outputname",
        vec_config="vsele_tau_id_wp_bit",
    )
    VsMuTauIDFlag_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsmu_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsMu],
        output="tau_1_vsmu_id_outputname",
        vec_config="vsmu_tau_id",
    )
    VsMuTauIDFlagOnly_1 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 0, {input}, {vsmu_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsMu],
        output="tau_1_vsmu_id_WPbit_outputname",
        vec_config="vsmu_tau_id_wp_bit",
    )

with scopes(["mt", "et", "tt"]):  # tau as subleading object
    tau_dxy_2 = Producer(
        call="quantities::dxy({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_dxy],
        output=[q.dxy_2],
    )
    tau_dz_2 = Producer(
        call="quantities::dz({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_dz],
        output=[q.dz_2],
    )
    tau_q_2 = Producer(
        call="quantities::charge({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_charge],
        output=[q.q_2],
    )
    tau_iso_2 = Producer(
        call="quantities::isolation({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_IDraw],
        output=[q.iso_2],
    )
    tau_decaymode_2 = Producer(
        call="quantities::tau::decaymode({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_decayMode],
        output=[q.tau_decaymode_2],
    )
    tau_gen_match_2 = Producer(
        call="quantities::tau::genmatch({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_genMatch],
        output=[q.tau_gen_match_2],
    )
    taujet_pt_2 = Producer(
        call="quantities::tau::matching_jet_pt({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Tau_associatedJet, nanoAOD.Jet_pt],
        output=[q.taujet_pt_2],
    )
    VsJetTauIDFlag_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsjet_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsJet],
        output="tau_2_vsjet_id_outputname",
        vec_config="vsjet_tau_id",
    )
    VsJetTauIDFlagOnly_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsjet_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsJet],
        output="tau_2_vsjet_id_WPbit_outputname",
        vec_config="vsjet_tau_id_wp_bit",
    )
    VsEleTauIDFlag_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsele_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsEle],
        output="tau_2_vsele_id_outputname",
        vec_config="vsele_tau_id",
    )
    VsEleTauIDFlagOnly_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsele_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsEle],
        output="tau_2_vsele_id_WPbit_outputname",
        vec_config="vsele_tau_id_wp_bit",
    )
    VsMuTauIDFlag_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsmu_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsMu],
        output="tau_2_vsmu_id_outputname",
        vec_config="vsmu_tau_id",
    )
    VsMuTauIDFlagOnly_2 = ExtendedVectorProducer(
        call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {vsmu_tau_id_WPbit})",
        input=[q.dileptonpair, nanoAOD.Tau_ID_vsMu],
        output="tau_2_vsmu_id_WPbit_outputname",
        vec_config="vsmu_tau_id_wp_bit",
    )

tau_decaymode_1_notau = Producer(
    call="event::quantity::Define({df}, {output}, -1)",
    input=[],
    output=[q.tau_decaymode_1],
    scopes=["et", "mt", "em", "ee", "mm"],
)
tau_decaymode_2_notau = Producer(
    call="event::quantity::Define({df}, {output}, -1)",
    input=[],
    output=[q.tau_decaymode_2],
    scopes=["em", "ee", "mm"],
)

UnrollMuLV1 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["mt", "mm"],
    subproducers=[
        pt_1,
        eta_1,
        phi_1,
        mass_1,
        muon_dxy_1,
        muon_dz_1,
        muon_q_1,
        muon_iso_1,
        muon_is_global_1,
    ],
)
UnrollMuLV2 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["mm", "em"],
    subproducers=[
        pt_2,
        eta_2,
        phi_2,
        mass_2,
        muon_dxy_2,
        muon_dz_2,
        muon_q_2,
        muon_iso_2,
        muon_is_global_2,
    ],
)
UnrollElLV1 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["et", "ee", "em"],
    subproducers=[
        pt_1,
        eta_1,
        phi_1,
        mass_1,
        electron_dxy_1,
        electron_dz_1,
        electron_q_1,
        electron_iso_1,
    ],
)
UnrollElLV2 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["ee"],
    subproducers=[
        pt_2,
        eta_2,
        phi_2,
        mass_2,
        electron_dxy_2,
        electron_dz_2,
        electron_q_2,
        electron_iso_2,
    ],
)
UnrollTauLV1 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        pt_1,
        eta_1,
        phi_1,
        mass_1,
        tau_dxy_1,
        tau_dz_1,
        tau_q_1,
        tau_iso_1,
        tau_decaymode_1,
        tau_gen_match_1,
        taujet_pt_1,
        VsJetTauIDFlag_1,
        VsEleTauIDFlag_1,
        VsMuTauIDFlag_1,
    ],
)
UnrollTauLV2 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt"],
    subproducers=[
        pt_2,
        eta_2,
        phi_2,
        mass_2,
        tau_dxy_2,
        tau_dz_2,
        tau_q_2,
        tau_iso_2,
        tau_decaymode_2,
        tau_gen_match_2,
        taujet_pt_2,
        VsJetTauIDFlag_2,
        VsEleTauIDFlag_2,
        VsMuTauIDFlag_2,
    ],
)

#####################
# Producer Groups
#####################

MTDiTauPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        UnrollMuLV1,
        UnrollTauLV2,
        tau_decaymode_1_notau,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)
MuMuPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["mm"],
    subproducers=[
        UnrollMuLV1,
        UnrollMuLV2,
        tau_decaymode_1_notau,
        tau_decaymode_2_notau,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)
ElElPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["ee"],
    subproducers=[
        UnrollElLV1,
        UnrollElLV2,
        tau_decaymode_1_notau,
        tau_decaymode_2_notau,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)
ETDiTauPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers=[
        UnrollElLV1,
        UnrollTauLV2,
        tau_decaymode_1_notau,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)
TTDiTauPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        UnrollTauLV1,
        UnrollTauLV2,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)
EMDiTauPairQuantities = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["em"],
    subproducers=[
        UnrollElLV1,
        UnrollMuLV2,
        tau_decaymode_1_notau,
        tau_decaymode_2_notau,
        m_vis,
        pt_vis,
        deltaR_ditaupair,
    ],
)

# advanced event quantities (can be caluculated when ditau pair and met and all jets are determined)
# leptons: q.p4_1, q.p4_2
# met: met_p4_recoilcorrected
# jets: good_jet_collection (if only the leading two are needed: q.jet_p4_1, q.jet_p4_2
# bjets: gen_bjet_collection

with scopes(["mt", "et", "tt", "em", "ee", "mm"]):
    Pzetamissvis = Producer(
        call="quantities::pzetamissvis({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.met_p4_recoilcorrected],
        output=[q.pzetamissvis],
    )
    mTdileptonMET = Producer(
        call="quantities::mTdileptonMET({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.met_p4_recoilcorrected],
        output=[q.mTdileptonMET],
    )
    mt_1 = Producer(
        call="quantities::mT({df}, {output}, {input})",
        input=[q.p4_1, q.met_p4_recoilcorrected],
        output=[q.mt_1],
    )
    mt_2 = Producer(
        call="quantities::mT({df}, {output}, {input})",
        input=[q.p4_2, q.met_p4_recoilcorrected],
        output=[q.mt_2],
    )
    pt_tt = Producer(
        call="quantities::pt_tt({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.met_p4_recoilcorrected],
        output=[q.pt_tt],
    )
    pt_ttjj = Producer(
        call="quantities::pt_ttjj({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.jet_p4_1, q.jet_p4_2, q.met_p4_recoilcorrected],
        output=[q.pt_ttjj],
    )
    mt_tot = Producer(
        call="quantities::mt_tot({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.met_p4_recoilcorrected],
        output=[q.mt_tot],
    )
    Pzetamissvis_pf = Producer(
        call="quantities::pzetamissvis({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.pzetamissvis_pf],
    )
    mTdileptonMET_pf = Producer(
        call="quantities::mTdileptonMET({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.mTdileptonMET_pf],
    )
    mt_1_pf = Producer(
        call="quantities::mT({df}, {output}, {input})",
        input=[q.p4_1, q.pfmet_p4_recoilcorrected],
        output=[q.mt_1_pf],
    )
    mt_2_pf = Producer(
        call="quantities::mT({df}, {output}, {input})",
        input=[q.p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.mt_2_pf],
    )
    pt_tt_pf = Producer(
        call="quantities::pt_tt({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.pt_tt_pf],
    )
    pt_ttjj_pf = Producer(
        call="quantities::pt_ttjj({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.jet_p4_1, q.jet_p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.pt_ttjj_pf],
    )
    mt_tot_pf = Producer(
        call="quantities::mt_tot({df}, {output}, {input})",
        input=[q.p4_1, q.p4_2, q.pfmet_p4_recoilcorrected],
        output=[q.mt_tot_pf],
    )
    pt_dijet = Producer(
        call="quantities::pt_dijet({df}, {output}, {input})",
        input=[q.jet_p4_1, q.jet_p4_2],
        output=[q.pt_dijet],
    )
    jet_hemisphere = Producer(
        call="quantities::jet_hemisphere({df}, {output}, {input})",
        input=[q.jet_p4_1, q.jet_p4_2],
        output=[q.jet_hemisphere],
    )
    DiTauPairMETQuantities = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            Pzetamissvis,
            mTdileptonMET,
            mt_1,
            mt_2,
            pt_tt,
            pt_ttjj,
            mt_tot,
            Pzetamissvis_pf,
            mTdileptonMET_pf,
            mt_1_pf,
            mt_2_pf,
            pt_tt_pf,
            pt_ttjj_pf,
            mt_tot_pf,
            pt_dijet,
            jet_hemisphere,
        ],
    )

p4_fastmtt_mt = Producer(
    call='quantities::p4_fastmtt({df}, {output}, {input}, "mt")',
    input=[
        q.pt_1,
        q.pt_2,
        q.eta_1,
        q.eta_2,
        q.phi_1,
        q.phi_2,
        q.mass_1,
        q.mass_2,
        q.met,
        q.metphi,
        q.metcov00,
        q.metcov01,
        q.metcov11,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
    ],
    output=[q.p4_fastmtt],
    scopes=["mt"],
)
p4_fastmtt_et = Producer(
    call='quantities::p4_fastmtt({df}, {output}, {input}, "et")',
    input=[
        q.pt_1,
        q.pt_2,
        q.eta_1,
        q.eta_2,
        q.phi_1,
        q.phi_2,
        q.mass_1,
        q.mass_2,
        q.met,
        q.metphi,
        q.metcov00,
        q.metcov01,
        q.metcov11,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
    ],
    output=[q.p4_fastmtt],
    scopes=["et"],
)
p4_fastmtt_tt = Producer(
    call='quantities::p4_fastmtt({df}, {output}, {input}, "tt")',
    input=[
        q.pt_1,
        q.pt_2,
        q.eta_1,
        q.eta_2,
        q.phi_1,
        q.phi_2,
        q.mass_1,
        q.mass_2,
        q.met,
        q.metphi,
        q.metcov00,
        q.metcov01,
        q.metcov11,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
    ],
    output=[q.p4_fastmtt],
    scopes=["tt"],
)
p4_fastmtt_em = Producer(
    call='quantities::p4_fastmtt({df}, {output}, {input}, "em")',
    input=[
        q.pt_1,
        q.pt_2,
        q.eta_1,
        q.eta_2,
        q.phi_1,
        q.phi_2,
        q.mass_1,
        q.mass_2,
        q.met,
        q.metphi,
        q.metcov00,
        q.metcov01,
        q.metcov11,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
    ],
    output=[q.p4_fastmtt],
    scopes=["em"],
)

with scopes(["mt", "et", "tt", "em", "ee", "mm"]):
    pt_fastmtt = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.p4_fastmtt],
        output=[q.pt_fastmtt],
    )
    eta_fastmtt = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.p4_fastmtt],
        output=[q.eta_fastmtt],
    )
    phi_fastmtt = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.p4_fastmtt],
        output=[q.phi_fastmtt],
    )
    m_fastmtt = Producer(
        call="quantities::mass({df}, {output}, {input})",
        input=[q.p4_fastmtt],
        output=[q.m_fastmtt],
    )
    FastMTTQuantities = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers={
            "mt": [p4_fastmtt_mt, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt],
            "et": [p4_fastmtt_et, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt],
            "tt": [p4_fastmtt_tt, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt],
            "em": [p4_fastmtt_em, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt],
        },
    )
