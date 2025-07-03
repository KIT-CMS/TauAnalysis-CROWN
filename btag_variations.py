from code_generation.configuration import Configuration

from .producers import scalefactors as scalefactors
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


def add_btagVariations(configuration: Configuration) -> None:  # adding btagging shape uncertainties
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)  # shift_config=(scopes: {shift_key: shift_map[direction]})
    with defaults(
        scopes=("mt", "et", "tt"),
        shift_key="btag_sf_variation",
        exclude_samples=["data", "embedding", "embedding_mc"],
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

    return configuration
