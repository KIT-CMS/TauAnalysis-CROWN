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
        ["mt"],
        {
            "model_file_path": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/2018/mt/{model_name}/model.onnx",
                }
            ),
        },
    )

    configuration.add_producers(
        ["mt"],
        [
            nn_output.event_parity_Float,
            nn_output.VariableConversionToFloatProducerGroup,
            # -----------------------------------------
            nn_output.Evaluate_DNN,
        ],
    )

    configuration.add_outputs(
        ["mt"],
        [
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
