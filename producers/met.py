from ..quantities import output as q
from ..quantities import nanoAOD, nanoAODv12
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for contruction of met related quantities
####################

with defaults(scopes=["global"]):
    with defaults(call="lorentzvector::BuildMET({df}, {output}, {input})"):
        BuildMetVector = Producer(input=[nanoAOD.PuppiMET_pt, nanoAOD.PuppiMET_phi], output=[q.puppimet_p4])
        BuildRawMetVector = Producer(input=[nanoAOD.RawPuppiMET_pt, nanoAOD.RawPuppiMET_phi], output=[q.met_p4])
        
        with defaults(output=[q.pfmet_p4]):
            BuildPFMetVector = Producer(input=[nanoAOD.PFMET_pt, nanoAOD.PFMET_phi])
            BuildPFMetVector_v12 = Producer(input=[nanoAODv12.MET_pt, nanoAODv12.MET_phi])

    with defaults(call="event::quantity::Rename<float>({df}, {output}, {input})"):
        with defaults(output=[q.metcov00]):
            MetCov00 = Producer(input=[nanoAOD.PuppiMET_covXX])
            MetCov00_v12 = Producer(input=[nanoAODv12.MET_covXX])
        with defaults(output=[q.metcov01]):
            MetCov01 = Producer(input=[nanoAOD.PuppiMET_covXY])
            MetCov01_v12 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov10]):
            MetCov10 = Producer(input=[nanoAOD.PuppiMET_covXY])
            MetCov10_v12 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov11]):
            MetCov11 = Producer(input=[nanoAOD.PuppiMET_covYY])
            MetCov11_v12 = Producer(input=[nanoAODv12.MET_covYY])
        
        MetSumEt = Producer(input=[nanoAOD.PuppiMET_sumEt], output=[q.metSumEt])

    with defaults(call="lorentzvector::GetPt({df}, {output}, {input})"):
        MetPt_uncorrected = Producer(input=[q.met_p4], output=[q.met_uncorrected])
        PuppiMetPt = Producer(input=[q.puppimet_p4], output=[q.puppimet])
        PFMetPt_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmet_uncorrected])

    with defaults(call="lorentzvector::GetPhi({df}, {output}, {input})"):
        MetPhi_uncorrected = Producer(input=[q.met_p4], output=[q.metphi_uncorrected])
        PuppiMetPhi = Producer(input=[q.puppimet_p4], output=[q.puppimetphi])
        PFMetPhi_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmetphi_uncorrected])

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
            PuppiMetPt,
            PuppiMetPhi,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00,
            MetCov01,
            MetCov10,
            MetCov11,
            MetSumEt,
        ],
    )

    MetBasics_v12 = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            BuildMetVector,
            BuildRawMetVector,
            BuildPFMetVector_v12,
            MetPt_uncorrected,
            MetPhi_uncorrected,
            PuppiMetPt,
            PuppiMetPhi,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00_v12,
            MetCov01_v12,
            MetCov10_v12,
            MetCov11_v12,
            MetSumEt,
        ],
    )

    MetMask = Producer(
        call="physicsobject::CutMinSingle<float>({df}, {output}, {input}, 0)",
        input=[nanoAOD.PuppiMET_ptUnclusteredUp],
        output=[q.met_mask],
    )

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    # PuppiMET with jet propagated
    # for run 3
    METTypeI = Producer(
        call='met::TypeIMET({df}, correctionManager, {output}, {input}, {jet_jer_file}, {jet_jec_algo}, {jet_jes_tag}, {jet_jes_sources}, {jet_jer_tag}, {jet_jes_shift}, {jet_jer_shift}, "{era}", {is_data})',
        input=[
            q.met_p4,
            q.Jet_rawPt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.Jet_area,
            nanoAOD.Jet_muonSubtrFactor,
            nanoAOD.CorrT1METJet_rawPt,
            nanoAOD.CorrT1METJet_eta,
            nanoAOD.CorrT1METJet_phi,
            nanoAOD.CorrT1METJet_area,
            nanoAOD.CorrT1METJet_muonSubtrFactor,
            nanoAOD.Jet_chEmEF,
            nanoAOD.Jet_neEmEF,
            nanoAOD.CorrT1METJet_EmEF,
            q.gen_pt,
            q.gen_eta,
            q.gen_phi,
            nanoAOD.Rho_fixedGridRhoFastjetAll,
            q.Jet_seed,
            nanoAOD.run,
        ],
        output = [q.met_p4_jetcorrected],
    )

    METTypeI_v2 = Producer(
        call='met::TypeIMET_v2({df}, correctionManager, {output}, {input})',
        input=[
            q.met_p4,
            q.Jet_pt_L1corrected, 
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.CorrT1METJet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.CorrT1METJet_phi,
            nanoAOD.Jet_chEmEF,
            nanoAOD.Jet_neEmEF,
            nanoAOD.CorrT1METJet_EmEF,
            ],
        output = [q.met_p4_jetcorrected],
    )
    
    # for run 2
    with defaults(call="physicsobject::PropagateToMET({df}, {output}, {input}, {propagateJets}, {min_jetpt_met_propagation})"):
        PartialJetsToMetInput = [
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.Jet_mass,
        ]
        PropagateJetsToMet = Producer(
            input=[q.puppimet_p4] + PartialJetsToMetInput,
            output=[q.met_p4_jetcorrected],
        )
        PropagateJetsToPFMet = Producer(
            input=[q.pfmet_p4] + PartialJetsToMetInput,
            output=[q.pfmet_p4_jetcorrected],
        )
        
    # apply to both
    with defaults(call="lorentzvector::PropagateToMET({df}, {output}, {input}, {propagateLeptons})"):
        PropagateLeptonsToMet = Producer(
            input=[q.met_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.met_p4_leptoncorrected],
        )
        PropagateLeptonsToPFMet = Producer(
            input=[q.pfmet_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.pfmet_p4_leptoncorrected],
        )

    with defaults(call='met::RecoilCorrection({df}, correctionManager, {output}, {input}, "{recoil_corrections_file}", "Recoil_correction", "{recoil_method}", "{DY_order}", "{recoil_variation}", {applyRecoilCorrections})'):
        ApplyRecoilCorrections = Producer(
            input=[q.met_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.met_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.pfmet_p4_recoilcorrected],
        )

    with defaults(call='met::RecoilCorrection({df}, {output}, {input}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})'):
        ApplyRecoilCorrections_Run2 = Producer(
            input=[q.met_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.Jet_pt_corrected],
            output=[q.met_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet_Run2 = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.Jet_pt_corrected],
            output=[q.pfmet_p4_recoilcorrected],
        )

    with defaults(call="lorentzvector::GetPt({df}, {output}, {input})"):
        MetPt = Producer(input=[q.met_p4_recoilcorrected], output=[q.met])
        PFMetPt = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmet])

    with defaults(call="lorentzvector::GetPhi({df}, {output}, {input})"):
        MetPhi = Producer(input=[q.met_p4_recoilcorrected], output=[q.metphi])
        PFMetPhi = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmetphi])

    with defaults(call=None, input=None, output=None):
        MetCorrections = ProducerGroup(
            subproducers=[
                METTypeI_v2,
                PropagateLeptonsToMet,
                ApplyRecoilCorrections,
                MetPt,
                MetPhi,
            ],
        )
        PFMetCorrections = ProducerGroup(
            subproducers=[
                PropagateLeptonsToPFMet,
                PropagateJetsToPFMet,
                ApplyRecoilCorrectionsPFMet,
                PFMetPt,
                PFMetPhi,
            ],
        )

        MetCorrections_Run2 = ProducerGroup(
            subproducers=[
                PropagateLeptonsToMet,
                PropagateJetsToMet,
                ApplyRecoilCorrections_Run2,
                MetPt,
                MetPhi,
            ],
        )
        PFMetCorrections_Run2 = ProducerGroup(
            subproducers=[
                PropagateLeptonsToPFMet,
                PropagateJetsToPFMet,
                ApplyRecoilCorrectionsPFMet_Run2,
                PFMetPt,
                PFMetPhi,
            ],
        )
