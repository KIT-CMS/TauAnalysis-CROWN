from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..helper.ProducerWarapper import (
    AutoExtendedVectorProducer as ExtendedVectorProducer,
    scopes,
)

####################
# Set of producers used for trigger flags
####################

with scopes(["mm"]):
    MuMuGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singlemoun_trigger",
    )
    MuMuGenerateDoubleMuonTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="doublemuon_trigger",
    )

with scopes(["ee"]):
    ElElGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singleelectron_trigger",
    )
    ElElGenerateDoubleMuonTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="doubleelectron_trigger",
    )

with scopes(["mt"]):
    MTGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singlemoun_trigger",
    )
    MTGenerateCrossTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="mutau_cross_trigger",
    )
    MTGenerateCrossTriggerFlagsEmbedding = ExtendedVectorProducer(
        call="trigger::MatchDoubleTriggerObject({df}, {output}, {input}, {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})",
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="mutau_cross_trigger_embedding",
    )

with scopes(["et"]):
    ETGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singleelectron_trigger",
    )
    ETGenerateCrossTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="eltau_cross_trigger",
    )

with scopes(["em"]):
    EMGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singleelectron_trigger",
    )
    EMGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singlemoun_trigger",
    )
    EMGenerateCrossTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="elmu_cross_trigger",
    )

with scopes(["tt"]):
    GenerateSingleLeadingTauTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
        input=[
            q.p4_1,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="singletau_trigger_leading",
    )
    TTGenerateDoubleTriggerFlags = ExtendedVectorProducer(
        call='trigger::GenerateDoubleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})',
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="doubletau_trigger",
    )
    TTGenerateDoubleTriggerFlagsEmbedding = ExtendedVectorProducer(
        call="trigger::MatchDoubleTriggerObject({df}, {output}, {input}, {p1_ptcut}, {p2_ptcut}, {p1_etacut}, {p2_etacut}, {p1_trigger_particle_id}, {p2_trigger_particle_id}, {p1_filterbit}, {p2_filterbit}, {max_deltaR_triggermatch})",
        input=[
            q.p4_1,
            q.p4_2,
            nanoAOD.TriggerObject_bit,
            nanoAOD.TriggerObject_id,
            nanoAOD.TriggerObject_pt,
            nanoAOD.TriggerObject_eta,
            nanoAOD.TriggerObject_phi,
        ],
        output="flagname",
        vec_config="doubletau_trigger_embedding",
    )

GenerateSingleTrailingTauTriggerFlags = ExtendedVectorProducer(
    call='trigger::GenerateSingleTriggerFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {etacut}, {trigger_particle_id}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.p4_2,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["et", "mt", "tt"],
    vec_config="singletau_trigger_trailing",
)
