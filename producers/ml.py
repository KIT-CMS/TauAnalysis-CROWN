from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer

standard_columns = [
    q.bpair_btag_value_1,
    q.bpair_btag_value_2,
    q.bpair_deltaR,
    q.bpair_m_inv,
    q.bpair_pt_1,
    q.bpair_pt_dijet,
    q.deltaR_ditaupair,
    q.jpt_1,
    q.m_fastmtt,
    q.mjj,
    q.nbtag,
    q.njets,
    q.pt_fastmtt
]

expanded_columns = standard_columns + [
    q.mtt_coll_approx,
    q.m_vis,
    q.mt_tot,
    q.jpt_2,
    q.pt_1,
    q.pt_dijet,
    q.pt_vis
]

Evaluate_NN_ORT = Producer(
    name="Evaluate_NN_ORT",
    call='ml::NNEvaluate_ORT<20>({df}, onnxSessionManager, {output}, "{model_file_path_even}", "{model_file_path_odd}", {input_vec})',
    input=expanded_columns,
    output=[q.nn_output_vector, q.predicted_class, q.predicted_max_value],
    scopes=["tt", "mt", "et"],
)
