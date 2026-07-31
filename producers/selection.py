"""Atomic selection-flag producers and the region-mask machinery.

This module only defines *how* a cut is evaluated. *Which* cuts make up which
region, and which era uses which thresholds, is defined in the top level
``analysis_configurations/tau/selection.py`` -- look there first if you want to
know or change what a mask means.

Two kinds of objects live here:

``selcut_*`` producers
    One producer per atomic cut. They write an internal ``bool`` column
    (``q.selcut_*``) that is *not* part of the ntuple output. Thresholds, WP
    names, trigger flag names and column types are supplied through config
    parameters so that a single producer can serve several scopes and eras.

``CombineFlags`` / ``PreselectionFilter``
    ``make_mask_producer()`` builds the region masks by AND-ing a list of
    ``selcut_*`` flags with ``event::CombineFlags(..., "all_of")``.
    ``PreselectionFilter`` is the opt-in hard event filter on ``presel_mask``.

Every cut is expressed with the generic CROWN core helpers only
(``event::quantity::{Min,Greater,Max,MaxOrEqual,AbsMax,Equal}Flag``,
``event::quantity::Product``, ``event::CombineFlags`` and ``event::filter::``);
there is no analysis specific C++ addon for the selection. Cuts that are not a
single comparison (closed isolation intervals, the accepted tau decay mode
list, their negations) are composed from those primitives with a
``ProducerGroup`` writing intermediate ``selcut_*`` columns.

Columns that are leaves of a ``QuantityGroup`` (the tau ID working point flags
``id_tau_vsJet_Medium_2`` and the trigger flags ``trg_single_mu24``, ...) cannot
be passed as ordinary input quantities. They are referenced by name through a
quoted config-parameter placeholder inside the call, while the corresponding
``ExtendedVectorProducer.output_group`` is declared as ``input`` purely so that
the producer ordering places the flag producer after the group.
"""

from code_generation.producer import Producer as _RawProducer

from ..quantities import output as q
from ..scripts.CROWNWrapper import BaseFilter, Producer, ProducerGroup, defaults
from ..producers import pairquantities as pairquantities
from ..producers import triggers as triggers

# scopes for which the selection masks are defined
LT_SCOPES = ["et", "mt"]
TT_SCOPES = ["tt"]
LTT_SCOPES = ["et", "mt", "tt"]
ALL_SCOPES = ["et", "mt", "tt", "em"]

# `output_group`s that carry the tau-vs-jet/-ele/-mu ID working point flags.
# The leg-1 groups only exist in the tt scope, the leg-2 groups in et/mt/tt.
_VSJET_2 = pairquantities.VsJetTauIDFlag_2.output_group  # Medium
_VSJET_ONLY_2 = pairquantities.VsJetTauIDFlagOnly_2.output_group  # VVVLoose, ...
_VSJET_1 = pairquantities.VsJetTauIDFlag_1.output_group
_VSJET_ONLY_1 = pairquantities.VsJetTauIDFlagOnly_1.output_group
_VSELE_2 = pairquantities.VsEleTauIDFlag_2.output_group
_VSELE_1 = pairquantities.VsEleTauIDFlag_1.output_group
_VSMU_2 = pairquantities.VsMuTauIDFlag_2.output_group
_VSMU_1 = pairquantities.VsMuTauIDFlag_1.output_group


# The accepted hadronic tau decay modes are cut on one by one and OR-ed
# together, so the value cannot come from a (scope-global) config parameter.
def _decaymode_call(mode):
    """`event::quantity::EqualFlag` call comparing the decay mode to `mode`."""
    return (
        "event::quantity::EqualFlag<{selection_decaymode_type}>"
        "({df}, {output}, {input}, " + str(mode) + ")"
    )


##############################################################################
# preselection: hadronic tau requirements
##############################################################################

with defaults(scopes=LTT_SCOPES):
    # (tau_decaymode_2 == 0) || (... == 1) || (... == 10) || (... == 11),
    # built as one `EqualFlag` per accepted decay mode plus an `any_of`
    with defaults(input=[q.tau_decaymode_2]):
        PreselTauDecayModeEq0_2 = Producer(
            call=_decaymode_call(0),
            output=[q.selcut_presel_tau_dm_2_eq_0],
        )
        PreselTauDecayModeEq1_2 = Producer(
            call=_decaymode_call(1),
            output=[q.selcut_presel_tau_dm_2_eq_1],
        )
        PreselTauDecayModeEq10_2 = Producer(
            call=_decaymode_call(10),
            output=[q.selcut_presel_tau_dm_2_eq_10],
        )
        PreselTauDecayModeEq11_2 = Producer(
            call=_decaymode_call(11),
            output=[q.selcut_presel_tau_dm_2_eq_11],
        )

    PreselTauDecayMode_2 = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "any_of")''',
        input=[
            q.selcut_presel_tau_dm_2_eq_0,
            q.selcut_presel_tau_dm_2_eq_1,
            q.selcut_presel_tau_dm_2_eq_10,
            q.selcut_presel_tau_dm_2_eq_11,
        ],
        output=[q.selcut_presel_tau_dm_2],
        subproducers=[
            PreselTauDecayModeEq0_2,
            PreselTauDecayModeEq1_2,
            PreselTauDecayModeEq10_2,
            PreselTauDecayModeEq11_2,
        ],
    )

    # id_tau_vsEle_<WP>_2 == 1 and id_tau_vsMu_<WP>_2 == 1
    PreselVsEleTauID_2 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_2", 1)''',
        input=[_VSELE_2],
        output=[q.selcut_presel_vsele_2],
    )
    PreselVsMuTauID_2 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_2", 1)''',
        input=[_VSMU_2],
        output=[q.selcut_presel_vsmu_2],
    )

with defaults(scopes=TT_SCOPES):
    with defaults(input=[q.tau_decaymode_1]):
        PreselTauDecayModeEq0_1 = Producer(
            call=_decaymode_call(0),
            output=[q.selcut_presel_tau_dm_1_eq_0],
        )
        PreselTauDecayModeEq1_1 = Producer(
            call=_decaymode_call(1),
            output=[q.selcut_presel_tau_dm_1_eq_1],
        )
        PreselTauDecayModeEq10_1 = Producer(
            call=_decaymode_call(10),
            output=[q.selcut_presel_tau_dm_1_eq_10],
        )
        PreselTauDecayModeEq11_1 = Producer(
            call=_decaymode_call(11),
            output=[q.selcut_presel_tau_dm_1_eq_11],
        )

    PreselTauDecayMode_1 = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "any_of")''',
        input=[
            q.selcut_presel_tau_dm_1_eq_0,
            q.selcut_presel_tau_dm_1_eq_1,
            q.selcut_presel_tau_dm_1_eq_10,
            q.selcut_presel_tau_dm_1_eq_11,
        ],
        output=[q.selcut_presel_tau_dm_1],
        subproducers=[
            PreselTauDecayModeEq0_1,
            PreselTauDecayModeEq1_1,
            PreselTauDecayModeEq10_1,
            PreselTauDecayModeEq11_1,
        ],
    )

    PreselVsEleTauID_1 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_1", 1)''',
        input=[_VSELE_1],
        output=[q.selcut_presel_vsele_1],
    )
    PreselVsMuTauID_1 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_1", 1)''',
        input=[_VSMU_1],
        output=[q.selcut_presel_vsmu_1],
    )


##############################################################################
# preselection: kinematics, trigger and jet veto map
##############################################################################

with defaults(scopes=ALL_SCOPES):
    # pt_1 > {presel_pt_1}  (light lepton in et/mt/em, leading tau in tt)
    PreselPt_1 = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {presel_pt_1})''',
        input=[q.pt_1],
        output=[q.selcut_presel_pt_1],
    )
    # pt_2 > {presel_pt_2}  (hadronic tau in et/mt/tt, muon in em)
    PreselPt_2 = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {presel_pt_2})''',
        input=[q.pt_2],
        output=[q.selcut_presel_pt_2],
    )
    # jet_vetomap == 0
    JetVetoMapFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.jet_vetomap],
        output=[q.selcut_jet_veto],
    )

with defaults(scopes=["em"]):
    # abs(eta_1) < 2.5
    PreselElectronEta_1 = Producer(
        call='''event::quantity::AbsMaxFlag<float>({df}, {output}, {input}, {presel_abs_eta_1})''',
        input=[q.eta_1],
        output=[q.selcut_presel_eta_1],
    )

# The trigger flag columns are leaves of the trigger `output_group`s, which are
# scope dependent; for tt the group is swapped out for embedding samples, hence
# the second producer plus the ReplaceProducer rule set up in selection.py.
with defaults(
    call='''event::quantity::EqualFlag<bool>({df}, {output}, "{presel_trigger_flag}", 1)''',
    output=[q.selcut_presel_trigger],
):
    PreselTriggerFlag = Producer(
        scopes=["et", "mt", "em"],
        input={
            "et": [triggers.ETGenerateSingleElectronTriggerFlags.output_group],
            "mt": [triggers.MTGenerateSingleMuonTriggerFlags.output_group],
            "em": [triggers.EMGenerateSingleMuonTriggerFlags.output_group],
        },
    )
    PreselTriggerFlag_tt = Producer(
        scopes=TT_SCOPES,
        input=[triggers.TTGenerateDoubleTauTriggerFlags.output_group],
    )
    PreselTriggerFlag_tt_embedding = Producer(
        scopes=TT_SCOPES,
        input=[triggers.TTGenerateDoubleTauTriggerFlagsEmbedding.output_group],
    )


##############################################################################
# lepton vetoes
##############################################################################

with defaults(scopes=LTT_SCOPES):
    with defaults(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)'''
    ):
        NoExtraElectronFlag = Producer(
            input=[q.extraelec_veto], output=[q.selcut_no_extraelec]
        )
        NoExtraMuonFlag = Producer(
            input=[q.extramuon_veto], output=[q.selcut_no_extramuon]
        )
        NoDileptonFlag = Producer(
            input=[q.dilepton_veto], output=[q.selcut_no_dilepton]
        )

    # (extramuon_veto < 0.5) && (extraelec_veto < 0.5) && (dilepton_veto < 0.5)
    LeptonVetoFlag = Producer(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_no_extraelec, q.selcut_no_extramuon, q.selcut_no_dilepton],
        output=[q.selcut_lepton_veto],
    )
    # !((extramuon_veto == 0) && (extraelec_veto == 0) && (dilepton_veto == 0))
    # used by the ttbar signal-/application-like regions in et and mt
    LeptonVetoInvertedFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.selcut_lepton_veto],
        output=[q.selcut_lepton_veto_inv],
    )
    # (extramuon_veto < 0.5) && (extraelec_veto < 0.5), i.e. without the
    # dilepton veto; used by the tt subleading process fraction regions
    LeptonVetoNoDileptonFlag = Producer(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_no_extraelec, q.selcut_no_extramuon],
        output=[q.selcut_lepton_veto_nodilep],
    )


##############################################################################
# tau vs jet ID: isolated / non-isolated / anti-isolated legs
##############################################################################

with defaults(scopes=LTT_SCOPES):
    TauIsoFlag_2 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_2", 1)''',
        input=[_VSJET_2],
        output=[q.selcut_tau_iso_2],
    )
    TauNonIsoFlag_2 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_2", 0)''',
        input=[_VSJET_2],
        output=[q.selcut_tau_noniso_2],
    )
    TauVVVLooseFlag_2 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_wp}_2", 1)''',
        input=[_VSJET_ONLY_2],
        output=[q.selcut_tau_vvvloose_2],
    )

with defaults(scopes=TT_SCOPES):
    TauIsoFlag_1 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_1", 1)''',
        input=[_VSJET_1],
        output=[q.selcut_tau_iso_1],
    )
    TauNonIsoFlag_1 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_1", 0)''',
        input=[_VSJET_1],
        output=[q.selcut_tau_noniso_1],
    )
    TauVVVLooseFlag_1 = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_wp}_1", 1)''',
        input=[_VSJET_ONLY_1],
        output=[q.selcut_tau_vvvloose_1],
    )


##############################################################################
# light lepton isolation (et, mt)
#
# Two variants per flag: the 2022/2023 configs use a closed interval
# `((iso_1 >= lo) && (iso_1 <= hi))`, the 2024+ configs a plain `iso_1 < hi`.
# selection.py books exactly one of them per era.
##############################################################################

with defaults(scopes=LT_SCOPES, input=[q.iso_1]):
    # --- nominal signal-lepton isolation -------------------------------------
    # `(iso_1 >= {lep_iso_min}) && (iso_1 <= {lep_iso_max})`
    LepIsoLowerEdge = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {lep_iso_min})''',
        output=[q.selcut_lep_iso_lo],
    )
    LepIsoUpperEdge = Producer(
        call='''event::quantity::MaxOrEqualFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_iso_hi],
    )
    LepIsoFlag_Upper = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_iso],
    )

    # --- isolation window of the QCD determination regions -------------------
    # `(iso_1 >= {qcd_lep_iso_min}) && (iso_1 <= {qcd_lep_iso_max})`
    QCDLepIsoLowerEdge = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {qcd_lep_iso_min})''',
        output=[q.selcut_qcd_lep_iso_lo],
    )
    QCDLepIsoUpperEdge = Producer(
        call='''event::quantity::MaxOrEqualFlag<float>({df}, {output}, {input}, {qcd_lep_iso_max})''',
        output=[q.selcut_qcd_lep_iso_hi],
    )
    QCDLepIsoFlag_Upper = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, {qcd_lep_iso_max})''',
        output=[q.selcut_qcd_lep_iso],
    )

    # --- complement of the QCD isolation window (DR to SR corrections) -------
    # the window is recomputed into its own columns instead of reusing
    # `selcut_qcd_lep_iso`, so that the inverted flag does not depend on the
    # non-inverted producer being booked as well
    QCDLepAntiIsoLowerEdge = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {qcd_lep_iso_min})''',
        output=[q.selcut_qcd_lep_antiiso_lo],
    )
    QCDLepAntiIsoUpperEdge = Producer(
        call='''event::quantity::MaxOrEqualFlag<float>({df}, {output}, {input}, {qcd_lep_iso_max})''',
        output=[q.selcut_qcd_lep_antiiso_hi],
    )
    QCDLepAntiIsoFlag_Lower = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {qcd_lep_iso_max})''',
        output=[q.selcut_qcd_lep_antiiso],
    )

with defaults(scopes=LT_SCOPES):
    LepIsoFlag_Interval = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_lep_iso_lo, q.selcut_lep_iso_hi],
        output=[q.selcut_lep_iso],
        subproducers=[LepIsoLowerEdge, LepIsoUpperEdge],
    )
    QCDLepIsoFlag_Interval = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_qcd_lep_iso_lo, q.selcut_qcd_lep_iso_hi],
        output=[q.selcut_qcd_lep_iso],
        subproducers=[QCDLepIsoLowerEdge, QCDLepIsoUpperEdge],
    )
    QCDLepAntiIsoWindow = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_qcd_lep_antiiso_lo, q.selcut_qcd_lep_antiiso_hi],
        output=[q.selcut_qcd_lep_antiiso_win],
        subproducers=[QCDLepAntiIsoLowerEdge, QCDLepAntiIsoUpperEdge],
    )
    # exactly the logical negation of `QCDLepAntiIsoWindow`
    QCDLepAntiIsoFlag_Interval = ProducerGroup(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.selcut_qcd_lep_antiiso_win],
        output=[q.selcut_qcd_lep_antiiso],
        subproducers=[QCDLepAntiIsoWindow],
    )


##############################################################################
# transverse mass and b-tagged jet multiplicity (et, mt)
##############################################################################

with defaults(scopes=LT_SCOPES, input=[q.mt_1]):
    MtBelow50Flag = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, 50.0)''',
        output=[q.selcut_mt_lt_50],
    )
    MtBelow70Flag = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_mt_lt_70],
    )
    MtAboveZeroFlag = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, 0.0)''',
        output=[q.selcut_mt_gt_0],
    )
    # W+jets determination region: `mt_1 > 70` in mt for 2022/2023,
    # `mt_1 >= 70` in et always and in mt from 2024 on
    WjetsMtFlag_Strict = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_wjets_mt],
    )
    WjetsMtFlag_Inclusive = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_wjets_mt],
    )

with defaults(scopes=LT_SCOPES, input=[q.nbtag]):
    NBtagGeZeroFlag = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, {input}, 0)''',
        output=[q.selcut_nbtag_ge_0],
    )
    NBtagEqZeroFlag = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
        output=[q.selcut_nbtag_eq_0],
    )
    # ttbar determination regions: nbtag >= 1 (mt) / >= 2 (et 2022preEE) /
    # >= 0 (everything else), see selection.py
    TTbarNBtagFlag = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, {input}, {ttbar_nbtag_min})''',
        output=[q.selcut_ttbar_nbtag],
    )


##############################################################################
# tau pair charge
##############################################################################

with defaults(scopes=ALL_SCOPES):
    # `q_1 * q_2` as a single `double` column, shared by both sign flags. The
    # two legs can have different stored types (`int` for the light lepton,
    # `Short_t` for the hadronic tau), hence the two type parameters.
    ChargeProduct = Producer(
        call='''event::quantity::Product<{charge_type_1}, {charge_type_2}>({df}, {output}, {input})''',
        input=[q.q_1, q.q_2],
        output=[q.selcut_q_prod],
    )

    # both sign flags read the same product column; `ChargeProduct` is booked
    # once as an ordinary producer (see `_atomic_producers` in selection.py)
    # instead of as a subproducer of both, so that it is defined exactly once
    with defaults(input=[q.selcut_q_prod]):
        # (q_1 * q_2) < 0
        OppositeSignFlag = Producer(
            call='''event::quantity::MaxFlag<double>({df}, {output}, {input}, 0.0)''',
            output=[q.sel_os],
        )
        # (q_1 * q_2) > 0
        SameSignFlag = Producer(
            call='''event::quantity::GreaterFlag<double>({df}, {output}, {input}, 0.0)''',
            output=[q.sel_ss],
        )


##############################################################################
# masks and the opt-in preselection filter
##############################################################################

PreselectionFilter = BaseFilter(
    call='''event::filter::Flag({df}, "PreselectionFilter", {input})''',
    input=[q.presel_mask],
    scopes=ALL_SCOPES,
)


def make_mask_producer(name, output_quantity, flags, scopes):
    """Build the producer that ANDs a list of atomic selection flags.

    Args:
        name: name of the producer (used for logging and code generation)
        output_quantity: the mask `Quantity` to be written
        flags: list of `selcut_*` quantities that make up the region
        scopes: scopes the mask is defined for

    Returns:
        A `Producer` evaluating `event::CombineFlags(..., "all_of")`.

    Note:
        The raw `code_generation.producer.Producer` is used instead of the
        `CROWNWrapper` one because the wrapper derives the producer name from
        the source line of the assignment, which does not work for producers
        created inside a loop.
    """
    return _RawProducer(
        name=name,
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=list(flags),
        output=[output_quantity],
        scopes=list(scopes),
    )
