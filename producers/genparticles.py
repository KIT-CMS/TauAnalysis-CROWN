from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers to get the genParticles from the ditaupair
####################
with defaults(call="ditau_pairselection::buildgenpair({df}, {input}, {output})", output=[q.gen_dileptonpair]):
    MTGenPair = Producer(input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Tau_indexToGen], scopes=["mt"])
    ETGenPair = Producer(input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Tau_indexToGen], scopes=["et"])
    TTGenPair = Producer(input=[q.dileptonpair, nanoAOD.Tau_indexToGen, nanoAOD.Tau_indexToGen], scopes=["tt"])
    EMGenPair = Producer(input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Muon_indexToGen], scopes=["em"])
    MuMuGenPair = Producer(input=[q.dileptonpair, nanoAOD.Muon_indexToGen, nanoAOD.Muon_indexToGen], scopes=["mm"])
    ElElGenPair = Producer(input=[q.dileptonpair, nanoAOD.Electron_indexToGen, nanoAOD.Electron_indexToGen], scopes=["ee"])

with defaults(
    call="ditau_pairselection::buildtruegenpair({df}, {input}, {output}, {truegen_mother_pdgid}, {truegen_daughter_1_pdgid}, {truegen_daugher_2_pdgid})",
    input=[
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_status,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_motherid,
        nanoAOD.GenParticle_pt,
    ],
):
    EmbeddingGenPair = Producer(output=[q.gen_dileptonpair], scopes=["mm", "ee", "em", "et", "mt", "tt"])
    MuMuTrueGenPair = Producer(output=[q.truegenpair], scopes=["mm"])

####################
# Set of general producers for Gen DiTauPair Quantities
####################

with defaults(scopes=["mt", "et", "tt", "em", "mm", "ee"]):
    with defaults(call="lorentzvector::Build({df}, {output}, {input}, 0)", output=[q.gen_p4_1]):
        LVGenParticle1 = Producer(
            input=[
                nanoAOD.GenParticle_pt,
                nanoAOD.GenParticle_eta,
                nanoAOD.GenParticle_phi,
                nanoAOD.GenParticle_mass,
                q.gen_dileptonpair,
            ],
        )
        LVTrueGenParticle1 = Producer(
            input=[
                nanoAOD.GenParticle_pt,
                nanoAOD.GenParticle_eta,
                nanoAOD.GenParticle_phi,
                nanoAOD.GenParticle_mass,
                q.truegenpair,
            ],
        )

    with defaults(call="lorentzvector::Build({df}, {output}, {input}, 1)", output=[q.gen_p4_2]):
        LVGenParticle2 = Producer(
            input=[
                nanoAOD.GenParticle_pt,
                nanoAOD.GenParticle_eta,
                nanoAOD.GenParticle_phi,
                nanoAOD.GenParticle_mass,
                q.gen_dileptonpair,
            ],
        )
        LVTrueGenParticle2 = Producer(
            input=[
                nanoAOD.GenParticle_pt,
                nanoAOD.GenParticle_eta,
                nanoAOD.GenParticle_phi,
                nanoAOD.GenParticle_mass,
                q.truegenpair,
            ],
        )

    with defaults(input=[q.gen_p4_1]):
        gen_pt_1 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.gen_pt_1])
        gen_eta_1 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.gen_eta_1])
        gen_phi_1 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.gen_phi_1])
        gen_mass_1 = Producer(call="lorentzvector::GetMass({df}, {output}, {input})", output=[q.gen_mass_1])
    with defaults(input=[q.gen_p4_2]):
        gen_pt_2 = Producer(call="lorentzvector::GetPt({df}, {output}, {input})", output=[q.gen_pt_2])
        gen_eta_2 = Producer(call="lorentzvector::GetEta({df}, {output}, {input})", output=[q.gen_eta_2])
        gen_phi_2 = Producer(call="lorentzvector::GetPhi({df}, {output}, {input})", output=[q.gen_phi_2])
        gen_mass_2 = Producer(call="lorentzvector::GetMass({df}, {output}, {input})", output=[q.gen_mass_2])

    gen_pdgid_1 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 0)",
        input=[nanoAOD.GenParticle_pdgId, q.gen_dileptonpair],
        output=[q.gen_pdgid_1],
    )
    gen_pdgid_2 = Producer(
        call="event::quantity::Get<int>({df}, {output}, {input}, 1)",
        input=[nanoAOD.GenParticle_pdgId, q.gen_dileptonpair],
        output=[q.gen_pdgid_2],
    )
    gen_m_vis = Producer(
        call="lorentzvector::GetMass({df}, {output}, {input})",
        input=[q.gen_p4_1, q.gen_p4_2],
        output=[q.gen_m_vis],
    )

with defaults(input=[nanoAOD.GenJet_pt, nanoAOD.Jet_associatedGenJet, nanoAOD.Tau_associatedJet, q.dileptonpair]):
    gen_taujet_pt_1 = Producer(
        call="quantities::GenJetMatching({df}, {output}, {input}, 0)",
        output=[q.gen_taujet_pt_1],
        scopes=["tt"],
    )
    gen_taujet_pt_2 = Producer(
        call="quantities::GenJetMatching({df}, {output}, {input}, 1)",
        output=[q.gen_taujet_pt_2],
        scopes=["mt", "et", "tt"],
    )

with defaults(call=None, input=None, output=None):
    UnrollGenMuLV1 = ProducerGroup(
        scopes=["mt", "mm"],
        subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
    )
    UnrollGenMuLV2 = ProducerGroup(
        scopes=["em", "mm"],
        subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
    )
    UnrollGenElLV1 = ProducerGroup(
        scopes=["em", "ee", "et"],
        subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1],
    )
    UnrollGenElLV2 = ProducerGroup(
        scopes=["ee"],
        subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2],
    )
    UnrollGenTauLV1 = ProducerGroup(
        scopes=["tt"],
        subproducers=[gen_pt_1, gen_eta_1, gen_phi_1, gen_mass_1, gen_pdgid_1, gen_taujet_pt_1],
    )
    UnrollGenTauLV2 = ProducerGroup(
        scopes=["mt", "et", "tt"],
        subproducers=[gen_pt_2, gen_eta_2, gen_phi_2, gen_mass_2, gen_pdgid_2, gen_taujet_pt_2],
    )
    MTGenDiTauPairQuantities = ProducerGroup(
        scopes=["mt"],
        subproducers=[MTGenPair, LVGenParticle1, LVGenParticle2, UnrollGenMuLV1, UnrollGenTauLV2, gen_m_vis],
    )
    ETGenDiTauPairQuantities = ProducerGroup(
        scopes=["et"],
        subproducers=[ETGenPair, LVGenParticle1, LVGenParticle2, UnrollGenElLV1, UnrollGenTauLV2, gen_m_vis],
    )
    TTGenDiTauPairQuantities = ProducerGroup(
        scopes=["tt"],
        subproducers=[TTGenPair, LVGenParticle1, LVGenParticle2, UnrollGenTauLV1, UnrollGenTauLV2, gen_m_vis],
    )
    EMGenDiTauPairQuantities = ProducerGroup(
        scopes=["em"],
        subproducers=[EMGenPair, LVGenParticle1, LVGenParticle2, UnrollGenElLV1, UnrollGenMuLV2, gen_m_vis],
    )
    ElElGenPairQuantities = ProducerGroup(
        scopes=["ee"],
        subproducers=[ElElGenPair, LVGenParticle1, LVGenParticle2, UnrollGenElLV1, UnrollGenElLV2, gen_m_vis],
    )
    MuMuGenPairQuantities = ProducerGroup(
        scopes=["mm"],
        subproducers=[MuMuGenPair, LVGenParticle1, LVGenParticle2, UnrollGenMuLV1, UnrollGenMuLV2, gen_m_vis],
    )
    MuMuTrueGenDiTauPairQuantities = ProducerGroup(
        scopes=["mm"],
        subproducers=[MuMuTrueGenPair, LVTrueGenParticle1, LVTrueGenParticle2, UnrollGenMuLV1, UnrollGenMuLV2, gen_m_vis],
    )


#######################
# DiTau Genmatching
#######################

with defaults(scopes=["mt", "et", "tt", "em", "ee", "mm"]):
    GenPairForGenMatching = Producer(
        call="genparticles::tau::HadronicGenTaus({df}, {output}, {input})",
        input=[
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_motherid,
        ],
        output=[q.hadronic_gen_taus],
    )

    GenMatchP1 = Producer(
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
    )

    GenMatchP2 = Producer(
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
