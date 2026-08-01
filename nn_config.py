from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import nn_output as nn_output
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

    # model_name = "SANNT/groupedDNN"
    model_name = "CENNT/groupedDNN"

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
                        "2018": f"payloads/ml/2018/mt/{model_name}/model.onnx",
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
            nn_output.EraFlags,
            nn_output.event_parity_Float,
            nn_output.VariableConversionToFloatProducerGroup,
        ],
    )

    if int(era[:4]) < 2022:
        configuration.add_producers(["mt"], [nn_output.Evaluate_DNN_run2],)
    else:
        configuration.add_producers(["mt", "et", "tt"], [nn_output.Evaluate_DNN_run3],)

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.is_2025,
            q.is_2024,
            q.is_2023postBPix,
            q.is_2023preBPix,
            q.is_2022postEE,
            q.is_2022preEE,
            q.is_2018,
            q.is_2017,
            q.is_2016postVFP,
            q.is_2016preVFP,
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
