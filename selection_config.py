"""Selection masks: the analysis event selections, defined once, in CROWN.

Every selection used downstream (TauKITFlow shape production, TauFakeFactors
fake factor and correction measurements) is written to the ntuple as a boolean
branch. Downstream tools then filter on a single branch instead of
re-composing cut strings, which removes the main source of drift between the
three places the same cuts used to be written down.

WHERE THE MASKS ARE PRODUCED -- THE THREE MODES
-----------------------------------------------
The masks come in two groups: **"preselection"** (`presel_mask` and the two
sign flags `sel_os` / `sel_ss`, i.e. what shape production needs, and exactly
the trio that carries systematic shifts) and **"regions"** (the `ff_*` region
masks, i.e. what TauFakeFactors needs). `NTUPLE_MASK_GROUPS` below says which
of the two the MAIN ntuple production carries; `selection_friends.py` books
whatever is left over, so the two paths can neither double-book nor drop a
mask. Together with `APPLY_PRESELECTION_FILTER` this gives three modes:

  1. everything in the main ntuple (the default, and the historical behaviour)::

        NTUPLE_MASK_GROUPS = ("preselection", "regions")
        APPLY_PRESELECTION_FILTER = False

  2. everything as a friend tree, nothing in the ntuple::

        NTUPLE_MASK_GROUPS = ()
        APPLY_PRESELECTION_FILTER = False

  3. the preselection applied as a hard FILTER at ntuple production, the region
     masks as a friend on top of the filtered ntuple::

        NTUPLE_MASK_GROUPS = ("preselection",)
        APPLY_PRESELECTION_FILTER = True

In every mode the union of the main and the friend production is the very same
complete set of mask branches; only the file they end up in changes. Friends
align by entry index, so in mode 3 every friend of an ntuple (xsec, fake
factors, DNN and this selection friend) is produced from the filtered ntuple.

HOW TO READ THIS FILE
---------------------
`add_selection()` is the single entry point. It is called from `config.py` for
the masks inside the main ntuple, and from `selection_friends.py` (with
`friend=True`) for the complementary masks as a friend tree on top of an
existing ntuple, so that the two paths cannot drift apart. It is
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
#: the preselection does not require a re-production. Only available where the
#: "preselection" group is produced, i.e. in the main ntuple.
APPLY_PRESELECTION_FILTER = False

#: Only these masks get shifted copies. The `ff_*` masks are only consumed by
#: TauFakeFactors, which runs on nominal ntuples; giving them a copy per
#: systematic shift would add thousands of unused branches per file.
#:
#: This is at the same time the definition of the "preselection" group: it is
#: exactly `presel_mask` plus the two sign flags, so the group split needs no
#: second list of mask names that could drift away from this one.
MASKS_WITH_SHIFTS = ["presel_mask", "sel_os", "sel_ss"]

#: Which mask groups the MAIN ntuple production carries. The friend production
#: (`selection_friends.py`) automatically books exactly the groups left over,
#: so the two can never double-book or drop a mask. See the module docstring
#: for the three modes this expresses.
NTUPLE_MASK_GROUPS = ("preselection", "regions")

#: The complement, i.e. what `selection_friends.py` produces. Derived, never
#: set by hand.
FRIEND_MASK_GROUPS = tuple(
    group for group in ("preselection", "regions") if group not in NTUPLE_MASK_GROUPS
)


def group_producers(scope: str, groups):
    """Split the tables of `producers/selection.py` into the requested groups.

    The two groups are read off the tables themselves instead of from a second
    list of names: a producer that writes a public branch belongs to
    "preselection" if that branch is one of `MASKS_WITH_SHIFTS` -- `presel_mask`
    and the two sign flags, which are written by flag producers rather than by
    the region table -- and to "regions" otherwise, which leaves exactly the
    `ff_*` masks.

    The atomic `selcut_*` flags are then derived from the `input` lists of the
    booked producers, followed through the flag table until nothing new turns
    up, so that a regions-only production does not compute the preselection
    flags it never reads (and the other way round). The walk deliberately stops
    at a column another group writes: in a split production `sel_os`/`sel_ss`
    are produced by the main ntuple and read back from it, so their producers
    must not be booked a second time in the friend.

    Args:
        scope: the scope to book, e.g. "mt"
        groups: the mask groups to book, a subset of ("preselection", "regions")

    Returns:
        `(public, flags)`: the producers writing an output branch, and the
        atomic flag producers they need, both in the order of the tables.
    """
    masks = list(selection.MASKS.get(scope, []))
    flags = list(selection.FLAGS.get(scope, []))

    group_of = {
        producer: (
            "preselection"
            if producer.output[0].name in MASKS_WITH_SHIFTS
            else "regions"
        )
        for producer in masks + flags
        if producer in masks or producer.output[0].name in MASKS_WITH_SHIFTS
    }
    public = [
        producer for producer in masks + flags if group_of.get(producer) in groups
    ]

    written_by = {
        producer.output[0]: producer for producer in flags if producer not in group_of
    }
    needed, pending = set(), [
        quantity for producer in public for quantity in producer.input[scope]
    ]
    while pending:
        producer = written_by.get(pending.pop())
        if producer is not None and producer not in needed:
            needed.add(producer)
            pending.extend(producer.input[scope])

    return public, [
        producer for producer in flags if producer in needed or producer in public
    ]


def add_selection(
    configuration: Configuration,
    scopes,
    era: str,
    sample: str,
    apply_preselection_filter=None,
    friend=False,
    groups=None,
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
        groups: the mask groups to book, a subset of `("preselection",
            "regions")`. Defaults to `NTUPLE_MASK_GROUPS`, the main ntuple
            share; `selection_friends.py` passes the complement.
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
    if groups is None:
        groups = NTUPLE_MASK_GROUPS
    if apply_preselection_filter and "preselection" not in groups:
        raise ValueError(
            "The preselection filter needs the `preselection` mask group, which "
            f"this production does not carry (booked groups: {tuple(groups)})."
        )
    if not groups:
        return configuration

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

    # driven by the `FLAGS` and `MASKS` tables of `producers/selection.py`,
    # split into the requested groups by `group_producers()` above: a scope gets
    # exactly the masks of the booked groups and exactly the atomic flags those
    # masks read. In a friend production the handful of flag producers that
    # declare their `output_group` only to be ordered after it are swapped for
    # their input-less `*_friend` twins, since in a friend job that group does
    # not run and the column comes from the input ntuple.
    friend_flags = selection.FRIEND_FLAGS if friend else {}
    booked = {scope: group_producers(scope, groups) for scope in selection.MASKS}
    for scope, (public_producers, flag_producers) in booked.items():
        configuration.add_producers(
            [scope],
            [friend_flags.get(producer, producer) for producer in flag_producers],
        )

    #########################
    # The masks and their output branches
    #########################

    # every producer of a booked group writes exactly one public branch: the
    # masks of the region table, plus `sel_os` / `sel_ss`, which belong to the
    # preselection group but are written directly by the charge flag producers
    # and are therefore outputs without being masks.
    for scope, (public_producers, flag_producers) in booked.items():
        configuration.add_producers(
            [scope],
            [
                producer
                for producer in public_producers
                if producer in selection.MASKS[scope]
            ],
        )
        configuration.add_outputs(
            [scope], [producer.output[0] for producer in public_producers]
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
    # A production without the preselection group has no trigger flag producer
    # to replace either.
    if not friend and selection.PreselTriggerFlag_tt in booked["tt"][1]:
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
