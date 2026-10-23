from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer, ProducerGroup
from .fakefactors_generic import _read_model, _quantities
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
            is_2018 := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2018})''',
                output=[q.is_2018],
            ),
            is_2017 := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2017})''',
                output=[q.is_2017],
            ),
            is_2016postVFP := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2016postVFP})''',
                output=[q.is_2016postVFP],
            ),
            is_2016preVFP := Producer(
                call='''event::quantity::Define<float>({df}, {output}, {is_2016preVFP})''',
                output=[q.is_2016preVFP],
            ),
        ]
    EraFlags = ProducerGroup(call=None, input=None, output=None, subproducers=EraFlags_ProducerCollection)


def evaluate_dnn(scope, model_file_path):
    # inputs in the order of the ONNX model metadata, the <name>_float cast preferred since the evaluator takes floats
    features = [f"{f}_float" if hasattr(q, f"{f}_float") else f for f in _read_model("tau", model_file_path)[0]]
    return Producer(
        name=f"Evaluate_DNN_{scope}",
        call=f'''ml_sm::Extracted_NN_Output<{len(features)}>(
            {{df}},
            onnxSessionManager,
            {{output}},
            "{{model_file_path}}",
            {{input_vec}})''',
        input=_quantities(q, features),
        output=[q.nn_output_vector, q.nn_predicted_class, q.nn_predicted_max_value],
        scopes=[scope],
    )
