from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..scripts.ProducerWrapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    scopes,
)

####################
# Set of producers used for contruction of met related quantities
####################

with scopes(["global"]):
    BuildMetVector = Producer(
        call="lorentzvectors::buildMet({df}, {input}, {output})",
        input=[
            nanoAOD.MET_pt,
            nanoAOD.MET_phi,
        ],
        output=[q.met_p4],
    )
    BuildPFMetVector = Producer(
        call="lorentzvectors::buildMet({df}, {input}, {output})",
        input=[
            nanoAOD.PFMET_pt,
            nanoAOD.PFMET_phi,
        ],
        output=[q.pfmet_p4],
    )
    MetCov00 = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[
            nanoAOD.MET_covXX,
        ],
        output=[q.metcov00],
    )
    MetCov01 = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[
            nanoAOD.MET_covXY,
        ],
        output=[q.metcov01],
    )
    MetCov10 = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[
            nanoAOD.MET_covXY,
        ],
        output=[q.metcov10],
    )
    MetCov11 = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[
            nanoAOD.MET_covYY,
        ],
        output=[q.metcov11],
    )
    MetSumEt = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[
            nanoAOD.MET_sumEt,
        ],
        output=[q.metSumEt],
    )
    MetPt_uncorrected = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.met_p4],
        output=[q.met_uncorrected],
    )
    MetPhi_uncorrected = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.met_p4],
        output=[q.metphi_uncorrected],
    )
    PFMetPt_uncorrected = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.pfmet_p4],
        output=[q.pfmet_uncorrected],
    )
    PFMetPhi_uncorrected = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.pfmet_p4],
        output=[q.pfmetphi_uncorrected],
    )
    CalculateGenBosonVector = Producer(
        call="met::calculateGenBosonVector({df}, {input}, {output}, {is_data})",
        input=[
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_status,
            nanoAOD.GenParticle_statusFlags,
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

with scopes(["et", "mt", "tt", "em", "mm", "ee"]):
    PropagateLeptonsToMet = Producer(
        call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
        input=[q.met_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
        output=[q.met_p4_leptoncorrected],
    )
    PropagateLeptonsToPFMet = Producer(
        call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
        input=[q.pfmet_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
        output=[q.pfmet_p4_leptoncorrected],
    )
    PropagateJetsToMet = Producer(
        call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
        input=[
            q.met_p4_leptoncorrected,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.Jet_mass,
        ],
        output=[q.met_p4_jetcorrected],
    )
    PropagateJetsToPFMet = Producer(
        call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
        input=[
            q.pfmet_p4_leptoncorrected,
            q.Jet_pt_corrected,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            q.Jet_mass_corrected,
            nanoAOD.Jet_pt,
            nanoAOD.Jet_eta,
            nanoAOD.Jet_phi,
            nanoAOD.Jet_mass,
        ],
        output=[q.pfmet_p4_jetcorrected],
    )
    ApplyRecoilCorrections = Producer(
        call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
        input=[
            q.met_p4_jetcorrected,
            q.recoil_genboson_p4_vec,
            q.Jet_pt_corrected,
        ],
        output=[q.met_p4_recoilcorrected],
    )
    ApplyRecoilCorrectionsPFMet = Producer(
        call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
        input=[
            q.pfmet_p4_jetcorrected,
            q.recoil_genboson_p4_vec,
            q.Jet_pt_corrected,
        ],
        output=[q.pfmet_p4_recoilcorrected],
    )
    MetPt = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.met_p4_recoilcorrected],
        output=[q.met],
    )
    PFMetPt = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.pfmet_p4_recoilcorrected],
        output=[q.pfmet],
    )
    MetPhi = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.met_p4_recoilcorrected],
        output=[q.metphi],
    )
    PFMetPhi = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.pfmet_p4_recoilcorrected],
        output=[q.pfmetphi],
    )
    MetCorrections = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            PropagateLeptonsToMet,
            PropagateJetsToMet,
            ApplyRecoilCorrections,
            MetPt,
            MetPhi,
        ],
    )
    PFMetCorrections = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            PropagateLeptonsToPFMet,
            PropagateJetsToPFMet,
            ApplyRecoilCorrectionsPFMet,
            PFMetPt,
            PFMetPhi,
        ],
    )
