import correctionlib
import json
from typing import List, Union, Tuple
import os


class FFCorrectionNames:
    @staticmethod
    def process_name(name: str) -> str:
        if "process_fractions" in name:
            return "fraction_variation"

        process = name.split("_")[0]  # QCD, Wjets, ttbar
        if "fake_factors" in name:
            return f"{process}_variation"

        suffix = "DR_SR" if "DR_SR" in name else "non_closure"
        return f"{process}_{suffix}_correction"

    @staticmethod
    def get_names(
        ff_file: str,
        correction_file: str,
    ) -> List[Tuple[str, str]]:
        prefix = "analysis_configurations/tau"
        ff_file = os.path.join(prefix, ff_file)
        correction_file = os.path.join(prefix, correction_file)
        correction_collection = [
            (FFCorrectionNames.process_name(correction["name"]), value["key"].replace("Up", ""))
            for corrections in (
                json.loads(correctionlib.CorrectionSet.from_file(ff_file)._data)["corrections"],
                json.loads(correctionlib.CorrectionSet.from_file(correction_file)._data)["corrections"],
            )
            for correction in corrections
            for value in correction["data"]["content"]
            if value["key"].endswith("Up")
            # (producer_variation_argument, variation_name_without_direction)
        ]
        return correction_collection
