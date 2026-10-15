import importlib
import json
import math
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

# {vec_open}/{vec_close} are literal braces, <layout> the event quantities of the classic corrections,
# <parameter> the config parameter set by the shifts
PACK_CALL = '''fakefactors::generic::build_inputs({df}, {output}, {input_vec})'''
CORRECTION_CALL = (
    '''fakefactors::generic::correction_term({df}, correctionManager, {output}, {input}, '''
    '''<layout>, "<process>", "<correction>", "{<parameter>}", "{<file>}")'''
)
NON_CLOSURE_CALL = (
    '''fakefactors::generic::non_closure_term(\n'''
    '''        {df}, correctionManager, {output}, {input}, <layout>, "<process>", "<correction>", "<prefix>", '''
    '''<variables>, "{<parameter>}", "{corr_file}")'''
)
FRACTIONS_CALL = (
    '''fakefactors::generic::fractions({df}, correctionManager, {output}, {input}, '''
    '''<layout>, "<correction>", "{<parameter>}", <processes>, "{file}")'''
)
ONNX_CALL = '''fakefactors::generic::onnx_term({df}, onnxSessionManager, {output}, {input}, "{<parameter>}")'''
ONNX_FRACTIONS_CALL = (
    '''fakefactors::generic::onnx_fractions({df}, onnxSessionManager, {output}, {input}, '''
    '''"{<parameter>}", <n_processes>)'''
)
COMBINE_CALL = (
    '''fakefactors::generic::combine<<n_columns>>({df}, {output}, {input_vec}, '''
    '''{vec_open}<n_terms>{vec_close}, <strict>)'''
)


def add_fake_factors(
    configuration, scope, analysis, era, payloads, legs, non_closure, iso_wp, ml=None, split_info=False,
):
    # legs: hadronic tau leg index -> suffix of its correction names, e.g. {1: "", 2: "_subleading"}
    # non_closure: "coarse" (compound shifts), "fine" (per variable shifts) or "both"
    # iso_wp: the tau vsJet WP of the signal region, selecting the failing tau of the fully hadronic fake factor weight
    # ml: leg index -> ONNX models replacing the classic corrections of the terms they list (see ML in sm_fake_factors_generic.py)
    # split_info: also write the terms of every process (fake factor, DR->SR, non-closure) and the fractions
    q = importlib.import_module(f"analysis_configurations.{analysis}.quantities.output")

    # payload files and the corrections they hold
    files = {
        "file": f"{payloads}/fake_factors_{scope}.json.gz",
        "corr_file": f"{payloads}/FF_corrections_{scope}.json.gz",
    }
    files = {
        key: path
        for key, path in files.items()
        if os.path.exists(os.path.join("analysis_configurations", analysis, path))
    }
    configuration.add_config_parameters(scope, files)

    corrections = {}
    for path in files.values():
        payload = os.path.join("analysis_configurations", analysis, path)
        schema = json.loads(correctionlib.CorrectionSet.from_file(payload)._data)
        for correction in (schema.get("corrections") or []) + (schema.get("compound_corrections") or []):
            corrections[correction["name"]] = correction

    shifts = {}
    parity = None
    for n, suffix in legs.items():
        spec = dict((ml or {}).get(n, {}))
        if spec:
            # the ONNX models are found by their directories: <term> for the nominal one and <term>_<uncertainty>Up/Down
            # (one word, plain Up/Down without it) for the variations; the legacy directories of other names are ignored
            analysis_dir = os.path.join("analysis_configurations", analysis)
            models_dir = os.path.join(analysis_dir, spec["model"].split("{name}")[0])
            exists = lambda name, kind: os.path.exists(os.path.join(analysis_dir, spec["model"].format(name=name, kind=kind)))
            uncertainties = lambda directory, kind: sorted(
                {
                    d[len(directory) + 1:-2]
                    for d in os.listdir(models_dir)
                    if d.startswith(f"{directory}_") and d.endswith("Up") and "_" not in d[len(directory) + 1:-2]
                    and exists(d, kind) and exists(f"{d[:-2]}Down", kind)
                },
                key=lambda u: (("", "Stat").index(u) if u in ("", "Stat") else 2, u),
            )
            dr_sr = {p: f"{p}_DR_SR_correction" for p in spec["processes"]}
            spec["ff"] = {p: uncertainties(p, "ff") for p in spec["processes"] if exists(p, "ff")}
            spec["dr_sr"] = {p: uncertainties(d, "ff") for p, d in dr_sr.items() if exists(d, "ff")}
            if exists("fractions", "nn_output"):
                spec["fractions"] = {p: uncertainties(f"fractions_{p}", "nn_output") for p in spec["processes"]}
        processes = _find_processes(corrections, suffix, legs.values(), spec.get("processes"))
        guard = getattr(q, f"pt_{n}")

        # the terms of the leg: (kind, process) -> classic correction, None for an ONNX model
        terms = {("fractions", ""): None if "fractions" in spec else f"process_fractions{suffix}"}
        for p in processes:
            candidates = (
                ("ff", f"{p['name']}{suffix}_fake_factors"),
                ("dr_sr", p["dr_sr"]),
                ("non_closure", p["non_closure"]),
            )
            for kind, correction in candidates:
                if p["name"] in spec.get(kind, {}):
                    terms[kind, p["name"]] = None
                elif correction in corrections:
                    terms[kind, p["name"]] = correction
                elif kind == "ff":
                    raise ValueError(f"no '{correction}' correction in the payloads and no ONNX model for it")

        fractions = terms["fractions", ""]
        if fractions and fractions not in corrections:
            raise ValueError(f"no '{fractions}' correction in the payloads and no ONNX models for it")

        # the event quantities read by the classic corrections, packed into one column
        layout = list(dict.fromkeys(
            v["name"]
            for c in terms.values() if c
            for v in corrections[c]["inputs"]
            if v["name"] not in NON_QUANTITY_INPUTS
        ))
        pack = Quantity(f"ff_inputs_{n}")
        producers = []
        if layout:
            producers.append(Producer(
                name=f"FakeFactorInputs_{scope}_{n}", call=PACK_CALL,
                input=_quantities(q, layout), output=[pack], scopes=[scope],
            ))
        tokens = {
            "<layout>": "{vec_open}" + ", ".join(f'"{name}"' for name in layout) + "{vec_close}",
            "<processes>": "{vec_open}" + ", ".join(f'"{p["name"]}"' for p in processes) + "{vec_close}",
            "<n_processes>": str(len(processes)),
        }

        # one producer and output column per term, with the variations that change it
        columns, term_shifts, ml_packs = {}, [], {}
        for (kind, name), correction in terms.items():
            column = columns[kind, name] = Quantity(
                f"ff_fractions_{n}" if kind == "fractions" else f"ff_{kind}_{name}_{n}"
            )
            p = next((p for p in processes if p["name"] == name), {})

            if correction:
                parameter = {
                    "fractions": f"fraction_variation{suffix}",
                    "ff": f"{name}{suffix}_variation",
                    "dr_sr": correction,
                    "non_closure": f"{name}{suffix}_non_closure_correction",
                }[kind]
                call = {
                    "fractions": FRACTIONS_CALL,
                    "ff": CORRECTION_CALL,
                    "dr_sr": CORRECTION_CALL,
                    "non_closure": NON_CLOSURE_CALL,
                }[kind]
                variables = ", ".join(f'"{v}"' for v in p.get("non_closure_variables", []))
                term_tokens = {
                    "<process>": name,
                    "<correction>": correction,
                    "<parameter>": parameter,
                    "<file>": "corr_file" if kind == "dr_sr" else "file",
                    "<prefix>": p.get("non_closure_prefix", ""),
                    "<variables>": "{vec_open}" + variables + "{vec_close}",
                }
                nominal, inputs = "nominal", [guard, pack]

                # variation keys of the correction (or of the corrections it stacks), the non-closure ones as selected
                variations = []
                for component in corrections[correction].get("stack", [correction]):
                    for entry in corrections[component]["data"]["content"]:
                        match = VARIATION_KEY.match(entry["key"])
                        if not match:
                            continue
                        base = match.group(1)
                        is_coarse = "_non_closure_Corr" in base
                        if "non_closure" in base and non_closure != "both" and is_coarse != (non_closure == "coarse"):
                            continue
                        direction = (match.group(2) or match.group(3)).capitalize()
                        variations.append((base + direction, entry["key"]))

            else:
                # the models of the variations are the files <directory>_<uncertainty>Up/Down of the nominal one
                directory = {"fractions": "fractions", "ff": name, "dr_sr": f"{name}_DR_SR_correction"}[kind]
                model = lambda d: spec["model"].format(name=d, kind="nn_output" if kind == "fractions" else "ff")
                features, n_outputs = _read_model(analysis, model(directory))
                if n_outputs != (len(processes) if kind == "fractions" else 1):
                    raise ValueError(f"{model(directory)} has {n_outputs} outputs for {len(processes)} processes")

                if kind == "fractions":
                    entries = [
                        (f"fractions_{proc}_{unc}", f"{proc}_fraction", unc)
                        for proc, uncs in spec[kind].items()
                        for unc in uncs
                    ]
                else:
                    label = f"{name}_DR_SR_Corr" if kind == "dr_sr" else name
                    entries = [(f"{directory}_{unc}", label, unc) for unc in spec[kind][name]]

                variations = []
                for variation_directory, label, unc in entries:
                    for direction in ("Up", "Down"):
                        path = model(variation_directory + direction)
                        if _read_model(analysis, path) != (features, n_outputs):
                            raise ValueError(
                                f"{path} differs from {model(directory)} in the input features or the outputs"
                            )
                        shift_name = "_".join(filter(None, ["CMS_fake_t", label, unc, era[:4], scope])) + direction
                        variations.append((shift_name, path))

                # one packed input column per distinct feature list of the models
                if features not in ml_packs:
                    ml_packs[features] = Quantity(f"ff_inputs_{n}_ml{len(ml_packs)}")
                    if "event_parity" in features and parity is None:
                        parity = Producer(
                            name=f"EventParity_{scope}", call="ml_sm::EventParity({df}, {output}, {input})",
                            input=[Quantity("event")], output=[q.event_parity_float], scopes=[scope],
                        )
                        producers.append(parity)
                    producers.append(Producer(
                        name=f"FakeFactorInputs_{scope}_{n}_ml{len(ml_packs) - 1}", call=PACK_CALL,
                        input=_quantities(q, features), output=[ml_packs[features]], scopes=[scope],
                    ))

                parameter = f"fractions{suffix}_model" if kind == "fractions" else f"{name}{suffix}_{kind}_model"
                call = ONNX_FRACTIONS_CALL if kind == "fractions" else ONNX_CALL
                term_tokens, nominal, inputs = {"<parameter>": parameter}, model(directory), [guard, ml_packs[features]]

            producer = Producer(
                name=f"FakeFactor_{kind}{name}_{scope}_{n}", call=_fill(call, tokens | term_tokens),
                input=inputs, output=[column], scopes=[scope],
            )
            producers.append(producer)
            configuration.add_config_parameters(scope, {parameter: nominal})
            term_shifts.append((kind, producer, parameter, variations))

        # the fake factor is the sum over the processes of fraction * fake factor * DR->SR * non-closure,
        # the raw one has no corrections
        combined = {}
        outputs = (
            (getattr(q, f"raw_fake_factor_{n}"), ("ff",), "false"),
            (getattr(q, f"fake_factor_{n}"), ("ff", "dr_sr", "non_closure"), "true"),
        )
        for output, kinds, strict in outputs:
            per_process = [
                [columns[kind, p["name"]] for kind in kinds if (kind, p["name"]) in columns]
                for p in processes
            ]
            inputs = [guard, columns["fractions", ""]] + [column for entry in per_process for column in entry]
            call = _fill(COMBINE_CALL, {
                "<n_columns>": str(len(inputs) - 2),
                "<n_terms>": ", ".join(str(len(entry)) for entry in per_process),
                "<strict>": strict,
            })
            combined[kinds] = Producer(
                name=f"{'Raw' if strict == 'false' else ''}FakeFactors_{scope}_{n}", call=call,
                input=inputs, output=[output], scopes=[scope],
            )
        raw, corrected = combined.values()

        split_columns = [columns[term] for term in columns] if split_info else []
        configuration.add_producers(scope, producers + [raw, corrected])
        configuration.add_outputs(
            scope, [getattr(q, f"raw_fake_factor_{n}"), getattr(q, f"fake_factor_{n}")] + split_columns
        )

        # a term is varied by the parameter selecting its variation;
        # DR->SR and non-closure only change the corrected fake factor
        for kind, producer, parameter, variations in term_shifts:
            affected = [producer] + ([raw] if kind in ("fractions", "ff") else []) + [corrected]
            for name, value in variations:
                shift_config, shift_producers = shifts.setdefault(name, ({}, []))
                shift_config[parameter] = value
                shift_producers.extend(x for x in affected if x not in shift_producers)

    # ff_weight, the weight of the anti-isolated region: the fake factor of the hadronic tau (et/mt) or half of the one
    # of the failing tau (tt); the fake factors of the legs stay available
    if len(legs) == 1:
        ff_weight = Producer(
            name=f"FakeFactorWeight_{scope}", call='''event::quantity::Copy<float>({df}, {output}, {input})''',
            input=[q.fake_factor_2], output=[q.ff_weight], scopes=[scope],
        )
    else:
        ff_weight = Producer(
            name=f"FakeFactorWeight_{scope}", call='''event::quantity::AntiIsoFakeFactor({df}, {output}, {input})''',
            input=[
                q.fake_factor_1, q.fake_factor_2,
                Quantity(f"id_tau_vsJet_{iso_wp}_1"), Quantity(f"id_tau_vsJet_{iso_wp}_2"),
            ],
            output=[q.ff_weight], scopes=[scope],
        )
    configuration.add_producers(scope, [ff_weight])
    configuration.add_outputs(scope, [q.ff_weight])

    # Run 3 and ML payloads must carry the final nuisance names as variation keys
    # (TAUER's fake_factors/rename_payload_keys.py converts old ones)
    if (int(era[:4]) >= 2022 or ml) and (legacy := [n for n in shifts if not n.startswith("CMS_fake_t_")]):
        raise ValueError(
            f"the variation keys of {payloads} do not follow CMS_fake_t_<process>_<uncertainty>_<era>_<channel>, "
            f"e.g. {legacy[0]}"
        )

    for name, (shift_config, shift_producers) in shifts.items():
        configuration.add_shift(SystematicShift(
            name=name, shift_config={(scope,): shift_config}, producers={(scope,): shift_producers},
        ))


def _find_processes(corrections, suffix, suffixes, ml_names):
    # the processes of a leg are the <process><suffix>_fake_factors corrections (or the ones of the ONNX models),
    # DR->SR and non-closure are optional
    names = ml_names or [
        match.group(1)
        for name in corrections
        if (match := re.fullmatch(rf"(.+){re.escape(suffix)}_fake_factors", name))
        and not any(s and match.group(1).endswith(s) for s in suffixes)
    ]
    if not names:
        raise ValueError(f"no '<process>{suffix}_fake_factors' correction in the payloads")

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
            # the compound stacks one correction per variable, the variable is inserted into the variation names
            # after the prefix, e.g. CMS_fake_t_QCD_non_closure_CorrStatShift_2024_mtUp
            # -> CMS_fake_t_QCD_non_closure_<variable>_CorrStatShift_2024_mtUp
            stack = corrections[non_closure]["stack"]
            process["non_closure_variables"] = [
                c.removeprefix(f"{name}{suffix}_non_closure_").removesuffix("_correction") for c in stack
            ]
            coarse = next(
                (e["key"] for c in stack for e in corrections[c]["data"]["content"] if "non_closure_Corr" in e["key"]),
                None,
            )
            if coarse:
                process["non_closure_prefix"] = coarse[: coarse.index("non_closure_Corr") + len("non_closure_")]
            else:
                process["non_closure_prefix"] = f"{name}{suffix}_non_closure_"
        processes.append(process)
    return processes


def _read_model(analysis, path):
    # input features in the order of the model metadata and number of outputs of an ONNX model
    import onnx

    model = onnx.load(os.path.join("analysis_configurations", analysis, path), load_external_data=False)
    text = next(entry.value for entry in model.metadata_props if entry.key == "input_tensor")
    dims = lambda value: [dim.dim_value for dim in value.type.tensor_type.shape.dim]
    features = tuple(line for line in text.split("\n")[2:] if line)
    n_inputs = math.prod(dims(model.graph.input[0]))
    if n_inputs != len(features):
        raise ValueError(f"{path} has {n_inputs} inputs for the {len(features)} features of its metadata")
    return features, math.prod(dims(model.graph.output[0]))


def _quantities(q, layout):
    # payload names must match the analysis quantities, optionally as the <name>_float version
    quantities = [getattr(q, name, None) or getattr(q, f"{name}_float", None) for name in layout]
    if None in quantities:
        raise AttributeError(
            f"payload input '{layout[quantities.index(None)]}' (or '..._float') is not a quantity in {q.__name__}"
        )
    return quantities


def _fill(template, tokens):
    for token, value in tokens.items():
        template = template.replace(token, value)
    return template
