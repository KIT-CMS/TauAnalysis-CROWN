from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for loosest selection of muons
####################

with defaults(scopes=["global"]):
    MuonPtCorrection = Producer(
        call='''physicsobject::muon::PtCorrection({df}, correctionManager, {output}, {input}, 26.0, "{muon_sr_file}", "{muon_sr_shift}", {is_data})''',
        input=[nanoAOD.Muon_pt, nanoAOD.Muon_eta, nanoAOD.Muon_phi, nanoAOD.Muon_charge, nanoAOD.Muon_nTrackerLayers, nanoAOD.luminosityBlock, nanoAOD.event],
        output=[q.muon_pt_corrected]
    )
    MuonPtCorrection_Run2 = Producer(
        call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
        input=[nanoAOD.Muon_pt],
        output=[q.muon_pt_corrected]
    )

    MuonPtCut = Producer(
        call='''physicsobject::CutGreater<float>({df}, {output}, {input}, {min_muon_pt})''',
        input=[q.muon_pt_corrected],
        output=[q._MuonPtCut],
    )
    MuonEtaCut = Producer(
        call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_eta})''',
        input=[nanoAOD.Muon_eta],
        output=[q._MuonEtaCut],
    )
    MuonDxyCut = Producer(
        call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_dxy})''',
        input=[nanoAOD.Muon_dxy],
        output=[q._MuonDxyCut],
    )
    MuonDzCut = Producer(
        call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_dz})''',
        input=[nanoAOD.Muon_dz],
        output=[q._MuonDzCut],
    )
    MuonIDCut = Producer(
        call='''physicsobject::CutEqual<bool>({df}, {output}, {input}, true)''',
        input=[nanoAOD.Muon_mediumId],
        output=[q._MuonIDCut],
    )
    MuonIsoCut = Producer(
        call='''physicsobject::CutSmaller<float>({df}, {output}, {input}, {max_muon_iso})''',
        input=[nanoAOD.Muon_pfRelIso04_all],
        output=[q._MuonIsoCut],
    )

    with defaults(output=[]):
        DiMuonVetoPtCut = Producer(call='''physicsobject::CutGreater<float>({df}, {output}, {input}, {min_dimuonveto_pt})''', input=[q.muon_pt_corrected])
        DiMuonVetoIDCut = Producer(call='''physicsobject::CutEqual<bool>({df}, {output}, {input}, true)''', input=[nanoAOD.Muon_looseId])
        DiMuonVetoMuons = ProducerGroup(
            call='''physicsobject::CombineMasks({df}, {output}, {input}, "all_of")''',
            input=[q._MuonEtaCut, q._MuonDxyCut, q._MuonDzCut, q._MuonIsoCut],
            subproducers=[DiMuonVetoPtCut, DiMuonVetoIDCut],
        )

    DiMuonVeto = ProducerGroup(
        call='''physicsobject::LeptonPairVeto({df}, {output}, {input}, {dileptonveto_dR})''',
        input=[
            q.muon_pt_corrected,
            nanoAOD.Muon_eta,
            nanoAOD.Muon_phi,
            nanoAOD.Muon_mass,
            nanoAOD.Muon_charge,
        ],
        output=[q.dimuon_veto],
        subproducers=[DiMuonVetoMuons],
    )
    BaseMuons = ProducerGroup(
        call='''physicsobject::CombineMasks({df}, {output}, {input}, "all_of")''',
        input=[],
        output=[q.base_muons_mask],
        subproducers=[
            MuonPtCut,
            MuonEtaCut,
            MuonDxyCut,
            MuonDzCut,
            MuonIDCut,
            MuonIsoCut,
        ],
    )

####################
# Set of producers used for more specific selection of muons in channels
####################

with defaults(scopes=["em", "mt", "mm"]):
    with defaults(output=[]):
        GoodMuonPtCut = Producer(call='''physicsobject::CutGreater<float>({df}, {output}, {input}, {min_muon_pt})''', input=[q.muon_pt_corrected])
        GoodMuonEtaCut = Producer(call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_eta})''', input=[nanoAOD.Muon_eta])
        GoodMuonIsoCut = Producer(call='''physicsobject::CutSmaller<float>({df}, {output}, {input}, {max_muon_iso})''', input=[nanoAOD.Muon_pfRelIso04_all])
        GoodMuonDzCut = Producer(call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_dz})''', input=[nanoAOD.Muon_dz])
        GoodMuonDxyCut = Producer(call='''physicsobject::CutAbsSmaller<float>({df}, {output}, {input}, {max_muon_dxy})''', input=[nanoAOD.Muon_dxy])

    with defaults(
        call='''physicsobject::CombineMasks({df}, {output}, {input}, "all_of")''',
        input=[q.base_muons_mask],
        output=[q.good_muons_mask],
    ):
        GoodMuons = ProducerGroup(subproducers=[GoodMuonPtCut, GoodMuonEtaCut, GoodMuonIsoCut])
        GoodMuonsWithDzDxyCuts = ProducerGroup(subproducers=[GoodMuons, GoodMuonDzCut, GoodMuonDxyCut])

    NumberOfGoodMuons = Producer(
        call='''physicsobject::Count({df}, {output}, {input})''',
        input=[q.good_muons_mask],
        output=[q.nmuons],
    )
    VetoMuons = Producer(
        call='''physicsobject::VetoSingleObject({df}, {output}, {input}, {muon_index_in_pair})''',
        input=[q.base_muons_mask, q.dileptonpair],
        output=[q.veto_muons_mask],
    )

VetoSecondMuon = Producer(
    call='''physicsobject::VetoSingleObject({df}, {output}, {input}, {second_muon_index_in_pair})''',
    input=[q.veto_muons_mask, q.dileptonpair],
    output=[q.veto_muons_mask_2],
    scopes=["mm"],
)

ExtraMuonsVeto = Producer(
    call='''physicsobject::Veto({df}, {output}, {input})''',
    input={
        "em": [q.veto_muons_mask],
        "et": [q.base_muons_mask],
        "mt": [q.veto_muons_mask],
        "tt": [q.base_muons_mask],
        "mm": [q.veto_muons_mask_2],
    },
    output=[q.extramuon_veto],
    scopes=["em", "et", "mt", "tt", "mm"],
)
