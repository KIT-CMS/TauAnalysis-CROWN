from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import ml as ml
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier

training_type = "equal_weights"

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

    # Aus smhtt_ul:
    # ("fold0", lambda df: odd_id(df)), -> auf fold0 trainiertes Model (auf ungeraden events trainiert) verwenden, wenn event id gerade ist
    # ("fold1", lambda df: ~odd_id(df)), -> auf fold1 trainiertes Model (auf geraden events trainiert) verwenden, wenn event id ungerade ist

    configuration.add_config_parameters(
        ["tt"],
        {
            "model_file_path_odd": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/tt/odd/model.onnx",
                }
            ),
            "model_file_path_even": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/tt/even/model.onnx",
                }
            ),
        },
    )

    configuration.add_config_parameters(
        ["mt"],
        {
            "model_file_path_odd": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/mt/odd/model.onnx",
                }
            ),
            "model_file_path_even": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/mt/even/model.onnx",
                }
            ),
        },
    )

    configuration.add_config_parameters(
        ["et"],
        {
            "model_file_path_odd": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/et/odd/model.onnx",
                }
            ),
            "model_file_path_even": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": f"payloads/ml/{training_type}/et/even/model.onnx",
                }
            ),
        },
    )

    configuration.add_producers(
        ["tt", "mt", "et"],
        [
            # ml.DefineMassXColumns,
            # ml.DefineMassYColumns,
            # ml.MTTransformVars,
            # ml.Evaluate_PNN,
            ml.Evaluate_NN_ORT,
        ],
    )

    configuration.add_outputs(
        ["tt", "mt", "et"],
        [q.nn_output_vector, q.predicted_class, q.predicted_max_value],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
