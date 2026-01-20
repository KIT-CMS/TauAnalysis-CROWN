from __future__ import annotations  # needed for type annotations in > python 3.7
from code_generation.configuration import Configuration

# Map internal era names to JERC JSON era names for JERC sources
JERC_ERA_MAP = {
    "2016preVFP":"2016preVFP",
    "2016postVFP":"2016postVFP", 
    "2017":"2017", 
    "2018":"2018",
    "2022preEE": "2022",
    "2022postEE": "2022EE",
    "2023preBPix": "2023",
    "2023postBPix": "2023BPix",
    "2024": "2024",
}

# for btag jes sources look here https://docs.google.com/spreadsheets/d/1Feuj1n0MdotcPq19Mht7SUIgvkXkA4hiB0BxEuBShLw/edit?gid=1345121349#gid=1345121349
# but these slides suggest to use full set for run3 https://indico.cern.ch/event/1476286/contributions/6217358/attachments/2965803/5217826/JERC_run3Uncertainties_2024-11-12.pdf
# also because the btga jes uncertainties are provided only for the full set of sources
            

from .producers import jets as jets
from .producers import scalefactors as scalefactors
from .scripts.CROWNWrapper import (defaults,
                                   get_adjusted_add_shift_SystematicShift)

# taken from here: https://cms-jerc.web.cern.ch/Recommendations/#run-2


def add_jetVariations(configuration: Configuration, era: str) -> Configuration:
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    class JES_CONFIG:
        INDIVIDUAL = True if int(era[:4]) >= 2022 else False # preferred configuration for run3 (as of Oct. 25)
        INDIVIDUAL = False if int(era[:4]) >= 2022 else True  # preferred configuration for run2

    with defaults(exclude_samples=["data", "embedding", "embedding_mc"]):
        if era not in ["2024", "2025"]:
            with defaults(
                scopes=("mt", "et", "tt"),
                shift_key="btag_sf_variation",
                producers=[scalefactors.btagging_SF],
            ):
                add_shift(name="btagUncHF", shift_map={"Up": "up_hf", "Down": "down_hf"})
                add_shift(name="btagUncHFstats1", shift_map={"Up": "up_hfstats1", "Down": "down_hfstats1"})
                add_shift(name="btagUncHFstats2", shift_map={"Up": "up_hfstats2", "Down": "down_hfstats2"})
                add_shift(name="btagUncLF", shift_map={"Up": "up_lf", "Down": "down_lf"})
                add_shift(name="btagUncLFstats1", shift_map={"Up": "up_lfstats1", "Down": "down_lfstats1"})
                add_shift(name="btagUncLFstats2", shift_map={"Up": "up_lfstats2", "Down": "down_lfstats2"})
                add_shift(name="btagUncCFerr1", shift_map={"Up": "up_cferr1", "Down": "down_cferr1"})
                add_shift(name="btagUncCFerr2", shift_map={"Up": "up_cferr2", "Down": "down_cferr2"})
        else:
            with defaults(
                scopes=("mt", "et", "tt"),
                shift_key="btag_sf_variation",
                producers=[scalefactors.btaggingWP_SF],
            ):
                add_shift(name="btagUnc", shift_map={"Up": "up", "Down": "down"})
                add_shift(name="btagUncfsr", shift_map={"Up": "up_fsrdef", "Down": "down_fsrdef"})
                add_shift(name="btagUnchdamp", shift_map={"Up": "up_hdamp", "Down": "down_hdamp"})
                add_shift(name="btagUncisr", shift_map={"Up": "up_isrdef", "Down": "down_isrdef"})
                add_shift(name="btagUncjer", shift_map={"Up": "up_jer", "Down": "down_jer"})
                add_shift(name="btagUncjes", shift_map={"Up": "up_jes", "Down": "down_jes"})
                add_shift(name="btagUncmass", shift_map={"Up": "up_mass", "Down": "down_mass"})
                add_shift(name="btagUncstat", shift_map={"Up": "up_statistic", "Down": "down_statistic"})
                add_shift(name="btagUnctune", shift_map={"Up": "up_tune", "Down": "down_tune"})

        with defaults(scopes="global", producers=[jets.JetEnergyCorrection]):
            add_shift(name="jerUnc", shift_key="jet_jer_shift", shift_map={"Up": '"up"', "Down": '"down"'})
            if era == "2018":  # --- HEM 15/16 issue ---
                add_shift(
                    name="jesUncHEMIssue",
                    shift_key=["jet_jes_shift", "jet_jes_sources"],
                    shift_map={"Up": [1, '{"HEMIssue"}'], "Down": [-1, '{"HEMIssue"}']},
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
                        shift_key=["jet_jes_shift", "jet_jes_sources"],
                        shift_map={"Up": [1, f'{{"{name}"}}'], "Down": [-1, f'{{"{name}"}}']},
                        scopes="global",
                        producers=[jets.JetEnergyCorrection]
                    )
                    add_shift(
                        shift_key="btag_sf_variation",
                        shift_map={"Up": f"up_jes{name}", "Down": f"down_jes{name}"},
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
                ("Absolute", lambda era: f'{{"Regrouped_Absolute_{JERC_ERA_MAP[era]}"}}', era),
                ("BBEC1", lambda era: f'{{"Regrouped_BBEC1_{JERC_ERA_MAP[era]}"}}', era),
                ("HF", lambda era: f'{{"Regrouped_HF_{JERC_ERA_MAP[era]}"}}', era),
                ("EC2", lambda era: f'{{"Regrouped_EC2_{JERC_ERA_MAP[era]}"}}', era),
                ("RelativeSample", lambda era: f'{{"Regrouped_RelativeSample_{JERC_ERA_MAP[era]}"}}', era),
            ]:
                if is_yearly:
                    mapped_era = JERC_ERA_MAP[era]
                    JES_source_val = JES_source(era)
                    name_val = f"jesUnc{name}Year"
                else:
                    JES_source_val = JES_source
                    name_val = f"jesUnc{name}"
                btag_variation_source = name

                with defaults(name=name_val):
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_sources"],
                        shift_map={"Up": [1, JES_source_val], "Down": [-1, JES_source_val]},
                        scopes="global",
                        producers=[jets.JetEnergyCorrection],
                    )
                    add_shift(
                        shift_key="btag_sf_variation",
                        shift_map={"Up": f"up_jes{btag_variation_source}", "Down": f"down_jes{btag_variation_source}"},
                        scopes=("mt", "et", "tt"),
                        producers=[scalefactors.btagging_SF]
                    )

    return configuration
