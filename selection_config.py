from code_generation.configuration import Configuration
from code_generation.rules import AppendProducer, ReplaceProducer

from .producers import selection as selection
from .quantities import output as q
from .tau_triggersetup import DOUBLETAU_TRIGGER_FLAG

##############################################################################
# module level switches
##############################################################################

# If True, events failing `presel_mask` are dropped from the ntuple instead of only being flagged
APPLY_PRESELECTION_FILTER = False

# Which mask groups the ntuple production carries
NTUPLE_MASK_GROUPS = ("preselection", "regions")

# The complement, i.e. what `selection_friends.py` produces
FRIEND_MASK_GROUPS = tuple(
    group for group in ("preselection", "regions") if group not in NTUPLE_MASK_GROUPS
)

NOMINAL_ONLY_QUANTITIES = (
    # the atomic flags of the regions
    q.selcut_no_extraelec,
    q.selcut_no_extramuon,
    q.selcut_no_dilepton,
    q.selcut_lepton_veto,
    q.selcut_lepton_veto_inv,
    q.selcut_tau_iso_1,
    q.selcut_tau_iso_2,
    q.selcut_tau_noniso_1,
    q.selcut_tau_noniso_2,
    q.selcut_tau_vvvloose_1,
    q.selcut_tau_vvvloose_2,
    q.selcut_lep_iso,
    q.selcut_lep_antiiso,
    q.selcut_mt_lt_70,
    q.selcut_wjets_mt,
    q.selcut_nbtag_eq_0,
    q.selcut_ttbar_nbtag,
    q.selcut_q_prod,
    q.selcut_os,
    q.selcut_ss,
    # the region masks themselves
    q.ff_qcd_SRlike,
    q.ff_qcd_ARlike,
    q.ff_qcd_sub_SRlike,
    q.ff_qcd_sub_ARlike,
    q.ff_wjets_SRlike,
    q.ff_wjets_ARlike,
    q.ff_wjets_SRlike_ss,
    q.ff_wjets_ARlike_ss,
    q.ff_ttbar_SR,
    q.ff_ttbar_AR,
    q.ff_ttbar_SRlike,
    q.ff_ttbar_ARlike,
    q.ff_ttbar_SRlike_ss,
    q.ff_ttbar_ARlike_ss,
    q.ff_fraction_SR,
    q.ff_fraction_AR,
    q.ff_fraction_sub_SR,
    q.ff_fraction_sub_AR,
    q.ff_qcd_DR_SR_SRlike,
    q.ff_qcd_DR_SR_ARlike,
    q.ff_qcd_AR_SR_SRlike,
    q.ff_qcd_AR_SR_ARlike,
    q.ff_qcd_sub_DR_SR_SRlike,
    q.ff_qcd_sub_DR_SR_ARlike,
    q.ff_qcd_sub_AR_SR_SRlike,
    q.ff_qcd_sub_AR_SR_ARlike,
    q.ff_wjets_DR_SR_SRlike,
    q.ff_wjets_DR_SR_ARlike,
    q.ff_wjets_DR_SR_SRlike_ss,
    q.ff_wjets_DR_SR_ARlike_ss,
    q.ff_wjets_AR_SR_SRlike,
    q.ff_wjets_AR_SR_ARlike,
    q.ff_wjets_AR_SR_SRlike_ss,
    q.ff_wjets_AR_SR_ARlike_ss,
)


def add_selection(
    configuration: Configuration,
    scopes,
    era: str,
    sample: str,
    apply_preselection_filter=None,
    friend=False,
    groups=None,
) -> Configuration:
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

    # tau vs jet working points of the fake factor regions
    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "ff_tau_iso_vsjet_wp": "Medium",
            "ff_tau_antiiso_vsjet_wp": "VVVLoose",
        },
    )

    # light lepton isolation of the fake factor regions
    configuration.add_config_parameters(
        ["et", "mt"],
        {
            "lep_iso_max": 0.15,
        },
    )

    # preselection tau ID working points and trigger flag names. The pt and eta
    # thresholds live in `tau_triggersetup.py` and in the object selection of
    # `config.py`
    configuration.add_config_parameters(
        ["et"],
        {
            "presel_vsele_wp": "Tight",
            "presel_vsmu_wp": "VLoose_Tight",
            "presel_trigger_flag": "trg_single_ele30",
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "presel_vsele_wp": "VVLoose",
            "presel_vsmu_wp": "Tight_VVLoose",
            "presel_trigger_flag": "trg_single_mu24",
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "presel_vsele_wp": "VVLoose",
            "presel_vsmu_wp": "VLoose_VVLoose",
            "presel_trigger_flag": DOUBLETAU_TRIGGER_FLAG,
        },
    )
    configuration.add_config_parameters(
        ["em"],
        {
            "presel_pt_1": 25.0,  # electron pt
            "presel_trigger_flag": "trg_single_mu24",
        },
    )

    #########################
    # Producers 
    #########################

    for scope in [scope for scope in ["et", "mt", "tt", "em"] if scope in scopes]:
        variants = selection.FRIEND_FLAGS if friend else {}
        if friend:
            selection.set_friend_columns(configuration, scope)

        def pick(*producers):
            return [variants.get(producer, producer) for producer in producers]

        if "preselection" in groups:
            if scope in ["et", "mt"]:
                configuration.add_producers(
                    [scope],
                    pick(
                        selection.JetVetoMapFlag,
                        selection.PreselTriggerFlag,
                        selection.PreselVsEleTauID_2,
                        selection.PreselVsMuTauID_2,
                        selection.presel_mask,
                    ),
                )
            elif scope == "tt":
                configuration.add_producers(
                    [scope],
                    pick(
                        selection.JetVetoMapFlag,
                        selection.PreselTriggerFlag_tt,
                        # both tau legs, hence every tau flag twice
                        selection.PreselVsEleTauID_1,
                        selection.PreselVsEleTauID_2,
                        selection.PreselVsMuTauID_1,
                        selection.PreselVsMuTauID_2,
                        selection.presel_mask_tt,
                    ),
                )
            elif scope == "em":
                configuration.add_producers(
                    [scope],
                    pick(
                        selection.JetVetoMapFlag,
                        selection.PreselTriggerFlag,
                        selection.PreselPt_1,
                        selection.presel_mask_em,
                    ),
                )
            configuration.add_outputs([scope], [q.presel_mask])

        if "regions" in groups:
            if scope in ["et", "mt"]:
                configuration.add_producers(
                    [scope],
                    pick(
                        # `q_1 * q_2`, the shared input of both sign flags
                        selection.ChargeProduct,
                        selection.OppositeSignFlag,
                        selection.SameSignFlag,
                        selection.NoExtraElectronFlag,
                        selection.NoExtraMuonFlag,
                        selection.NoDileptonFlag,
                        selection.LeptonVetoFlag,
                        selection.LeptonVetoInvertedFlag,
                        selection.TauIsoFlag_2,
                        selection.TauNonIsoFlag_2,
                        selection.TauVVVLooseFlag_2,
                        selection.MtBelow70Flag,
                        selection.WjetsMtFlag,
                        selection.NBtagEqZeroFlag,
                        selection.TTbarNBtagFlag,
                        selection.LepIsoFlag,
                        selection.LepAntiIsoFlag,
                        # QCD
                        selection.ff_qcd_SRlike,
                        selection.ff_qcd_ARlike,
                        # W+jets
                        selection.ff_wjets_SRlike,
                        selection.ff_wjets_ARlike,
                        selection.ff_wjets_SRlike_ss,
                        selection.ff_wjets_ARlike_ss,
                        # ttbar
                        selection.ff_ttbar_SR,
                        selection.ff_ttbar_AR,
                        selection.ff_ttbar_SRlike,
                        selection.ff_ttbar_ARlike,
                        selection.ff_ttbar_SRlike_ss,
                        selection.ff_ttbar_ARlike_ss,
                        # process fractions
                        selection.ff_fraction_SR,
                        selection.ff_fraction_AR,
                        # QCD DR/AR to SR corrections
                        selection.ff_qcd_DR_SR_SRlike,
                        selection.ff_qcd_DR_SR_ARlike,
                        selection.ff_qcd_AR_SR_SRlike,
                        selection.ff_qcd_AR_SR_ARlike,
                        # W+jets DR/AR to SR corrections
                        selection.ff_wjets_DR_SR_SRlike,
                        selection.ff_wjets_DR_SR_ARlike,
                        selection.ff_wjets_DR_SR_SRlike_ss,
                        selection.ff_wjets_DR_SR_ARlike_ss,
                        selection.ff_wjets_AR_SR_SRlike,
                        selection.ff_wjets_AR_SR_ARlike,
                        selection.ff_wjets_AR_SR_SRlike_ss,
                        selection.ff_wjets_AR_SR_ARlike_ss,
                    ),
                )
                configuration.add_outputs(
                    [scope],
                    [
                        q.ff_qcd_SRlike,
                        q.ff_qcd_ARlike,
                        q.ff_wjets_SRlike,
                        q.ff_wjets_ARlike,
                        q.ff_wjets_SRlike_ss,
                        q.ff_wjets_ARlike_ss,
                        q.ff_ttbar_SR,
                        q.ff_ttbar_AR,
                        q.ff_ttbar_SRlike,
                        q.ff_ttbar_ARlike,
                        q.ff_ttbar_SRlike_ss,
                        q.ff_ttbar_ARlike_ss,
                        q.ff_fraction_SR,
                        q.ff_fraction_AR,
                        q.ff_qcd_DR_SR_SRlike,
                        q.ff_qcd_DR_SR_ARlike,
                        q.ff_qcd_AR_SR_SRlike,
                        q.ff_qcd_AR_SR_ARlike,
                        q.ff_wjets_DR_SR_SRlike,
                        q.ff_wjets_DR_SR_ARlike,
                        q.ff_wjets_DR_SR_SRlike_ss,
                        q.ff_wjets_DR_SR_ARlike_ss,
                        q.ff_wjets_AR_SR_SRlike,
                        q.ff_wjets_AR_SR_ARlike,
                        q.ff_wjets_AR_SR_SRlike_ss,
                        q.ff_wjets_AR_SR_ARlike_ss,
                    ],
                )
            elif scope == "tt":
                configuration.add_producers(
                    [scope],
                    pick(
                        selection.ChargeProduct,
                        selection.OppositeSignFlag,
                        selection.SameSignFlag,
                        selection.NoExtraElectronFlag,
                        selection.NoExtraMuonFlag,
                        selection.NoDileptonFlag,
                        selection.LeptonVetoFlag,
                        selection.TauIsoFlag_1,
                        selection.TauIsoFlag_2,
                        selection.TauNonIsoFlag_1,
                        selection.TauNonIsoFlag_2,
                        selection.TauVVVLooseFlag_1,
                        selection.TauVVVLooseFlag_2,
                        # QCD, leading tau
                        selection.ff_qcd_SRlike_tt,
                        selection.ff_qcd_ARlike_tt,
                        # QCD, subleading tau
                        selection.ff_qcd_sub_SRlike_tt,
                        selection.ff_qcd_sub_ARlike_tt,
                        # process fractions
                        selection.ff_fraction_SR_tt,
                        selection.ff_fraction_AR_tt,
                        selection.ff_fraction_sub_SR_tt,
                        selection.ff_fraction_sub_AR_tt,
                        # DR/AR to SR corrections, leading tau
                        selection.ff_qcd_DR_SR_SRlike_tt,
                        selection.ff_qcd_DR_SR_ARlike_tt,
                        selection.ff_qcd_AR_SR_SRlike_tt,
                        selection.ff_qcd_AR_SR_ARlike_tt,
                        # DR/AR to SR corrections, subleading tau
                        selection.ff_qcd_sub_DR_SR_SRlike_tt,
                        selection.ff_qcd_sub_DR_SR_ARlike_tt,
                        selection.ff_qcd_sub_AR_SR_SRlike_tt,
                        selection.ff_qcd_sub_AR_SR_ARlike_tt,
                    ),
                )
                configuration.add_outputs(
                    [scope],
                    [
                        q.ff_qcd_SRlike,
                        q.ff_qcd_ARlike,
                        q.ff_qcd_sub_SRlike,
                        q.ff_qcd_sub_ARlike,
                        q.ff_fraction_SR,
                        q.ff_fraction_AR,
                        q.ff_fraction_sub_SR,
                        q.ff_fraction_sub_AR,
                        q.ff_qcd_DR_SR_SRlike,
                        q.ff_qcd_DR_SR_ARlike,
                        q.ff_qcd_AR_SR_SRlike,
                        q.ff_qcd_AR_SR_ARlike,
                        q.ff_qcd_sub_DR_SR_SRlike,
                        q.ff_qcd_sub_DR_SR_ARlike,
                        q.ff_qcd_sub_AR_SR_SRlike,
                        q.ff_qcd_sub_AR_SR_ARlike,
                    ],
                )
            # em has no fake factor regions yet

    ################################
    ######### Modifications ########
    ################################

    # only Run 2 swaps in the embedding ditau trigger group, see tau_embedding_settings.py
    if (
        not friend
        and "preselection" in groups
        and "tt" in scopes
        and int(era[:4]) < 2022
    ):
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
            [scope for scope in ["et", "mt", "tt", "em"] if scope in scopes],
            AppendProducer(
                producers=[selection.PreselectionFilter],
                samples=list(configuration.available_sample_types),
            ),
        )

    return configuration


def restrict_selection_shifts(configuration: Configuration, scopes, shifts=None) -> Configuration:
    # Keep the fake factor regions on nominal only.
    announced = list(shifts or [])
    for scope in scopes:
        for quantity in NOMINAL_ONLY_QUANTITIES:
            for shift in list(quantity.shifts.get(scope, set())) + announced:
                quantity.ignore_shift(shift, scope)
            quantity.shifts[scope] = set()

    return configuration
