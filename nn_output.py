from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import ml as ml
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):

    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    _name = "with_angular_quantities__m10toNaN__Sigmoid__FF_False"

    configuration.add_config_parameters(
        ["global", "tt", "mt", "et", "ee", "mm", "em"],
        {f"is_{e}": 1.0 if era == e else 0.0 for e in available_eras},
    )

    for scope in ["mt", "et", "tt"]:
        configuration.add_config_parameters(
            [scope],
            {
                "model_file_path": EraModifier(
                    {
                        "2016preVFP": "",
                        "2016postVFP": "",
                        "2017": "",
                        "2018": f"payloads/ml/{scope}/ONNX_combined/{_name}/model.onnx",
                        "2022preEE": f"payloads/DNN/{scope}/model.onnx",
                        "2022postEE": f"payloads/DNN/{scope}/model.onnx",
                        "2023preBPix": f"payloads/DNN/{scope}/model.onnx",
                        "2023postBPix": f"payloads/DNN/{scope}/model.onnx",
                        "2024": f"payloads/DNN/{scope}/model.onnx",
                        "2025": f"payloads/DNN/{scope}/model.onnx",
                    }
                ),
            },
        )

    configuration.add_producers(
        ["mt", "et", "tt"],
        [
            ml.EraFlags,
            ml.event_parity_Float,
            ml.VariableConversionToFloatProducerGroup,
            ml.Evaluate_DNN,
        ],
    )

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.is_2025,
            q.is_2024,
            q.is_2023postBPix,
            q.is_2023preBPix,
            q.is_2022postEE,
            q.is_2022preEE,
            q.nn_output_vector,
            q.nn_predicted_class,
            q.nn_predicted_max_value,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
