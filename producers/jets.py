from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..scripts.ProducerWrapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    scopes,
)

####################
# Set of producers used for selection possible good jets
####################

with scopes(["global"]):
    JetPtCorrection = Producer(
        call="physicsobject::jet::PtCorrectionMC({df}, correctionManager, {output}, {input}, {jet_jec_file}, {jet_jec_algo}, {jet_jes_tag}, {jet_jes_sources}, {jet_jer_tag}, {jet_reapplyJES}, {jet_jes_shift}, {jet_jer_shift})",
        input=[
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.Jet_area,
            nanoAOD.Jet_rawFactor,
            nanoAOD.Jet_ID,
            nanoAOD.GenJet_pt,
            nanoAOD.GenJet_eta,
            nanoAOD.GenJet_phi,
            nanoAOD.rho,
        ],
        output=[q.Jet_pt_corrected],
    )
    JetPtCorrection_data = Producer(
        call="physicsobject::jet::PtCorrectionData({df}, correctionManager, {output}, {input}, {jet_jec_file}, {jet_jec_algo}, {jet_jes_tag_data})",
        input=[
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_area,
            nanoAOD.Jet_rawFactor,
            nanoAOD.rho,
        ],
        output=[q.Jet_pt_corrected],
    )
    JetMassCorrection = Producer(
        call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
        input=[
            nanoAOD.Jet_mass,
            nanoAOD.Jet_pt,
            q.Jet_pt_corrected,
        ],
        output=[q.Jet_mass_corrected],
    )

    # in data and embdedded sample, we simply rename the nanoAOD jets to the jet_pt_corrected column

    RenameJetPt = Producer(
        call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
        input=[nanoAOD.Jet_pt],
        output=[q.Jet_pt_corrected],
    )
    RenameJetMass = Producer(
        call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
        input=[nanoAOD.Jet_mass],
        output=[q.Jet_mass_corrected],
    )
    RenameJetsData = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[RenameJetPt, RenameJetMass],
    )
    JetEnergyCorrection = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[JetPtCorrection, JetMassCorrection],
    )
    JetEnergyCorrection_data = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[JetPtCorrection_data, JetMassCorrection],
    )
    JetPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt})",
        input=[q.Jet_pt_corrected],
        output=[],
    )
    BJetPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_bjet_pt})",
        input=[q.Jet_pt_corrected],
        output=[],
    )
    JetEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_jet_eta})",
        input=[nanoAOD.Jet_eta],
        output=[],
    )
    BJetEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_bjet_eta})",
        input=[nanoAOD.Jet_eta],
        output=[],
    )
    JetIDCut = Producer(
        call="physicsobject::CutMin<int>({df}, {output}, {input}, {jet_id})",
        input=[nanoAOD.Jet_ID],
        output=[q.jet_id_mask],
    )
    JetPUIDCut = Producer(
        call="physicsobject::jet::CutPileupID({df}, {output}, {input}, {jet_puid}, {jet_puid_max_pt})",
        input=[nanoAOD.Jet_PUID, q.Jet_pt_corrected],
        output=[q.jet_puid_mask],
    )
    BTagCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {btag_cut})",
        input=[nanoAOD.BJet_discriminator],
        output=[],
    )
    GoodJets = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_jets_mask],
        subproducers=[JetPtCut, JetEtaCut, JetIDCut, JetPUIDCut],
    )
    GoodBJets = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask, q.jet_puid_mask],
        output=[q.good_bjets_mask],
        subproducers=[BJetPtCut, BJetEtaCut, BTagCut],
    )

####################
# Set of producers to apply a veto of jets overlapping with ditaupair candidates and ordering jets by their pt
# 1. check all jets vs the two lepton candidates, if they are not within deltaR = 0.5, keep them --> mask
# 2. Combine mask with good_jets_mask
# 3. Generate JetCollection, an RVec containing all indices of good Jets in pt order
# 4. generate jet quantity outputs
####################

with scopes(["mt", "et", "tt", "em", "mm", "ee"]):
    VetoOverlappingJets = Producer(
        call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
        input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, q.p4_1, q.p4_2],
        output=[q.jet_overlap_veto_mask],
    )
    GoodJetsWithVeto = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.good_jets_mask],
        output=[],
        subproducers=[VetoOverlappingJets],
    )
    GoodBJetsWithVeto = Producer(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.good_bjets_mask, q.jet_overlap_veto_mask],
        output=[],
    )
    JetCollection = ProducerGroup(
        call="physicsobject::OrderByPt({df}, {output}, {input})",
        input=[q.Jet_pt_corrected],
        output=[q.good_jet_collection],
        subproducers=[GoodJetsWithVeto],
    )
    BJetCollection = ProducerGroup(
        call="physicsobject::OrderByPt({df}, {output}, {input})",
        input=[q.Jet_pt_corrected],
        output=[q.good_bjet_collection],
        subproducers=[GoodBJetsWithVeto],
    )

    ##########################
    # Basic Jet Quantities
    # njets, pt, eta, phi, b-tag value
    ##########################

    LVJet1 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
        input=[
            q.good_jet_collection,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
        ],
        output=[q.jet_p4_1],
    )
    LVJet2 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
        input=[
            q.good_jet_collection,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
        ],
        output=[q.jet_p4_2],
    )
    NumberOfJets = Producer(
        call="physicsobject::Count({df}, {output}, {input})",
        input=[q.good_jet_collection],
        output=[q.njets],
    )
    jpt_1 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.jet_p4_1],
        output=[q.jpt_1],
    )
    jpt_2 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.jet_p4_2],
        output=[q.jpt_2],
    )
    jeta_1 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.jet_p4_1],
        output=[q.jeta_1],
    )
    jeta_2 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.jet_p4_2],
        output=[q.jeta_2],
    )
    jphi_1 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.jet_p4_1],
        output=[q.jphi_1],
    )
    jphi_2 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.jet_p4_2],
        output=[q.jphi_2],
    )
    jtag_value_1 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
        input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
        output=[q.jtag_value_1],
    )
    jtag_value_2 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
        input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
        output=[q.jtag_value_2],
    )
    mjj = Producer(
        call="quantities::m_vis({df}, {output}, {input_vec})",
        input=[q.jet_p4_1, q.jet_p4_2],
        output=[q.mjj],
    )
    BasicJetQuantities = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            LVJet1,
            LVJet2,
            NumberOfJets,
            jpt_1,
            jeta_1,
            jphi_1,
            jtag_value_1,
            jpt_2,
            jeta_2,
            jphi_2,
            jtag_value_2,
            mjj,
        ],
    )

    ##########################
    # Basic b-Jet Quantities
    # nbtag, pt, eta, phi, b-tag value
    ##########################

    LVBJet1 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
        input=[
            q.good_bjet_collection,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
        ],
        output=[q.bjet_p4_1],
    )
    LVBJet2 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
        input=[
            q.good_bjet_collection,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
        ],
        output=[q.bjet_p4_2],
    )
    NumberOfBJets = Producer(
        call="physicsobject::Count({df}, {output}, {input})",
        input=[q.good_bjet_collection],
        output=[q.nbtag],
    )
    bpt_1 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.bjet_p4_1],
        output=[q.bpt_1],
    )
    bpt_2 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.bjet_p4_2],
        output=[q.bpt_2],
    )
    beta_1 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.bjet_p4_1],
        output=[q.beta_1],
    )
    beta_2 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.bjet_p4_2],
        output=[q.beta_2],
    )
    bphi_1 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.bjet_p4_1],
        output=[q.bphi_1],
    )
    bphi_2 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.bjet_p4_2],
        output=[q.bphi_2],
    )
    btag_value_1 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
        input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
        output=[q.btag_value_1],
    )
    btag_value_2 = Producer(
        call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
        input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
        output=[q.btag_value_2],
    )
    BasicBJetQuantities = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            LVBJet1,
            LVBJet2,
            NumberOfBJets,
            bpt_1,
            beta_1,
            bphi_1,
            btag_value_1,
            bpt_2,
            beta_2,
            bphi_2,
            btag_value_2,
        ],
    )
