from ..quantities import output as q
from ..quantities import nanoAOD, nanoAODv12
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults
from code_generation.configuration import Configuration

####################
# Set of producers used for selection possible good jets
####################

with defaults(scopes=["global"]):
    with defaults(output=[q.Jet_BTag]):
        JetBTagPNet = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Jet_btagPNetB],
        )

        JetBTagUParT = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Jet_btagUParTAK4B],
        )

    JetID = Producer(
        call="physicsobject::jet::quantity::ID({df}, correctionManager, {output}, {input}, {jet_id_json}, {jet_collection_name})",
        input=[
            nanoAOD.Jet_eta,
            nanoAOD.Jet_chHEF,
            nanoAOD.Jet_neHEF,
            nanoAOD.Jet_chEmEF,
            nanoAOD.Jet_neEmEF,
            nanoAOD.Jet_muEF,
            nanoAOD.Jet_chMultiplicity,
            nanoAOD.Jet_neMultiplicity,
        ],
        output=[q.Jet_ID],
    )

    JetIDRun3NanoV12Corrected = Producer(
        call="physicsobject::jet::quantities::CorrectJetIDRun3NanoV12({df}, {output}, {input})",
        input=[
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAODv12.Jet_jetId,
            nanoAOD.Jet_neHEF,
            nanoAOD.Jet_neEmEF,
            nanoAOD.Jet_muEF,
            nanoAOD.Jet_chEmEF,
        ],
        output=[q.Jet_ID],
    )

    JetVetoMapVeto = Producer(
        call="""physicsobject::jet::vetoes::jet_vetomap({df}, correctionManager, {output}, {input}, "{jet_veto_map_file}", "{jet_veto_map_name}", "{jet_veto_map_type}", {jet_veto_min_pt}, {jet_veto_id_wp}, {jet_veto_max_em_frac})""",
        input=[
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_ID,
            nanoAOD.Jet_chEmEF,
            nanoAOD.Jet_neEmEF,
        ],
        output=[q.Jet_vetomap],
        scopes=["global"],
    )

    JetSmearingSeed = Producer(
        call="event::quantity::GenerateSeed({df}, {output}, {input}, {jer_master_seed})",
        input=[
            nanoAOD.luminosityBlock,
            nanoAOD.run,
            nanoAOD.event,
        ],
        output=[],
    )

    with defaults(output=[q.Jet_pt_corrected]):
        JetPtCorrection = ProducerGroup(
            call='physicsobject::jet::PtCorrectionMC({df}, correctionManager, {output}, {input}, {jet_jer_file}, {jet_jec_algo}, {jet_jes_tag_mc}, {jet_jes_sources}, {jet_jer_tag}, {jet_reapplyJES}, {jet_jes_shift}, {jet_jer_shift}, "{era}")',
            input=[
                nanoAOD.Jet_pt,
                nanoAOD.Jet_eta,
                nanoAOD.Jet_phi,
                nanoAOD.Jet_area,
                nanoAOD.Jet_rawFactor,
                q.Jet_ID,
                nanoAOD.GenJet_pt,
                nanoAOD.GenJet_eta,
                nanoAOD.GenJet_phi,
                nanoAOD.Rho_fixedGridRhoFastjetAll,
            ],
            subproducers=[JetSmearingSeed],
        )
        JetPtCorrection_data = Producer(
            call='physicsobject::jet::PtCorrectionData({df}, correctionManager, {output}, {input}, "{era}", {jet_jer_file}, {jet_jec_algo}, {jet_jes_tag_data})',
            input=[
                nanoAOD.Jet_pt, 
                nanoAOD.Jet_eta, 
                nanoAOD.Jet_area, 
                nanoAOD.Jet_rawFactor, 
                nanoAOD.Rho_fixedGridRhoFastjetAll, 
                nanoAOD.Jet_phi, 
                nanoAOD.run],
        )
        RenameJetPt = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Jet_pt],
        )

    with defaults(output=[q.Jet_mass_corrected]):
        JetMassCorrection = Producer(
            call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
            input=[nanoAOD.Jet_mass, nanoAOD.Jet_pt, q.Jet_pt_corrected],
        )
        RenameJetMass = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Jet_mass],
        )

    with defaults(call=None, input=None, output=None):
        RenameJetsData = ProducerGroup(subproducers=[RenameJetPt, RenameJetMass])
        JetEnergyCorrection = ProducerGroup(subproducers=[JetPtCorrection, JetMassCorrection])
        JetEnergyCorrection_data = ProducerGroup(subproducers=[JetPtCorrection_data, JetMassCorrection])

    with defaults(output=[]):
        JetPtCut_loose = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt_loose})", input=[q.Jet_pt_corrected], output=[q.Jet_pt_cut_loose])
        JetPtCut_tight = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt_tight})", input=[q.Jet_pt_corrected])
        
        JetEtaCut_Min1 = Producer(call="physicsobject::CutAbsMin<float>({df}, {output}, {input}, {jet_eta_1})", input=[nanoAOD.Jet_eta])
        JetEtaCut_Min2 = Producer(call="physicsobject::CutAbsMin<float>({df}, {output}, {input}, {jet_eta_2})", input=[nanoAOD.Jet_eta])
        JetEtaCut_Max1 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_1})", input=[nanoAOD.Jet_eta])
        JetEtaCut_Max2 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_2})", input=[nanoAOD.Jet_eta])
        JetEtaCut_Max3 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_3})", input=[nanoAOD.Jet_eta])

        BJetPtCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_bjet_pt})", input=[q.Jet_pt_corrected])
        BJetEtaCut = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_bjet_eta})", input=[nanoAOD.Jet_eta])
        BTagCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {btag_cut})", input=[q.Jet_BTag])


    JetIDCut = Producer(
        call="physicsobject::CutMin<int>({df}, {output}, {input}, {jet_id})",
        input=[q.Jet_ID],
        output=[q.jet_id_mask],
    )

    # pt>30 & |eta| < 2.5 & id
    LooseJets_LowEta = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask, q.Jet_pt_cut_loose],
        output=[q.loose_jets_mask_loweta],
        subproducers=[JetEtaCut_Max1],
    )
    # pt>30 &  3 < |eta| < 4.7 & id
    LooseJets_HighEta = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask, q.Jet_pt_cut_loose],
        output=[q.loose_jets_mask_higheta],
        subproducers=[JetEtaCut_Min2, JetEtaCut_Max3],
    )
    # pt>30 & (|eta|<2.5 || 3<|eta|<4.7) & id
    GoodJets_loose = Producer(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "any_of")',
        input=[q.loose_jets_mask_loweta, q.loose_jets_mask_higheta],
        output=[q.good_jets_mask_loose],
    )
    # pt>50 & 2.5<|eta|<3 & id
    GoodJets_tight = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask],
        output=[q.good_jets_mask_tight],
        subproducers=[JetPtCut_tight, JetEtaCut_Min1, JetEtaCut_Max2],
    )
    # (pt>30 & (|eta|<2.5 || 3<|eta|<4.7) & id) || (pt>50 & 2.5<|eta|<3 & id)
    GoodJets = Producer(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "any_of")',
        input=[q.good_jets_mask_loose, q.good_jets_mask_tight],
        output=[q.good_jets_mask],
    )
    GoodBJets = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask],
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

with defaults(scopes=["mt", "et", "tt", "em", "mm", "ee"]):
    VetoOverlappingJets = Producer(
        call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
        input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, q.p4_1, q.p4_2],
        output=[q.jet_overlap_veto_mask],
    )

    with defaults(call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")', output=[]):
        GoodJetsWithVeto = ProducerGroup(input=[q.good_jets_mask], subproducers=[VetoOverlappingJets])
        GoodBJetsWithVeto = Producer(input=[q.good_bjets_mask, q.jet_overlap_veto_mask])

    with defaults(call="physicsobject::OrderByPt({df}, {output}, {input})", input=[q.Jet_pt_corrected]):
        JetCollection = ProducerGroup(output=[q.good_jet_collection], subproducers=[GoodJetsWithVeto])
        BJetCollection = ProducerGroup(output=[q.good_bjet_collection], subproducers=[GoodBJetsWithVeto])

    ##########################
    # Basic Jet Quantities
    # njets, pt, eta, phi, b-tag value
    ##########################

    LVJet1 = Producer(
        call="lorentzvector::Build({df}, {output}, {input}, 0)",
        input=[
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            q.good_jet_collection,
        ],
        output=[q.jet_p4_1],
    )
    LVJet2 = Producer(
        call="lorentzvector::Build({df}, {output}, {input}, 1)",
        input=[
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            q.good_jet_collection,
        ],
        output=[q.jet_p4_2],
    )
    NumberOfJets = Producer(
        call="physicsobject::Size<Int_t>({df}, {output}, {input})",
        input=[q.good_jet_collection],
        output=[q.njets],
    )

    with defaults(input=[q.jet_p4_1]):
        jpt_1 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.jpt_1])
        jeta_1 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.jeta_1])
        jphi_1 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.jphi_1])
    with defaults(input=[q.jet_p4_2]):
        jpt_2 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.jpt_2])
        jeta_2 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.jeta_2])
        jphi_2 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.jphi_2])

    with defaults(input=[q.Jet_BTag, q.good_jet_collection]):
        jtag_value_1 = Producer(call="event::quantity::Get<float>({df}, {output}, {input}, 0)",output=[q.jtag_value_1])
        jtag_value_2 = Producer(call="event::quantity::Get<float>({df}, {output}, {input}, 1)", output=[q.jtag_value_2])

    mjj = Producer(
        call="lorentzvector::GetMass({df}, {output}, {input})",
        input=[q.jet_p4_1, q.jet_p4_2],
        output=[q.mjj],
    )

    ##########################
    # Basic b-Jet Quantities
    # nbtag, pt, eta, phi, b-tag value
    ##########################

    with defaults(
        input=[
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            q.good_bjet_collection,
        ],
    ):
        LVBJet1 = Producer(call="lorentzvector::Build({df}, {output}, {input}, 0)", output=[q.bjet_p4_1])
        LVBJet2 = Producer(call="lorentzvector::Build({df}, {output}, {input}, 1)", output=[q.bjet_p4_2])

    NumberOfBJets = Producer(
        call="physicsobject::Size<Int_t>({df}, {output}, {input})",
        input=[q.good_bjet_collection],
        output=[q.nbtag],
    )

    with defaults(input=[q.bjet_p4_1]):
        bpt_1 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.bpt_1])
        beta_1 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.beta_1])
        bphi_1 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.bphi_1])
    with defaults(input=[q.bjet_p4_2]):
        bpt_2 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.bpt_2])
        beta_2 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.beta_2])
        bphi_2 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.bphi_2])

    with defaults(input=[q.Jet_BTag, q.good_bjet_collection]):
        btag_value_1 = Producer(call="event::quantity::Get<float>({df}, {output}, {input}, 0)", output=[q.btag_value_1])
        btag_value_2 = Producer(call="event::quantity::Get<float>({df}, {output}, {input}, 1)", output=[q.btag_value_2])

    ############################
    # Grouping the basic jet and b-jet quantities
    ############################

    with defaults(call=None, input=None, output=None):
        BasicJetQuantities = ProducerGroup(
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
        BasicBJetQuantities = ProducerGroup(
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
