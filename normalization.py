"""
Generates the per-(sample_type, era) nick -> {xsec, nevents, generator_weight}
lookup table that cpp_addons/src/normalization.cxx's SampleNormalization
producer loads at runtime, so the weights friend can normalize MC without a
separate Python friend task -- see project memory
(crown-weights-friend-project-status.md).

The table is written into CROWN's own data/ directory (data/normalization/),
which cmake's `install(DIRECTORY data/ ...)` rule already ships into every
build's tarball (see cmake/Build.cmake) -- the exact same mechanism used for
data/jsonpog-integration. Referenced downstream via a path relative to the
CWD the compiled executable runs from, matching how config.py already
references e.g. "data/jsonpog-integration/...". Not committed: gitignored,
regenerated fresh at every code-gen/build.
"""
import json
import os
from typing import Dict

# KingMaker's nanoAOD_version is a user-supplied luigi parameter, not
# statically derivable from era in general (see project memory:
# kingmaker-nanoaod-version-autodetect-pending). This mirrors the convention
# TauKITFlow's xsec/build_friend_tree.py documents (--dataset-config help
# text) and sample_database/'s own directory layout: v9 for Run2, v12 for
# 2022/2023, v15 for 2024/2025/2026. Update both together if/when the
# pending autodetect feature lands.
ERA_TO_NANOAOD_VERSION: Dict[str, str] = {
    "2016preVFP": "nanoAOD_v9",
    "2016postVFP": "nanoAOD_v9",
    "2017": "nanoAOD_v9",
    "2018": "nanoAOD_v9",
    "2022preEE": "nanoAOD_v12",
    "2022postEE": "nanoAOD_v12",
    "2023preBPix": "nanoAOD_v12",
    "2023postBPix": "nanoAOD_v12",
    "2024": "nanoAOD_v15",
    "2025": "nanoAOD_v15",
    "2026": "nanoAOD_v15",
}

# KingMaker/CROWN/analysis_configurations/tau/normalization.py -> up 3 to
# KingMaker/ -> sample_database/. Not discoverable any other way from inside
# the CROWN repo (CROWN has no knowledge of KingMaker's layout otherwise) --
# this assumes the checkout layout this analysis is developed in.
_TAU_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_CROWN_ROOT = os.path.abspath(os.path.join(_TAU_CONFIG_DIR, "..", ".."))
_KINGMAKER_ROOT = os.path.abspath(os.path.join(_CROWN_ROOT, ".."))
_DEFAULT_SAMPLE_DATABASE_ROOT = os.path.join(_KINGMAKER_ROOT, "sample_database")

# CROWN's own data/ directory -- cmake's `install(DIRECTORY data/ ...)` rule
# (cmake/Build.cmake) ships everything under here into every build's
# tarball, the same mechanism data/jsonpog-integration already relies on.
DATA_NORMALIZATION_DIR = os.path.join(_CROWN_ROOT, "data", "normalization")


def build_norm_table(era: str, sample_type: str, output_dir: str,
                      sample_database_root: str = None) -> str:
    """
    Reads sample_database/{nanoAOD_version}/datasets.json, filters to entries
    matching (era, sample_type), and writes {nick: {xsec, nevents,
    generator_weight}} to output_dir/{sample_type}_{era}_norm_table.json.

    Returns the path relative to CROWN's repo root (data/normalization/...),
    the form the runtime SampleNormalization producer call is given -- the
    executable is always run from a CWD containing a `data/` sibling
    directory (see module docstring).

    Silently returns an empty table for sample types that carry no per-nick
    normalization (data, embedding) -- SampleNormalization is only wired in
    for MC samples downstream, so this is never actually loaded for those,
    but build_config() doesn't know sample_type in advance, so this stays a
    no-op rather than raising.
    """
    sample_database_root = sample_database_root or _DEFAULT_SAMPLE_DATABASE_ROOT
    nanoaod_version = ERA_TO_NANOAOD_VERSION.get(era)
    if nanoaod_version is None:
        raise ValueError(
            f"normalization.build_norm_table: no nanoAOD version mapping for era {era!r} "
            f"-- add it to ERA_TO_NANOAOD_VERSION"
        )
    datasets_path = os.path.join(sample_database_root, nanoaod_version, "datasets.json")

    table = {}
    if sample_type not in ("data", "embedding", "embedding_mc"):
        with open(datasets_path) as f:
            datasets = json.load(f)
        for entry in datasets.values():
            if entry.get("era") != era or entry.get("sample_type") != sample_type:
                continue
            table[entry["nick"]] = {
                "xsec": float(entry["xsec"]),
                "nevents": float(entry["nevents"]),
                "generator_weight": float(entry["generator_weight"]),
            }
        if not table:
            raise ValueError(
                f"normalization.build_norm_table: no entries found in {datasets_path} "
                f"for era={era!r} sample_type={sample_type!r} -- either the database is "
                f"missing this (sample_type, era), or ERA_TO_NANOAOD_VERSION picked the "
                f"wrong nanoAOD version"
            )

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{sample_type}_{era}_norm_table.json"
    with open(os.path.join(output_dir, filename), "w") as f:
        json.dump(table, f)
    return f"data/normalization/{filename}"
