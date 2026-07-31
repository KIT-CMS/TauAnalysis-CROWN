"""Selection masks: the analysis event selections, defined once, in CROWN.

Every selection used downstream (TauKITFlow shape production, TauFakeFactors
fake factor and correction measurements) is written to the ntuple as a boolean
branch. Downstream tools then filter on a single branch instead of
re-composing cut strings, which removes the main source of drift between the
three places the same cuts used to be written down.

HOW TO READ THIS FILE
---------------------
1. `_era_parameters()` collects *everything* that depends on the era (and on
   the scope) in one place: thresholds, working points and trigger flag names.
   Only the *preselection* is era dependent at all -- see below.
2. `add_selection()` books the producers, config parameters and outputs of
   each scope.

The literal region table -- one `Producer` per mask, one line per region,
listing exactly the atomic cuts it consists of -- is NOT here: it is at the
bottom of `producers/selection.py` (`LT_MASKS`, `TT_MASKS`, `EM_MASKS`).
**If you want to know or change what a mask means, look there.**

WHAT THE MASKS CONTAIN
----------------------
`presel_mask` is the per-channel `preselection:` block of
`TauKITFlow/config/cuts.yaml`. The `ff_*` masks are the *region* cut sets of
`TauFakeFactors/configs/smhtt_ul/{era}/fake_factors_{ch}.yaml` and
`corrections_{ch}.yaml`; they do NOT include the preselection (downstream
applies `presel_mask` separately, exactly as it applies the preselection skim
today) and they do NOT include the `split_categories` (njets/... ) binning or
any category/DNN cut.

WHICH TauFakeFactors CONFIGS THE `ff_*` MASKS COME FROM
-------------------------------------------------------
TauFakeFactors measures the fake factors on the pre- and post-halves of a year
*together* and therefore reads ONE config per year, from the combined `2022/`
and `2023/` directories. The per-half directories (`2022preEE/`, `2022postEE/`,
`2023preBPix/`, `2023postBPix/`) are stale and unused; do not take cut values
from them.

The combined `2022/` and `2023/` configs and the `2024/`, `2025/` and `2026/`
ones are IDENTICAL in every region cut, so:

    THE FAKE FACTOR REGION MASKS ARE COMPLETELY ERA INDEPENDENT.

The only era dependence left in this file is in the preselection: the tt double
tau trigger path changed from the HPS to the PNet one in 2024, together with
the offline tau pt threshold (40 -> 35 GeV).

Naming conventions:
  `_ss`        same-sign variant, i.e. the region with `tau_pair_sign` flipped
               to `(q_1*q_2) > 0`. These correspond to the in-code QCD
               estimation overrides in `FF_Wjets.py` and `FF_ttbar.py`.
  `DR_SR_*`    the region after merging the `DR_SR` `SRlike_cuts`/`ARlike_cuts`
               overrides of `corrections_{ch}.yaml` (`modify_config`,
               `to_AR_SR=False`).
  `AR_SR_*`    the same but with the `AR_SR_cuts` block applied on top of both
               the SR-like and the AR-like variant (`to_AR_SR=True`).
  `_sub`       the subleading-tau variant of a tt region.

The masks encode the `nbtag` cuts exactly as written in the yaml files, even
though the current TauFakeFactors `apply_region_filters` silently skips them.
This is a deliberate, signed-off difference; see the validation notes of the
selection-mask work.

TWO YAML CUTS ARE INTENTIONALLY OMITTED
---------------------------------------
`nbtag: (nbtag >= 0)` (the QCD, process fraction and `AR_SR` regions) and
`lep_mt: (mt_1 > 0)` (the W+jets `DR_SR` regions) are NOT part of any mask.
Both are unconditionally true -- `nbtag` is a jet multiplicity and `mt_1` a
transverse mass, so neither can ever be negative -- and dropping them leaves
every mask semantically identical while saving two columns per event. A
cut-by-cut diff of the masks against the yaml files will show these two as
missing; that is expected and is the only such difference.
"""

from code_generation.configuration import Configuration
from code_generation.rules import AppendProducer, ReplaceProducer

from .producers import selection as selection
from .quantities import output as q
from .tau_triggersetup import DOUBLETAU_HPS_ERAS

##############################################################################
# module level switches
##############################################################################

#: If True, events failing `presel_mask` are dropped from the ntuple instead of
#: only being flagged. Off by default: keeping every event means a change of
#: the preselection does not require a re-production.
APPLY_PRESELECTION_FILTER = False

#: Only these masks get shifted copies. The `ff_*` masks are only consumed by
#: TauFakeFactors, which runs on nominal ntuples; giving them a copy per
#: systematic shift would add thousands of unused branches per file.
MASKS_WITH_SHIFTS = ["presel_mask", "sel_os", "sel_ss"]

#: Masks are only defined for the Run 3 eras; the Run 2 configurations use the
#: `nanoAODv9` producer variants, for which the selection has never been
#: written down in the form used here.
SUPPORTED_ERAS = list(DOUBLETAU_HPS_ERAS) + ["2024", "2025", "2026"]

#: Eras from which the 2024+ selection variants apply.
RUN3_2024_PLUS = ["2024", "2025", "2026"]

SUPPORTED_SCOPES = ["et", "mt", "tt", "em"]


##############################################################################
# 1. era (and scope) dependent parameters -- CHANGE CUT VALUES HERE
##############################################################################


def _era_parameters(scope, era):
    """Return the config parameters for a scope and era.

    Only the preselection is era dependent (the tt double tau trigger and its
    pt threshold changed in 2024); the fake factor regions are not.
    """
    is_2024plus = era in RUN3_2024_PLUS

    parameters = {}

    # ---- preselection -------------------------------------------------------
    if scope in ("et", "mt", "tt"):
        parameters.update(
            {
                # Stored column type of the hadronic tau decay mode. It is
                # `int`, NOT the `UChar_t` of the nanoAOD branch:
                # `event::quantity::Get<T>` casts `UChar_t` and `Short_t`
                # results to `int` (see include/event.hxx), so the template
                # argument of `Get` is the type of the *input branch* while
                # the column it writes is `int`. The accepted modes themselves
                # come from the `tau_dms` config parameter, shared with the
                # object level decay mode cut.
                "selection_decaymode_type": "int",
                # tau vs jet working points used by the fake factor regions
                "ff_tau_iso_wp": "Medium",
                "ff_tau_antiiso_wp": "VVVLoose",
            }
        )

    if scope == "et":
        parameters.update(
            {
                "presel_vsele_wp": "Tight",
                "presel_vsmu_wp": "VLoose_Tight",
                "presel_pt_1": 32.0,  # electron pt
                "presel_pt_2": 20.0,  # tau pt
                "presel_trigger_flag": "trg_single_ele30",
            }
        )
    elif scope == "mt":
        parameters.update(
            {
                "presel_vsele_wp": "VVLoose",
                "presel_vsmu_wp": "Tight_VVLoose",
                "presel_pt_1": 26.0,  # muon pt
                "presel_pt_2": 20.0,  # tau pt
                "presel_trigger_flag": "trg_single_mu24",
            }
        )
    elif scope == "tt":
        # the double tau trigger changed from the HPS to the PNet path in 2024,
        # together with the offline pt threshold (40 -> 35 GeV)
        tau_pt = 35.0 if is_2024plus else 40.0
        parameters.update(
            {
                "presel_vsele_wp": "VVLoose",
                "presel_vsmu_wp": "VLoose_VVLoose",
                "presel_pt_1": tau_pt,
                "presel_pt_2": tau_pt,
                "presel_trigger_flag": (
                    "trg_double_tau30_mediumiso_pnet"
                    if is_2024plus
                    else "trg_double_tau35_mediumiso_hps"
                ),
            }
        )
    elif scope == "em":
        parameters.update(
            {
                "presel_abs_eta_1": 2.5,  # electron eta
                "presel_pt_1": 25.0,  # electron pt
                "presel_pt_2": 26.0,  # muon pt
                "presel_trigger_flag": "trg_single_mu24",
            }
        )

    # ---- fake factor regions -----------------------------------------------
    # Era independent, see the module docstring. The single light lepton
    # isolation threshold `iso_1 < 0.15` (and its complement `iso_1 >= 0.15`,
    # used by the QCD DR-to-SR / AR-to-SR corrections) is shared by every
    # region of et and mt.
    if scope in ("et", "mt"):
        parameters["lep_iso_max"] = 0.15

    return parameters


##############################################################################
# 2. booking
##############################################################################


def _atomic_producers(scope):
    """Producers evaluating the atomic cuts needed by the masks of a scope."""
    common = [
        selection.JetVetoMapFlag,
        selection.PreselPt_1,
        selection.PreselPt_2,
        # `q_1 * q_2`, the shared input of both sign flags
        selection.ChargeProduct,
        selection.OppositeSignFlag,
        selection.SameSignFlag,
    ]

    if scope == "em":
        return common + [selection.PreselElectronEta_1, selection.PreselTriggerFlag]

    vetoes = [
        selection.NoExtraElectronFlag,
        selection.NoExtraMuonFlag,
        selection.NoDileptonFlag,
        selection.LeptonVetoFlag,
    ]

    if scope == "tt":
        return common + vetoes + [
            selection.PreselTriggerFlag_tt,
            selection.PreselTauDecayMode_1,
            selection.PreselTauDecayMode_2,
            selection.PreselVsEleTauID_1,
            selection.PreselVsEleTauID_2,
            selection.PreselVsMuTauID_1,
            selection.PreselVsMuTauID_2,
            selection.TauIsoFlag_1,
            selection.TauIsoFlag_2,
            selection.TauNonIsoFlag_1,
            selection.TauNonIsoFlag_2,
            selection.TauVVVLooseFlag_1,
            selection.TauVVVLooseFlag_2,
        ]

    # et and mt
    return common + vetoes + [
        selection.LeptonVetoInvertedFlag,
        selection.PreselTriggerFlag,
        selection.PreselTauDecayMode_2,
        selection.PreselVsEleTauID_2,
        selection.PreselVsMuTauID_2,
        selection.TauIsoFlag_2,
        selection.TauNonIsoFlag_2,
        selection.TauVVVLooseFlag_2,
        selection.MtBelow70Flag,
        selection.WjetsMtFlag,
        selection.NBtagEqZeroFlag,
        selection.TTbarNBtagFlag,
        selection.LepIsoFlag,
        selection.LepAntiIsoFlag,
    ]


def add_selection(
    configuration: Configuration,
    scopes,
    era: str,
    sample: str,
    apply_preselection_filter=None,
) -> Configuration:
    """Book the selection mask producers, parameters and outputs.

    Args:
        configuration: the configuration being built
        scopes: the scopes selected for this production
        era: the era being produced
        sample: the sample group being produced
        apply_preselection_filter: if True, additionally drop every event that
            fails `presel_mask`. Defaults to the module constant
            `APPLY_PRESELECTION_FILTER`.

    Returns:
        The configuration, with the selection masks added.
    """
    if apply_preselection_filter is None:
        apply_preselection_filter = APPLY_PRESELECTION_FILTER

    if era not in SUPPORTED_ERAS:
        return configuration

    selected = [scope for scope in scopes if scope in SUPPORTED_SCOPES]
    if not selected:
        return configuration

    for scope in selected:
        parameters = _era_parameters(scope, era)
        configuration.add_config_parameters([scope], parameters)
        configuration.add_producers([scope], _atomic_producers(scope))

        # the region table lives in `producers/selection.py`; every mask
        # producer writes exactly one public branch. `sel_os` / `sel_ss` are
        # written directly by the charge producers, so they are outputs
        # without being masks.
        mask_producers = selection.MASKS[scope]
        configuration.add_producers([scope], list(mask_producers))
        configuration.add_outputs(
            [scope],
            [producer.output[0] for producer in mask_producers] + [q.sel_os, q.sel_ss],
        )

    # tt embedding samples use a different double tau trigger producer, so the
    # trigger flag producer has to follow a different `output_group`
    if "tt" in selected:
        configuration.add_modification_rule(
            "tt",
            ReplaceProducer(
                producers=[
                    selection.PreselTriggerFlag_tt,
                    selection.PreselTriggerFlag_tt_embedding,
                ],
                samples=["embedding"],
            ),
        )

    if apply_preselection_filter:
        configuration.add_modification_rule(
            selected,
            AppendProducer(
                producers=[selection.PreselectionFilter],
                # the filter applies to every sample; a ProducerRule insists on
                # an explicit sample list, so pass all of them
                samples=list(configuration.available_sample_types),
            ),
        )

    return configuration


def restrict_selection_shifts(configuration: Configuration, scopes) -> Configuration:
    """Drop the systematic copies of the masks that are only used on nominal.

    Must be called *after* the systematic shifts have been added, because
    shifts propagate from the shifted inputs (tau energy scale, MET, jets, ...)
    down to every mask at `add_shift` time.

    Only `MASKS_WITH_SHIFTS` keep their shifted copies; without this, each of
    the ~26 fake factor masks of et/mt would be duplicated once per systematic
    variation, adding thousands of branches that no consumer reads. The
    internal `selcut_*` flags that feed exclusively into those masks are
    trimmed as well, so that no unused shifted column is computed at all.

    `Quantity.get_shifts` does not consult `ignored_shifts`, so the already
    collected shifts have to be dropped explicitly; `ignore_shift` is called in
    addition to keep any later propagation from re-adding them.
    """
    if configuration.era not in SUPPORTED_ERAS:
        return configuration

    for scope in [s for s in scopes if s in SUPPORTED_SCOPES]:
        keep, drop = set(), set()
        # sub-flags that only feed other selcut_* flags and therefore never
        # appear in the region table itself
        if scope != "em":
            drop.update(
                [
                    q.selcut_no_extraelec,
                    q.selcut_no_extramuon,
                    q.selcut_no_dilepton,
                ]
            )
        for producer in selection.MASKS[scope]:
            mask, flags = producer.output[0], producer.input[scope]
            if mask.name in MASKS_WITH_SHIFTS:
                keep.update(flags)
            else:
                drop.add(mask)
                drop.update(flags)
        drop = {
            quantity
            for quantity in drop
            if quantity not in keep and quantity.name not in MASKS_WITH_SHIFTS
        }

        for quantity in drop:
            for shift in list(quantity.shifts.get(scope, set())):
                quantity.ignore_shift(shift, scope)
            quantity.shifts[scope] = set()

    return configuration
