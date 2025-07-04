from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers to get the genParticles from the ditaupair
####################
MTGenPair = Producer(
    name="MTGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["mt"],
)
ETGenPair = Producer(
    name="ETGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["et"],
)
TTGenPair = Producer(
    name="TTGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Tau_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["tt"],
)
EMGenPair = Producer(
    name="EMGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Muon_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["em"],
)
MuMuGenPair = Producer(
    name="MuMuGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Muon_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["mm"],
)
ElElGenPair = Producer(
    name="ElElGenPair",
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Electron_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["ee"],
)
MuMuTrueGenPair = Producer(
    name="GenPair",
    call="ditau_pairselection::buildtruegenpair({df}, {input}, {output}, {truegen_mother_pdgid}, {truegen_daughter_1_pdgid}, {truegen_daugher_2_pdgid})",
    input=[
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_status,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_motherid,
        nanoAOD.GenParticle_pt,
    ],
    output=[q.truegenpair],
    scopes=["mm"],
)
EmbeddingGenPair = Producer(
    name="EmbeddingGenPair",
    call="ditau_pairselection::buildtruegenpair({df}, {input}, {output}, {truegen_mother_pdgid}, {truegen_daughter_1_pdgid}, {truegen_daugher_2_pdgid})",
    input=[
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_status,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_motherid,
        nanoAOD.GenParticle_pt,
    ],
    output=[q.gen_dileptonpair],
    scopes=["mm", "ee", "em", "et", "mt", "tt"],
)
####################
# Set of general producers for Gen DiTauPair Quantities
####################

LVGenParticle1 = Producer(
    name="LVGenParticle1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        q.gen_dileptonpair,
    ],
    output=[q.gen_p4_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LVGenParticle2 = Producer(
    name="LVGenParticle2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        q.gen_dileptonpair,
    ],
    output=[q.gen_p4_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LVTrueGenParticle1 = Producer(
    name="LVTrueGenParticle1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        q.truegenpair,
    ],
    output=[q.gen_p4_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LVTrueGenParticle2 = Producer(
    name="LVTrueGenParticle2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        q.truegenpair,
    ],
    output=[q.gen_p4_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_pt_1 = Producer(
    name="gen_pt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.gen_p4_1],
    output=[q.gen_pt_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_pt_2 = Producer(
    name="gen_pt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.gen_p4_2],
    output=[q.gen_pt_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_eta_1 = Producer(
    name="gen_eta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.gen_p4_1],
    output=[q.gen_eta_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_eta_2 = Producer(
    name="gen_eta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.gen_p4_2],
    output=[q.gen_eta_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_phi_1 = Producer(
    name="gen_phi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.gen_p4_1],
    output=[q.gen_phi_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_phi_2 = Producer(
    name="gen_phi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.gen_p4_2],
    output=[q.gen_phi_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_mass_1 = Producer(
    name="gen_mass_1",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.gen_p4_1],
    output=[q.gen_mass_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_mass_2 = Producer(
    name="gen_mass_2",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.gen_p4_2],
    output=[q.gen_mass_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_pdgid_1 = Producer(
    name="gen_pdgid_1",
    call="event::quantity::Get<int>({df}, {output}, {input}, 0)",
    input=[nanoAOD.GenParticle_pdgId, q.gen_dileptonpair],
    output=[q.gen_pdgid_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_pdgid_2 = Producer(
    name="gen_pdgid_2",
    call="event::quantity::Get<int>({df}, {output}, {input}, 1)",
    input=[nanoAOD.GenParticle_pdgId, q.gen_dileptonpair],
    output=[q.gen_pdgid_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_m_vis = Producer(
    name="gen_m_vis",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.gen_p4_1, q.gen_p4_2],
    output=[q.gen_m_vis],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
gen_taujet_pt_1 = Producer(
    name="gen_taujet_pt_1",
    call="quantities::GenJetMatching({df}, {output}, {input}, 0)",
    input=[
        nanoAOD.GenJet_pt,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.Tau_associatedJet,
        q.dileptonpair,
    ],
    output=[q.gen_taujet_pt_1],
    scopes=["tt"],
)
gen_taujet_pt_2 = Producer(
    name="gen_taujet_pt_2",
    call="quantities::GenJetMatching({df}, {output}, {input}, 1)",
    input=[
        nanoAOD.GenJet_pt,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.Tau_associatedJet,
        q.dileptonpair,
    ],
    output=[q.gen_taujet_pt_2],
    scopes=["mt", "et", "tt"],
)
UnrollGenMuLV1 = ProducerGroup(
    name="UnrollGenMuLV1",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "mm"],
    subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
)
UnrollGenMuLV2 = ProducerGroup(
    name="UnrollGenMuLV2",
    call=None,
    input=None,
    output=None,
    scopes=["em", "mm"],
    subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
)
UnrollGenElLV1 = ProducerGroup(
    name="UnrollGenElLV1",
    call=None,
    input=None,
    output=None,
    scopes=["em", "ee", "et"],
    subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
)
UnrollGenElLV2 = ProducerGroup(
    name="UnrollGenElLV2",
    call=None,
    input=None,
    output=None,
    scopes=["ee"],
    subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
)
UnrollGenTauLV1 = ProducerGroup(
    name="UnrollGenTauLV1",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        gen_pt_1,
        gen_eta_1,
        gen_phi_1,
        gen_mass_1,
        gen_pdgid_1,
        gen_taujet_pt_1,
    ],
)
UnrollGenTauLV2 = ProducerGroup(
    name="UnrollGenLV2",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt"],
    subproducers=[
        gen_pt_2,
        gen_eta_2,
        gen_phi_2,
        gen_mass_2,
        gen_pdgid_2,
        gen_taujet_pt_2,
    ],
)

MTGenDiTauPairQuantities = ProducerGroup(
    name="MTGenDiTauPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        MTGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenMuLV1,
        UnrollGenTauLV2,
        gen_m_vis,
    ],
)
ETGenDiTauPairQuantities = ProducerGroup(
    name="ETGenDiTauPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers=[
        ETGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenElLV1,
        UnrollGenTauLV2,
        gen_m_vis,
    ],
)
TTGenDiTauPairQuantities = ProducerGroup(
    name="TTGenDiTauPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        TTGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenTauLV1,
        UnrollGenTauLV2,
        gen_m_vis,
    ],
)
EMGenDiTauPairQuantities = ProducerGroup(
    name="EMGenDiTauPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["em"],
    subproducers=[
        EMGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenElLV1,
        UnrollGenMuLV2,
        gen_m_vis,
    ],
)
ElElGenPairQuantities = ProducerGroup(
    name="ElElGenPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["ee"],
    subproducers=[
        ElElGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenElLV1,
        UnrollGenElLV2,
        gen_m_vis,
    ],
)
MuMuGenPairQuantities = ProducerGroup(
    name="MuMuGenPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mm"],
    subproducers=[
        MuMuGenPair,
        LVGenParticle1,
        LVGenParticle2,
        UnrollGenMuLV1,
        UnrollGenMuLV2,
        gen_m_vis,
    ],
)
MuMuTrueGenDiTauPairQuantities = ProducerGroup(
    name="MuMuGenPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mm"],
    subproducers=[
        MuMuTrueGenPair,
        LVTrueGenParticle1,
        LVTrueGenParticle2,
        UnrollGenMuLV1,
        UnrollGenMuLV2,
        gen_m_vis,
    ],
)


#######################
# DiTau Genmatching
#######################

GenPairForGenMatching = Producer(
    name="GenPairForGenMatching",
    call="genparticles::tau::HadronicGenTaus({df}, {output}, {input})",
    input=[
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_motherid,
    ],
    output=[q.hadronic_gen_taus],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)

GenMatchP1 = Producer(
    name="GenMatchP1",
    call="genparticles::tau::GenMatching({df}, {output}, {input})",
    input=[
        q.hadronic_gen_taus,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_motherid,
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,        
        q.p4_1,
    ],
    output=[q.gen_match_1],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)

GenMatchP2 = Producer(
    name="GenMatchP2",
    call="genparticles::tau::GenMatching({df}, {output}, {input})",
    input=[
        q.hadronic_gen_taus,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_motherid,
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        q.p4_2,
    ],
    output=[q.gen_match_2],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)

GenMatching = ProducerGroup(
    name="GenMatching",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
    subproducers=[
        GenPairForGenMatching,
        GenMatchP1,
        GenMatchP2,
    ],
)
