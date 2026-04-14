from ..quantities import output as q
from ..quantities import nanoAODv15, nanoAODv12, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for contruction of met related quantities
####################

with defaults(scopes=["global"]):
    with defaults(call="lorentzvector::BuildMET({df}, {output}, {input})"):
        BuildMetVector = Producer(input=[nanoAODv15.PuppiMET_pt, nanoAODv15.PuppiMET_phi], output=[q.puppimet_p4])
        BuildRawMetVector = Producer(input=[nanoAODv15.RawPuppiMET_pt, nanoAODv15.RawPuppiMET_phi], output=[q.rawmet_p4])
        
        with defaults(output=[q.pfmet_p4]):
            BuildPFMetVector_v15 = Producer(input=[nanoAODv15.PFMET_pt, nanoAODv15.PFMET_phi])
            BuildPFMetVector = Producer(input=[nanoAODv12.MET_pt, nanoAODv12.MET_phi])

    with defaults(call="event::quantity::Rename<float>({df}, {output}, {input})"):
        with defaults(output=[q.metcov00]):
            MetCov00_v15 = Producer(input=[nanoAODv15.PuppiMET_covXX])
            MetCov00 = Producer(input=[nanoAODv12.MET_covXX])
        with defaults(output=[q.metcov01]):
            MetCov01_v15 = Producer(input=[nanoAODv15.PuppiMET_covXY])
            MetCov01 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov10]):
            MetCov10_v15 = Producer(input=[nanoAODv15.PuppiMET_covXY])
            MetCov10 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov11]):
            MetCov11_v15 = Producer(input=[nanoAODv15.PuppiMET_covYY])
            MetCov11 = Producer(input=[nanoAODv12.MET_covYY])
        
        MetSumEt = Producer(input=[nanoAODv15.PuppiMET_sumEt], output=[q.metSumEt])

    with defaults(call="lorentzvector::GetPt({df}, {output}, {input})"):
        MetPt_uncorrected = Producer(input=[q.puppimet_p4], output=[q.puppimet_uncorrected])
        PFMetPt_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmet_uncorrected])

    with defaults(call="lorentzvector::GetPhi({df}, {output}, {input})"):
        MetPhi_uncorrected = Producer(input=[q.puppimet_p4], output=[q.puppimetphi_uncorrected])
        PFMetPhi_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmetphi_uncorrected])

    MetBasics_v15 = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            BuildMetVector,
            BuildRawMetVector,
            BuildPFMetVector_v15,
            MetPt_uncorrected,
            MetPhi_uncorrected,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00_v15,
            MetCov01_v15,
            MetCov10_v15,
            MetCov11_v15,
            MetSumEt,
        ],
    )

    MetBasics = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            BuildMetVector,
            BuildRawMetVector,
            BuildPFMetVector,
            MetPt_uncorrected,
            MetPhi_uncorrected,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00,
            MetCov01,
            MetCov10,
            MetCov11,
            MetSumEt,
        ],
    )

    MetMask = Producer(
        call="event::quantity::MinFlag<float>({df}, {output}, {input}, 0)",
        input=[nanoAODv15.PuppiMET_ptUnclusteredUp],
        output=[q.met_mask],
    )

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    # PuppiMET with jet propagated
    # for run 3 v15

    METTypeI = Producer(
        call='met::Type1Correction({df}, {output}, {input})',
        input=[
            q.rawmet_p4,
            q.jet_pt_L1_T1MET_corrected,
            q.jet_pt_T1MET_corrected,
            nanoAODv15.Jet_phi,
            nanoAODv15.Jet_muonSubtrDeltaPhi,
            nanoAODv15.Jet_chEmEF,
            nanoAODv15.Jet_neEmEF,
            nanoAODv15.CorrT1METJet_phi,
            nanoAODv15.CorrT1METJet_muonSubtrDeltaPhi,
            nanoAODv15.CorrT1METJet_EmEF,
        ],
        output = [q.puppimet_p4_jetcorrected],
    )
    METTypeI_v12 = Producer(
        call='met::Type1Correction({df}, {output}, {input})',
        input=[
            q.rawmet_p4,
            q.jet_pt_L1_T1MET_corrected,
            q.jet_pt_T1MET_corrected,
            nanoAODv15.Jet_phi,
            nanoAODv15.Jet_chEmEF,
            nanoAODv15.Jet_neEmEF,
            nanoAODv15.CorrT1METJet_phi,
        ],
        output = [q.puppimet_p4_jetcorrected],
    )
    
    # for run 2 and run3 v12
    with defaults(call="physicsobject::PropagateToMET({df}, {output}, {input}, {propagateJets}, {min_jetpt_met_propagation})"):
        PartialJetsToMetInput = [
            q.jet_pt_corrected,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            q.jet_mass_corrected,
            nanoAODv15.Jet_pt,
            nanoAODv15.Jet_eta,
            nanoAODv15.Jet_phi,
            nanoAODv15.Jet_mass,
        ]
        PropagateJetsToMet = Producer(
            input=[q.puppimet_p4] + PartialJetsToMetInput,
            output=[q.puppimet_p4_jetcorrected],
        )
        PropagateJetsToPFMet = Producer(
            input=[q.pfmet_p4] + PartialJetsToMetInput,
            output=[q.pfmet_p4_jetcorrected],
        )
        
    # apply to both
    with defaults(call="lorentzvector::PropagateToMET({df}, {output}, {input}, {propagateLeptons})"):
        PropagateLeptonsToMet = Producer(
            input=[q.puppimet_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.puppimet_p4_leptoncorrected],
        )
        PropagateLeptonsToPFMet = Producer(
            input=[q.pfmet_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.pfmet_p4_leptoncorrected],
        )

    with defaults(call='met::RecoilCorrection({df}, correctionManager, {output}, {input}, "{recoil_corrections_file}", "Recoil_correction", "{recoil_method}", "{DY_order}", "{recoil_variation}", {applyRecoilCorrections})'):
        ApplyRecoilCorrections = Producer(
            input=[q.puppimet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.puppimet_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.pfmet_p4_recoilcorrected],
        )

    with defaults(call='met::RecoilCorrection({df}, {output}, {input}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})'):
        ApplyRecoilCorrections_Run2 = Producer(
            input=[q.puppimet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.jet_pt_corrected],
            output=[q.puppimet_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet_Run2 = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.jet_pt_corrected],
            output=[q.pfmet_p4_recoilcorrected],
        )

    with defaults(call="lorentzvector::GetPt({df}, {output}, {input})"):
        MetPt = Producer(input=[q.puppimet_p4_recoilcorrected], output=[q.puppimet])
        PFMetPt = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmet])

    with defaults(call="lorentzvector::GetPhi({df}, {output}, {input})"):
        MetPhi = Producer(input=[q.puppimet_p4_recoilcorrected], output=[q.puppimetphi])
        PFMetPhi = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmetphi])

    with defaults(call=None, input=None, output=None):
        MetCorrections = ProducerGroup(
            subproducers=[
                METTypeI,
                PropagateLeptonsToMet,
                ApplyRecoilCorrections,
                MetPt,
                MetPhi,
            ],
        )
        MetCorrections_v12 = ProducerGroup(
            subproducers=[
                METTypeI_v12,
                PropagateLeptonsToMet,
                ApplyRecoilCorrections,
                MetPt,
                MetPhi,
            ],
        )
        PFMetCorrections = ProducerGroup(
            subproducers=[
                PropagateJetsToPFMet,
                PropagateLeptonsToPFMet,
                ApplyRecoilCorrectionsPFMet,
                PFMetPt,
                PFMetPhi,
            ],
        )

        MetCorrections_Run2 = ProducerGroup(
            subproducers=[
                PropagateJetsToMet,
                PropagateLeptonsToMet,
                ApplyRecoilCorrections_Run2,
                MetPt,
                MetPhi,
            ],
        )
        PFMetCorrections_Run2 = ProducerGroup(
            subproducers=[
                PropagateJetsToPFMet,
                PropagateLeptonsToPFMet,
                ApplyRecoilCorrectionsPFMet_Run2,
                PFMetPt,
                PFMetPhi,
            ],
        )
