# hadronic tau decay modes the analysis accepts
# the selection masks cut on the very same list
TAU_DECAY_MODES = "0,1,10,11"

RUN2_ERAS = ["2016preVFP", "2016postVFP", "2017", "2018"]

# sample types with the Z pT reweighting (Run 3 shifts included in the weight, see producers/weights.py)
ZPT_SAMPLES = ["dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "electroweak_boson"]

# signal sample types with the ggH NNLOPS reweighting (applied to the ggH family events)
GGH_SAMPLES = ["ggh_htautau", "rem_htautau", "rem_higgs"]

# signal sample types with HTXS information and the LHEScaleWeight variations of the STXS scheme
STXS_SAMPLES = ["ggh_htautau", "vbf_htautau", "rem_htautau", "rem_higgs"]

# per-era luminosity in pb^-1; "2025" is 2025+2026 data combined
LUMI_PB = {
    "2016preVFP": 19500.0, "2016postVFP": 16800.0, "2017": 41500.0, "2018": 59830.0,
    "2022preEE": 8086.069205, "2022postEE": 26674.924045,
    "2023preBPix": 17964.217998, "2023postBPix": 9676.737966,
    "2024": 109816.515335, "2025": 135047.093128, "2026": 25148.977841,
}
# share of the Summer24 MC kept for 2024 (event.EraSplitFlag), the rest goes to 2025, whose lumi includes 2026;
# the split weight is 1 / the measured generator-weight fraction of each part (norm table split_fraction), else 1 / the lumi share
MC_SPLIT_FRACTION = LUMI_PB["2024"] / (LUMI_PB["2024"] + LUMI_PB["2025"])
MC_SPLIT_FRACTION_26ONLY = (LUMI_PB["2024"] + LUMI_PB["2025"] - LUMI_PB["2026"]) / (LUMI_PB["2024"] + LUMI_PB["2025"])
ERA_SPLIT_FRACTION = {"2024": MC_SPLIT_FRACTION, "2025": 1 - MC_SPLIT_FRACTION, "2026": MC_SPLIT_FRACTION_26ONLY}
ERA_SPLIT_VALUES = {"2024": {"min": 0.0, "max": MC_SPLIT_FRACTION}, "2025": {"min": MC_SPLIT_FRACTION, "max": 1.0}, "2026": {"min": MC_SPLIT_FRACTION_26ONLY, "max": 1.0}}