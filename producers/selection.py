from ..quantities import output as q
from code_generation.helpers import defaults
from code_generation.producer import Producer, ProducerGroup
from code_generation.quantity import Quantity
from code_generation.producer import Producer as _RawProducer
from code_generation.producer import SwitchProducer

##############################################################################
# preselection: hadronic tau requirements
##############################################################################

with defaults(
    scopes=["et", "mt", "tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    PreselVsEleTauID_2 = Producer(
        input=[Quantity("id_tau_vsEle_{presel_vsele_wp}_2")], output=[q.selcut_presel_vsele_2]
    )
    PreselVsMuTauID_2 = Producer(
        input=[Quantity("id_tau_vsMu_{presel_vsmu_wp}_2")], output=[q.selcut_presel_vsmu_2]
    )

with defaults(
    scopes=["tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    PreselVsEleTauID_1 = Producer(
        input=[Quantity("id_tau_vsEle_{presel_vsele_wp}_1")], output=[q.selcut_presel_vsele_1]
    )
    PreselVsMuTauID_1 = Producer(
        input=[Quantity("id_tau_vsMu_{presel_vsmu_wp}_1")], output=[q.selcut_presel_vsmu_1]
    )


##############################################################################
# preselection: kinematics, trigger and jet veto map
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em"]):
    # offline lepton/tau pt thresholds matching the trigger turn-on plateau
    PreselLepPt_1 = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {presel_lep_pt_1})''',
        input=[q.pt_1],
        output=[q.selcut_presel_lep_pt_1],
    )
    PreselLepPt_2 = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {presel_lep_pt_2})''',
        input=[q.pt_2],
        output=[q.selcut_presel_lep_pt_2],
    )

    # jet_vetomap == 0
    JetVetoMapFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.jet_vetomap],
        output=[q.selcut_jet_veto],
    )


##############################################################################
# lepton vetoes
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em"]):
    # `extraelec_veto == 0`, `extramuon_veto == 0`, `dilepton_veto = 0`
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

    # (extramuon_veto == 0) && (extraelec_veto == 0) && (dilepton_veto == 0)
    LeptonVetoFlag = Producer(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_no_extraelec, q.selcut_no_extramuon, q.selcut_no_dilepton],
        output=[q.selcut_lepton_veto],
    )
    # !((extramuon_veto == 0) && (extraelec_veto == 0) && (dilepton_veto == 0))
    LeptonVetoInvertedFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.selcut_lepton_veto],
        output=[q.selcut_lepton_veto_inv],
    )


##############################################################################
# tau vs jet ID: isolated / non-isolated / anti-isolated legs
##############################################################################

with defaults(
    scopes=["et", "mt", "tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    TauIsoFlag_2 = Producer(
        input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2")], output=[q.selcut_tau_iso_2]
    )
    TauVVVLooseFlag_2 = Producer(
        input=[Quantity("id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_2")],
        output=[q.selcut_tau_vvvloose_2],
    )
TauNonIsoFlag_2 = Producer(
    scopes=["et", "mt", "tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
    input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2")],
    output=[q.selcut_tau_noniso_2],
)

with defaults(
    scopes=["tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    TauIsoFlag_1 = Producer(
        input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1")], output=[q.selcut_tau_iso_1]
    )
    TauVVVLooseFlag_1 = Producer(
        input=[Quantity("id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_1")],
        output=[q.selcut_tau_vvvloose_1],
    )
TauNonIsoFlag_1 = Producer(
    scopes=["tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
    input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1")],
    output=[q.selcut_tau_noniso_1],
)


##############################################################################
# light lepton isolation (et, mt, em)
##############################################################################

with defaults(scopes=["et", "mt"], input=[q.iso_1]):
    # `iso_1 < {lep_iso_max}`
    LepIsoFlag = Producer(
        call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_iso],
    )
    # `iso_1 >= {lep_iso_max}`
    LepAntiIsoFlag = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {lep_iso_max})''',
        output=[q.selcut_lep_antiiso],
    )

    # Run 2 QCD region only: `iso_1 >= {lep_iso_min_qcd}` && `iso_1 < {lep_iso_max}`
    LepIsoMinQCDFlag_Run2 = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {lep_iso_min_qcd})''',
        output=[q.selcut_lep_iso_min_qcd_run2],
    )
    LepIsoQCDWindowFlag_Run2 = ProducerGroup(
        call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
        input=[q.selcut_lep_iso],
        output=[q.selcut_lep_iso_qcd_run2],
        subproducers=[LepIsoMinQCDFlag_Run2],
    )

with defaults(scopes=["em"], call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, {lep_iso_max})'''):
    # electron leg (`pt_1`/`iso_1`): `iso_1 < {lep_iso_max}`
    EleIsoFlag_em = Producer(input=[q.iso_1], output=[q.selcut_em_ele_iso])
    # muon leg (`pt_2`/`iso_2`): `iso_2 < {lep_iso_max}`
    MuonIsoFlag_em = Producer(input=[q.iso_2], output=[q.selcut_em_muon_iso])


##############################################################################
# transverse mass and b-tagged jet multiplicity (et, mt)
##############################################################################

with defaults(scopes=["et", "mt"], input=[q.mt_1]):
    # `mt_1 < {mt_cut}`: signal region, ttbar and process fraction regions
    MtBelow70Flag = Producer(
        call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, {mt_cut})''',
        output=[q.selcut_mt_lt_70],
    )
    # QCD region: `mt_1 < {mt_cut_qcd}` (Run 2: 50, Run 3: same as {mt_cut})
    MtBelowQcdCutFlag = Producer(
        call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, {mt_cut_qcd})''',
        output=[q.selcut_mt_lt_qcd],
    )
    # `mt_1 >= {mt_cut}`: the W+jets determination regions
    WjetsMtFlag = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, {mt_cut})''',
        output=[q.selcut_wjets_mt],
    )

with defaults(scopes=["et", "mt"], input=[q.nbtag]):
    NBtagEqZeroFlag = Producer(
        call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
        output=[q.selcut_nbtag_eq_0],
    )
    # ttbar determination regions: `nbtag >= 1`
    TTbarNBtagFlag = Producer(
        call='''event::quantity::MinFlag<int>({df}, {output}, {input}, 1)''',
        output=[q.selcut_ttbar_nbtag],
    )


##############################################################################
# tau pair charge
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"]):
    ChargeProduct = Producer(
        call='''event::quantity::Product<int, int>({df}, {output}, {input})''',
        input=[q.q_1, q.q_2],
        output=[q.selcut_q_prod],
    )

    with defaults(input=[q.selcut_q_prod]):
        # (q_1 * q_2) < 0
        OppositeSignFlag = Producer(
            call='''event::quantity::SmallerFlag<double>({df}, {output}, {input}, 0.0)''',
            output=[q.selcut_os],
        )
        # (q_1 * q_2) > 0
        SameSignFlag = Producer(
            call='''event::quantity::GreaterFlag<double>({df}, {output}, {input}, 0.0)''',
            output=[q.selcut_ss],
        )


##############################################################################
# region masks: preselection, FF calculation/corrections, and the fully
# shifted signal region (SR_mask)
##############################################################################

with defaults(scopes=["et", "mt"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    # leg 1 (lepton) pt is already encoded in `selcut_presel_trigger` itself
    # (the single-lepton trigger flag's own ptcut), so only the tau (leg 2)
    # pt needs a separate flat AND term here
    presel_mask = Producer(
        input=[
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
            q.selcut_presel_lep_pt_2,
            q.selcut_jet_veto,
        ],
        output=[q.presel_mask],
    )
    # Run 2 has no jet veto map, and the trigger+pt requirement is folded
    # into `selcut_presel_trigger` itself (see `build_trigger_pt_or_flag`)
    presel_mask_Run2 = Producer(
        input=[
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
        ],
        output=[q.presel_mask],
    )

    # --- the fully shifted signal region
    _region_inputs = [
        q.selcut_presel_vsele_2,
        q.selcut_presel_vsmu_2,
        q.selcut_presel_trigger,
        q.selcut_presel_lep_pt_2,
        q.selcut_jet_veto,
        q.selcut_tau_iso_2,
        q.selcut_lep_iso,
        q.selcut_mt_lt_70,
        q.selcut_lepton_veto,
        q.selcut_os,
    ]
    SR_mask = Producer(input=_region_inputs, output=[q.SR_mask])

    # Run 2: no jet veto map, and no separate lep-pt term
    _region_inputs_Run2 = [
        inp
        for inp in _region_inputs
        if inp not in (q.selcut_jet_veto, q.selcut_presel_lep_pt_2)
    ]
    SR_mask_Run2 = Producer(input=_region_inputs_Run2, output=[q.SR_mask])

    # --- QCD fake factors ---
    ff_qcd_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_qcd,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_SRlike],
    )
    ff_qcd_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_qcd,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_ARlike],
    )

    # --- W+jets fake factors (and their same-sign QCD estimation) ---
    ff_wjets_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_wjets_mt,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_SRlike],
    )
    ff_wjets_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_wjets_mt,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_ARlike],
    )
    ff_wjets_SRlike_ss = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_wjets_mt,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_SRlike_ss],
    )
    ff_wjets_ARlike_ss = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_wjets_mt,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_ARlike_ss],
    )

    # --- ttbar fake factors: SR/AR (MC), SR-like/AR-like (inverted veto) ---
    ff_ttbar_SR = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_SR],
    )
    ff_ttbar_AR = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_AR],
    )
    ff_ttbar_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto_inv,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_SRlike],
    )
    ff_ttbar_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto_inv,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_ARlike],
    )
    ff_ttbar_SRlike_ss = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto_inv,
            q.selcut_ss,
        ],
        output=[q.ff_ttbar_SRlike_ss],
    )
    ff_ttbar_ARlike_ss = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_ttbar_nbtag,
            q.selcut_lepton_veto_inv,
            q.selcut_ss,
        ],
        output=[q.ff_ttbar_ARlike_ss],
    )

    # --- process fractions ---
    ff_fraction_SR = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_SR],
    )
    ff_fraction_AR = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_AR],
    )

    # --- QCD DR to SR corrections (lepton isolation inverted) ---
    ff_qcd_DR_SR_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_antiiso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_DR_SR_SRlike],
    )
    ff_qcd_DR_SR_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_antiiso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_DR_SR_ARlike],
    )
    ff_qcd_AR_SR_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_antiiso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_AR_SR_SRlike],
    )
    ff_qcd_AR_SR_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_antiiso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_AR_SR_ARlike],
    )

    # --- W+jets DR to SR corrections (and their same-sign variants) ---
    ff_wjets_DR_SR_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_DR_SR_SRlike],
    )
    ff_wjets_DR_SR_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_DR_SR_ARlike],
    )
    ff_wjets_DR_SR_SRlike_ss = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_DR_SR_SRlike_ss],
    )
    ff_wjets_DR_SR_ARlike_ss = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_nbtag_eq_0,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_DR_SR_ARlike_ss],
    )
    ff_wjets_AR_SR_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_AR_SR_SRlike],
    )
    ff_wjets_AR_SR_ARlike = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_wjets_AR_SR_ARlike],
    )
    ff_wjets_AR_SR_SRlike_ss = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_AR_SR_SRlike_ss],
    )
    ff_wjets_AR_SR_ARlike_ss = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_wjets_AR_SR_ARlike_ss],
    )

    # --- Run 2 QCD fake factors: narrower lep iso window, see above ---
    ff_qcd_SRlike_Run2 = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso_qcd_run2,
            q.selcut_mt_lt_qcd,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_SRlike],
    )
    ff_qcd_ARlike_Run2 = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso_qcd_run2,
            q.selcut_mt_lt_qcd,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_ARlike],
    )

    # --- Run 2 ttbar fake factors: no nbtag requirement
    ff_ttbar_SR_Run2 = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_SR],
    )
    ff_ttbar_AR_Run2 = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_AR],
    )
    ff_ttbar_SRlike_Run2 = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto_inv,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_SRlike],
    )
    ff_ttbar_ARlike_Run2 = Producer(
        input=[
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
            q.selcut_lepton_veto_inv,
            q.selcut_os,
        ],
        output=[q.ff_ttbar_ARlike],
    )

with defaults(scopes=["tt"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    # both tau legs' pt are already encoded in `selcut_presel_trigger` itself
    # (the doubletau trigger flag's own p1/p2 ptcuts), so no separate flat
    # lep-pt AND terms are needed here
    presel_mask_tt = Producer(
        input=[
            q.selcut_presel_vsele_1,
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_1,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
            q.selcut_jet_veto,
        ],
        output=[q.presel_mask],
    )
    # Run 2: no jet veto map, and no separate lep-pt terms
    presel_mask_tt_Run2 = Producer(
        input=[
            q.selcut_presel_vsele_1,
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_1,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
        ],
        output=[q.presel_mask],
    )

    # --- the fully shifted signal region ---
    _region_inputs_tt = [
        q.selcut_presel_vsele_1,
        q.selcut_presel_vsele_2,
        q.selcut_presel_vsmu_1,
        q.selcut_presel_vsmu_2,
        q.selcut_presel_trigger,
        q.selcut_jet_veto,
        q.selcut_tau_iso_1,
        q.selcut_tau_iso_2,
        q.selcut_lepton_veto,
        q.selcut_os,
    ]
    SR_mask_tt = Producer(input=_region_inputs_tt, output=[q.SR_mask])

    # Run 2: no jet veto map (only 2018 has a working tt trigger, see
    # `tau_triggersetup.py`, but the swap is unconditional on era < 2022)
    _region_inputs_tt_Run2 = [
        inp for inp in _region_inputs_tt if inp not in (q.selcut_jet_veto,)
    ]
    SR_mask_tt_Run2 = Producer(input=_region_inputs_tt_Run2, output=[q.SR_mask])

    # --- QCD fake factors, leading tau ---
    ff_qcd_SRlike_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_SRlike],
    )
    ff_qcd_ARlike_tt = Producer(
        input=[
            q.selcut_tau_vvvloose_1,
            q.selcut_tau_noniso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_ARlike],
    )

    # --- QCD fake factors, subleading tau ---
    ff_qcd_sub_SRlike_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_sub_SRlike],
    )
    ff_qcd_sub_ARlike_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_sub_ARlike],
    )

    # --- process fractions ---
    ff_fraction_SR_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_SR],
    )
    ff_fraction_AR_tt = Producer(
        input=[
            q.selcut_tau_vvvloose_1,
            q.selcut_tau_noniso_1,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_AR],
    )
    ff_fraction_sub_SR_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_sub_SR],
    )
    ff_fraction_sub_AR_tt = Producer(
        input=[
            q.selcut_tau_noniso_1,
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_fraction_sub_AR],
    )

    # --- DR to SR corrections, leading tau ---
    ff_qcd_DR_SR_SRlike_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_DR_SR_SRlike],
    )
    ff_qcd_DR_SR_ARlike_tt = Producer(
        input=[
            q.selcut_tau_vvvloose_1,
            q.selcut_tau_noniso_1,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_DR_SR_ARlike],
    )
    ff_qcd_AR_SR_SRlike_tt = Producer(
        input=[
            q.selcut_tau_iso_1,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_AR_SR_SRlike],
    )
    ff_qcd_AR_SR_ARlike_tt = Producer(
        input=[
            q.selcut_tau_vvvloose_1,
            q.selcut_tau_noniso_1,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_AR_SR_ARlike],
    )

    # --- DR to SR corrections, subleading tau ---
    ff_qcd_sub_DR_SR_SRlike_tt = Producer(
        input=[
            q.selcut_tau_noniso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_sub_DR_SR_SRlike],
    )
    ff_qcd_sub_DR_SR_ARlike_tt = Producer(
        input=[
            q.selcut_tau_noniso_1,
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_ss,
        ],
        output=[q.ff_qcd_sub_DR_SR_ARlike],
    )
    ff_qcd_sub_AR_SR_SRlike_tt = Producer(
        input=[
            q.selcut_tau_noniso_1,
            q.selcut_tau_iso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_sub_AR_SR_SRlike],
    )
    ff_qcd_sub_AR_SR_ARlike_tt = Producer(
        input=[
            q.selcut_tau_noniso_1,
            q.selcut_tau_vvvloose_2,
            q.selcut_tau_noniso_2,
            q.selcut_lepton_veto,
            q.selcut_os,
        ],
        output=[q.ff_qcd_sub_AR_SR_ARlike],
    )


# ---------------------------------------------------------------------------
# em -- only the signal region mask; no presel_mask, no fake factor regions
# (no jet->tau fake background in em)
# ---------------------------------------------------------------------------

with defaults(scopes=["em"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    _region_inputs_em = [
        q.selcut_presel_lep_pt_1,
        q.selcut_presel_lep_pt_2,
        q.selcut_presel_trigger,
        q.selcut_jet_veto,
        q.selcut_em_ele_iso,
        q.selcut_em_muon_iso,
        q.selcut_lepton_veto,
        q.selcut_os,
    ]
    SR_mask_em = Producer(input=_region_inputs_em, output=[q.SR_mask])

    # Run 2: no jet veto map, and no separate lep-pt terms
    _region_inputs_em_Run2 = [
        inp
        for inp in _region_inputs_em
        if inp not in (q.selcut_jet_veto, q.selcut_presel_lep_pt_1, q.selcut_presel_lep_pt_2)
    ]
    SR_mask_em_Run2 = Producer(input=_region_inputs_em_Run2, output=[q.SR_mask])

# era-dependent (run2/run3) SwitchProducers, used by selection_friends.py via `.get(era)`
class PreselMaskSwitch(SwitchProducer):
    run2 = presel_mask_Run2
    run3 = presel_mask

class SRMaskSwitch(SwitchProducer):
    run2 = SR_mask_Run2
    run3 = SR_mask

class FFQcdSRlikeSwitch(SwitchProducer):
    run2 = ff_qcd_SRlike_Run2
    run3 = ff_qcd_SRlike

class FFQcdARlikeSwitch(SwitchProducer):
    run2 = ff_qcd_ARlike_Run2
    run3 = ff_qcd_ARlike

class FFTtbarSRSwitch(SwitchProducer):
    run2 = ff_ttbar_SR_Run2
    run3 = ff_ttbar_SR

class FFTtbarARSwitch(SwitchProducer):
    run2 = ff_ttbar_AR_Run2
    run3 = ff_ttbar_AR

class FFTtbarSRlikeSwitch(SwitchProducer):
    run2 = ff_ttbar_SRlike_Run2
    run3 = ff_ttbar_SRlike

class FFTtbarARlikeSwitch(SwitchProducer):
    run2 = ff_ttbar_ARlike_Run2
    run3 = ff_ttbar_ARlike

class PreselMaskTTSwitch(SwitchProducer):
    run2 = presel_mask_tt_Run2
    run3 = presel_mask_tt

class SRMaskTTSwitch(SwitchProducer):
    run2 = SR_mask_tt_Run2
    run3 = SR_mask_tt

class SRMaskEMSwitch(SwitchProducer):
    run2 = SR_mask_em_Run2
    run3 = SR_mask_em


def build_trigger_pt_or_flag(scope, flagnames, output, pt1_max_by_flag=None, pt2_min_param=None):
    """OR of HLT-path legs for a Run 2 friend-tree trigger flag; `flagnames` is a list of already-produced ntuple branches.
    The leg's own object (`pt_1`) is already cut on by the flag itself (see `matchParticle` in `src/triggers.cxx`);
    `pt1_max_by_flag` (per-flag upper `pt_1` bound, only et 2017) and `pt2_min_param` (a config-parameter name for the
    other leg's offline pt, added via `add_config_parameters`) cover the bounds the flag itself can't express."""
    pt1_max_by_flag = pt1_max_by_flag or {}
    producers = []
    leg_outputs = []
    for i, flagname in enumerate(flagnames):
        leg = f"PreselTriggerPtLeg_{scope}_{i}"
        terms = []

        flag_output = [Quantity(f"{leg}_flag")]
        producers.append(
            _RawProducer(
                name=f"{leg}_flag",
                call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 1)''',
                input=[Quantity(flagname)],
                output=flag_output,
                scopes=[scope],
            )
        )
        terms.append(flag_output[0])

        pt1_max = pt1_max_by_flag.get(flagname)
        if pt1_max is not None:
            bound_output = [Quantity(f"{leg}_pt1max")]
            producers.append(
                _RawProducer(
                    name=f"{leg}_pt1max",
                    call=f'''event::quantity::SmallerFlag<float>({{df}}, {{output}}, {{input}}, {pt1_max})''',
                    input=[q.pt_1],
                    output=bound_output,
                    scopes=[scope],
                )
            )
            terms.append(bound_output[0])

        if pt2_min_param is not None:
            bound_output = [Quantity(f"{leg}_pt2min")]
            producers.append(
                _RawProducer(
                    name=f"{leg}_pt2min",
                    call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {%s})''' % pt2_min_param,
                    input=[q.pt_2],
                    output=bound_output,
                    scopes=[scope],
                )
            )
            terms.append(bound_output[0])

        leg_output = [Quantity(f"{leg}_all")]
        producers.append(
            _RawProducer(
                name=f"{leg}_all",
                call='''event::CombineFlags({df}, {output}, {input}, "all_of")''',
                input=terms,
                output=leg_output,
                scopes=[scope],
            )
        )
        leg_outputs.append(leg_output[0])

    producers.append(
        _RawProducer(
            name=f"PreselTriggerPtOr_{scope}",
            call='''event::CombineFlags({df}, {output}, {input}, "any_of")''',
            input=leg_outputs,
            output=output,
            scopes=[scope],
        )
    )
    return producers


##############################################################################
# ee, mm: friend-tree signal region mask only (OS + single-lepton trigger OR);
# no fake factor regions. Era-dependent trigger flag lists live in
# tau_triggersetup.py; the underlying HLT flag columns are produced and
# written to the ntuple by the main-tree trigger producers in producers/triggers.py.
##############################################################################


def build_trigger_or_flag(scope, flagnames, output):
    """Any-of combination of the scope's HLT trigger flags, read by name from the ntuple."""
    return _RawProducer(
        name=f"TriggerOrFlag_{scope}",
        call='''event::CombineFlags({df}, {output}, {input}, "any_of")''',
        input=[Quantity(name) for name in flagnames],
        output=output,
        scopes=[scope],
    )


with defaults(scopes=["mm"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    SR_mask_mm = Producer(
        input=[q.selcut_os, q.selcut_presel_trigger], output=[q.SR_mask]
    )

with defaults(scopes=["ee"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    SR_mask_ee = Producer(
        input=[q.selcut_os, q.selcut_presel_trigger], output=[q.SR_mask]
    )
