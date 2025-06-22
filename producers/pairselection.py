from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..helper.ProducerWarapper import (
    AutoFiler as Filter,
    AutoProducer as Producer,
    scopes,
)
####################
# Set of producers used for contruction of MT good pairs and the coressponding lorentz vectors
####################

with scopes(["mt"]):
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

with scopes(["mm"]):
    MuMuPairSelection = Producer(
        call="ditau_pairselection::mumu::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            q.good_muons_mask,
        ],
        output=[q.dileptonpair],
    )
    MuMuPairSelectionOSPreferred = Producer(
        call="ditau_pairselection::mumu::PairSelectionOSPreferred({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            nanoAOD.Muon_charge,
            q.good_muons_mask,
        ],
        output=[q.dileptonpair],
    )
    ZMuMuPairSelection = Producer(
        call="ditau_pairselection::mumu::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            q.good_muons_mask,
        ],
        output=[q.dileptonpair],
    )
    ZMuMuPairSelectionOSPreferred = Producer(
        call="ditau_pairselection::mumu::ZBosonPairSelectionOSPreferred({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            nanoAOD.Muon_pt,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            nanoAOD.Muon_charge,
            q.good_muons_mask,
        ],
        output=[q.dileptonpair],
    )
    GoodMuMuPairFlag = Producer(
        call="ditau_pairselection::flagGoodPairs({df}, {output}, {input})",
        input=[q.dileptonpair],
        output=[],
    )
    GoodMuMuPairFilter = Filter(
        call='event::filter::Flags({df}, "GoodMuMuPairs", {input}, "any_of")',
        input=[],
        subproducers=[GoodMuMuPairFlag],
    )

with scopes(["ee"]):
    ElElPairSelection = Producer(
        call="ditau_pairselection::elel::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Electron_pt_corrected,
            nanoAOD.Electron_eta,
            nanoAOD.Electron_phi,
            nanoAOD.Electron_mass,
            q.good_electrons_mask,
        ],
        output=[q.dileptonpair],
    )
    ZElElPairSelection = Producer(
        call="ditau_pairselection::elel::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
        input=[
            q.Electron_pt_corrected,
            nanoAOD.Electron_eta,
            nanoAOD.Electron_phi,
            nanoAOD.Electron_mass,
            q.good_electrons_mask,
        ],
        output=[q.dileptonpair],
    )
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

with scopes(["et"]):
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

with scopes(["tt"]):
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

with scopes(["em"]):
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

LVMu1 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.p4_1],
    scopes=["mt", "mm"],
)
LVMu2 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.p4_2],
    scopes=["mm", "em"],
)
LVEl1 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
    ],
    output=[q.p4_1],
    scopes=["et", "ee", "em"],
)
LVEl2 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
    ],
    output=[q.p4_2],
    scopes=["ee"],
)
LVTau1 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        q.Tau_pt_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        q.Tau_mass_corrected,
    ],
    output=[q.p4_1],
    scopes=["tt"],
)
LVTau2 = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        q.Tau_pt_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        q.Tau_mass_corrected,
    ],
    output=[q.p4_2],
    scopes=["mt", "et", "tt"],
)

# uncorrected versions of all particles, used for MET propagation

LVMu1Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.p4_1_uncorrected],
    scopes=["mt", "mm"],
)
LVMu2Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.p4_2_uncorrected],
    scopes=["mm", "em"],
)
LVEl1Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
    ],
    output=[q.p4_1_uncorrected],
    scopes=["em", "et", "ee"],
)
LVEl2Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
    ],
    output=[q.p4_2_uncorrected],
    scopes=["ee"],
)
LVTau1Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Tau_pt,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        nanoAOD.Tau_mass,
    ],
    output=[q.p4_1_uncorrected],
    scopes=["tt"],
)
LVTau2Uncorrected = Producer(
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dileptonpair,
        nanoAOD.Tau_pt,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        nanoAOD.Tau_mass,
    ],
    output=[q.p4_2_uncorrected],
    scopes=["mt", "et", "tt"],
)
