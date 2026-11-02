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
