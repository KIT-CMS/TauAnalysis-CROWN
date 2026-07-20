from code_generation.quantity import NanoAODQuantity

from ..quantities import output as q
from ..quantities import nanoAODv15, nanoAODv12, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for contruction of met related quantities
####################

# The Run3 (v15/v12) MET pipeline recomputes its own Type-1 corrected MET
# starting from RawPuppiMET + JECs (see METTypeI / METTypeI_v12 below), instead
# of relying on the officially Type-1-corrected PuppiMET_pt/phi branch stored
# in NanoAOD. The unclustered energy variation, however, is only provided by
# NanoAOD as an absolute pt/phi variant of that official (Type-1 corrected)
# PuppiMET branch (PuppiMET_ptUnclusteredUp/Down, PuppiMET_phiUnclusteredUp/Down)
# -- there is no dedicated "raw MET + unclustered variation" branch. To
# propagate this NanoAOD-provided unclustered variation onto our own
# recomputed MET, we build the delta between the official nominal PuppiMET and
# its Unclustered-shifted variant, and add this delta on top of our own MET.
# For this, we need a reference to the *always-nominal* PuppiMET_pt/phi
# branches that is immune to the metUnclusteredEnUp/Down shift substitution
# (which is registered on nanoAODv15.PuppiMET_pt/phi directly). We therefore
# define separate NanoAODQuantity instances pointing at the same branches.
PuppiMET_pt_nominal_ref = NanoAODQuantity("PuppiMET_pt")
PuppiMET_phi_nominal_ref = NanoAODQuantity("PuppiMET_phi")

with defaults(scopes=["global"]):
    with defaults(call='''lorentzvector::BuildMET({df}, {output}, {input})'''):
        BuildMetVector = Producer(input=[nanoAODv15.PuppiMET_pt, nanoAODv15.PuppiMET_phi], output=[q.puppimet_p4])
        BuildRawMetVector = Producer(input=[nanoAODv15.RawPuppiMET_pt, nanoAODv15.RawPuppiMET_phi], output=[q.rawmet_p4])

        with defaults(output=[q.pfmet_p4]):
            BuildPFMetVector = Producer(input=[nanoAODv15.PFMET_pt, nanoAODv15.PFMET_phi])
            BuildPFMetVector_v12 = Producer(input=[nanoAODv12.MET_pt, nanoAODv12.MET_phi])

    with defaults(call='''event::quantity::Rename<float>({df}, {output}, {input})'''):
        with defaults(output=[q.metcov00]):
            MetCov00 = Producer(input=[nanoAODv15.PuppiMET_covXX])
            MetCov00_v12 = Producer(input=[nanoAODv12.MET_covXX])
        with defaults(output=[q.metcov01]):
            MetCov01 = Producer(input=[nanoAODv15.PuppiMET_covXY])
            MetCov01_v12 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov10]):
            MetCov10 = Producer(input=[nanoAODv15.PuppiMET_covXY])
            MetCov10_v12 = Producer(input=[nanoAODv12.MET_covXY])
        with defaults(output=[q.metcov11]):
            MetCov11 = Producer(input=[nanoAODv15.PuppiMET_covYY])
            MetCov11_v12 = Producer(input=[nanoAODv12.MET_covYY])

        MetSumEt = Producer(input=[nanoAODv15.PuppiMET_sumEt], output=[q.metSumEt])

    with defaults(call='''lorentzvector::GetPt({df}, {output}, {input})'''):
        MetPt_uncorrected = Producer(input=[q.rawmet_p4], output=[q.puppimet_uncorrected])
        PFMetPt_uncorrected = Producer(input=[q.pfmet_p4], output=[q.pfmet_uncorrected])

    with defaults(call='''lorentzvector::GetPhi({df}, {output}, {input})'''):
        MetPhi_uncorrected = Producer(input=[q.rawmet_p4], output=[q.puppimetphi_uncorrected])
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
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, 0)''',
        input=[nanoAODv15.PuppiMET_ptUnclusteredUp],
        output=[q.met_mask],
    )

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    # PuppiMET with jet propagated
    # for run 3 v15

    METTypeI = Producer(
        call='''met::Type1Correction({df}, {output}, {input})''',
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
        call='''met::Type1Correction({df}, {output}, {input})''',
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
    with defaults(call='''physicsobject::PropagateToMET({df}, {output}, {input}, "{propagateJets}", {min_jetpt_met_propagation})'''):
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
    with defaults(call='''lorentzvector::PropagateToMET({df}, {output}, {input}, "{propagateLeptons}")'''):
        PropagateLeptonsToMet = Producer(
            input=[q.puppimet_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.puppimet_p4_leptoncorrected],
        )
        PropagateLeptonsToPFMet = Producer(
            input=[q.pfmet_p4_jetcorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
            output=[q.pfmet_p4_leptoncorrected],
        )

    with defaults(call='''met::RecoilCorrection({df}, correctionManager, {output}, {input}, "{recoil_corrections_file}", "Recoil_correction", "{recoil_method}", "{DY_order}", "{recoil_variation}", {applyRecoilCorrections})'''):
        ApplyRecoilCorrections = Producer(
            input=[q.puppimet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.puppimet_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
            output=[q.pfmet_p4_recoilcorrected],
        )

    # Recoil uncertainty variations (Response/Resolution, Up/Down) are
    # applied via the "Uncertainty" method of the recoil correction. Per the
    # HLepRare documentation, these uncertainties have to be evaluated on top
    # of the *nominally recoil-corrected* MET (H_para/H_perp are computed from
    # the already QuantileMapHist-corrected MET, not from the pre-recoil
    # MET), so this producer is chained after ApplyRecoilCorrections and
    # takes its output (q.puppimet_p4_recoilcorrected, always computed with
    # the nominal "QuantileMapHist" method) as its input MET. It is a no-op
    # (renames through) unless a recoil response/resolution shift is active.
    ApplyRecoilUncertainty = Producer(
        call='''met::RecoilCorrection({df}, correctionManager, {output}, {input}, "{recoil_corrections_file}", "Recoil_correction", "Uncertainty", "{DY_order}", "{recoil_uncertainty_variation}", {applyRecoilUncertainty})''',
        input=[q.puppimet_p4_recoilcorrected, q.genboson_p4, q.visgenboson_p4, q.njets],
        output=[q.puppimet_p4_recoiluncertaintycorrected],
    )

    # Bundles the nominal (QuantileMapHist) recoil correction with the
    # response/resolution uncertainty step that must be evaluated on top of
    # it (see comment on ApplyRecoilUncertainty above). This is purely a
    # convenience grouping to avoid repeating the same two-producer chain in
    # both MetCorrections and MetCorrections_v12 below; ApplyRecoilCorrections
    # and ApplyRecoilUncertainty remain independently usable/addressable
    # (e.g. config.py's metRecoilResponse/metRecoilResolution shifts still
    # target met.ApplyRecoilUncertainty directly, and other configs such as
    # doublemuon_controlregion.py still use met.ApplyRecoilCorrections on its
    # own without the uncertainty step).
    RecoilCorrectionRun3 = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            ApplyRecoilCorrections,
            ApplyRecoilUncertainty,
        ],
    )

    with defaults(call='''met::RecoilCorrection({df}, {output}, {input}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, "{recoil_systematic_shift_up}", "{recoil_systematic_shift_down}", {is_wjets})'''):
        ApplyRecoilCorrections_Run2 = Producer(
            input=[q.puppimet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.jet_pt_corrected],
            output=[q.puppimet_p4_recoilcorrected],
        )
        ApplyRecoilCorrectionsPFMet_Run2 = Producer(
            input=[q.pfmet_p4_leptoncorrected, q.genboson_p4, q.visgenboson_p4, q.jet_pt_corrected],
            output=[q.pfmet_p4_recoilcorrected],
        )

    # Propagate the NanoAOD-provided unclustered energy variation (only
    # available as an absolute pt/phi variant of the officially Type-1
    # corrected PuppiMET, see comment on PuppiMET_pt_nominal_ref above) onto
    # our own re-derived (raw MET + JEC) MET as an additive x/y shift:
    #   MET_new = MET + (shifted_nanoAOD_PuppiMET - nominal_nanoAOD_PuppiMET)
    # Under nominal running (no metUnclusteredEnUp/Down shift active), the
    # "shiftable" and "nominal" inputs both resolve to the same PuppiMET_pt/phi
    # branch, so the applied shift is exactly zero and the MET is unchanged.
    ApplyUnclusteredMetShift = Producer(
        call='''met::PropagateUnclusteredEnergyToMET({df}, {output}, {input}, {propagateUnclustered})''',
        input=[
            q.puppimet_p4_recoiluncertaintycorrected,
            PuppiMET_pt_nominal_ref,
            PuppiMET_phi_nominal_ref,
            nanoAODv15.PuppiMET_pt,
            nanoAODv15.PuppiMET_phi,
        ],
        output=[q.puppimet_p4_unclustered_corrected],
    )

    with defaults(call='''lorentzvector::GetPt({df}, {output}, {input})'''):
        MetPt = Producer(input=[q.puppimet_p4_recoilcorrected], output=[q.puppimet])
        MetPt_Run3 = Producer(input=[q.puppimet_p4_unclustered_corrected], output=[q.puppimet])
        PFMetPt = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmet])

    with defaults(call='''lorentzvector::GetPhi({df}, {output}, {input})'''):
        MetPhi = Producer(input=[q.puppimet_p4_recoilcorrected], output=[q.puppimetphi])
        MetPhi_Run3 = Producer(input=[q.puppimet_p4_unclustered_corrected], output=[q.puppimetphi])
        PFMetPhi = Producer(input=[q.pfmet_p4_recoilcorrected], output=[q.pfmetphi])

    with defaults(call=None, input=None, output=None):
        MetCorrections = ProducerGroup(
            subproducers=[
                METTypeI,
                PropagateLeptonsToMet,
                RecoilCorrectionRun3,
                ApplyUnclusteredMetShift,
                MetPt_Run3,
                MetPhi_Run3,
            ],
        )
        MetCorrections_v12 = ProducerGroup(
            subproducers=[
                METTypeI_v12,
                PropagateLeptonsToMet,
                RecoilCorrectionRun3,
                ApplyUnclusteredMetShift,
                MetPt_Run3,
                MetPhi_Run3,
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
