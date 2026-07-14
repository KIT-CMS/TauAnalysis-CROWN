from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from ..scripts.CROWNWrapper import Producer, defaults, ExtendedVectorProducer, VectorProducer, ProducerGroup

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    with defaults(call='''utility::Cast<float, int>({df}, {output}, "float", {input}).first'''):
        ConversionToFloatCollection = [
            njets_Float := Producer(input=[q.njets], output=[q.njets_float]),
            nbtag_Float := Producer(input=[q.nbtag], output=[q.nbtag_float]),
            tau_decaymode_2_Float := Producer(input=[q.tau_decaymode_2], output=[q.tau_decaymode_2_float]),
            tau_decaymode_1_Float := Producer(input=[q.tau_decaymode_1], output=[q.tau_decaymode_1_float]),
        ]

    with defaults(call='''utility::Cast<float, double>({df}, {output}, "float", {input}).first'''):
        ConversionToFloatCollection += [
            pzetamissvis_Float := Producer(input=[q.pzetamissvis], output=[q.pzetamissvis_float]),
        ]

    VariableConversionToFloatProducerGroup = ProducerGroup(subproducers=ConversionToFloatCollection)

    with defaults(call='''ml_sm::EventParity({df}, {output}, {input})'''):
        event_parity_Float = Producer(input=[nanoAOD.event], output=[q.event_parity_float])

    # era flags
    with defaults(input=[]):
        EraFlags_ProducerCollection = [
            is_2025 := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2025})''',
                output=[q.is_2025],
            ),
            is_2024 := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2024})''',
                output=[q.is_2024],
            ),
            is_2023postBPix := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2023postBPix})''',
                output=[q.is_2023postBPix],
            ),
            is_2023preBPix := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2023preBPix})''',
                output=[q.is_2023preBPix],
            ),
            is_2022postEE := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2022postEE})''',
                output=[q.is_2022postEE],
            ),
            is_2022preEE := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2022preEE})''',
                output=[q.is_2022preEE],
            ),
        ]
    EraFlags = ProducerGroup(call=None, input=None, output=None, subproducers=EraFlags_ProducerCollection)


inputs = [
    q.pt_1,
    q.pt_2,
    q.eta_1,
    q.eta_2,
    q.jpt_1,
    q.jpt_2,
    q.jeta_1,
    q.jeta_2,
    q.m_fastmtt,
    q.m_vis,
    q.mjj,
    q.pt_vis,
    q.pt_dijet,
    q.pt_tt,
    q.pt_ttjj,
    q.njets_float,
    q.nbtag_float,
    q.puppimet,
    q.deltaEta_ditaupair,
    q.deltaR_ditaupair,
    q.mt_1,
    q.mt_2,
    q.pt_fastmtt,
    q.mt_tot,
    # q.pzetamissvis_float,
    q.deltaR_jj,
    q.deltaEta_jj,
    # q.deltaR_1j1,
    # q.deltaR_2j2,
    # q.deltaR_2j1,
    # q.deltaR_1j2,
    # q.deltaR_12j1,
    # q.deltaR_12j2,
    # q.deltaEta_1j1,
    # q.deltaEta_1j2,
    # q.deltaEta_2j1,
    # q.deltaEta_2j2,
    # q.deltaEta_12j1,
    # q.deltaEta_12j2,
    q.is_2025,
    q.is_2024,
    q.is_2023postBPix,
    q.is_2023preBPix,
    q.is_2022postEE,
    q.is_2022preEE,
]  # 26 + 6 = 32 + event parity = 33

with defaults(
    output=[q.nn_output_vector, q.nn_predicted_class, q.nn_predicted_max_value],
    scopes=["mt", "et", "tt"],
    # subproducers=FloatConvertedVariablesProducers, # included in FF
):
    Evaluate_DNN = Producer(
        call='''ml_sm::Extracted_NN_Output<33>(
            {df},
            onnxSessionManager,
            {output},
            "{model_file_path}",
            {input_vec})''',
        input=[q.event_parity_float] + inputs,
    )