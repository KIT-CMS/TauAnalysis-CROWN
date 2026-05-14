from ..quantities import output as q
from ..quantities import nanoAODv15, nanoAODv12, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for selection possible good jets
####################

with defaults(scopes=["global"]):
    with defaults(output=[q.jet_BTag]):
        JetBTagDeep = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv15.Jet_btagDeepFlavB],
        )
        # not present in v9
        JetBTagPNet = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv15.Jet_btagPNetB],
        )
        # not present in v9 or v12
        JetBTagUParT = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv15.Jet_btagUParTAK4B],
        )
    
    with defaults(output=[q.fixedGridRho]):
        # not present in v9
        JetRho = Producer(
            call="event::quantity::Rename<float>({df}, {output}, {input})",
            input=[nanoAODv15.Rho_fixedGridRhoFastjetAll],
        )
        # not present in v12 and above
        JetRho_v9 = Producer(
            call="event::quantity::Rename<float>({df}, {output}, {input})",
            input=[nanoAODv9.fixedGridRhoFastjetAll],
        )

    with defaults(output=[q.jet_ID]):
        JetID = Producer(
            call="physicsobject::jet::quantity::ID({df}, correctionManager, {output}, {input}, {jet_id_json}, {jet_collection_name})",
            input=[
                nanoAODv15.Jet_eta,
                nanoAODv15.Jet_chHEF,
                nanoAODv15.Jet_neHEF,
                nanoAODv15.Jet_chEmEF,
                nanoAODv15.Jet_neEmEF,
                nanoAODv15.Jet_muEF,
                nanoAODv15.Jet_chMultiplicity,
                nanoAODv15.Jet_neMultiplicity,
            ],
        )
        JetIDRun3NanoV12Corrected = Producer(
            call="physicsobject::jet::quantity::PatchedIDNanoV12({df}, {output}, {input})",
            input=[
                nanoAODv15.Jet_pt,
                nanoAODv15.Jet_eta,
                nanoAODv12.Jet_jetId,
                nanoAODv15.Jet_neHEF,
                nanoAODv15.Jet_neEmEF,
                nanoAODv15.Jet_muEF,
                nanoAODv15.Jet_chEmEF,
            ],
        )
        JetID_rename = Producer(
            call="event::quantity::Rename<ROOT::RVec<int>>({df}, {output}, {input})",
            input=[nanoAODv9.Jet_jetId],
        )

    JetVetoMapVeto = Producer(
        call="""physicsobject::jet::VetoMap({df}, correctionManager, {output}, {input}, "{jet_veto_map_file}", "{jet_veto_map_name}", "{jet_veto_map_type}", {jet_veto_min_pt}, {jet_veto_id_wp}, {jet_veto_max_em_frac})""",
        input=[
            q.jet_pt_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            q.jet_ID,
            nanoAODv15.Jet_chEmEF,
            nanoAODv15.Jet_neEmEF,
        ],
        output=[q.jet_vetomap],
        scopes=["global"],
    )

    JetSmearingSeed = Producer(
        call="event::quantity::GenerateSeed({df}, {output}, {input}, {jet_jer_master_seed})",
        input=[
            nanoAODv15.luminosityBlock,
            nanoAODv15.run,
            nanoAODv15.event,
        ],
        output=[q.jet_seed],
    )

    RawJet = Producer(
        call="physicsobject::jet::RawPt({df}, {output}, {input})",
        input=[
            nanoAODv15.Jet_pt,
            nanoAODv15.Jet_rawFactor,
        ],
        output=[q.jet_rawPt],
    )

    with defaults(call="event::quantity::Rename<ROOT::VecOps::RVec<float>>({df}, {output}, {input})"):
        # rename gen jet variable for data otherwise jet pt correction producer doesn't work for both mc and data at the same time
        with defaults(output=[q.gen_jet_pt]):
            GenPt = Producer(input=[nanoAODv15.GenJet_pt])
            GenPt_data = Producer(input=[nanoAODv15.Jet_pt])
        with defaults(output=[q.gen_jet_eta]):
            GenEta = Producer(input=[nanoAODv15.GenJet_eta])
            GenEta_data = Producer(input=[nanoAODv15.Jet_eta])
        with defaults(output=[q.gen_jet_phi]):
            GenPhi = Producer(input=[nanoAODv15.GenJet_phi])
            GenPhi_data = Producer(input=[nanoAODv15.Jet_phi])

    GenJet = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[GenPt, GenEta, GenPhi],
    )

    GenJet_data = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[GenPt_data, GenEta_data, GenPhi_data],
    )

    JetPtCorrection_L1 = Producer(
        call='physicsobject::jet::PtCorrectionL1({df}, correctionManager, {output}, {input}, "{jet_jec_file}", "{jet_jec_algo}", "{jet_jes_tag}")',
        input=[
            q.jet_rawPt,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            nanoAODv15.Jet_area,
            nanoAODv15.Jet_muonSubtrFactor,
            nanoAODv15.CorrT1METJet_rawPt,
            nanoAODv15.CorrT1METJet_eta,
            nanoAODv15.CorrT1METJet_phi,
            nanoAODv15.CorrT1METJet_area,
            nanoAODv15.CorrT1METJet_muonSubtrFactor,
            q.fixedGridRho,
        ],
        output=[q.jet_pt_L1_corrected, q.jet_pt_L1_T1MET_corrected],
    )
    JetPtCorrectionL2L3 = Producer(
        call='physicsobject::jet::PtCorrectionL2L3({df}, correctionManager, {output}, {input}, "{jet_jec_file}", "{jet_jec_algo}", "{jet_jes_tag}", {jet_jes_sources}, "{jet_jer_tag}", {jet_jes_shift}, "{jet_jer_shift}", "{era}")',
        input=[
            q.jet_pt_L1_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            nanoAODv15.Jet_area,
            q.jet_ID,
            q.jet_pt_L1_T1MET_corrected,
            nanoAODv15.CorrT1METJet_eta,
            nanoAODv15.CorrT1METJet_phi,
            nanoAODv15.CorrT1METJet_area,
            q.gen_jet_pt,
            q.gen_jet_eta,
            q.gen_jet_phi,
            q.fixedGridRho,
            q.jet_seed,
            nanoAODv15.run
        ],
        output=[q.jet_pt_corrected, q.jet_pt_T1MET_corrected],
    )

    with defaults(output=[q.jet_pt_corrected]):
        JetPtCorrection = Producer(
            call='physicsobject::jet::PtCorrectionMC({df}, correctionManager, {output}, {input}, "{jet_jec_file}", "{jet_jec_algo}", "{jet_jes_tag}", {jet_jes_sources}, "{jet_jer_tag}", {jet_reapplyJES}, {jet_jes_shift}, "{jet_jer_shift}", "{era}")',
            input=[
                nanoAODv15.Jet_pt,
                nanoAODv15.Jet_eta,
                nanoAODv15.Jet_phi,
                nanoAODv15.Jet_area,
                nanoAODv15.Jet_rawFactor,
                q.jet_ID,
                nanoAODv15.GenJet_pt,
                nanoAODv15.GenJet_eta,
                nanoAODv15.GenJet_phi,
                q.fixedGridRho,
                q.jet_seed,
            ],
        )
        JetPtCorrection_data = Producer(
            call='physicsobject::jet::PtCorrectionData({df}, correctionManager, {output}, {input}, "{jet_jec_file}", "{jet_jec_algo}", "{jet_jes_tag}", "{era}")',
            input=[
                nanoAODv15.Jet_pt,
                nanoAODv15.Jet_eta,
                nanoAODv15.Jet_phi,
                nanoAODv15.Jet_area,
                nanoAODv15.Jet_rawFactor,
                q.fixedGridRho, 
                nanoAODv15.run],
        )
        RenameJetPt = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv15.Jet_pt],
        )

    with defaults(output=[q.jet_mass_corrected]):
        JetMassCorrection = Producer(
            call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
            input=[nanoAODv15.Jet_mass, nanoAODv15.Jet_pt, q.jet_pt_corrected],
        )
        RenameJetMass = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv15.Jet_mass],
        )

    with defaults(call=None, input=None, output=None):
        RenameJetsData = ProducerGroup(subproducers=[RenameJetPt, RenameJetMass])
        JetEnergyCorrection_Run3 = ProducerGroup(subproducers=[RawJet, JetPtCorrection_L1, JetPtCorrectionL2L3, JetMassCorrection])
        JetEnergyCorrection = ProducerGroup(subproducers=[JetPtCorrection, JetMassCorrection])
        JetEnergyCorrection_data = ProducerGroup(subproducers=[JetPtCorrection_data, JetMassCorrection])

    with defaults(output=[]):
        JetPtCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt})", input=[q.jet_pt_corrected])
        JetPtCut_loose = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt_loose})", input=[q.jet_pt_corrected], output=[q.jet_pt_mask_loose])
        JetPtCut_tight = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt_tight})", input=[q.jet_pt_corrected])
        
        JetEtaCut = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_jet_eta})", input=[nanoAODv15.Jet_eta])
        JetEtaCut_Min1 = Producer(call="physicsobject::CutAbsMin<float>({df}, {output}, {input}, {jet_eta_1})", input=[nanoAODv15.Jet_eta])
        JetEtaCut_Min2 = Producer(call="physicsobject::CutAbsMin<float>({df}, {output}, {input}, {jet_eta_2})", input=[nanoAODv15.Jet_eta])
        JetEtaCut_Max1 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_1})", input=[nanoAODv15.Jet_eta])
        JetEtaCut_Max2 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_2})", input=[nanoAODv15.Jet_eta])
        JetEtaCut_Max3 = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {jet_eta_3})", input=[nanoAODv15.Jet_eta], output=[q.jet_eta_mask_max])

        BJetPtCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_bjet_pt})", input=[q.jet_pt_corrected])
        BJetEtaCut = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_bjet_eta})", input=[nanoAODv15.Jet_eta])
        BTagCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {btag_cut})", input=[q.jet_BTag])


    JetIDCut = Producer(
        call="physicsobject::CutMin<int>({df}, {output}, {input}, {jet_id})",
        input=[q.jet_ID],
        output=[q.jet_id_mask],
    )

    JetPUIDCut = Producer(
        call="physicsobject::jet::CutPileupID({df}, {output}, {input}, {jet_puid}, {jet_puid_max_pt})",
        input=[nanoAODv9.Jet_puId, q.jet_pt_corrected],
        output=[q.jet_puid_mask],
    )

    # pt>30 & |eta| < 2.5 & id
    LooseJets_LowEta = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask, q.jet_pt_mask_loose],
        output=[q.loose_jets_mask_loweta],
        subproducers=[JetEtaCut_Max1],
    )
    # pt>30 &  3 < |eta| < 4.7 & id
    LooseJets_HighEta = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask, q.jet_pt_mask_loose, q.jet_eta_mask_max],
        output=[q.loose_jets_mask_higheta],
        subproducers=[JetEtaCut_Min2],
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
    
    with defaults(call='physicsobject::CombineMasks({df}, {output}, {input}, "any_of")'):
        # (pt>30 & (|eta|<2.5 || 3<|eta|<4.7) & id) || (pt>50 & 2.5<|eta|<3 & id) for run 3
        GoodJets = Producer(
            input=[q.good_jets_mask_loose, q.good_jets_mask_tight],
            output=[q.good_jets_mask],
        )
    # run 2 without horn selection, pt>30 and eta<4.7
    GoodJets_Run2 = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_jets_mask],
        subproducers=[JetPtCut, JetEtaCut, JetIDCut, JetPUIDCut],
    )

    GoodBJets = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.jet_id_mask],
        output=[q.good_bjets_mask],
        subproducers=[BJetPtCut, BJetEtaCut, BTagCut],
    )
    GoodBJets_Run2 = ProducerGroup(
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

with defaults(scopes=["mt", "et", "tt", "em", "mm", "ee"]):
    VetoOverlappingJets = Producer(
        call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
        input=[nanoAODv15.Jet_eta, nanoAODv15.Jet_phi, q.p4_1, q.p4_2],
        output=[q.jet_overlap_veto_mask],
    )

    with defaults(call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")', output=[]):
        GoodJetsWithVeto = ProducerGroup(input=[q.good_jets_mask], subproducers=[VetoOverlappingJets])
        GoodBJetsWithVeto = Producer(input=[q.good_bjets_mask, q.jet_overlap_veto_mask])

    with defaults(call="physicsobject::OrderByPt({df}, {output}, {input})", input=[q.jet_pt_corrected]):
        JetCollection = ProducerGroup(output=[q.good_jet_collection], subproducers=[GoodJetsWithVeto])
        BJetCollection = ProducerGroup(output=[q.good_bjet_collection], subproducers=[GoodBJetsWithVeto])

    JetPtVec = Producer(
        call="event::quantity::Take<float>({df}, {output}, {input})",
        input=[q.jet_pt_corrected, q.good_jet_collection],
        output=[q.jet_pt_vec],
    )
    JetEtaVec = Producer(
        call="event::quantity::Take<float>({df}, {output}, {input})",
        input=[nanoAODv15.Jet_eta, q.good_jet_collection],
        output=[q.jet_eta_vec],
    )
    JetHadFlavVec = Producer(
        call="event::quantity::Take<UChar_t>({df}, {output}, {input})",
        input=[nanoAODv15.Jet_hadronFlavour, q.good_jet_collection],
        output=[q.jet_hadronflavour_vec],
    )
    JetBTagVec = Producer(
        call="event::quantity::Take<float>({df}, {output}, {input})",
        input=[q.jet_BTag, q.good_jet_collection],
        output=[q.jet_btag_value_vec],
    )
   
    
    ##########################
    # Basic Jet Quantities
    # njets, pt, eta, phi, b-tag value
    ##########################

    LVJet1 = Producer(
        call="lorentzvector::Build({df}, {output}, {input}, 0)",
        input=[
            q.jet_pt_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            q.jet_mass_corrected,
            q.good_jet_collection,
        ],
        output=[q.jet_p4_1],
    )
    LVJet2 = Producer(
        call="lorentzvector::Build({df}, {output}, {input}, 1)",
        input=[
            q.jet_pt_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            q.jet_mass_corrected,
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

    with defaults(input=[q.jet_BTag, q.good_jet_collection]):
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
            q.jet_pt_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            q.jet_mass_corrected,
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

    with defaults(input=[q.jet_BTag, q.good_bjet_collection]):
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
