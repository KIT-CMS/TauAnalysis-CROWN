from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from .producers import fakefactors_generic as ff

# hadronic tau leg index -> suffix of its correction names
LEGS = {"et": {2: ""}, "mt": {2: ""}, "tt": {1: "", 2: "_subleading"}}

# which non-closure variations become shifts: "coarse" (compound), "fine" (per variable) or "both"
NON_CLOSURE = "coarse"

# directory (relative to the analysis folder) containing fake_factors_<scope>.json.gz and FF_corrections_<scope>.json.gz
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


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
    *,
    analysis: str,
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
        ff.add_fake_factors(configuration, scope, analysis, PAYLOADS[scope][era], LEGS[scope], NON_CLOSURE)

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
