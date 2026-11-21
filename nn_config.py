from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import nn_output as nn_output
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration


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

    configuration.add_producers(
        ["mt", "et", "tt"],
        [
            nn_output.EraFlags,
            nn_output.event_parity_Float,
            nn_output.VariableConversionToFloatProducerGroup,
        ],
    )

    run2 = int(era[:4]) < 2022
    for scope in ["mt"] if run2 else ["mt", "et", "tt"]:
        model_file_path = f"payloads/ml/{era}/{scope}/{model_name}/model.onnx" if run2 else f"payloads/DNN/{scope}/model.onnx"
        configuration.add_config_parameters([scope], {"model_file_path": model_file_path})
        configuration.add_producers([scope], [nn_output.evaluate_dnn(scope, model_file_path)])

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
