from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup


ScalarHadRecoil = Producer(
    name="ScalarHadRecoil",
    call="basefunctions::SumPerEvent<Float_t>({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        q.good_jet_collection,
    ],
    output=[q.ht],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
ScalarHadRecoil_boosted = Producer(
    name="ScalarHadRecoil_boosted",
    call="basefunctions::SumPerEvent<Float_t>({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        q.good_jet_collection_boosted,
    ],
    output=[q.ht_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
GoodJetsP4 = Producer(
    name="GoodJetsP4",
    call="lorentzvectors::BuildP4Collection({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection,
    ],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
GoodJetsP4_boosted = Producer(
    name="GoodJetsP4_boosted",
    call="lorentzvectors::BuildP4Collection({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection_boosted,
    ],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilP4 = ProducerGroup(
    name="VectorialHadRecoilP4",
    call="basefunctions::SumPerEvent<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input}, ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.))",
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        GoodJetsP4,
    ]
)
VectorialHadRecoilP4_boosted = ProducerGroup(
    name="VectorialHadRecoilP4_boosted",
    call="basefunctions::SumPerEvent<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input}, ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.))",
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        GoodJetsP4_boosted,
    ]
)
MissingHadRecoilP4 = ProducerGroup(
    name="MissingHadRecoilP4",
    call="basefunctions::Negative<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input})",
    input=[],
    output=[q.mht_p4],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        VectorialHadRecoilP4,
    ]
)
MissingHadRecoilP4_boosted = ProducerGroup(
    name="MissingHadRecoilP4_boosted",
    call="basefunctions::Negative<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input})",
    input=[],
    output=[q.mht_p4_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        VectorialHadRecoilP4_boosted,
    ]
)
MissingHadRecoilPt = Producer(
    name="MissingHadRecoilPt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.mht_p4],
    output=[q.mht_pt],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
MissingHadRecoilPt_boosted = Producer(
    name="MissingHadRecoilPt_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.mht_p4_boosted],
    output=[q.mht_pt_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
MissingHadRecoilPhi = Producer(
    name="MissingHadRecoilPhi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.mht_p4],
    output=[q.mht_phi],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
MissingHadRecoilPhi_boosted = Producer(
    name="MissingHadRecoilPhi_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.mht_p4_boosted],
    output=[q.mht_phi_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
SoftActivityJetHT = Producer(
    name="SoftActivityJetHT",
    call="basefunctions::rename<Float_t>({df}, {input}, {output})",
    input=[nanoAOD.SoftActivityJetHT],
    output=[q.soft_activity_jet_ht],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
SoftActivityJetHT10 = Producer(
    name="SoftActivityJetHT10",
    call="basefunctions::rename<Float_t>({df}, {input}, {output})",
    input=[nanoAOD.SoftActivityJetHT10],
    output=[q.soft_activity_jet_ht_10],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
HadRecoilQuantities = ProducerGroup(
    name="HadRecoilQuantities",
    call=None,
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        ScalarHadRecoil,
        MissingHadRecoilP4,
        MissingHadRecoilPt,
        MissingHadRecoilPhi,
        SoftActivityJetHT,
        SoftActivityJetHT10,
    ],
)
HadRecoilQuantities_boosted = ProducerGroup(
    name="HadRecoilQuantities_boosted",
    call=None,
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        ScalarHadRecoil_boosted,
        MissingHadRecoilP4_boosted,
        MissingHadRecoilPt_boosted,
        MissingHadRecoilPhi_boosted,
    ],
)
