from __future__ import annotations  # needed for type annotations in > python 3.7

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.producer import Producer
from code_generation.quantity import Quantity
from code_generation.systematics import SystematicShift

from .producers import fakefactors as ff
from .producers import nn_output
from .quantities import output as q


@dataclass(frozen=True)
class Channel:
    # input column -> corrections evaluated on it, as wired in cpp_addons/src/fakefactors.cxx
    inputs: Dict[Quantity, Tuple[str, ...]]
    fake_factor_producers: Tuple[Producer, ...]
    # the subset of fake_factor_producers that reads corr_file
    corrected_producers: Tuple[Producer, ...]


LT = Channel(
    inputs={
        q.ff_input_lt: ("QCD_fake_factors", "Wjets_fake_factors", "ttbar_fake_factors"),
        q.ff_input_fraction_lt: ("process_fractions",),
        q.ff_input_dr_lt: ("QCD_DR_SR_correction", "Wjets_DR_SR_correction"),
        q.ff_input_nc_lt: ("QCD_compound_correction", "Wjets_compound_correction", "ttbar_compound_correction"),
    },
    fake_factor_producers=(ff.RawFakeFactors_sm_lt, ff.FakeFactors_sm_lt),
    corrected_producers=(ff.FakeFactors_sm_lt,),
)

TT = Channel(
    inputs={
        q.ff_input_qcd_tt: ("QCD_fake_factors",),
        q.ff_input_qcdsub_tt: ("QCD_subleading_fake_factors",),
        q.ff_input_fraction_tt: ("process_fractions", "process_fractions_subleading"),
        q.ff_input_dr_tt: ("QCD_DR_SR_correction", "QCD_subleading_DR_SR_correction"),
        q.ff_input_nc_qcd_tt: ("QCD_compound_correction",),
        q.ff_input_nc_qcdsub_tt: ("QCD_subleading_compound_correction",),
    },
    fake_factor_producers=(ff.RawFakeFactors_sm_tt_1, ff.FakeFactors_sm_tt_1, ff.RawFakeFactors_sm_tt_2, ff.FakeFactors_sm_tt_2),
    corrected_producers=(ff.FakeFactors_sm_tt_1, ff.FakeFactors_sm_tt_2),
)

CHANNELS = {"et": LT, "mt": LT, "tt": TT}

# which non-closure variations become shifts: "coarse", "fine" or "both"
NON_CLOSURE = "coarse"

# directory containing fake_factors_<scope>.json.gz and FF_corrections_<scope>.json.gz
_RUN3_PAYLOADS = {
    "2022preEE": "payloads/fake_factors/sm/2022/260916",
    "2022postEE": "payloads/fake_factors/sm/2022/260916",
    "2023preBPix": "payloads/fake_factors/sm/2023/260916",
    "2023postBPix": "payloads/fake_factors/sm/2023/260916",
    "2024": "payloads/fake_factors/sm/2024",
    "2025": "payloads/fake_factors/sm/2025",
    "2026": "payloads/fake_factors/sm/2025",  # to update later on
}
PAYLOADS = {
    "et": _RUN3_PAYLOADS,
    "mt": {"2018": "payloads/fake_factors/sm/2018/with_embedding", **_RUN3_PAYLOADS},
    "tt": _RUN3_PAYLOADS,
}

OUTPUTS = {
    "et": [q.raw_fake_factor_2, q.fake_factor_2],
    "mt": [q.raw_fake_factor_2, q.fake_factor_2],
    "tt": [q.raw_fake_factor_1, q.fake_factor_1, q.raw_fake_factor_2, q.fake_factor_2],
}


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
) -> FriendTreeConfiguration:
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

    for scope in scopes:
        channel = CHANNELS[scope]
        payloads = PAYLOADS[scope][era]
        files = {
            "file": f"{payloads}/fake_factors_{scope}.json.gz",
            "corr_file": f"{payloads}/FF_corrections_{scope}.json.gz",
        }
        schemas = ff.load_schemas(files)
        parameters, variations = ff.variations(schemas, NON_CLOSURE)

        configuration.add_config_parameters(scope, {**parameters, **files})
        configuration.add_producers(
            scope,
            [
                nn_output.VariableConversionToFloatProducerGroup,
                *ff.input_producers(channel.inputs, scope, schemas),
                *channel.fake_factor_producers,
            ],
        )
        configuration.add_outputs(scope, OUTPUTS[scope])

        for parameter, variation in variations:
            if parameter.endswith("_correction"):
                producers = channel.corrected_producers
            else:
                producers = channel.fake_factor_producers
            for direction in ("Up", "Down"):
                configuration.add_shift(
                    SystematicShift(
                        name=f"{variation}{direction}",
                        shift_config={(scope,): {parameter: f"{variation}{direction}"}},
                        producers={(scope,): producers},
                    )
                )

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
