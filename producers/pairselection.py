from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, Filter

####################
# Set of producers used for contruction of MT good pairs and the coressponding lorentz vectors
####################

MTPairSelection = Producer(
    name="MTPairSelection",
    call="ditau_pairselection::mutau::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        q.Tau_pt_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        q.Tau_mass_corrected,
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
    scopes=["mt"],
)
boostedMTPairSelection = Producer(
    name="boostedMTPairSelection",
    call="boosted_ditau_pairselection::mutau::PairSelection({df}, {input_vec}, {output}, {boosted_pairselection_min_dR}, {boosted_pairselection_max_dR})",
    input=[
        q.boostedTau_pt_corrected,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        q.boostedTau_mass_corrected,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.good_muons_mask,
        q.good_boostedtaus_mask,
    ],
    output=[q.boosteddileptonpair],
    scopes=["mt"],
)

GoodMTPairFlag = Producer(
    name="GoodMTPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["mt"],
)
GoodBoostedMTPairFlag = Producer(
    name="GoodboostedMTPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.boosteddileptonpair],
    output=[],
    scopes=["mt"],
)

GoodMTPairFilter = Filter(
    name="GoodMTPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodMuTauPairs", {input})',
    input=[],
    scopes=["mt"],
    subproducers=[GoodMTPairFlag, GoodBoostedMTPairFlag],
)

MuMuPairSelection = Producer(
    name="MuMuPairSelection",
    call="ditau_pairselection::mumu::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.good_muons_mask,
    ],
    output=[q.dileptonpair],
    scopes=["mm"],
)
MuMuPairSelectionOSPreferred = Producer(
    name="MuMuPairSelectionOSPreferred",
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
    scopes=["mm"],
)
ZMuMuPairSelection = Producer(
    name="ZMuMuPairSelection",
    call="pairselection::mumu::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.good_muons_mask,
    ],
    output=[q.dileptonpair],
    scopes=["mm"],
)
ZMuMuPairSelectionOSPreferred = Producer(
    name="ZMuMuPairSelectionOSPrefered",
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
    scopes=["mm"],
)
GoodMuMuPairFlag = Producer(
    name="GoodMuMuPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["mm"],
)

GoodMuMuPairFilter = Filter(
    name="GoodMuMuPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodMuMuPairs", {input})',
    input=[],
    scopes=["mm"],
    subproducers=[GoodMuMuPairFlag],
)

ElElPairSelection = Producer(
    name="ElElPairSelection",
    call="pairselection::elel::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
        q.good_electrons_mask,
    ],
    output=[q.dileptonpair],
    scopes=["ee"],
)
ZElElPairSelection = Producer(
    name="ZElElPairSelection",
    call="ditau_pairselection::elel::ZBosonPairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
        q.good_electrons_mask,
    ],
    output=[q.dileptonpair],
    scopes=["ee"],
)

GoodElElPairFlag = Producer(
    name="GoodElElPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["ee"],
)

GoodElElPairFilter = Filter(
    name="GoodElElPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodElElPairs", {input})',
    input=[],
    scopes=["ee"],
    subproducers=[GoodElElPairFlag],
)

ETPairSelection = Producer(
    name="ETPairSelection",
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
    scopes=["et"],
)
boostedETPairSelection = Producer(
    name="boostedETPairSelection",
    call="boosted_ditau_pairselection::eltau::PairSelection({df}, {input_vec}, {output}, {boosted_pairselection_min_dR}, {boosted_pairselection_max_dR})",
    input=[
        q.boostedTau_pt_corrected,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        q.boostedTau_mass_corrected,
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
        q.good_electrons_mask,
        q.good_boostedtaus_mask,
    ],
    output=[q.boosteddileptonpair],
    scopes=["et"],
)

GoodETPairFlag = Producer(
    name="GoodETPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["et"],
)
GoodBoostedETPairFlag = Producer(
    name="GoodboostedETPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.boosteddileptonpair],
    output=[],
    scopes=["et"],
)

GoodETPairFilter = Filter(
    name="GoodETPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodElTauPairs", {input})',
    input=[],
    scopes=["et"],
    subproducers=[GoodETPairFlag, GoodBoostedETPairFlag],
)

####################
## TauTau Pair Selection
####################
TTPairSelection = Producer(
    name="TTPairSelection",
    call="ditau_pairselection::tautau::PairSelection({df}, {input_vec}, {output}, {pairselection_min_dR})",
    input=[
        q.Tau_pt_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_phi,
        q.Tau_mass_corrected,
        nanoAOD.Tau_IDraw,
        q.good_taus_mask,
    ],
    output=[q.dileptonpair],
    scopes=["tt"],
)
boostedTTPairSelection = Producer(
    name="boostedTTPairSelection",
    call="boosted_ditau_pairselection::tautau::PairSelection({df}, {input_vec}, {output}, {boosted_pairselection_min_dR}, {boosted_pairselection_max_dR})",
    input=[
        q.boostedTau_pt_corrected,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        q.boostedTau_mass_corrected,
        q.good_boostedtaus_mask,
    ],
    output=[q.boosteddileptonpair],
    scopes=["tt"],
)

GoodTTPairFlag = Producer(
    name="GoodTTPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["tt"],
)
GoodBoostedTTPairFlag = Producer(
    name="GoodTTPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.boosteddileptonpair],
    output=[],
    scopes=["tt"],
)

GoodTTPairFilter = Filter(
    name="GoodTTPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodTauTauPairs", {input})',
    input=[],
    scopes=["tt"],
    subproducers=[GoodTTPairFlag, GoodBoostedTTPairFlag],
)
####################
## ElMu Pair Selection
####################

EMPairSelection = Producer(
    name="EMPairSelection",
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
    scopes=["em"],
)

GoodEMPairFlag = Producer(
    name="GoodEMPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dileptonpair],
    output=[],
    scopes=["em"],
)

GoodEMPairFilter = Filter(
    name="GoodEMPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodElMuPairs", {input})',
    input=[],
    scopes=["em"],
    subproducers=[GoodEMPairFlag],
)

####################
## BB Pair Selection
####################

BBPairSelection = Producer(
    name="BBPairSelection",
    call="bb_pairselection::PairSelection({df}, {input_vec}, {output}, {bb_pairselection_min_dR}, {btag_cut})",
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        nanoAOD.BJet_discriminator,
        q.good_bjet_collection,
        q.good_jet_collection,
    ],
    output=[q.dibjetpair],
    scopes=["et", "mt", "tt", "mm"],
)
BBPairSelection_boosted = Producer(
    name="BBPairSelection_boosted",
    call="bb_pairselection::PairSelection({df}, {input_vec}, {output}, {bb_pairselection_min_dR}, {btag_cut})",
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        nanoAOD.BJet_discriminator,
        q.good_bjet_collection_boosted,
        q.good_jet_collection_boosted,
    ],
    output=[q.dibjetpair_boosted],
    scopes=["et", "mt", "tt", "mm"],
)
GoodBBPairFlag = Producer(
    name="GoodBBPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dibjetpair],
    output=[],
    scopes=["et", "mt", "tt", "mm"],
)
GoodBBPairFlag_boosted = Producer(
    name="GoodBBPairFlag",
    call="pairselection::flagGoodPairs({df}, {output}, {input})",
    input=[q.dibjetpair_boosted],
    output=[],
    scopes=["et", "mt", "tt", "mm"],
)
GoodBBPairFilter = Filter(
    name="GoodBBPairFilter",
    call='basefunctions::FilterFlagsAny({df}, "GoodBBPairs", {input})',
    input=[],
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[GoodBBPairFlag, GoodBBPairFlag_boosted],
)

####################
## TauTau pair 4-vectors
####################

LVMu1 = Producer(
    name="LVMu1",
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
    name="LVMu2",
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
    name="LVEl1",
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
    name="LVEl2",
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
    name="LVTau1",
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
    name="LVTau2",
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
## uncorrected versions of all particles, used for MET propagation
LVMu1Uncorrected = Producer(
    name="LVMu1Uncorrected",
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
    name="LVMu2Uncorrected",
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
    name="LVEl1Uncorrected",
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
    name="LVEl2Uncorrected",
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
    name="LVTau1Uncorrected",
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
    name="LVTau2Uncorrected",
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

####################
## Additional hadronic taus
####################

additionalBoostedTau = Producer(
    name="additionalBoostedTau",
    call="pairselection::findAdditionalTau({df}, {input}, {output})",
    input=[
        q.good_boostedtaus_mask,
        q.boosteddileptonpair,
    ],
    output=[q.additional_boostedtau],
    scopes=["mt", "et", "tt"],
)
LVaddBoostedTau = Producer(
    name="LVaddBoostedTau",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.additional_boostedtau,
        q.boostedTau_pt_corrected,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        q.boostedTau_mass_corrected,
    ],
    output=[q.boosted_p4_add],
    scopes=["mt", "et", "tt"],
)

####################
## BB pair Lorentzvectors
####################

LVbjet1 = Producer(
    name="LVbjet1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dibjetpair,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
    ],
    output=[q.bpair_p4_1],
    scopes=["mt", "et", "tt", "mm"],
)
LVbjet2 = Producer(
    name="LVbjet2",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dibjetpair,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
    ],
    output=[q.bpair_p4_2],
    scopes=["mt", "et", "tt", "mm"],
)
LVbjet1_boosted = Producer(
    name="LVbjet1_boosted",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dibjetpair_boosted,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
    ],
    output=[q.bpair_p4_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
LVbjet2_boosted = Producer(
    name="LVbjet2_boosted",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dibjetpair_boosted,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
    ],
    output=[q.bpair_p4_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
