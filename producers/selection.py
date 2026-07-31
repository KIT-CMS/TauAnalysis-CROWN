"""Atomic selection-flag producers and the region masks.

Two kinds of objects live here:

``selcut_*`` producers
    One producer per atomic cut. They write an internal ``bool`` column
    (``q.selcut_*``) that is *not* part of the ntuple output. Thresholds, WP
    names, accepted decay modes, trigger flag names and column types are
    supplied through config parameters so that a single producer can serve
    several scopes and eras.

mask producers
    One producer per public mask branch, AND-ing a list of ``selcut_*`` flags
    with ``event::CombineFlags(..., "all_of")``. They form the literal region
    table at the bottom of this file: one line per region, the ``input`` list
    *is* the definition of the region. **If a region changes, change it
    there.** ``PreselectionFilter`` is the opt-in hard event filter on
    ``presel_mask``.

The masks are era independent; only the scope varies. The per-era thresholds,
working points and trigger flag names of the *preselection*, and the booking of
all of this into a ``Configuration``, live in the top level
``analysis_configurations/tau/selection.py``.

Every cut is expressed with the generic CROWN core helpers only
(``event::quantity::{Min,Greater,Max,AbsMax,Equal,InList}Flag``,
``event::quantity::Product``, ``event::CombineFlags`` and ``event::filter::``);
there is no analysis specific C++ addon for the selection. The only cut that is
not a single comparison is the combined lepton veto and its negation, composed
from those primitives with intermediate ``selcut_*`` columns.

The yaml files spell the boolean/flag columns out as ``col > 0.5`` ("pass") and
``col < 0.5`` ("fail"). Those are reproduced here as ``MinFlag<T>(..., 1)`` and
``MaxFlag<T>(..., 1)``, which are exactly equivalent for any non-negative
integer or bool column and do not rely on the flag producers upstream only ever
emitting 0 or 1. Genuine equality cuts (``nbtag == 0``) use ``EqualFlag``; the
accepted hadronic tau decay modes use ``InListFlag`` with the values of the
``tau_dms`` config parameter.

TWO YAML CUTS ARE DELIBERATELY NOT IN THE MASKS
-----------------------------------------------
``nbtag: (nbtag >= 0)`` (QCD / fraction / AR_SR regions) and
``lep_mt: (mt_1 > 0)`` (W+jets DR_SR regions) are unconditionally true --
``nbtag`` is a jet count and ``mt_1`` a transverse mass, both non-negative by
construction. They are omitted, so the masks are semantically identical to the
yaml regions even though a literal cut-by-cut diff against the yaml files will
show these two as missing.

Columns that are leaves of a ``QuantityGroup`` (the tau ID working point flags
``id_tau_vsJet_Medium_2`` and the trigger flags ``trg_single_mu24``, ...) cannot
be passed as ordinary input quantities. They are referenced by name through a
quoted config-parameter placeholder inside the call, while the corresponding
``ExtendedVectorProducer.output_group`` is declared as ``input`` purely so that
the producer ordering places the flag producer after the group.
"""

from ..quantities import output as q
from ..scripts.CROWNWrapper import BaseFilter, Producer, defaults
from ..producers import pairquantities as pairquantities
from ..producers import triggers as triggers

##############################################################################
# preselection: hadronic tau requirements
##############################################################################

with defaults(scopes=["et", "mt", "tt"]):
    # tau_decaymode_2 is one of the modes listed in the `tau_dms` config
    # parameter, which also drives the object level decay mode cut in
    # `producers/taus.py`, so the two can never drift apart
    PreselTauDecayMode_2 = Producer(
        call='''event::quantity::InListFlag<{selection_decaymode_type}>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})''',
        input=[q.tau_decaymode_2],
        output=[q.selcut_presel_tau_dm_2],
    )

    # id_tau_vsEle_<WP>_2 > 0.5 and id_tau_vsMu_<WP>_2 > 0.5
    PreselVsEleTauID_2 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_2", 1)''',
        input=[pairquantities.VsEleTauIDFlag_2.output_group],
        output=[q.selcut_presel_vsele_2],
    )
    PreselVsMuTauID_2 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_2", 1)''',
        input=[pairquantities.VsMuTauIDFlag_2.output_group],
        output=[q.selcut_presel_vsmu_2],
    )

with defaults(scopes=["tt"]):
    # tau_decaymode_1 is one of the modes listed in `tau_dms`, as above
    PreselTauDecayMode_1 = Producer(
        call='''event::quantity::InListFlag<{selection_decaymode_type}>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})''',
        input=[q.tau_decaymode_1],
        output=[q.selcut_presel_tau_dm_1],
    )

    PreselVsEleTauID_1 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_1", 1)''',
        input=[pairquantities.VsEleTauIDFlag_1.output_group],
        output=[q.selcut_presel_vsele_1],
    )
    PreselVsMuTauID_1 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_1", 1)''',
        input=[pairquantities.VsMuTauIDFlag_1.output_group],
        output=[q.selcut_presel_vsmu_1],
    )


##############################################################################
# preselection: kinematics, trigger and jet veto map
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em"]):
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
    # jet_vetomap < 0.5
    JetVetoMapFlag = Producer(
        call='''event::quantity::MaxFlag<bool>({df}, {output}, {input}, 1)''',
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
    call='''event::quantity::MinFlag<bool>({df}, {output}, "{presel_trigger_flag}", 1)''',
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
        scopes=["tt"],
        input=[triggers.TTGenerateDoubleTauTriggerFlags.output_group],
    )
    PreselTriggerFlag_tt_embedding = Producer(
        scopes=["tt"],
        input=[triggers.TTGenerateDoubleTauTriggerFlagsEmbedding.output_group],
    )


##############################################################################
# lepton vetoes
##############################################################################

with defaults(scopes=["et", "mt", "tt"]):
    # `extraelec_veto < 0.5`, `extramuon_veto < 0.5`, `dilepton_veto < 0.5`
    with defaults(
        call='''event::quantity::MaxFlag<bool>({df}, {output}, {input}, 1)'''
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
    # !((extramuon_veto < 0.5) && (extraelec_veto < 0.5) && (dilepton_veto < 0.5))
    # used by the ttbar signal-/application-like regions in et and mt. This is a
    # genuine negation of an internal `bool` column, hence `EqualFlag<bool>`.
    LeptonVetoInvertedFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.selcut_lepton_veto],
        output=[q.selcut_lepton_veto_inv],
    )


##############################################################################
# tau vs jet ID: isolated / non-isolated / anti-isolated legs
##############################################################################

with defaults(scopes=["et", "mt", "tt"]):
    TauIsoFlag_2 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_2", 1)''',
        input=[pairquantities.VsJetTauIDFlag_2.output_group],
        output=[q.selcut_tau_iso_2],
    )
    TauNonIsoFlag_2 = Producer(
        call='''event::quantity::MaxFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_2", 1)''',
        input=[pairquantities.VsJetTauIDFlag_2.output_group],
        output=[q.selcut_tau_noniso_2],
    )
    TauVVVLooseFlag_2 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_wp}_2", 1)''',
        input=[pairquantities.VsJetTauIDFlagOnly_2.output_group],
        output=[q.selcut_tau_vvvloose_2],
    )

with defaults(scopes=["tt"]):
    TauIsoFlag_1 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_1", 1)''',
        input=[pairquantities.VsJetTauIDFlag_1.output_group],
        output=[q.selcut_tau_iso_1],
    )
    TauNonIsoFlag_1 = Producer(
        call='''event::quantity::MaxFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_wp}_1", 1)''',
        input=[pairquantities.VsJetTauIDFlag_1.output_group],
        output=[q.selcut_tau_noniso_1],
    )
    TauVVVLooseFlag_1 = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_wp}_1", 1)''',
        input=[pairquantities.VsJetTauIDFlagOnly_1.output_group],
        output=[q.selcut_tau_vvvloose_1],
    )


##############################################################################
# light lepton isolation (et, mt)
#
# Every fake factor region uses `iso_1 < 0.15`; the QCD DR-to-SR / AR-to-SR
# correction regions use its exact complement `iso_1 >= 0.15`. Both are a single
# comparison, in every era and both channels.
##############################################################################

with defaults(scopes=["et", "mt"], input=[q.iso_1]):
    # `iso_1 < {lep_iso_max}`
    LepIsoFlag = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_iso],
    )
    # `iso_1 >= {lep_iso_max}`, the logical complement of `LepIsoFlag` by
    # construction -- no negation producer needed
    LepAntiIsoFlag = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_antiiso],
    )


##############################################################################
# transverse mass and b-tagged jet multiplicity (et, mt)
##############################################################################

with defaults(scopes=["et", "mt"], input=[q.mt_1]):
    # `mt_1 < 70`: QCD, ttbar and process fraction regions
    MtBelow70Flag = Producer(
        call='''event::quantity::MaxFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_mt_lt_70],
    )
    # `mt_1 >= 70`: the W+jets determination regions, in every era and channel
    WjetsMtFlag = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_wjets_mt],
    )

with defaults(scopes=["et", "mt"], input=[q.nbtag]):
    NBtagEqZeroFlag = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
        output=[q.selcut_nbtag_eq_0],
    )
    # ttbar determination regions: `nbtag >= 1`, in every era and channel
    TTbarNBtagFlag = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, {input}, 1)''',
        output=[q.selcut_ttbar_nbtag],
    )


##############################################################################
# tau pair charge
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em"]):
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
# region masks -- THE LITERAL REGION TABLE
#
# One `Producer` per mask, one line per region: the `input` list *is* the
# definition of what the mask means. If a region changes, change it here.
#
# The masks are era independent; only the *scope* varies, hence the three
# blocks below (et/mt share one table, tt has its own, em has only the
# preselection). The public branch name is the `output` quantity, so the tt
# variants can carry a `_tt` suffixed producer name while writing the same
# branch name as their et/mt namesakes.
#
# Short aliases keep every region on a single line; they are the `selcut_*`
# flags produced above.
##############################################################################

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

lep_iso = q.selcut_lep_iso  # iso_1 < 0.15
lep_anti = q.selcut_lep_antiiso  # iso_1 >= 0.15

mt70 = q.selcut_mt_lt_70  # mt_1 < 70
w_mt = q.selcut_wjets_mt  # mt_1 >= 70
nbeq0 = q.selcut_nbtag_eq_0  # nbtag == 0
tt_nb = q.selcut_ttbar_nbtag  # nbtag >= 1

anti = [vvl2, nis2]  # (vsJet VVVLoose > 0.5) && (vsJet Medium < 0.5)

# ---------------------------------------------------------------------------
# et and mt
# ---------------------------------------------------------------------------

with defaults(scopes=["et", "mt"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    presel_mask = Producer(input=[dm2, vse2, vsm2, pt1, pt2, trg, jetveto],  output=[q.presel_mask])

    # --- QCD fake factors ---
    ff_qcd_SRlike = Producer(input=[iso2, lep_iso, mt70, veto, ss_],          output=[q.ff_qcd_SRlike])
    ff_qcd_ARlike = Producer(input=[*anti, lep_iso, mt70, veto, ss_],         output=[q.ff_qcd_ARlike])

    # --- W+jets fake factors (and their same-sign QCD estimation) ---
    ff_wjets_SRlike = Producer(input=[iso2, lep_iso, w_mt, nbeq0, veto, os_],  output=[q.ff_wjets_SRlike])
    ff_wjets_ARlike = Producer(input=[*anti, lep_iso, w_mt, nbeq0, veto, os_], output=[q.ff_wjets_ARlike])
    ff_wjets_SRlike_ss = Producer(input=[iso2, lep_iso, w_mt, nbeq0, veto, ss_],  output=[q.ff_wjets_SRlike_ss])
    ff_wjets_ARlike_ss = Producer(input=[*anti, lep_iso, w_mt, nbeq0, veto, ss_], output=[q.ff_wjets_ARlike_ss])

    # --- ttbar fake factors: SR/AR (MC), SR-like/AR-like (inverted veto) ---
    ff_ttbar_SR = Producer(input=[iso2, lep_iso, mt70, tt_nb, veto, os_],          output=[q.ff_ttbar_SR])
    ff_ttbar_AR = Producer(input=[*anti, lep_iso, mt70, tt_nb, veto, os_],         output=[q.ff_ttbar_AR])
    ff_ttbar_SRlike = Producer(input=[iso2, lep_iso, mt70, tt_nb, veto_inv, os_],  output=[q.ff_ttbar_SRlike])
    ff_ttbar_ARlike = Producer(input=[*anti, lep_iso, mt70, tt_nb, veto_inv, os_], output=[q.ff_ttbar_ARlike])
    ff_ttbar_SRlike_ss = Producer(input=[iso2, lep_iso, mt70, tt_nb, veto_inv, ss_],  output=[q.ff_ttbar_SRlike_ss])
    ff_ttbar_ARlike_ss = Producer(input=[*anti, lep_iso, mt70, tt_nb, veto_inv, ss_], output=[q.ff_ttbar_ARlike_ss])

    # --- process fractions ---
    ff_fraction_SR = Producer(input=[iso2, lep_iso, mt70, veto, os_],   output=[q.ff_fraction_SR])
    ff_fraction_AR = Producer(input=[*anti, lep_iso, mt70, veto, os_],  output=[q.ff_fraction_AR])

    # --- QCD DR to SR corrections (lepton isolation inverted) ---
    ff_qcd_DR_SR_SRlike = Producer(input=[iso2, lep_anti, mt70, veto, ss_],   output=[q.ff_qcd_DR_SR_SRlike])
    ff_qcd_DR_SR_ARlike = Producer(input=[*anti, lep_anti, mt70, veto, ss_],  output=[q.ff_qcd_DR_SR_ARlike])
    ff_qcd_AR_SR_SRlike = Producer(input=[iso2, lep_anti, mt70, veto, os_],   output=[q.ff_qcd_AR_SR_SRlike])
    ff_qcd_AR_SR_ARlike = Producer(input=[*anti, lep_anti, mt70, veto, os_],  output=[q.ff_qcd_AR_SR_ARlike])

    # --- W+jets DR to SR corrections (and their same-sign variants) ---
    ff_wjets_DR_SR_SRlike = Producer(input=[iso2, lep_iso, nbeq0, veto, os_],   output=[q.ff_wjets_DR_SR_SRlike])
    ff_wjets_DR_SR_ARlike = Producer(input=[*anti, lep_iso, nbeq0, veto, os_],  output=[q.ff_wjets_DR_SR_ARlike])
    ff_wjets_DR_SR_SRlike_ss = Producer(input=[iso2, lep_iso, nbeq0, veto, ss_],   output=[q.ff_wjets_DR_SR_SRlike_ss])
    ff_wjets_DR_SR_ARlike_ss = Producer(input=[*anti, lep_iso, nbeq0, veto, ss_],  output=[q.ff_wjets_DR_SR_ARlike_ss])
    ff_wjets_AR_SR_SRlike = Producer(input=[iso2, lep_iso, mt70, veto, os_],    output=[q.ff_wjets_AR_SR_SRlike])
    ff_wjets_AR_SR_ARlike = Producer(input=[*anti, lep_iso, mt70, veto, os_],   output=[q.ff_wjets_AR_SR_ARlike])
    ff_wjets_AR_SR_SRlike_ss = Producer(input=[iso2, lep_iso, mt70, veto, ss_],    output=[q.ff_wjets_AR_SR_SRlike_ss])
    ff_wjets_AR_SR_ARlike_ss = Producer(input=[*anti, lep_iso, mt70, veto, ss_],   output=[q.ff_wjets_AR_SR_ARlike_ss])

#: the masks of the et and mt scopes, in table order
LT_MASKS = [
    presel_mask,
    ff_qcd_SRlike, ff_qcd_ARlike,
    ff_wjets_SRlike, ff_wjets_ARlike, ff_wjets_SRlike_ss, ff_wjets_ARlike_ss,
    ff_ttbar_SR, ff_ttbar_AR,
    ff_ttbar_SRlike, ff_ttbar_ARlike, ff_ttbar_SRlike_ss, ff_ttbar_ARlike_ss,
    ff_fraction_SR, ff_fraction_AR,
    ff_qcd_DR_SR_SRlike, ff_qcd_DR_SR_ARlike,
    ff_qcd_AR_SR_SRlike, ff_qcd_AR_SR_ARlike,
    ff_wjets_DR_SR_SRlike, ff_wjets_DR_SR_ARlike,
    ff_wjets_DR_SR_SRlike_ss, ff_wjets_DR_SR_ARlike_ss,
    ff_wjets_AR_SR_SRlike, ff_wjets_AR_SR_ARlike,
    ff_wjets_AR_SR_SRlike_ss, ff_wjets_AR_SR_ARlike_ss,
]


# ---------------------------------------------------------------------------
# tt
# ---------------------------------------------------------------------------

with defaults(scopes=["tt"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    presel_mask_tt = Producer(input=[dm1, dm2, vse1, vse2, vsm1, vsm2, pt1, pt2, trg, jetveto], output=[q.presel_mask])

    # --- QCD fake factors, leading tau ---
    ff_qcd_SRlike_tt = Producer(input=[iso1, iso2, veto, ss_],        output=[q.ff_qcd_SRlike])
    ff_qcd_ARlike_tt = Producer(input=[vvl1, nis1, iso2, veto, ss_],  output=[q.ff_qcd_ARlike])

    # --- QCD fake factors, subleading tau ---
    ff_qcd_sub_SRlike_tt = Producer(input=[iso1, iso2, veto, ss_],        output=[q.ff_qcd_sub_SRlike])
    ff_qcd_sub_ARlike_tt = Producer(input=[iso1, vvl2, nis2, veto, ss_],  output=[q.ff_qcd_sub_ARlike])

    # --- process fractions ---
    ff_fraction_SR_tt = Producer(input=[iso1, iso2, veto, os_],             output=[q.ff_fraction_SR])
    ff_fraction_AR_tt = Producer(input=[vvl1, nis1, nis2, veto, os_],       output=[q.ff_fraction_AR])
    ff_fraction_sub_SR_tt = Producer(input=[iso1, iso2, veto, os_],         output=[q.ff_fraction_sub_SR])
    ff_fraction_sub_AR_tt = Producer(input=[nis1, vvl2, nis2, veto, os_],   output=[q.ff_fraction_sub_AR])

    # --- DR to SR corrections, leading tau ---
    ff_qcd_DR_SR_SRlike_tt = Producer(input=[iso1, nis2, veto, ss_],              output=[q.ff_qcd_DR_SR_SRlike])
    ff_qcd_DR_SR_ARlike_tt = Producer(input=[vvl1, nis1, nis2, veto, ss_],        output=[q.ff_qcd_DR_SR_ARlike])
    ff_qcd_AR_SR_SRlike_tt = Producer(input=[iso1, nis2, veto, os_],              output=[q.ff_qcd_AR_SR_SRlike])
    ff_qcd_AR_SR_ARlike_tt = Producer(input=[vvl1, nis1, nis2, veto, os_],        output=[q.ff_qcd_AR_SR_ARlike])

    # --- DR to SR corrections, subleading tau ---
    ff_qcd_sub_DR_SR_SRlike_tt = Producer(input=[nis1, iso2, veto, ss_],          output=[q.ff_qcd_sub_DR_SR_SRlike])
    ff_qcd_sub_DR_SR_ARlike_tt = Producer(input=[nis1, vvl2, nis2, veto, ss_],    output=[q.ff_qcd_sub_DR_SR_ARlike])
    ff_qcd_sub_AR_SR_SRlike_tt = Producer(input=[nis1, iso2, veto, os_],          output=[q.ff_qcd_sub_AR_SR_SRlike])
    ff_qcd_sub_AR_SR_ARlike_tt = Producer(input=[nis1, vvl2, nis2, veto, os_],    output=[q.ff_qcd_sub_AR_SR_ARlike])

#: the masks of the tt scope, in table order
TT_MASKS = [
    presel_mask_tt,
    ff_qcd_SRlike_tt, ff_qcd_ARlike_tt,
    ff_qcd_sub_SRlike_tt, ff_qcd_sub_ARlike_tt,
    ff_fraction_SR_tt, ff_fraction_AR_tt,
    ff_fraction_sub_SR_tt, ff_fraction_sub_AR_tt,
    ff_qcd_DR_SR_SRlike_tt, ff_qcd_DR_SR_ARlike_tt,
    ff_qcd_AR_SR_SRlike_tt, ff_qcd_AR_SR_ARlike_tt,
    ff_qcd_sub_DR_SR_SRlike_tt, ff_qcd_sub_DR_SR_ARlike_tt,
    ff_qcd_sub_AR_SR_SRlike_tt, ff_qcd_sub_AR_SR_ARlike_tt,
]


# ---------------------------------------------------------------------------
# em -- preselection only; the sign flags are written by the charge producers
# ---------------------------------------------------------------------------

with defaults(scopes=["em"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    presel_mask_em = Producer(input=[eta1, pt1, pt2, trg, jetveto], output=[q.presel_mask])

#: the masks of the em scope
EM_MASKS = [presel_mask_em]

#: scope -> the mask producers defined for it
MASKS = {"et": LT_MASKS, "mt": LT_MASKS, "tt": TT_MASKS, "em": EM_MASKS}


##############################################################################
# the opt-in preselection filter
##############################################################################

PreselectionFilter = BaseFilter(
    call='''event::filter::Flag({df}, "PreselectionFilter", {input})''',
    input=[q.presel_mask],
    scopes=["et", "mt", "tt", "em"],
)
