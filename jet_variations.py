from __future__ import annotations  # needed for type annotations in > python 3.7
from code_generation.configuration import Configuration

from .producers import jets as jets
from .producers import scalefactors as scalefactors
from .scripts.CROWNWrapper import (defaults,
                                   get_adjusted_add_shift_SystematicShift)

# Map internal era names to JERC JSON era names for JERC sources
ERA_MAP = {
    "2016preVFP":"2016",
    "2016postVFP":"2016", 
    "2017":"2017", 
    "2018":"2018",
    "2022preEE": "2022",
    "2022postEE": "2022EE",
    "2023preBPix": "2023",
    "2023postBPix": "2023BPix",
    "2024": "2024",
    "2025": "2025",
    "2026": "2026",
}

# for btag jes sources look here https://docs.google.com/spreadsheets/d/1Feuj1n0MdotcPq19Mht7SUIgvkXkA4hiB0BxEuBShLw/edit?gid=1345121349#gid=1345121349
# but these slides suggest to use full set for run3 https://indico.cern.ch/event/1476286/contributions/6217358/attachments/2965803/5217826/JERC_run3Uncertainties_2024-11-12.pdf
# also because the btag jes uncertainties are provided only for the full set of sources


# taken from here: https://cms-jerc.web.cern.ch/Recommendations/#run-2

def add_jetVariations(configuration: Configuration, era: str) -> Configuration:
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)
    era_tag = ERA_MAP[era]

    class JES_CONFIG:
        # no regrouped btag variations for 2022 and 2023, for 2024 it's a different scheme in any case
        # regrouped jes are available for all eras
        # Run 3 (>=2022) uses the JERC-recommended reduced/regrouped JES source
        # scheme ("preferred configuration" below); legacy Run 2 (<2022) keeps
        # the full individual JES source breakdown.
        REGROUPED = True if int(era[:4])>=2022 else False
        jet_pt_correction_producer = jets.JetEnergyCorrection_v12 if int(era[:4])<2022 else jets.JetEnergyCorrection

    with defaults(exclude_samples=["data", "embedding", "embedding_mc"]):
        if int(era[:4]) < 2022:
            with defaults(
                scopes=("mt", "et", "tt"),
                shift_key="btag_sf_variation",
                producers=[scalefactors.btagging_SF],
            ):
                add_shift(name="CMS_btag_fullShape_hf", shift_map={"Up": "up_hf", "Down": "down_hf"})
                add_shift(name=f"CMS_btag_fullShape_hfstats1_{era_tag}", shift_map={"Up": "up_hfstats1", "Down": "down_hfstats1"})
                add_shift(name=f"CMS_btag_fullShape_hfstats2_{era_tag}", shift_map={"Up": "up_hfstats2", "Down": "down_hfstats2"})
                add_shift(name="CMS_btag_fullShape_lf", shift_map={"Up": "up_lf", "Down": "down_lf"})
                add_shift(name=f"CMS_btag_fullShape_lfstats1_{era_tag}", shift_map={"Up": "up_lfstats1", "Down": "down_lfstats1"})
                add_shift(name=f"CMS_btag_fullShape_lfstats2_{era_tag}", shift_map={"Up": "up_lfstats2", "Down": "down_lfstats2"})
                add_shift(name="CMS_btag_fullShape_cferr1", shift_map={"Up": "up_cferr1", "Down": "down_cferr1"})
                add_shift(name="CMS_btag_fullShape_cferr2", shift_map={"Up": "up_cferr2", "Down": "down_cferr2"})
        else:
            with defaults(
                scopes=("mt", "et", "tt"),
                shift_key="btag_sf_variation",
                producers=[scalefactors.btaggingWP_SF],
            ):
                add_shift(name="CMS_btag_fixedWP_bc_correlated", shift_map={"Up": "up_correlated", "Down": "down_correlated"})
                add_shift(name=f"CMS_btag_fixedWP_bc_uncorrelated_{era_tag}", shift_map={"Up_uncorrelated": "up", "Down": "down_uncorrelated"})
                add_shift(name="CMS_btag_fixedWP_light_correlated", shift_map={"Up": "up_correlated", "Down": "down_correlated"})
                add_shift(name=f"CMS_btag_fixedWP_light_uncorrelated_{era_tag}", shift_map={"Up_uncorrelated": "up", "Down": "down_uncorrelated"})

        with defaults(scopes="global", producers=[JES_CONFIG.jet_pt_correction_producer]):
            add_shift(name=f"CMS_res_j_{era_tag}", shift_key="jet_jer_shift", shift_map={"Up": "up", "Down": "down"})
            if era == "2018":  # --- HEM 15/16 issue ---
                add_shift(
                    name="CMS_scale_j_HEMIssue_2018",
                    shift_key=["jet_jes_shift", "jet_jes_source"],
                    shift_map={"Up": [1, "HEMIssue"], "Down": [-1, "HEMIssue"]},
                )

        with defaults(name="CMS_scale_j_Total"):  # two components of CMS_scale_j_Total
            add_shift(
                shift_key=["jet_jes_shift", "jet_jes_source"],
                shift_map={"Up": [1, "Total"], "Down": [-1, "Total"]},
                scopes="global",
                producers=[JES_CONFIG.jet_pt_correction_producer]
            )
            if int(era[:4]) < 2022:
                add_shift(
                    shift_key="btag_sf_variation",
                    shift_map={"Up": "up_jes", "Down": "down_jes"},
                    scopes=("mt", "et", "tt"),
                    producers=[scalefactors.btagging_SF]
                )

        if not JES_CONFIG.REGROUPED:
            for name in [
                # --- CMS_scale_j_Absolute ---
                "SinglePionECAL",
                "SinglePionHCAL",
                "AbsoluteMPFBias",
                "AbsoluteScale",
                "Fragmentation",
                "PileUpDataMC",
                "RelativeFSR",
                "PileUpPtRef",
                # --- CMS_scale_j_Absolute_{era} ---
                "AbsoluteStat",
                "TimePtEta",
                "RelativeStatFSR",
                # --- CMS_scale_j_FlavorQCD ---
                "FlavorQCD",
                # --- CMS_scale_j_BBEC1 ---
                "PileUpPtEC1",
                "PileUpPtBB",
                "RelativePtBB",
                # --- CMS_scale_j_BBEC1_{era} ---
                "RelativeJEREC1",
                "RelativePtEC1",
                "RelativeStatEC",
                # --- CMS_scale_j_HF ---
                "RelativePtHF",
                "PileUpPtHF",
                "RelativeJERHF",
                # --- CMS_scale_j_HF_{era} ---
                "RelativeStatHF",
                # --- CMS_scale_j_EC2 ---
                "PileUpPtEC2",
                # --- CMS_scale_j_EC2_{era} ---
                "RelativeJEREC2",
                "RelativePtEC2",
                # --- CMS_scale_j_RelativeBal ---
                "RelativeBal",
                # --- CMS_scale_j_RelativeSample_{era} ---
                "RelativeSample",
            ]:
                # two components of CMS_scale_j_{name}
                with defaults(name=f"CMS_scale_j_{name}"):
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_source"],
                        shift_map={"Up": [1, name], "Down": [-1, name]},
                        scopes="global",
                        producers=[JES_CONFIG.jet_pt_correction_producer]
                    )
                    if int(era[:4]) < 2022:
                        add_shift(
                            shift_key="btag_sf_variation",
                            shift_map={"Up": f"up_jes{name}", "Down": f"down_jes{name}"},
                            scopes=("mt", "et", "tt"),
                            producers=[scalefactors.btagging_SF]
                        )

        else:  # preferred configuration
            for name, JES_source, *is_yearly in [
                ("Absolute", "Regrouped_Absolute"),
                ("FlavorQCD", "Regrouped_FlavorQCD"),
                ("BBEC1", "Regrouped_BBEC1"),
                ("HF", "Regrouped_HF"),
                ("EC2", "Regrouped_EC2"),
                ("RelativeBal", "Regrouped_RelativeBal"),
                # --- Yearly variations ---
                ("Absolute", lambda era: f"Regrouped_Absolute_{ERA_MAP[era]}", era),
                ("BBEC1", lambda era: f"Regrouped_BBEC1_{ERA_MAP[era]}", era),
                ("HF", lambda era: f"Regrouped_HF_{ERA_MAP[era]}", era),
                ("EC2", lambda era: f"Regrouped_EC2_{ERA_MAP[era]}", era),
                ("RelativeSample", lambda era: f"Regrouped_RelativeSample_{ERA_MAP[era]}", era),
            ]:
                with defaults(name=f"CMS_scale_j_{name}_{era_tag}" if is_yearly else f"CMS_scale_j_{name}"):
                    JES_source_val = JES_source(era) if is_yearly else JES_source
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_source"],
                        shift_map={"Up": [1, JES_source_val], "Down": [-1, JES_source_val]},
                        scopes="global",
                        producers=[JES_CONFIG.jet_pt_correction_producer],
                    )

                    if int(era[:4]) < 2022:
                        btag_variation_source = f"{name}_{era}" if is_yearly else name
                        add_shift(
                            shift_key="btag_sf_variation",
                            shift_map={"Up": f"up_jes{btag_variation_source}", "Down": f"down_jes{btag_variation_source}"},
                            scopes=("mt", "et", "tt"),
                            producers=[scalefactors.btagging_SF]
                        )

    return configuration
