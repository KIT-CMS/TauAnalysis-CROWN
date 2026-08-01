"""Selection masks: the analysis event selections, defined once, in CROWN.

Every selection used downstream (TauKITFlow shape production, TauFakeFactors
fake factor and correction measurements) is written to the ntuple as a boolean
branch. Downstream tools then filter on a single branch instead of
re-composing cut strings, which removes the main source of drift between the
three places the same cuts used to be written down.

HOW TO READ THIS FILE
---------------------
`add_selection()` is the single entry point. It is called from `config.py` for
the masks inside the main ntuple, and from `selection_friends.py` (with
`friend=True`) for the very same masks as a friend tree on top of an existing
ntuple, so that the two paths cannot drift apart. It is
written in the same idiom as `config.py` itself: literal
`configuration.add_config_parameters([...scopes...], {...})` and
`add_producers([...scopes...], [...])` blocks under banner comments, with
`EraModifier` for the (few) era dependent values. Which eras and scopes are
built is decided by `config.py`, not re-validated here.

The literal region table -- one `Producer` per mask, one flag per line, listing
exactly the atomic cuts it consists of -- is NOT here: it is at the bottom of
`producers/selection.py`, together with the `FLAGS` and `MASKS` mappings that
say which flags and which masks each scope gets. **If you want to know or change
what a mask means, look there.** The masks of a scope come from that mapping
alone, so a scope with no entry in it (ee, mm) simply gets no masks.

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
from code_generation.modifiers import EraModifier
from code_generation.rules import AppendProducer, ReplaceProducer

from .producers import selection as selection
from .quantities import output as q
from .tau_triggersetup import DOUBLETAU_HPS_ERAS, DOUBLETAU_TRIGGER_FLAG

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


def add_selection(
    configuration: Configuration,
    scopes,
    era: str,
    sample: str,
    apply_preselection_filter=None,
    friend=False,
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
        friend: if True, book the masks for a friend tree production on an
            existing CROWN ntuple (`selection_friends.py`) instead of for the
            main ntuple. Everything -- parameters, regions, output branches --
            is the same; only the flag producers that read a column out of an
            `output_group` are swapped for their input-less twins, and the
            producer rules that would reorder the producers are skipped. The
            main production path never passes this.

    Returns:
        The configuration, with the selection masks added.
    """
    if apply_preselection_filter is None:
        apply_preselection_filter = APPLY_PRESELECTION_FILTER

    ###########################
    ####### Parameters ########
    ###########################

    # tau vs jet working points of the fake factor regions. Era independent,
    # see the module docstring: the isolated leg is `id_tau_vsJet_Medium_*`,
    # the anti-isolated one `id_tau_vsJet_VVVLoose_*`.
    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "ff_tau_iso_vsjet_wp": "Medium",
            "ff_tau_antiiso_vsjet_wp": "VVVLoose",
        },
    )

    # light lepton isolation of the fake factor regions, era independent as
    # well: the single threshold `iso_1 < 0.15` (and its complement
    # `iso_1 >= 0.15`, used by the QCD DR-to-SR / AR-to-SR corrections) is
    # shared by every region of et and mt
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "lep_iso_max": 0.15,
        },
    )

    # preselection thresholds, tau ID working points and trigger flag names
    configuration.add_config_parameters(
        ["et"],
        {
            "presel_vsele_wp": "Tight",
            "presel_vsmu_wp": "VLoose_Tight",
            "presel_pt_1": 32.0,  # electron pt
            "presel_pt_2": 20.0,  # tau pt
            "presel_trigger_flag": "trg_single_ele30",
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "presel_vsele_wp": "VVLoose",
            "presel_vsmu_wp": "Tight_VVLoose",
            "presel_pt_1": 26.0,  # muon pt
            "presel_pt_2": 20.0,  # tau pt
            "presel_trigger_flag": "trg_single_mu24",
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "presel_vsele_wp": "VVLoose",
            "presel_vsmu_wp": "VLoose_VVLoose",
            # the only era dependence of the whole selection: the double tau
            # trigger changed from the HPS to the PNet path in 2024, together
            # with the offline tau pt threshold (40 -> 35 GeV). The flag name is
            # the very one the tt pair is triggered on, so it is taken straight
            # from the trigger setup instead of being spelled out again.
            "presel_pt_1": EraModifier(
                {hps_era: 40.0 for hps_era in DOUBLETAU_HPS_ERAS},
                default=35.0,  # 2024, 2025, 2026
            ),
            "presel_pt_2": EraModifier(
                {hps_era: 40.0 for hps_era in DOUBLETAU_HPS_ERAS},
                default=35.0,  # 2024, 2025, 2026
            ),
            "presel_trigger_flag": DOUBLETAU_TRIGGER_FLAG,
        },
    )
    configuration.add_config_parameters(
        ["em"],
        {
            "presel_abs_eta_1": 2.5,  # electron eta
            "presel_pt_1": 25.0,  # electron pt
            "presel_pt_2": 26.0,  # muon pt
            "presel_trigger_flag": "trg_single_mu24",
        },
    )

    #########################
    # Producers of the atomic cuts
    #########################

    # driven by the `FLAGS` table of `producers/selection.py`, the same way the
    # masks below are driven by `MASKS`. In a friend production the handful of
    # flag producers that declare their `output_group` only to be ordered after
    # it are swapped for their input-less `*_friend` twins, since in a friend job
    # that group does not run and the column comes from the input ntuple.
    friend_flags = selection.FRIEND_FLAGS if friend else {}
    for scope, flag_producers in selection.FLAGS.items():
        configuration.add_producers(
            [scope],
            [friend_flags.get(producer, producer) for producer in flag_producers],
        )

    #########################
    # The masks and their output branches
    #########################

    # driven entirely by the `MASKS` table of `producers/selection.py`: every
    # mask producer writes exactly one public branch, and a scope gets the masks
    # listed for it there and nothing else. `sel_os` / `sel_ss` are written
    # directly by the charge producers, so they are outputs without being masks.
    for scope, mask_producers in selection.MASKS.items():
        configuration.add_producers([scope], list(mask_producers))
        configuration.add_outputs(
            [scope],
            [producer.output[0] for producer in mask_producers] + [q.sel_os, q.sel_ss],
        )

    ################################
    ######### Modifications ########
    ################################

    # tt embedding samples read the double tau trigger flags from a different
    # `output_group`, so the trigger flag producer has to follow that one. A
    # friend production has no trigger group to follow and already uses the
    # input-less twin for every sample, so it needs no rule -- and must not get
    # one, because a rule appends the replacement at the end of the producer
    # list, and a friend production runs the producers in exactly that order.
    if not friend:
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

    # the opt-in hard filter on the preselection
    if apply_preselection_filter:
        configuration.add_modification_rule(
            list(selection.MASKS),
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
    for scope in scopes:
        if scope not in selection.MASKS:
            continue
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
