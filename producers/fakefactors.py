import json
import os
from typing import Dict, List, Tuple

import correctionlib
from code_generation.helpers import defaults
from code_generation.producer import Producer
from code_generation.quantity import Quantity

from ..quantities import output as q


# ---------------------------------------------------------------------------
# Fake factor producers
# ---------------------------------------------------------------------------

with defaults(scopes=["et", "mt"]):
    RawFakeFactors_sm_lt = Producer(
        call='''fakefactors::sm::raw_fakefactor_lt(
            {df},
            correctionManager,
            {output},
            {input},
            "{fraction_variation}",
            "{QCD_variation}",
            "{Wjets_variation}",
            "{ttbar_variation}",
            "{file}")''',
        input=[q.pt_2, q.njets, q.mt_1],
        output=[q.raw_fake_factor_2],
    )
    FakeFactors_sm_lt = Producer(
        call='''fakefactors::sm::fakefactor_lt(
            {df},
            correctionManager,
            {output_vec},
            {input},
            "{fraction_variation}",
            "{QCD_variation}",
            "{Wjets_variation}",
            "{ttbar_variation}",
            "{QCD_DR_SR_correction}",
            "{QCD_non_closure_correction}",
            "{Wjets_DR_SR_correction}",
            "{Wjets_non_closure_correction}",
            "{ttbar_non_closure_correction}",
            "{file}",
            "{corr_file}",
            false)''',
        input=[q.pt_2, q.ff_input_lt, q.ff_input_fraction_lt, q.ff_input_dr_lt, q.ff_input_nc_lt],
        output=[q.fake_factor_2],
    )

with defaults(scopes=["tt"]):
    with defaults(input=[q.pt_1, q.pt_2, q.njets, q.m_vis]):
        RawFakeFactors_sm_tt_1 = Producer(
            call='''fakefactors::sm::raw_fakefactor_tt(
                {df},
                correctionManager,
                {output},
                0,
                {input},
                "{QCD_variation}",
                "{fraction_variation}",
                "{file}")''',
            output=[q.raw_fake_factor_1],
        )
        RawFakeFactors_sm_tt_2 = Producer(
            call='''fakefactors::sm::raw_fakefactor_tt(
                {df},
                correctionManager,
                {output},
                1,
                {input},
                "{QCD_subleading_variation}",
                "{fraction_variation_subleading}",
                "{file}")''',
            output=[q.raw_fake_factor_2],
        )
    with defaults(
        input=[
            q.pt_1,
            q.pt_2,
            q.ff_input_qcd_tt,
            q.ff_input_qcdsub_tt,
            q.ff_input_fraction_tt,
            q.ff_input_dr_tt,
            q.ff_input_nc_qcd_tt,
            q.ff_input_nc_qcdsub_tt,
        ]
    ):
        FakeFactors_sm_tt_1 = Producer(
            call='''fakefactors::sm::fakefactor_tt(
                {df},
                correctionManager,
                {output_vec},
                0,
                {input},
                "{fraction_variation}",
                "{QCD_variation}",
                "{QCD_DR_SR_correction}",
                "{QCD_non_closure_correction}",
                "{file}",
                "{corr_file}",
                false)''',
            output=[q.fake_factor_1],
        )
        FakeFactors_sm_tt_2 = Producer(
            call='''fakefactors::sm::fakefactor_tt(
                {df},
                correctionManager,
                {output_vec},
                1,
                {input},
                "{fraction_variation_subleading}",
                "{QCD_subleading_variation}",
                "{QCD_subleading_DR_SR_correction}",
                "{QCD_subleading_non_closure_correction}",
                "{file}",
                "{corr_file}",
                false)''',
            output=[q.fake_factor_2],
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_schemas(files: Dict[str, str]) -> Dict[str, dict]:
    return {
        name: json.loads(correctionlib.CorrectionSet.from_file(os.path.join("analysis_configurations/tau", path))._data)
        for name, path in files.items()
    }


def input_producers(inputs: Dict[Quantity, Tuple[str, ...]], scope: str, schemas: Dict[str, dict]) -> List[Producer]:
    # One producer per input column, filled with the variables its corrections declare.
    # All corrections evaluated on the same column must declare the same inputs.
    corrections = {
        correction["name"]: correction
        for schema in schemas.values()
        for correction in (schema.get("corrections") or []) + (schema.get("compound_corrections") or [])
    }
    producers = []
    for column, names in inputs.items():
        missing = [name for name in names if name not in corrections]
        if missing:
            raise KeyError(f"corrections {missing} not found in the correction files")
        declared = {
            tuple(v["name"] for v in corrections[name]["inputs"] if v["name"] not in ("syst", "process"))
            for name in names
        }
        if len(declared) > 1:
            raise ValueError(f"corrections {list(names)} share the column {column.name} but declare different inputs: {declared}")

        quantities = []
        for variable in declared.pop():
            # correctionlib inputs are real-valued, prefer the float cast (e.g. njets -> njets_float)
            quantity = getattr(q, f"{variable}_float", None) or getattr(q, variable, None)
            if quantity is None:
                raise AttributeError(f"correction input '{variable}' has no matching CROWN quantity")
            quantities.append(quantity)

        producers.append(
            Producer(
                name=f"FFInput_{column.name}",
                call="fakefactors::build_model_input_column({df}, {output}, {input_vec})",
                input=quantities,
                output=[column],
                scopes=[scope],
            )
        )
    return producers


def variations(schemas: Dict[str, dict], non_closure: str) -> Tuple[Dict[str, str], List[Tuple[str, str]]]:
    # Config parameters selecting each correction's variation (set to nominal), and the
    # (config parameter, variation name) pairs to shift.
    # non_closure selects which non-closure variations are shifted: "coarse" 
    # (shared by all non-closure variables), "fine" (per variable) or "both".
    parameters, shifts = {}, set()
    for schema in schemas.values():
        for correction in schema["corrections"]:
            parameter = _config_parameter(correction["name"])
            parameters[parameter] = "nominal"
            for entry in correction["data"]["content"]:
                if not entry["key"].endswith("Up"):
                    continue
                variation = entry["key"].removesuffix("Up")
                if "non_closure" in variation and non_closure != "both":
                    is_coarse = "_non_closure_Corr" in variation
                    if is_coarse != (non_closure == "coarse"):
                        continue
                shifts.add((parameter, variation))
    return parameters, sorted(shifts)


def _config_parameter(correction_name: str) -> str:
    # Config parameter that selects the variation of a correction
    if correction_name == "process_fractions":
        return "fraction_variation"
    if correction_name == "process_fractions_subleading":
        return "fraction_variation_subleading"

    process = "QCD_subleading" if correction_name.startswith("QCD_subleading_") else correction_name.split("_")[0]
    remainder = correction_name[len(process) + 1:]
    if remainder == "fake_factors":
        return f"{process}_variation"
    if "DR_SR" in remainder:
        return f"{process}_DR_SR_correction"
    return f"{process}_non_closure_correction"
