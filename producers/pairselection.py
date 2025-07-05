from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, Filter, BaseFilter, defaults

####################
# Set of producers used for contruction of MT good pairs and the coressponding lorentz vectors
####################

with defaults(scopes=["mt"]):
    MTPairSelection = Producer(
        call="ditau_pairselection::mutau::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Tau_pt_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_phi,
            nanoAOD.Tau_mass,
            nanoAOD.Tau_IDraw,
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            nanoAOD.Muon_iso,
            q.good_muons_mask,
            q.good_taus_mask,
        ],
        output=[q.dileptonpair],
    )
    GoodMTPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodMTPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodMuTauPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodMTPairFlag],
    )

with defaults(scopes=["mm"]):
    with defaults(output=[q.dileptonpair]):
        with defaults(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                q.good_muons_mask,
            ],
        ):
            MuMuPairSelection = Producer(call="ditau_pairselection::mumu::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})")
            ZMuMuPairSelection = Producer(call="ditau_pairselection::mumu::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})")

        with defaults(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                nanoAOD.Muon_charge,
                q.good_muons_mask,
            ],
        ):
            MuMuPairSelectionOSPreferred = Producer(call="ditau_pairselection::mumu::PairSelectionOSPreferred({df}, {input_vec}, {output}, {pairselection_min_dR})")
            ZMuMuPairSelectionOSPreferred = Producer(call="ditau_pairselection::mumu::ZBosonPairSelectionOSPreferred({df}, {input_vec}, {output}, {pairselection_min_dR})")

    GoodMuMuPairFlag = Producer(
        name="GoodMuMuPairFlag",
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodMuMuPairFilter = Filter(
        name="GoodMuMuPairFilter",
        call='event::filter::Flags({df}, "GoodMuMuPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodMuMuPairFlag],
    )

with defaults(scopes=["ee"]):
    with defaults(
        input=[q.Electron_pt_corrected, nanoAOD.Electron_eta, nanoAOD.Electron_phi, nanoAOD.Electron_mass, q.good_electrons_mask],
        output=[q.dileptonpair],
    ):
        ElElPairSelection = Producer(call="ditau_pairselection::elel::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})")
        ZElElPairSelection = Producer(call="ditau_pairselection::elel::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})")

    GoodElElPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodElElPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodElElPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodElElPairFlag],
    )

with defaults(scopes=["et"]):
    ETPairSelection = Producer(
        call="ditau_pairselection::eltau::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Tau_pt_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_phi,
            nanoAOD.Tau_mass,
            nanoAOD.Tau_IDraw,
            q.Electron_pt_corrected,
            nanoAOD.Electron_eta,
            nanoAOD.Electron_phi,
            nanoAOD.Electron_mass,
            nanoAOD.Electron_iso,
            q.good_electrons_mask,
            q.good_taus_mask,
        ],
        output=[q.dileptonpair],
    )
    GoodETPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodETPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodElTauPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodETPairFlag],
    )

####################
# TauTau Pair Selection
####################

with defaults(scopes=["tt"]):
    TTPairSelection = Producer(
        call="ditau_pairselection::tautau::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Tau_pt_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_phi,
            nanoAOD.Tau_mass,
            nanoAOD.Tau_IDraw,
            q.good_taus_mask,
        ],
        output=[q.dileptonpair],
    )
    GoodTTPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodTTPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodTauTauPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodTTPairFlag],
    )

####################
# ElMu Pair Selection
####################

with defaults(scopes=["em"]):
    EMPairSelection = Producer(
        call="ditau_pairselection::elmu::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Electron_pt_corrected,
            nanoAOD.Electron_eta,
            nanoAOD.Electron_phi,
            nanoAOD.Electron_mass,
            nanoAOD.Electron_iso,
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            nanoAOD.Muon_iso,
            q.good_electrons_mask,
            q.good_muons_mask,
        ],
        output=[q.dileptonpair],
    )
    GoodEMPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodEMPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodElMuPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodEMPairFlag],
    )

with defaults(call="lorentzvector::Build({df}, {output}, {input}, 0)"):
    with defaults(output=[q.p4_1]):
        LVMu1 = Producer(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                q.dileptonpair,
            ],
            scopes=["mt", "mm"],
        )
        LVEl1 = Producer(
            input=[
                q.Electron_pt_corrected,
                nanoAOD.Electron_eta,
                nanoAOD.Electron_phi,
                nanoAOD.Electron_mass,
                q.dileptonpair,
            ],
            scopes=["et", "ee", "em"],
        )
        LVTau1 = Producer(
            input=[
                q.Tau_pt_corrected,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_phi,
                q.Tau_mass_corrected,
                q.dileptonpair,
            ],
            scopes=["tt"],
        )

    with defaults(output=[q.p4_1_uncorrected]):  # uncorrected versions of all particles, used for MET propagation
        LVMu1Uncorrected = Producer(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                q.dileptonpair,
            ],
            scopes=["mt", "mm"],
        )
        LVEl1Uncorrected = Producer(
            input=[
                q.Electron_pt_corrected,
                nanoAOD.Electron_eta,
                nanoAOD.Electron_phi,
                nanoAOD.Electron_mass,
                q.dileptonpair,
            ],
            scopes=["em", "et", "ee"],
        )
        LVTau1Uncorrected = Producer(
            input=[
                nanoAOD.Tau_pt,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_phi,
                nanoAOD.Tau_mass,
                q.dileptonpair,
            ],
            scopes=["tt"],
        )

with defaults(call="lorentzvector::Build({df}, {output}, {input}, 1)"):
    with defaults(output=[q.p4_2]):
        LVMu2 = Producer(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                q.dileptonpair,
            ],
            scopes=["mm", "em"],
        )

        LVEl2 = Producer(
            input=[
                q.Electron_pt_corrected,
                nanoAOD.Electron_eta,
                nanoAOD.Electron_phi,
                nanoAOD.Electron_mass,
                q.dileptonpair,
            ],
            scopes=["ee"],
        )

        LVTau2 = Producer(
            input=[
                q.Tau_pt_corrected,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_phi,
                q.Tau_mass_corrected,
                q.dileptonpair,
            ],
            scopes=["mt", "et", "tt"],
        )

    with defaults(output=[q.p4_2_uncorrected]):  # uncorrected versions of all particles, used for MET propagation
        LVMu2Uncorrected = Producer(
            input=[
                nanoAOD.Muon_pt,
                nanoAOD.Muon_eta,
                nanoAOD.Muon_phi,
                nanoAOD.Muon_mass,
                q.dileptonpair,
            ],
            scopes=["mm", "em"],
        )

        LVEl2Uncorrected = Producer(
            input=[
                q.Electron_pt_corrected,
                nanoAOD.Electron_eta,
                nanoAOD.Electron_phi,
                nanoAOD.Electron_mass,
                q.dileptonpair,
            ],
            scopes=["ee"],
        )

        LVTau2Uncorrected = Producer(
            input=[
                nanoAOD.Tau_pt,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_phi,
                nanoAOD.Tau_mass,
                q.dileptonpair,
            ],
            scopes=["mt", "et", "tt"],
        )
