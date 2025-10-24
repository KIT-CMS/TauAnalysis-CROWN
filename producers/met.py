from ..quantities import output as q
from ..quantities import nanoAOD, nanoAODv12
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for contruction of met related quantities
####################

with defaults(scopes=["global"]):
    with defaults(call="lorentzvector::BuildMET({df}, {output}, {input})"):
        BuildMetVector = Producer(input=[nanoAOD.PuppiMET_pt, nanoAOD.PuppiMET_phi], output=[q.met_p4])
        BuildPFMetVector = Producer(input=[nanoAOD.PFMET_pt, nanoAOD.PFMET_phi], output=[q.pfmet_p4])
        #nanoAODv12
        BuildPFMetVectorv12 = Producer(input=[nanoAODv12.MET_pt, nanoAODv12.MET_phi], output=[q.pfmet_p4])

    with defaults(call="event::quantity::Rename<float>({df}, {output}, {input})"):
        MetCov00 = Producer(input=[nanoAOD.PuppiMET_covXX], output=[q.metcov00])
        MetCov01 = Producer(input=[nanoAOD.PuppiMET_covXY], output=[q.metcov01])
        MetCov10 = Producer(input=[nanoAOD.PuppiMET_covXY], output=[q.metcov10])
        MetCov11 = Producer(input=[nanoAOD.PuppiMET_covYY], output=[q.metcov11])
        MetSumEt = Producer(input=[nanoAOD.PuppiMET_sumEt], output=[q.metSumEt])
        #nanoAODv12
        MetCov00v12 = Producer(input=[nanoAODv12.MET_covXX], output=[q.metcov00])
        MetCov01v12 = Producer(input=[nanoAODv12.MET_covXY], output=[q.metcov01])
        MetCov10v12 = Producer(input=[nanoAODv12.MET_covXY], output=[q.metcov10])
        MetCov11v12 = Producer(input=[nanoAODv12.MET_covYY], output=[q.metcov11])

    with defaults(call="lorentzvector::GetPt({df}, {output}, {input})"):
        MetPt_uncorrected = Producer(input=[q.met_p4], output=[q.met_uncorrected])
        PFMetPt_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmet_uncorrected])

    with defaults(call="lorentzvector::GetPhi({df}, {output}, {input})"):
        MetPhi_uncorrected = Producer(input=[q.met_p4], output=[q.metphi_uncorrected])
        PFMetPhi_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmetphi_uncorrected])

    CalculateGenBosonVector = Producer(
        call="met::calculateGenBosonVector({df}, {output}, {input}, {is_data})",
        input=[
            nanoAOD.GenPart_pt,
            nanoAOD.GenPart_eta,
            nanoAOD.GenPart_phi,
            nanoAOD.GenPart_mass,
            nanoAOD.GenPart_pdgId,
            nanoAOD.GenPart_status,
            nanoAOD.GenPart_statusFlags,
        ],
        output=[q.recoil_genboson_p4_vec],
    )
    GenBosonMass = Producer(
        call="met::genBosonMass({df}, {output}, {input})",
        input=[q.recoil_genboson_p4_vec],
        output=[q.genbosonmass],
    )
    MetBasics = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            BuildPFMetVector,
            BuildMetVector,
            MetPt_uncorrected,
            MetPhi_uncorrected,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00,
            MetCov01,
            MetCov10,
            MetCov11,
            MetSumEt,
            CalculateGenBosonVector,
            GenBosonMass,
        ],
    )

    MetBasicsv12 = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            BuildPFMetVectorv12,
            BuildMetVector,
            MetPt_uncorrected,
            MetPhi_uncorrected,
            PFMetPt_uncorrected,
            PFMetPhi_uncorrected,
            MetCov00v12,
            MetCov01v12,
            MetCov10v12,
            MetCov11v12,
            MetSumEt,
            CalculateGenBosonVector,
            GenBosonMass,
        ],
    )

    MetMask = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, 0)",
        input=[nanoAOD.PuppiMET_ptUnclusteredUp],
        output=[q.met_mask],
    )

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    GenZpt = Producer(
        call="met::calculateGenBosonPt({df}, {output}, {input}, {is_data})",
        input=[
            nanoAOD.GenPart_pt,
            nanoAOD.GenPart_eta,
            nanoAOD.GenPart_phi,
            nanoAOD.GenPart_mass,
            nanoAOD.GenPart_pdgId,
            nanoAOD.GenPart_status,
            nanoAOD.GenPart_statusFlags,
        ],
        output=[],
    )
    with defaults(call="met::propagateLeptonsToMet({df}, {output}, {input}, {propagateLeptons})"):
        PropagateLeptonsToMet = Producer(
            input=[q.met_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.met_p4_leptoncorrected],
        )
        PropagateLeptonsToPFMet = Producer(
            input=[q.pfmet_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.pfmet_p4_leptoncorrected],
        )

    with defaults(call="met::propagateJetsToMet({df}, {output}, {input}, {propagateJets}, {min_jetpt_met_propagation})"):
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
            input=[q.met_p4_leptoncorrected] + PartialJetsToMetInput,
            output=[q.met_p4_jetcorrected],
        )
        PropagateJetsToPFMet = Producer(
            input=[q.pfmet_p4_leptoncorrected] + PartialJetsToMetInput,
            output=[q.pfmet_p4_jetcorrected],
        )

    with defaults(call='met::applyRecoilCorrections({df}, correctionManager, {output}, {input}, "{recoil_corrections_file}", "{DY_order}", "{recoil_method}", "{recoil_variation}", {applyRecoilCorrections}, {is_wjets})'):
        ApplyRecoilCorrections = Producer(
            input=[q.met_p4_jetcorrected, q.recoil_genboson_p4_vec, q.njets],
            output=[q.met_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet = Producer(
            input=[q.pfmet_p4_jetcorrected, q.recoil_genboson_p4_vec, q.njets],
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
                PropagateLeptonsToMet,
                PropagateJetsToMet,
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
