from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import (
    ExtendedVectorProducer,
    defaults,
)

TriggerObject_collection = [
    nanoAOD.TriggerObject_bit,
    nanoAOD.TriggerObject_id,
    nanoAOD.TriggerObject_pt,
    nanoAOD.TriggerObject_eta,
    nanoAOD.TriggerObject_phi,
]

####################
# Set of producers used for trigger flags
####################
with defaults(output="flagname"):
    with defaults(
        call='''trigger::GenerateSingleTriggerFlag(
            {df},
            {output},
            {input},
            "{hlt_path}",
            {ptcut},
            {etacut},
            {trigger_particle_id},
            {filterbit},
            {max_deltaR_triggermatch})''',
    ):
        with defaults(input=[q.p4_1] + TriggerObject_collection):
            MTGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(scope=["mt"], vec_config="singlemoun_trigger")
            MuMuGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(scope=["mm"], vec_config="singlemoun_trigger")
            # ---
            ETGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(scope=["et"], vec_config="singleelectron_trigger")
            EMGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(scope=["em"], vec_config="singleelectron_trigger")
            ElElGenerateSingleElectronTriggerFlags = ExtendedVectorProducer(scope=["ee"], vec_config="singleelectron_trigger")
            # ---
            GenerateSingleLeadingTauTriggerFlags = ExtendedVectorProducer(scope=["tt"], vec_config="singletau_trigger_leading")
        with defaults(input=[q.p4_2] + TriggerObject_collection):
            EMGenerateSingleMuonTriggerFlags = ExtendedVectorProducer(scope=["em"], vec_config="singlemoun_trigger")
            # ---
            GenerateSingleTrailingTauTriggerFlags = ExtendedVectorProducer(scope=["et", "mt", "tt"], vec_config="singletau_trigger_trailing")
    with defaults(
        call='''trigger::GenerateDoubleTriggerFlag(
            {df},
            {output},
            {input},
            "{hlt_path}",
            {p1_ptcut},
            {p2_ptcut},
            {p1_etacut},
            {p2_etacut},
            {p1_trigger_particle_id},
            {p2_trigger_particle_id},
            {p1_filterbit},
            {p2_filterbit},
            {max_deltaR_triggermatch})''',
    ):
        with defaults(input=[q.p4_1, q.p4_2] + TriggerObject_collection):
            EMGenerateCrossTriggerFlags = ExtendedVectorProducer(scope=["em"], vec_config="elmu_cross_trigger")
            ETGenerateCrossTriggerFlags = ExtendedVectorProducer(scope=["et"], vec_config="eltau_cross_trigger")
            MTGenerateCrossTriggerFlags = ExtendedVectorProducer(scope=["mt"], vec_config="mutau_cross_trigger")
            TTGenerateDoubleTriggerFlags = ExtendedVectorProducer(scope=["tt"], vec_config="doubletau_trigger")
            MuMuGenerateDoubleMuonTriggerFlags = ExtendedVectorProducer(scope=["mm"], vec_config="doublemuon_trigger")
            ElElGenerateDoubleMuonTriggerFlags = ExtendedVectorProducer(scope=["ee"], vec_config="doubleelectron_trigger")
    with defaults(
        call='''trigger::MatchDoubleTriggerObject(
            {df},
            {output},
            {input},
            {p1_ptcut},
            {p2_ptcut},
            {p1_etacut},
            {p2_etacut},
            {p1_trigger_particle_id},
            {p2_trigger_particle_id},
            {p1_filterbit},
            {p2_filterbit},
            {max_deltaR_triggermatch})''',
    ):
        with defaults(input=[q.p4_1, q.p4_2] + TriggerObject_collection):
            MTGenerateCrossTriggerFlagsEmbedding = ExtendedVectorProducer(scope=["mt"], vec_config="mutau_cross_trigger_embedding")
            TTGenerateDoubleTriggerFlagsEmbedding = ExtendedVectorProducer(scope=["tt"], vec_config="doubletau_trigger_embedding")
