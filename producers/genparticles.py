from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..scripts.ProducerWrapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    scopes,
)

####################
# Set of producers to get the genParticles from the ditaupair
####################

MTGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["mt"],
)
ETGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["et"],
)
TTGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Tau_indexToGen, nanoAOD.Tau_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["tt"],
)
EMGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Muon_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["em"],
)
MuMuGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Muon_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["mm"],
)
ElElGenPair = Producer(
    call="ditau_pairselection::buildgenpair({df}, {input}, {output})",
    input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Electron_indexToGen],
    output=[q.gen_dileptonpair],
    scopes=["ee"],
)
MuMuTrueGenPair = Producer(
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

with scopes(["mt", "et", "tt", "em", "mm", "ee"]):
    EmbeddingGenPair = Producer(
        call="ditau_pairselection::buildtruegenpair({df}, {input}, {output}, {truegen_mother_pdgid}, {truegen_daughter_1_pdgid}, {truegen_daugher_2_pdgid})",
        input=[
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_status,
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_motherid,
            nanoAOD.GenParticle_pt,
        ],
        output=[q.gen_dileptonpair],
    )

    ####################
    # Set of general producers for Gen DiTauPair Quantities
    ####################

    LVGenParticle1 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
        input=[
            q.gen_dileptonpair,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
        ],
        output=[q.gen_p4_1],
    )
    LVGenParticle2 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
        input=[
            q.gen_dileptonpair,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
        ],
        output=[q.gen_p4_2],
    )
    LVTrueGenParticle1 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
        input=[
            q.truegenpair,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
        ],
        output=[q.gen_p4_1],
    )
    LVTrueGenParticle2 = Producer(
        call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
        input=[
            q.truegenpair,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
        ],
        output=[q.gen_p4_2],
    )
    gen_pt_1 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.gen_p4_1],
        output=[q.gen_pt_1],
    )
    gen_pt_2 = Producer(
        call="quantities::pt({df}, {output}, {input})",
        input=[q.gen_p4_2],
        output=[q.gen_pt_2],
    )
    gen_eta_1 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.gen_p4_1],
        output=[q.gen_eta_1],
    )
    gen_eta_2 = Producer(
        call="quantities::eta({df}, {output}, {input})",
        input=[q.gen_p4_2],
        output=[q.gen_eta_2],
    )
    gen_phi_1 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.gen_p4_1],
        output=[q.gen_phi_1],
    )
    gen_phi_2 = Producer(
        call="quantities::phi({df}, {output}, {input})",
        input=[q.gen_p4_2],
        output=[q.gen_phi_2],
    )
    gen_mass_1 = Producer(
        call="quantities::mass({df}, {output}, {input})",
        input=[q.gen_p4_1],
        output=[q.gen_mass_1],
    )
    gen_mass_2 = Producer(
        call="quantities::mass({df}, {output}, {input})",
        input=[q.gen_p4_2],
        output=[q.gen_mass_2],
    )
    gen_pdgid_1 = Producer(
        call="quantities::pdgid({df}, {output}, 0, {input})",
        input=[q.gen_dileptonpair, nanoAOD.GenParticle_pdgId],
        output=[q.gen_pdgid_1],
    )
    gen_pdgid_2 = Producer(
        call="quantities::pdgid({df}, {output}, 1, {input})",
        input=[q.gen_dileptonpair, nanoAOD.GenParticle_pdgId],
        output=[q.gen_pdgid_2],
    )
    gen_m_vis = Producer(
        call="quantities::m_vis({df}, {output}, {input_vec})",
        input=[q.gen_p4_1, q.gen_p4_2],
        output=[q.gen_m_vis],
    )

gen_taujet_pt_1 = Producer(
    call="quantities::tau::matching_genjet_pt({df}, {output}, 0, {input})",
    input=[
        q.dileptonpair,
        nanoAOD.Tau_associatedJet,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_pt,
    ],
    output=[q.gen_taujet_pt_1],
    scopes=["tt"],
)
gen_taujet_pt_2 = Producer(
    call="quantities::tau::matching_genjet_pt({df}, {output}, 1, {input})",
    input=[
        q.dileptonpair,
        nanoAOD.Tau_associatedJet,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_pt,
    ],
    output=[q.gen_taujet_pt_2],
    scopes=["mt", "et", "tt"],
)
UnrollGenMuLV1 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["mt", "mm"],
    subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
)
UnrollGenMuLV2 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["em", "mm"],
    subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
)
UnrollGenElLV1 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["em", "ee", "et"],
    subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
)
UnrollGenElLV2 = ProducerGroup(
    call=None,
    input=None,
    output=None,
    scopes=["ee"],
    subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
)
UnrollGenTauLV1 = ProducerGroup(
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

with scopes(["mt", "et", "tt", "em", "ee", "mm"]):
    GenPairForGenMatching = Producer(
        call="genmatching::tau::hadronicGenTaus({df}, {output}, {input})",
        input=[
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_motherid,
        ],
        output=[q.hadronic_gen_taus],
    )
    GenMatchP1 = Producer(
        call="genmatching::tau::genmatching({df}, {output}, {input})",
        input=[
            q.hadronic_gen_taus,
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
            q.p4_1,
        ],
        output=[q.gen_match_1],
    )
    GenMatchP2 = Producer(
        call="genmatching::tau::genmatching({df}, {output}, {input})",
        input=[
            q.hadronic_gen_taus,
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_pt,
            nanoAOD.GenParticle_eta,
            nanoAOD.GenParticle_phi,
            nanoAOD.GenParticle_mass,
            q.p4_2,
        ],
        output=[q.gen_match_2],
    )
    GenMatching = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            GenPairForGenMatching,
            GenMatchP1,
            GenMatchP2,
        ],
    )
