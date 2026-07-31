"""Selection masks: the analysis event selections, defined once, in CROWN.

Every selection used downstream (TauKITFlow shape production, TauFakeFactors
fake factor and correction measurements) is written to the ntuple as a boolean
branch. Downstream tools then filter on a single branch instead of
re-composing cut strings, which removes the main source of drift between the
three places the same cuts used to be written down.

HOW TO READ THIS FILE
---------------------
1. `_era_parameters()` collects *everything* that depends on the era (and on
   the scope) in one place: thresholds, working points, trigger flag names and
   the few cases where an era needs a structurally different cut (a closed
   isolation interval instead of a simple upper bound, `>` instead of `>=`).
2. `_mask_composition()` is the literal region table: one line per mask,
   listing exactly the atomic cuts it consists of. This is the definition of
   what each mask means -- if a region changes, change it here.
3. `add_selection()` books the required producers, config parameters and
   outputs generically from those two tables.

WHAT THE MASKS CONTAIN
----------------------
`presel_mask` is the per-channel `preselection:` block of
`TauKITFlow/config/cuts.yaml`. The `ff_*` masks are the *region* cut sets of
`TauFakeFactors/configs/smhtt_ul/{era}/fake_factors_{ch}.yaml` and
`corrections_{ch}.yaml`; they do NOT include the preselection (downstream
applies `presel_mask` separately, exactly as it applies the preselection skim
today) and they do NOT include the `split_categories` (njets/... ) binning or
any category/DNN cut.

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
    """Return the config parameters and producer variants for a scope and era.

    Returns a tuple ``(config_parameters, producer_variants)`` where
    ``producer_variants`` maps a role to the producer that implements it for
    this era, for the few cuts whose *form* (not only threshold) changes.
    """
    is_2024plus = era in RUN3_2024_PLUS

    # ---- charge column types (differ per leg and scope) ---------------------
    # q_1: electron/muon `int` in et/mt/em, tau `Short_t` in tt
    # q_2: tau `Short_t` in et/mt/tt, muon `int` in em
    charge_types = {
        "et": ("int", "Short_t"),
        "mt": ("int", "Short_t"),
        "tt": ("Short_t", "Short_t"),
        "em": ("int", "int"),
    }[scope]

    parameters = {
        "charge_type_1": charge_types[0],
        "charge_type_2": charge_types[1],
    }
    variants = {}

    # ---- preselection -------------------------------------------------------
    if scope in ("et", "mt", "tt"):
        parameters.update(
            {
                # accepted hadronic tau decay modes and the stored column type
                "selection_tau_decaymodes": "0, 1, 10, 11",
                "selection_decaymode_type": "UChar_t",
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

    # ---- fake factor regions (et, mt only) ----------------------------------
    if scope in ("et", "mt"):
        # light lepton isolation. 2022/2023 uses closed intervals, from 2024 on
        # the lower edge was dropped in favour of a plain upper bound.
        parameters["lep_iso_min"] = 0.0
        parameters["lep_iso_max"] = 0.15
        parameters["qcd_lep_iso_min"] = 0.02 if scope == "et" else 0.05
        parameters["qcd_lep_iso_max"] = 0.15
        if is_2024plus:
            variants["lep_iso"] = selection.LepIsoFlag_Upper
            variants["qcd_lep_iso"] = selection.QCDLepIsoFlag_Upper
            variants["qcd_lep_antiiso"] = selection.QCDLepAntiIsoFlag_Lower
        else:
            variants["lep_iso"] = selection.LepIsoFlag_Interval
            variants["qcd_lep_iso"] = selection.QCDLepIsoFlag_Interval
            variants["qcd_lep_antiiso"] = selection.QCDLepAntiIsoFlag_Interval

        # W+jets determination region transverse mass. `mt_1 > 70` only in mt
        # for 2022/2023, `mt_1 >= 70` everywhere else.
        if scope == "mt" and not is_2024plus:
            variants["wjets_mt"] = selection.WjetsMtFlag_Strict
        else:
            variants["wjets_mt"] = selection.WjetsMtFlag_Inclusive

        # ttbar determination region b-tag requirement
        if scope == "mt":
            parameters["ttbar_nbtag_min"] = 0 if is_2024plus else 1
        else:  # et
            parameters["ttbar_nbtag_min"] = 2 if era == "2022preEE" else 0

    # ---- fake factor regions (tt only) --------------------------------------
    if scope == "tt":
        # NOTE / known inconsistency in the upstream configs: the veto set of
        # the *subleading* process fraction regions drops the dilepton veto in
        # 2022preEE, 2023preBPix, 2024, 2025 and 2026, but keeps it in
        # 2022postEE and 2023postBPix. This looks like drift in the yaml files
        # rather than intent; it is reproduced faithfully here so that the
        # masks match the configs bit for bit. Fix upstream first, then here.
        if era in ("2022postEE", "2023postBPix"):
            variants["fraction_sub_veto"] = q.selcut_lepton_veto
        else:
            variants["fraction_sub_veto"] = q.selcut_lepton_veto_nodilep

    return parameters, variants


##############################################################################
# 2. region composition -- WHAT EACH MASK MEANS
##############################################################################


def _mask_composition(scope, variants):
    """Literal table of the atomic cuts making up each mask of a scope."""

    # short aliases, purely to keep the table below readable
    dm1, dm2 = q.selcut_presel_tau_dm_1, q.selcut_presel_tau_dm_2
    vse1, vse2 = q.selcut_presel_vsele_1, q.selcut_presel_vsele_2
    vsm1, vsm2 = q.selcut_presel_vsmu_1, q.selcut_presel_vsmu_2
    pt1, pt2 = q.selcut_presel_pt_1, q.selcut_presel_pt_2
    eta1 = q.selcut_presel_eta_1
    trg = q.selcut_presel_trigger
    jetveto = q.selcut_jet_veto

    veto = q.selcut_lepton_veto  # extraelec && extramuon && dilepton
    veto_inv = q.selcut_lepton_veto_inv  # !(the above)
    os_, ss_ = q.sel_os, q.sel_ss

    iso1, iso2 = q.selcut_tau_iso_1, q.selcut_tau_iso_2  # vsJet Medium > 0.5
    nis1, nis2 = q.selcut_tau_noniso_1, q.selcut_tau_noniso_2  # vsJet Medium < 0.5
    vvl1, vvl2 = q.selcut_tau_vvvloose_1, q.selcut_tau_vvvloose_2

    lep_iso = q.selcut_lep_iso
    qcd_iso = q.selcut_qcd_lep_iso
    qcd_anti = q.selcut_qcd_lep_antiiso

    mt50, mt70 = q.selcut_mt_lt_50, q.selcut_mt_lt_70
    mt0, w_mt = q.selcut_mt_gt_0, q.selcut_wjets_mt
    nb0, nbeq0 = q.selcut_nbtag_ge_0, q.selcut_nbtag_eq_0
    tt_nb = q.selcut_ttbar_nbtag

    if scope == "em":
        return {q.presel_mask: [eta1, pt1, pt2, trg, jetveto]}

    if scope == "tt":
        # veto set of the subleading process fraction regions, see the note in
        # `_era_parameters`
        sub_veto = variants["fraction_sub_veto"]
        return {
            q.presel_mask:              [dm1, dm2, vse1, vse2, vsm1, vsm2, pt1, pt2, trg, jetveto],
            # --- QCD fake factors, leading tau ---
            q.ff_qcd_SRlike:            [iso1, iso2, veto, ss_],
            q.ff_qcd_ARlike:            [vvl1, nis1, iso2, veto, ss_],
            # --- QCD fake factors, subleading tau ---
            q.ff_qcd_sub_SRlike:        [iso1, iso2, veto, ss_],
            q.ff_qcd_sub_ARlike:        [iso1, vvl2, nis2, veto, ss_],
            # --- process fractions ---
            q.ff_fraction_SR:           [iso1, iso2, veto, os_],
            q.ff_fraction_AR:           [vvl1, nis1, nis2, veto, os_],
            q.ff_fraction_sub_SR:       [iso1, iso2, sub_veto, os_],
            q.ff_fraction_sub_AR:       [nis1, vvl2, nis2, sub_veto, os_],
            # --- DR to SR corrections, leading tau ---
            q.ff_qcd_DR_SR_SRlike:      [iso1, nis2, veto, ss_],
            q.ff_qcd_DR_SR_ARlike:      [vvl1, nis1, nis2, veto, ss_],
            q.ff_qcd_AR_SR_SRlike:      [iso1, nis2, veto, os_],
            q.ff_qcd_AR_SR_ARlike:      [vvl1, nis1, nis2, veto, os_],
            # --- DR to SR corrections, subleading tau ---
            q.ff_qcd_sub_DR_SR_SRlike:  [nis1, iso2, veto, ss_],
            q.ff_qcd_sub_DR_SR_ARlike:  [nis1, vvl2, nis2, veto, ss_],
            q.ff_qcd_sub_AR_SR_SRlike:  [nis1, iso2, veto, os_],
            q.ff_qcd_sub_AR_SR_ARlike:  [nis1, vvl2, nis2, veto, os_],
        }

    # --- et and mt -----------------------------------------------------------
    # The W+jets DR-to-SR corrections override the lepton isolation. In et that
    # override is the QCD isolation window, in mt it is identical to the
    # nominal one; this holds for every supported era.
    w_iso = qcd_iso if scope == "et" else lep_iso
    anti = [vvl2, nis2]  # (vsJet VVVLoose > 0.5) && (vsJet Medium < 0.5)

    return {
        q.presel_mask:                 [dm2, vse2, vsm2, pt1, pt2, trg, jetveto],
        # --- QCD fake factors ---
        q.ff_qcd_SRlike:               [iso2, qcd_iso, mt50, nb0, veto, ss_],
        q.ff_qcd_ARlike:      [*anti,  qcd_iso, mt50, nb0, veto, ss_],
        # --- W+jets fake factors (and their same-sign QCD estimation) ---
        q.ff_wjets_SRlike:             [iso2, lep_iso, w_mt, nbeq0, veto, os_],
        q.ff_wjets_ARlike:    [*anti,  lep_iso, w_mt, nbeq0, veto, os_],
        q.ff_wjets_SRlike_ss:          [iso2, lep_iso, w_mt, nbeq0, veto, ss_],
        q.ff_wjets_ARlike_ss: [*anti,  lep_iso, w_mt, nbeq0, veto, ss_],
        # --- ttbar fake factors: SR/AR (MC), SR-like/AR-like (inverted veto) ---
        q.ff_ttbar_SR:                 [iso2, lep_iso, mt70, tt_nb, veto, os_],
        q.ff_ttbar_AR:        [*anti,  lep_iso, mt70, tt_nb, veto, os_],
        q.ff_ttbar_SRlike:             [iso2, lep_iso, mt70, tt_nb, veto_inv, os_],
        q.ff_ttbar_ARlike:    [*anti,  lep_iso, mt70, tt_nb, veto_inv, os_],
        q.ff_ttbar_SRlike_ss:          [iso2, lep_iso, mt70, tt_nb, veto_inv, ss_],
        q.ff_ttbar_ARlike_ss: [*anti,  lep_iso, mt70, tt_nb, veto_inv, ss_],
        # --- process fractions ---
        q.ff_fraction_SR:              [iso2, lep_iso, mt70, nb0, veto, os_],
        q.ff_fraction_AR:     [*anti,  lep_iso, mt70, nb0, veto, os_],
        # --- QCD DR to SR corrections (isolation window inverted) ---
        q.ff_qcd_DR_SR_SRlike:         [iso2, qcd_anti, mt50, nb0, veto, ss_],
        q.ff_qcd_DR_SR_ARlike:[*anti,  qcd_anti, mt50, nb0, veto, ss_],
        q.ff_qcd_AR_SR_SRlike:         [iso2, qcd_anti, mt70, nb0, veto, os_],
        q.ff_qcd_AR_SR_ARlike:[*anti,  qcd_anti, mt70, nb0, veto, os_],
        # --- W+jets DR to SR corrections (and their same-sign variants) ---
        q.ff_wjets_DR_SR_SRlike:          [iso2, w_iso, mt0, nbeq0, veto, os_],
        q.ff_wjets_DR_SR_ARlike: [*anti,  w_iso, mt0, nbeq0, veto, os_],
        q.ff_wjets_DR_SR_SRlike_ss:       [iso2, w_iso, mt0, nbeq0, veto, ss_],
        q.ff_wjets_DR_SR_ARlike_ss:[*anti, w_iso, mt0, nbeq0, veto, ss_],
        q.ff_wjets_AR_SR_SRlike:          [iso2, w_iso, mt70, nb0, veto, os_],
        q.ff_wjets_AR_SR_ARlike: [*anti,  w_iso, mt70, nb0, veto, os_],
        q.ff_wjets_AR_SR_SRlike_ss:       [iso2, w_iso, mt70, nb0, veto, ss_],
        q.ff_wjets_AR_SR_ARlike_ss:[*anti, w_iso, mt70, nb0, veto, ss_],
    }


##############################################################################
# 3. generic booking
##############################################################################


def _atomic_producers(scope, variants):
    """Producers evaluating the atomic cuts needed by the masks of a scope."""
    common = [
        selection.JetVetoMapFlag,
        selection.PreselPt_1,
        selection.PreselPt_2,
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
            selection.LeptonVetoNoDileptonFlag,
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
        selection.MtBelow50Flag,
        selection.MtBelow70Flag,
        selection.MtAboveZeroFlag,
        selection.NBtagGeZeroFlag,
        selection.NBtagEqZeroFlag,
        selection.TTbarNBtagFlag,
        variants["lep_iso"],
        variants["qcd_lep_iso"],
        variants["qcd_lep_antiiso"],
        variants["wjets_mt"],
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
        parameters, variants = _era_parameters(scope, era)
        configuration.add_config_parameters([scope], parameters)
        configuration.add_producers([scope], _atomic_producers(scope, variants))

        masks = _mask_composition(scope, variants)
        mask_producers = [
            selection.make_mask_producer(
                name=mask.name,
                output_quantity=mask,
                flags=flags,
                scopes=[scope],
            )
            for mask, flags in masks.items()
            # sel_os / sel_ss are written directly by the charge producers
            if mask not in (q.sel_os, q.sel_ss)
        ]
        configuration.add_producers([scope], mask_producers)
        configuration.add_outputs([scope], list(masks.keys()) + [q.sel_os, q.sel_ss])

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
        _, variants = _era_parameters(scope, era=configuration.era)
        composition = _mask_composition(scope, variants)

        keep, drop = set(), set()
        # sub-flags that only feed other selcut_* flags and therefore never
        # appear in the composition table itself
        if scope != "em":
            drop.update(
                [
                    q.selcut_no_extraelec,
                    q.selcut_no_extramuon,
                    q.selcut_no_dilepton,
                ]
            )
        for mask, flags in composition.items():
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
