import json
import os
from pprint import pprint

import correctionlib


def ff_process_name(name: str) -> str:
    if "process_fractions" in name:
        return "fraction_variation"

    process = name.split("_")[0]  # QCD, Wjets, ttbar
    if "fake_factors" in name:
        return f"{process}_variation"

    suffix = "DR_SR" if "DR_SR" in name else "non_closure"
    return f"{process}_{suffix}_correction"


def load_ff_correctionlib(path: str) -> correctionlib.CorrectionSet:
    return json.loads(correctionlib.CorrectionSet.from_file(path)._data)["corrections"]


def correction_names(
    ff_file: str,
    correction_file: str,
    as_tuple: bool = True
) -> list[str]:
    return [
        (
            (ff_process_name(correction["name"]), value["key"].replace("Up", ""))
            if as_tuple
            else value["key"].replace("Up", "")
        )
        for corrections in (
            load_ff_correctionlib(ff_file),
            load_ff_correctionlib(correction_file),
        )
        for correction in corrections
        for value in correction["data"]["content"]
        if value["key"].endswith("Up")
        # ("<producer variation argument>", "<variation name without direction>")
    ]


pprint(
    correction_names(
        "../payloads/fake_factors/sm/2018/with_embedding/fake_factors_mt.json.gz",
        "../payloads/fake_factors/sm/2018/with_embedding/FF_corrections_mt.json.gz",
        as_tuple=False,
    )
)
