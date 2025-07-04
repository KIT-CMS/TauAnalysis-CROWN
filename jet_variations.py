from __future__ import annotations  # needed for type annotations in > python 3.7

from code_generation.configuration import Configuration

from .producers import jets as jets
from .producers import scalefactors as scalefactors
from .scripts.CROWNWrapper import (defaults,
                                   get_adjusted_add_shift_SystematicShift)

# taken from here: https://cms-jerc.web.cern.ch/Recommendations/#run-2


def add_jetVariations(configuration: Configuration, era: str) -> Configuration:
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    class JES_CONFIG:
        INDIVIDUAL = False
        REGROUPED = True  # preferred configuration

    with defaults(exclude_samples=["data", "embedding", "embedding_mc"]):
        with defaults(scopes="global", producers=[jets.JetEnergyCorrection]):
            add_shift(name="jerUnc", shift_key="jet_jer_shift",
                      shift_map={"Up": '"up"', "Down": '"down"'})
            if era == "2018":  # --- HEM 15/16 issue ---
                add_shift(
                    name="jesUncHEMIssue",
                    shift_key=["jet_jes_shift", "jet_jes_sources"],
                    shift_map={"Up": [1, '{"HEMIssue"}'],
                               "Down": [-1, '{"HEMIssue"}']},
                )

        with defaults(name="jesUncTotal"):  # two components of jesUncTotal
            add_shift(
                shift_key=["jet_jes_shift", "jet_jes_sources"],
                shift_map={"Up": [1, '{"Total"}'], "Down": [-1, '{"Total"}']},
                scopes="global",
                producers=[jets.JetEnergyCorrection]
            )
            add_shift(
                shift_key="btag_sf_variation",
                shift_map={"Up": "up_jes", "Down": "down_jes"},
                scopes=("mt", "et", "tt"),
                producers=[scalefactors.btagging_SF]
            )

        if JES_CONFIG.INDIVIDUAL:
            for name in [
                # --- jesUncAbsolute ---
                "SinglePionECAL",
                "SinglePionHCAL",
                "AbsoluteMPFBias",
                "AbsoluteScale",
                "Fragmentation",
                "PileUpDataMC",
                "RelativeFSR",
                "PileUpPtRef",
                # --- jesUncAbsolute{era} ---
                "AbsoluteStat",
                "TimePtEta",
                "RelativeStatFSR",
                # --- jesUncFlavorQCD ---
                "FlavorQCD",
                # --- jesUncBBEC1 ---
                "PileUpPtEC1",
                "PileUpPtBB",
                "RelativePtBB",
                # --- jesUncBBEC1{era} ---
                "RelativeJEREC1",
                "RelativePtEC1",
                "RelativeStatEC",
                # --- jesUncHF ---
                "RelativePtHF",
                "PileUpPtHF",
                "RelativeJERHF",
                # --- jesUncHF{era} ---
                "RelativeStatHF",
                # --- jesUncEC2 ---
                "PileUpPtEC2",
                # --- jesUncEC2{era} ---
                "RelativeJEREC2",
                "RelativePtEC2",
                # --- jesUncRelativeBal ---
                "RelativeBal",
                # --- jesUncRelativeSample{era} ---
                "RelativeSample",
            ]:
                # two components of jesUnc{name}
                with defaults(name=f"jesUnc{name}"):
                    add_shift(
                        shift_key=["jet_jes_shift",
                                   "jet_jes_sources", "btag_sf_variation"],
                        shift_map={
                            "Up": [1, f'{{"{name}"}}', f"up_jes{name}"],
                            "Down": [-1, f'{{"{name}"}}', f"down_jes{name}"],
                        },
                        scopes="global",
                        producers=[jets.JetEnergyCorrection]
                    )
                    add_shift(
                        shift_key="btag_sf_variation",
                        shift_map={
                            "Up": f"up_jes{name}",
                            "Down": f"down_jes{name}"
                        },
                        scopes=("mt", "et", "tt"),
                        producers=[scalefactors.btagging_SF]
                    )

        elif JES_CONFIG.REGROUPED:  # preferred configuration
            for name, JES_source, *is_yearly in [
                ("Absolute", '{"Regrouped_Absolute"}'),
                ("FlavorQCD", '{"Regrouped_FlavorQCD"}'),
                ("BBEC1", '{"Regrouped_BBEC1"}'),
                ("HF", '{"Regrouped_HF"}'),
                ("EC2", '{"Regrouped_EC2"}'),
                ("RelativeBal", '{"Regrouped_RelativeBal"}'),
                # --- Yearly variations ---
                ("Absolute", f'{{"Regrouped_Absolute_{era}"}}', era),
                ("BBEC1", f'{{"Regrouped_BBEC1_{era}"}}', era),
                ("HF", f'{{"Regrouped_HF_{era}"}}', era),
                ("EC2", f'{{"Regrouped_EC2_{era}"}}', era),
                ("RelativeSample",
                 f'{{"Regrouped_RelativeSample_{era}"}}', era),
            ]:
                with defaults(name=f"jesUnc{name}{era}" if is_yearly else f"jesUnc{name}"):
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_sources"],
                        shift_map={"Up": [1, JES_source],
                                   "Down": [-1, JES_source]},
                        scopes="global",
                        producers=[jets.JetEnergyCorrection],
                    )
                    btag_variation_source = f"{name}_{era}" if is_yearly else name
                    add_shift(
                        shift_key="btag_sf_variation",
                        shift_map={"Up": f"up_jes{btag_variation_source}",
                                   "Down": f"down_jes{btag_variation_source}"},
                        scopes=("mt", "et", "tt"),
                        producers=[scalefactors.btagging_SF]
                    )

    return configuration
