import importlib
import json
import os
import re

import correctionlib
from code_generation.producer import Producer
from code_generation.quantity import Quantity
from code_generation.systematics import SystematicShift

# payload inputs that are not event quantities
NON_QUANTITY_INPUTS = ("process", "syst")
# variation keys look like "<name>Up" or "<name>_up"
VARIATION_KEY = re.compile(r"^(.*?)(?:_?(Up|Down)|_(up|down))$")

# {vec_open}/{vec_close} are literal braces, <layout> the event quantities read by the corrections, <leg> the corrections
# of the leg with their variations "{<parameter>}" that are set by the shifts
INPUTS_CALL = '''fakefactors::generic::build_inputs({df}, {output}, {input_vec})'''
RAW_CALL = '''fakefactors::generic::raw_fakefactor(
        {df},
        correctionManager,
        {output},
        {input},
        <layout>,
        "<pt>",
        <leg>,
        "{file}")'''
CORRECTED_CALL = '''fakefactors::generic::fakefactor(
        {df},
        correctionManager,
        {output_vec},
        {input},
        <layout>,
        "<pt>",
        <leg>,
        "{file}",
        "{corr_file}",
        false)'''
LEG = '''fakefactors::generic::Leg{vec_open}
            "<fractions>", "{<fraction_variation>}",
            {vec_open}
            <processes>
            {vec_close}
        {vec_close}'''


def add_fake_factors(configuration, scope, analysis, payloads, legs, non_closure):
    # legs: hadronic tau leg index -> suffix of its correction names, e.g. {1: "", 2: "_subleading"}
    # non_closure: "coarse" (compound shifts), "fine" (per variable shifts) or "both"
    q = importlib.import_module(f"analysis_configurations.{analysis}.quantities.output")
    files = {"file": f"{payloads}/fake_factors_{scope}.json.gz", "corr_file": f"{payloads}/FF_corrections_{scope}.json.gz"}
    configuration.add_config_parameters(scope, files)
    corrections = _read_corrections(analysis, files.values())

    shifts = {}
    for n, suffix in legs.items():
        processes = _find_processes(corrections, suffix, legs.values())
        parameters = _variation_parameters(suffix, processes)
        layout = _layout(corrections, parameters, n)
        inputs = Quantity(f"ff_inputs_{n}")
        raw_fake_factor, fake_factor = getattr(q, f"raw_fake_factor_{n}"), getattr(q, f"fake_factor_{n}")

        tokens = {
            "<layout>": "{vec_open}" + ", ".join(f'"{name}"' for name in layout) + "{vec_close}",
            "<pt>": f"pt_{n}",
            "<leg>": _leg(suffix, processes),
        }
        raw = Producer(name=f"RawFakeFactors_{scope}_{n}", call=_fill(RAW_CALL, tokens), input=[inputs], output=[raw_fake_factor], scopes=[scope])
        corrected = Producer(
            name=f"FakeFactors_{scope}_{n}", call=_fill(CORRECTED_CALL, tokens), input=[inputs], output=[fake_factor], scopes=[scope]
        )
        build_inputs = Producer(
            name=f"FakeFactorInputs_{scope}_{n}", call=INPUTS_CALL, input=_quantities(q, layout), output=[inputs], scopes=[scope]
        )
        configuration.add_producers(scope, [build_inputs, raw, corrected])
        configuration.add_outputs(scope, [raw_fake_factor, fake_factor])
        configuration.add_config_parameters(scope, {parameter: "nominal" for parameter in parameters.values()})

        # a correction is varied by the parameter selecting its variation; the fractions, DR->SR and non-closure
        # corrections only change the corrected fake factor
        for correction, parameter in parameters.items():
            producers = [corrected] if parameter.endswith("_correction") else [raw, corrected]
            for key in _variation_keys(corrections, correction, non_closure):
                name = _shift_name(key)
                shift_config, shift_producers = shifts.setdefault(name, ({}, []))
                shift_config[parameter] = key
                shift_producers.extend(p for p in producers if p not in shift_producers)

    for name, (shift_config, shift_producers) in shifts.items():
        configuration.add_shift(SystematicShift(name=name, shift_config={(scope,): shift_config}, producers={(scope,): shift_producers}))


def _read_corrections(analysis, paths):
    # name -> correction of all (compound) corrections of the payload files
    corrections = {}
    for path in paths:
        schema = json.loads(correctionlib.CorrectionSet.from_file(os.path.join("analysis_configurations", analysis, path))._data)
        for correction in (schema.get("corrections") or []) + (schema.get("compound_corrections") or []):
            corrections[correction["name"]] = correction
    return corrections


def _find_processes(corrections, suffix, suffixes):
    # the processes of a leg are the <process><suffix>_fake_factors corrections, DR->SR and non-closure are optional
    names = [
        match.group(1)
        for name in corrections
        if (match := re.fullmatch(rf"(.+){re.escape(suffix)}_fake_factors", name))
        and not any(s and match.group(1).endswith(s) for s in suffixes)
    ]
    if not names or f"process_fractions{suffix}" not in corrections:
        raise ValueError(f"no '<process>{suffix}_fake_factors' or 'process_fractions{suffix}' correction in the payloads")

    processes = []
    for name in names:
        dr_sr, non_closure = f"{name}{suffix}_DR_SR_correction", f"{name}{suffix}_compound_correction"
        process = {
            "name": name,
            "suffix": suffix,
            "dr_sr": dr_sr if dr_sr in corrections else "",
            "non_closure": non_closure if non_closure in corrections else "",
            "non_closure_variables": [],
            "non_closure_prefix": "",
        }
        if process["non_closure"]:
            # the compound stacks one correction per variable, the variable is inserted into the variation names after the prefix,
            # e.g. CMS_fake_t_QCD_non_closure_CorrStatShift_2024_mtUp -> CMS_fake_t_QCD_non_closure_<variable>_CorrStatShift_2024_mtUp
            stack = corrections[non_closure]["stack"]
            process["non_closure_variables"] = [c.removeprefix(f"{name}{suffix}_non_closure_").removesuffix("_correction") for c in stack]
            coarse = next((key for c in stack for key in _keys(corrections, c) if "non_closure_Corr" in key), None)
            process["non_closure_prefix"] = coarse[: coarse.index("non_closure_Corr") + len("non_closure_")] if coarse else f"{name}{suffix}_non_closure_"
        processes.append(process)
    return processes


def _variation_parameters(suffix, processes):
    # correction -> config parameter selecting its variation
    parameters = {f"process_fractions{suffix}": f"fraction_variation{suffix}"}
    for p in processes:
        parameters[f"{p['name']}{suffix}_fake_factors"] = f"{p['name']}{suffix}_variation"
        if p["dr_sr"]:
            parameters[p["dr_sr"]] = p["dr_sr"]
        if p["non_closure"]:
            parameters[p["non_closure"]] = f"{p['name']}{suffix}_non_closure_correction"
    return parameters


def _leg(suffix, processes):
    # one entry per process: name, fake factor, DR->SR, non-closure with its prefix and variables, the variation of
    # a correction that is not in the payloads stays "nominal"
    def variation(correction, parameter):
        return f'"{{{parameter}}}"' if correction else '"nominal"'

    vecs = []
    for p in processes:
        name = p["name"]
        entries = [
            f'"{name}"',
            f'"{name}{suffix}_fake_factors"', f'"{{{name}{suffix}_variation}}"',
            f'"{p["dr_sr"]}"', variation(p["dr_sr"], p["dr_sr"]),
            f'"{p["non_closure"]}"', f'"{p["non_closure_prefix"]}"', variation(p["non_closure"], f"{name}{suffix}_non_closure_correction"),
            "{vec_open}" + ", ".join(f'"{v}"' for v in p["non_closure_variables"]) + "{vec_close}",
        ]
        vecs.append("{vec_open}" + ", ".join(entries) + "{vec_close}")
    return _fill(LEG, {"<fractions>": f"process_fractions{suffix}", "<fraction_variation>": f"fraction_variation{suffix}", "<processes>": ",\n            ".join(vecs)})


def _layout(corrections, parameters, n):
    # every event quantity read by the corrections of the leg (first seen order), and the guard pt_<n>
    layout = []
    for correction in parameters:
        for variable in corrections[correction]["inputs"]:
            if variable["name"] not in NON_QUANTITY_INPUTS and variable["name"] not in layout:
                layout.append(variable["name"])
    if f"pt_{n}" not in layout:
        layout.append(f"pt_{n}")
    return layout


def _quantities(q, layout):
    # payload names must match the analysis quantities, optionally as the <name>_float version
    quantities = [getattr(q, name, None) or getattr(q, f"{name}_float", None) for name in layout]
    if None in quantities:
        raise AttributeError(f"payload input '{layout[quantities.index(None)]}' (or '..._float') is not a quantity in {q.__name__}")
    return quantities


def _keys(corrections, correction):
    return [entry["key"] for entry in corrections[correction]["data"]["content"]]


def _variation_keys(corrections, correction, non_closure):
    # variation keys of a correction (or of the corrections it stacks), the non-closure ones as selected
    for component in corrections[correction].get("stack", [correction]):
        for key in _keys(corrections, component):
            match = VARIATION_KEY.match(key)
            if not match:
                continue
            is_coarse = "_non_closure_Corr" in match.group(1)
            if "non_closure" in match.group(1) and non_closure != "both" and is_coarse != (non_closure == "coarse"):
                continue
            yield key


def _shift_name(key):
    match = VARIATION_KEY.match(key)
    return match.group(1) + (match.group(2) or match.group(3)).capitalize()


def _fill(template, tokens):
    for token, value in tokens.items():
        template = template.replace(token, value)
    return template
