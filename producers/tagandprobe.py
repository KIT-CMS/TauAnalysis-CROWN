from ..quantities import output as q
from ..quantities import tagandprobe_output as tp_q
from ..quantities import nanoAOD as nanoAOD
import .producers.muons as muons
import .producers.electrons as electrons
import .producers.photons as photons

from ..helper.ProducerWarapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    AutoExtendedVectorProducer as ExtendedVectorProducer,
    scopes,
)

with scopes(["global"]):
    BaseMuons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_muons_mask],
        scopes=["global"],
        subproducers=[
            muons.MuonPtCut,
            muons.MuonEtaCut,
        ],
    )
    BaseElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_electrons_mask],
        subproducers=[
            electrons.ElectronPtCut,
            electrons.ElectronEtaCut,
        ],
    )
    BasePhotons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_photons_mask],
        subproducers=[
            photons.PhotonPtCut,
            photons.PhotonEtaCut,
            photons.PhotonElectronVeto,
        ],
    )

with scopes(["mm"]):
    GoodMuons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_muons_mask],
        subproducers=[
            muons.GoodMuonPtCut,
            muons.GoodMuonEtaCut,
        ],
    )
    GoodMuonsWithDzDxyCut = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_muons_mask],
        subproducers=[
            muons.GoodMuonPtCut,
            muons.GoodMuonEtaCut,
            muons.GoodMuonDzCut,
            muons.GoodMuonDxyCut,
        ],
    )
    MuMuSingleMuonTriggerFlags_1 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_1",
        vec_config="singlemuon_trigger",
    )
    MuMuSingleMuonTriggerFlags_2 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
        input=[
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_2",
        vec_config="singlemuon_trigger",
    )
    MuMuDoubleMuonTriggerFlags_1 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch}, {p1_triggerobject_ptcut}, {p2_triggerobject_ptcut} )',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_1",
        vec_config="doublemuon_trigger",
    )
    MuMuDoubleMuonTriggerFlags_2 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch}, {p1_triggerobject_ptcut}, {p2_triggerobject_ptcut} )',
        input=[
            q.p4_2,
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_2",
        vec_config="doublemuon_trigger",
    )
    MuMuSingleMuonTriggerBitFlags_1 = ExtendedVectorProducer(
        call="trigger::tagandprobe::MatchSingleTriggerObject({df}, {output}, {input}, {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )",
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_1",
        vec_config="singlemuon_trigger_bit",  # works
    )
    MuMuSingleMuonTriggerBitFlags_2 = ExtendedVectorProducer(
        call="trigger::tagandprobe::MatchSingleTriggerObject({df}, {output}, {input}, {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )",
        input=[
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_2",
        vec_config="singlemuon_trigger_bit",  # works
    )

    # Producers to writeout the id variables for the tag and probe pairs

    MuonID_Loose_1 = Producer(
        call="quantities::muon::id({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_loose],
        output=[tp_q.id_loose_1],
    )
    MuonID_Loose_2 = Producer(
        call="quantities::muon::id({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_loose],
        output=[tp_q.id_loose_2],
    )
    MuonID_Medium_1 = Producer(
        call="quantities::muon::id({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_medium],
        output=[tp_q.id_medium_1],
    )
    MuonID_Medium_2 = Producer(
        call="quantities::muon::id({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_medium],
        output=[tp_q.id_medium_2],
    )
    MuonID_Tight_1 = Producer(
        call="quantities::muon::id({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_tight],
        output=[tp_q.id_tight_1],
    )
    MuonID_Tight_2 = Producer(
        call="quantities::muon::id({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Muon_id_tight],
        output=[tp_q.id_tight_2],
    )
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

with scopes(["ee"]):
    GoodElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_electrons_mask],
        subproducers=[
            electrons.GoodElectronPtCut,
            electrons.GoodElectronEtaCut,
        ],
    )
    ElElSingleElectronTriggerFlags_1 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_1",
        vec_config="singleelectron_trigger",
    )
    ElElSingleElectronTriggerFlags_2 = ExtendedVectorProducer(
        call='trigger::tagandprobe::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch}, {triggerobject_ptcut} )',
        input=[
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname_2",
        vec_config="singleelectron_trigger",
    )

    # Producers to writeout the id variables for the tag and probe pairs

    ElectronID_WP90_1 = Producer(
        call="quantities::muon::id({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_IDWP90],
        output=[tp_q.id_wp90_1],
    )
    ElectronID_WP90_2 = Producer(
        call="quantities::muon::id({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_IDWP90],
        output=[tp_q.id_wp90_2],
    )
    ElectronID_WP80_1 = Producer(
        call="quantities::muon::id({df}, {output}, 0, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_IDWP80],
        output=[tp_q.id_wp80_1],
    )
    ElectronID_WP80_2 = Producer(
        call="quantities::muon::id({df}, {output}, 1, {input})",
        input=[q.dileptonpair, nanoAOD.Electron_IDWP80],
        output=[tp_q.id_wp80_2],
    )
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

with scopes(["ee", "mm"]):
    FSR_Photon_Veto_1 = Producer(
        call="physicsobject::OverlapVeto({df}, {output}, {input}, {fsr_delta_r})",
        input=[
            q.p4_1,
            nanoAOD.Photon_pt,
            nanoAOD.Photon_eta,
            nanoAOD.Photon_phi,
            nanoAOD.Photon_mass,
            q.base_photons_mask,
        ],
        output=[tp_q.fsr_photon_veto_1],
    )
    FSR_Photon_Veto_2 = Producer(
        call="physicsobject::OverlapVeto({df}, {output}, {input}, {fsr_delta_r})",
        input=[
            q.p4_2,
            nanoAOD.Photon_pt,
            nanoAOD.Photon_eta,
            nanoAOD.Photon_phi,
            nanoAOD.Photon_mass,
            q.base_photons_mask,
        ],
        output=[tp_q.fsr_photon_veto_2],
    )
    FSR_Veto = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            FSR_Photon_Veto_1,
            FSR_Photon_Veto_2,
        ],
    )
