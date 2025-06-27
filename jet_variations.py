from __future__ import annotations  # needed for type annotations in > python 3.7

from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import jets as jets
from .producers import scalefactors as scalefactors
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


def add_jetVariations(configuration: Configuration, era: str):
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    USE_JES_INDIVIDUAL = False

    with defaults(exclude_samples=["data", "embedding", "embedding_mc"]):
        add_shift(
            name="jesUncTotal",
            shift_config={
                "Up": {
                    "global": {"jet_jes_shift": 1, "jet_jes_sources": '{"Total"}'},
                    ("mt", "et", "tt"): {"btag_sf_variation": "up_jes"},
                },
                "Down": {
                    "global": {"jet_jes_shift": -1, "jet_jes_sources": '{"Total"}'},
                    ("mt", "et", "tt"): {"btag_sf_variation": "down_jes"},
                },
            },
            producers={
                "global": {jets.JetEnergyCorrection},
                ("mt", "et", "tt"): {scalefactors.btagging_SF},
            },
        )
        with defaults(scopes="global", producers=[jets.JetEnergyCorrection]):
            add_shift(name="jerUnc", shift_key="jet_jer_shift", shift_map={"Up": '"up"', "Down": '"down"'})
            if era == "2018":  # --- HEM 15/16 issue ---
                add_shift(
                    name="jesUncHEMIssue",
                    shift_key=["jet_jes_shift", "jet_jes_sources"],
                    shift_map={"Up": [1, '{"HEMIssue"}'], "Down": [-1, '{"HEMIssue"}']},
                )

            if USE_JES_INDIVIDUAL:  # individual JES sources, not recommended
                with defaults(shift_key=["jet_jes_shift", "jet_jes_sources", "btag_sf_variation"]):
                    for JEC_source in [
                        "AbsoluteStat",
                        "AbsoluteScale",
                        "AbsoluteMPFBias",
                        "Fragmentation",
                        "SinglePionECAL",
                        "SinglePionHCAL",
                        "FlavorQCD",
                        "TimePtEta",
                        "RelativeJEREC1",
                        "RelativeJEREC2",
                        "RelativeJERHF",
                        "RelativePtBB",
                        "RelativePtEC1",
                        "RelativePtEC2",
                        "RelativePtHF",
                        "RelativeBal",
                        "RelativeSample",
                        "RelativeFSR",
                        "RelativeStatFSR",
                        "RelativeStatEC",
                        "RelativeStatHF",
                        "PileUpDataMC",
                        "PileUpPtRef",
                        "PileUpPtBB",
                        "PileUpPtEC1",
                        "PileUpPtEC2",
                        "PileUpPtHF",
                    ]:
                        add_shift(
                            name=f"jesUnc{JEC_source}",
                            shift_map={
                                "Up": [1, f'{{"{JEC_source}"}}', f"up_jes{JEC_source}"],
                                "Down": [-1, f'{{"{JEC_source}"}}', f"down_jes{JEC_source}"],
                            },
                        )
            else:  # jes reduced set of sources, recommended
                with defaults(shift_key=["jet_jes_shift", "jet_jes_sources"]):
                    for name, JES_source in [
                        ("jesUncAbsolute", '{"SinglePionECAL", "SinglePionHCAL", "AbsoluteMPFBias", "AbsoluteScale", "Fragmentation", "PileUpDataMC", "RelativeFSR", "PileUpPtRef"}'),
                        ("jesUncAbsoluteYear", '{"AbsoluteStat", "TimePtEta", "RelativeStatFSR"}'),
                        ("jesUncFlavorQCD", '{"FlavorQCD"}'),
                        ("jesUncBBEC1", '{"PileUpPtEC1", "PileUpPtBB", "RelativePtBB"}'),
                        ("jesUncBBEC1Year", '{"RelativeJEREC1", "RelativePtEC1", "RelativeStatEC"}'),
                        ("jesUncHF", '{"RelativePtHF", "PileUpPtHF", "RelativeJERHF"}'),
                        ("jesUncHFYear", '{"RelativeStatHF"}'),
                        ("jesUncEC2", '{"PileUpPtEC2"}'),
                        ("jesUncEC2Year", '{"RelativeJEREC2", "RelativePtEC2"}'),
                        ("jesUncRelativeBal", '{"RelativeBal"}'),
                        ("jesUncRelativeSampleYear", '{"RelativeSample"}')
                    ]:
                        add_shift(name=name, shift_map={"Up": [1, JES_source], "Down": [-1, JES_source]})

    return configuration
