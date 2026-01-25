from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, defaults, ExtendedVectorProducer, VectorProducer, ProducerGroup

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    with defaults(call='utility::Cast<float, int>({df}, {output}, "float", {input}).first'):
        ConversionToFloatCollection = [
            njets_Float := Producer(input=[q.njets], output=[q.njets_float]),
            nbtag_Float := Producer(input=[q.nbtag], output=[q.nbtag_float]),
            tau_decaymode_2_Float := Producer(input=[q.tau_decaymode_2], output=[q.tau_decaymode_2_float]),
            tau_decaymode_1_Float := Producer(input=[q.tau_decaymode_1], output=[q.tau_decaymode_1_float]),
        ]

    with defaults(call='utility::Cast<float, double>({df}, {output}, "float", {input}).first'):
        ConversionToFloatCollection += [
            pzetamissvis_Float := Producer(input=[q.pzetamissvis], output=[q.pzetamissvis_float]),
        ]

    VariableConversionToFloatProducerGroup = ProducerGroup(subproducers=ConversionToFloatCollection)

    with defaults(call='ml_sm::EventParity({df}, {output}, {input})'):
        event_parity_Float = Producer(input=[nanoAOD.event], output=[q.event_parity_float])


inputs_without_additional_angular_quantities = [
    q.pt_1,
    q.pt_2,
    q.eta_1,
    q.eta_2,
    q.jpt_1,
    q.jpt_2,
    q.jeta_1,
    q.jeta_2,
    q.m_fastmtt,
    q.pt_fastmtt,
    q.met,
    q.njets_float,
    q.nbtag_float,
    q.mt_tot,
    q.m_vis,
    q.pt_tt,
    q.pt_vis,
    q.mjj,
    q.pt_dijet,
    q.pt_ttjj,
    q.pzetamissvis_float,
    q.deltaEta_jj,
    q.deltaEta_ditaupair,
    q.deltaR_jj,
    q.deltaR_ditaupair,
]  # 25
inputs_with_additional_angular_quantities = [
    q.pt_1,
    q.pt_2,
    q.eta_1,
    q.eta_2,
    q.jpt_1,
    q.jpt_2,
    q.jeta_1,
    q.jeta_2,
    q.m_fastmtt,
    q.pt_fastmtt,
    q.met,
    q.njets_float,
    q.nbtag_float,
    q.mt_tot,
    q.m_vis,
    q.pt_tt,
    q.pt_vis,
    q.mjj,
    q.pt_dijet,
    q.pt_ttjj,
    q.pzetamissvis_float,
    q.deltaR_ditaupair,
    q.deltaEta_ditaupair,
    q.deltaEta_jj,
    q.deltaR_jj,
    q.deltaR_1j1,
    q.deltaR_1j2,
    q.deltaR_2j1,
    q.deltaR_2j2,
    q.deltaR_12j1,
    q.deltaR_12j2,
    q.deltaEta_1j1,
    q.deltaEta_1j2,
    q.deltaEta_2j1,
    q.deltaEta_2j2,
    q.deltaEta_12j1,
    q.deltaEta_12j2,
]  # 37

with defaults(
    output=[q.nn_output_vector, q.nn_predicted_class, q.nn_predicted_max_value],
    scopes=["mt"],
    # subproducers=FloatConvertedVariablesProducers,
):
    Evaluate_DNN_without_additional_angular_quantities = Producer(
        call='''ml_sm::Extracted_NN_Output<26>(
            {df},
            onnxSessionManager,
            {output},
            "{model_file_path}",
            {input_vec})''',
        input=[q.event_parity_float] + inputs_without_additional_angular_quantities,
    )
    Evaluate_DNN_with_additional_angular_quantities = Producer(
        call='''ml_sm::Extracted_NN_Output<38>(
            {df},
            onnxSessionManager,
            {output},
            "{model_file_path}",
            {input_vec})''',
        input=[q.event_parity_float] + inputs_with_additional_angular_quantities,
    )
