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
        ["mt"],
        {
            "model_file_path": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/mt/ONNX_combined/{_name}/model.onnx",
                }
            ),
        },
    )

    configuration.add_producers(
        ["mt"],
        [
            ml.event_parity_Float,
            ml.VariableConversionToFloatProducerGroup,
            # -----------------------------------------
            ml.Evaluate_DNN_with_additional_angular_quantities,
            # ml.Evaluate_DNN_without_additional_angular_quantities,
        ],
    )

    configuration.add_outputs(
        ["mt"],
        [
            # q.nn_output_vector,
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
