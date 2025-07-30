from ..quantities import output as q
from ..quantities import tagandprobe_output as tp_q
from ..quantities import nanoAOD as nanoAOD
from ..producers import muons as muons
from ..producers import electrons as electrons
from ..producers import photons as photons
from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults

TriggerObject_collection = [
    nanoAOD.TrigObj_filterBits,
    nanoAOD.TrigObj_id,
    nanoAOD.TrigObj_pt,
    nanoAOD.TrigObj_eta,
    nanoAOD.TrigObj_phi,
]

with defaults(scopes=["global"], input=[]):
    BaseMuons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        output=[q.base_muons_mask],
        subproducers=[muons.MuonPtCut, muons.MuonEtaCut],
    )
    BasePhotons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        output=[q.base_photons_mask],
        subproducers=[photons.PhotonPtCut, photons.PhotonEtaCut, photons.PhotonElectronVeto],
    )
    BaseElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        output=[q.base_electrons_mask],
        subproducers=[electrons.ElectronPtCut, electrons.ElectronEtaCut],
    )

with defaults(scopes=["mm"]):
    with defaults(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_muons_mask],
    ):
        GoodMuons = ProducerGroup(
            subproducers=[
                muons.GoodMuonPtCut,
                muons.GoodMuonEtaCut,
            ],
        )
        GoodMuonsWithDzDxyCut = ProducerGroup(
            subproducers=[
                muons.GoodMuonPtCut,
                muons.GoodMuonEtaCut,
                muons.GoodMuonDzCut,
                muons.GoodMuonDxyCut,
            ],
        )

    with defaults(output="flagname_1"):
        with defaults(input=[q.p4_1] + TriggerObject_collection):
            MuMuSingleMuonTriggerFlags_1 = ExtendedVectorProducer(
                call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
                vec_config="singlemuon_trigger",
            )
            MuMuSingleMuonTriggerBitFlags_1 = ExtendedVectorProducer(
                call="trigger::tagandprobe::MatchSingleTriggerObject({df}, {output}, {input}, {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )",
                vec_config="singlemuon_trigger_bit",  # works
            )

        with defaults(input=[q.p4_1, q.p4_2] + TriggerObject_collection):
            MuMuDoubleMuonTriggerFlags_1 = ExtendedVectorProducer(
                call='trigger::tagandprobe::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch}, {p1_triggerobject_ptcut}, {p2_triggerobject_ptcut} )',
                vec_config="doublemuon_trigger",
            )

    with defaults(output="flagname_2"):
        with defaults(input=[q.p4_2] + TriggerObject_collection):
            MuMuSingleMuonTriggerFlags_2 = ExtendedVectorProducer(
                call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
                vec_config="singlemuon_trigger",
            )
            MuMuSingleMuonTriggerBitFlags_2 = ExtendedVectorProducer(
                call="trigger::tagandprobe::MatchSingleTriggerObject({df}, {output}, {input}, {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )",
                vec_config="singlemuon_trigger_bit",  # works
            )
        with defaults(input=[q.p4_2, q.p4_1] + TriggerObject_collection):
            MuMuDoubleMuonTriggerFlags_2 = ExtendedVectorProducer(
                call='trigger::tagandprobe::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch}, {p1_triggerobject_ptcut}, {p2_triggerobject_ptcut} )',
                vec_config="doublemuon_trigger",
            )

    # Producers to writeout the id variables for the tag and probe pairs

    with defaults(call="event::quantity::Get<bool>({df}, {output}, {input}, 0)"):
        MuonID_Loose_1 = Producer(input=[nanoAOD.Muon_looseId, q.dileptonpair], output=[tp_q.id_loose_1])
        MuonID_Medium_1 = Producer(input=[nanoAOD.Muon_mediumId, q.dileptonpair], output=[tp_q.id_medium_1])
        MuonID_Tight_1 = Producer(input=[nanoAOD.Muon_tightId, q.dileptonpair], output=[tp_q.id_tight_1])

    with defaults(call="event::quantity::Get<bool>({df}, {output}, {input}, 1)"):
        MuonID_Loose_2 = Producer(input=[nanoAOD.Muon_looseId, q.dileptonpair], output=[tp_q.id_loose_2])
        MuonID_Medium_2 = Producer(input=[nanoAOD.Muon_mediumId, q.dileptonpair], output=[tp_q.id_medium_2])
        MuonID_Tight_2 = Producer(input=[nanoAOD.Muon_tightId, q.dileptonpair], output=[tp_q.id_tight_2])

    MuonIDs = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            MuonID_Loose_1,
            MuonID_Loose_2,
            MuonID_Medium_1,
            MuonID_Medium_2,
            MuonID_Tight_1,
            MuonID_Tight_2,
        ],
    )

###########################
# Electrons
###########################

with defaults(scopes=["ee"]):
    GoodElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_electrons_mask],
        subproducers=[
            electrons.GoodElectronPtCut,
            electrons.GoodElectronEtaCut,
        ],
    )

    with defaults(vec_configs="singleelectron_trigger"):
        ElElSingleElectronTriggerFlags_1 = ExtendedVectorProducer(
            call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
            input=[q.p4_1] + TriggerObject_collection,
            output="flagname_1",
        )
        ElElSingleElectronTriggerFlags_2 = ExtendedVectorProducer(
            call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
            input=[q.p4_2] + TriggerObject_collection,
            output="flagname_2",
        )

    # Producers to writeout the id variables for the tag and probe pairs

    with defaults(call="event::quantity::Get<bool>({df}, {output}, {input}, 0)"):
        ElectronID_WP90_1 = Producer(input=[nanoAOD.Electron_mvaFall17V2noIso_WP90, q.dileptonpair], output=[tp_q.id_wp90_1])
        ElectronID_WP80_1 = Producer(input=[nanoAOD.Electron_mvaFall17V2noIso_WP80, q.dileptonpair], output=[tp_q.id_wp80_1])
    with defaults(call="event::quantity::Get<bool>({df}, {output}, {input}, 1)"):
        ElectronID_WP90_2 = Producer(input=[nanoAOD.Electron_mvaFall17V2noIso_WP90, q.dileptonpair], output=[tp_q.id_wp90_2])
        ElectronID_WP80_2 = Producer(input=[nanoAOD.Electron_mvaFall17V2noIso_WP80, q.dileptonpair], output=[tp_q.id_wp80_2])

    ElectronIDs = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            ElectronID_WP90_1,
            ElectronID_WP90_2,
            ElectronID_WP80_1,
            ElectronID_WP80_2,
        ],
    )

########################################
# FSR Photon Veto
########################################

Photon_quantities = [
    nanoAOD.Photon_pt,
    nanoAOD.Photon_eta,
    nanoAOD.Photon_phi,
    nanoAOD.Photon_mass,
    q.base_photons_mask,
]

with defaults(scopes=["ee", "mm"]):
    with defaults(call="physicsobject::OverlapVeto({df}, {output}, {input}, {fsr_delta_r})"):
        FSR_Photon_Veto_1 = Producer(input=[q.p4_1] + Photon_quantities, output=[tp_q.fsr_photon_veto_1])
        FSR_Photon_Veto_2 = Producer(input=[q.p4_2] + Photon_quantities, output=[tp_q.fsr_photon_veto_2])

    FSR_Veto = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[FSR_Photon_Veto_1, FSR_Photon_Veto_2],
    )
