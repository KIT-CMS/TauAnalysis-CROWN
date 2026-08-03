from ..quantities import output as q
from ..scripts.CROWNWrapper import Producer, ProducerGroup, Quantity, BaseFilter, defaults
from code_generation.producer import Producer as _RawProducer, BaseFilter as _RawBaseFilter
from ..producers import pairquantities as pairquantities
from ..producers import triggers as triggers

##############################################################################
# preselection: hadronic tau requirements
##############################################################################

with defaults(
    scopes=["et", "mt", "tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    # non tau vsJet iso/wp in preselection since ff don't use this
    with defaults(output=[q.selcut_presel_vsele_2]):
        PreselVsEleTauID_2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_2", 1)''',
            input=[pairquantities.VsEleTauIDFlag_2.output_group],
        )
        # Run 2 (nanoAODv9)
        PreselVsEleTauID_2_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_2", 1)''',
            input=[pairquantities.VsEleTauIDFlag_2_v9.output_group],
        )
        PreselVsEleTauID_2_friend = Producer(input=[Quantity("id_tau_vsEle_{presel_vsele_wp}_2")])
    with defaults(output=[q.selcut_presel_vsmu_2]):
        PreselVsMuTauID_2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_2", 1)''',
            input=[pairquantities.VsMuTauIDFlag_2.output_group],
        )
        PreselVsMuTauID_2_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_2", 1)''',
            input=[pairquantities.VsMuTauIDFlag_2_v9.output_group],
        )
        PreselVsMuTauID_2_friend = Producer(input=[Quantity("id_tau_vsMu_{presel_vsmu_wp}_2")])

with defaults(
    scopes=["tt"],
    call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
):
    with defaults(output=[q.selcut_presel_vsele_1]):
        PreselVsEleTauID_1 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_1", 1)''',
            input=[pairquantities.VsEleTauIDFlag_1.output_group],
        )
        PreselVsEleTauID_1_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsEle_{presel_vsele_wp}_1", 1)''',
            input=[pairquantities.VsEleTauIDFlag_1_v9.output_group],
        )
        PreselVsEleTauID_1_friend = Producer(input=[Quantity("id_tau_vsEle_{presel_vsele_wp}_1")])
    with defaults(output=[q.selcut_presel_vsmu_1]):
        PreselVsMuTauID_1 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_1", 1)''',
            input=[pairquantities.VsMuTauIDFlag_1.output_group],
        )
        PreselVsMuTauID_1_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsMu_{presel_vsmu_wp}_1", 1)''',
            input=[pairquantities.VsMuTauIDFlag_1_v9.output_group],
        )
        PreselVsMuTauID_1_friend = Producer(input=[Quantity("id_tau_vsMu_{presel_vsmu_wp}_1")])


##############################################################################
# preselection: kinematics, trigger and jet veto map
##############################################################################

with defaults(scopes=["em"]):
    # `pt_1 > {presel_pt_1}`, the electron of the em channel. The muon leg is
    # covered by the single muon trigger, the electron is not triggered on.
    PreselPt_1 = Producer(
        call='''event::quantity::GreaterFlag<float>({df}, {output}, {input}, {presel_pt_1})''',
        input=[q.pt_1],
        output=[q.selcut_presel_pt_1],
    )

with defaults(scopes=["et", "mt", "tt", "em"]):
    # jet_vetomap == 0
    JetVetoMapFlag = Producer(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 0)''',
        input=[q.jet_vetomap],
        output=[q.selcut_jet_veto],
    )

with defaults(output=[q.selcut_presel_trigger]):
    with defaults(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, "{presel_trigger_flag}", 1)'''
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
    with defaults(
        call='''event::quantity::EqualFlag<bool>({df}, {output}, {input}, 1)'''
    ):
        PreselTriggerFlag_friend = Producer(
            scopes=["et", "mt", "em"],
            input=[Quantity("{presel_trigger_flag}")],
        )
        PreselTriggerFlag_tt_friend = Producer(
            scopes=["tt"],
            input=[Quantity("{presel_trigger_flag}")],
        )


##############################################################################
# lepton vetoes
##############################################################################

with defaults(scopes=["et", "mt", "tt"]):
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

with defaults(scopes=["et", "mt", "tt"]):
    with defaults(output=[q.selcut_tau_iso_2]):
        TauIsoFlag_2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2", 1)''',
            input=[pairquantities.VsJetTauIDFlag_2.output_group],
        )
        # Run 2 (nanoAODv9): see `PreselVsEleTauID_2_Run2` above
        TauIsoFlag_2_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2", 1)''',
            input=[pairquantities.VsJetTauIDFlag_2_v9.output_group],
        )
        TauIsoFlag_2_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2")],
        )
    with defaults(output=[q.selcut_tau_noniso_2]):
        TauNonIsoFlag_2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2", 0)''',
            input=[pairquantities.VsJetTauIDFlag_2.output_group],
        )
        TauNonIsoFlag_2_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2", 0)''',
            input=[pairquantities.VsJetTauIDFlag_2_v9.output_group],
        )
        TauNonIsoFlag_2_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_2")],
        )
    with defaults(output=[q.selcut_tau_vvvloose_2]):
        TauVVVLooseFlag_2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_2", 1)''',
            input=[pairquantities.VsJetTauIDFlagOnly_2.output_group],
        )
        TauVVVLooseFlag_2_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_2", 1)''',
            input=[pairquantities.VsJetTauIDFlagOnly_2_v9.output_group],
        )
        TauVVVLooseFlag_2_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_2")],
        )

with defaults(scopes=["tt"]):
    with defaults(output=[q.selcut_tau_iso_1]):
        TauIsoFlag_1 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1", 1)''',
            input=[pairquantities.VsJetTauIDFlag_1.output_group],
        )
        TauIsoFlag_1_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1", 1)''',
            input=[pairquantities.VsJetTauIDFlag_1_v9.output_group],
        )
        TauIsoFlag_1_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1")],
        )
    with defaults(output=[q.selcut_tau_noniso_1]):
        TauNonIsoFlag_1 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1", 0)''',
            input=[pairquantities.VsJetTauIDFlag_1.output_group],
        )
        TauNonIsoFlag_1_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1", 0)''',
            input=[pairquantities.VsJetTauIDFlag_1_v9.output_group],
        )
        TauNonIsoFlag_1_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 0)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_iso_vsjet_wp}_1")],
        )
    with defaults(output=[q.selcut_tau_vvvloose_1]):
        TauVVVLooseFlag_1 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_1", 1)''',
            input=[pairquantities.VsJetTauIDFlagOnly_1.output_group],
        )
        TauVVVLooseFlag_1_Run2 = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, "id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_1", 1)''',
            input=[pairquantities.VsJetTauIDFlagOnly_1_v9.output_group],
        )
        TauVVVLooseFlag_1_friend = Producer(
            call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''',
            input=[Quantity("id_tau_vsJet_{ff_tau_antiiso_vsjet_wp}_1")],
        )


##############################################################################
# light lepton isolation (et, mt)
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


##############################################################################
# transverse mass and b-tagged jet multiplicity (et, mt)
##############################################################################

with defaults(scopes=["et", "mt"], input=[q.mt_1]):
    # `mt_1 < 70`: QCD (Run 3 only, see `MtBelow50Flag_Run2` below), ttbar and
    # process fraction regions
    MtBelow70Flag = Producer(
        call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, 70.0)''',
        output=[q.selcut_mt_lt_70],
    )
    # Run 2 QCD region only: `mt_1 < 50` 
    MtBelow50Flag_Run2 = Producer(
        call='''event::quantity::SmallerFlag<float>({df}, {output}, {input}, 50.0)''',
        output=[q.selcut_mt_lt_50_qcd_run2],
    )
    # `mt_1 >= 70`: the W+jets determination regions
    WjetsMtFlag = Producer(
        call='''event::quantity::MinFlag<float>({df}, {output}, {input}, 70.0)''',
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
# region masks for preselection, FF calculation and corrections
##############################################################################

with defaults(scopes=["et", "mt"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    presel_mask = Producer(
        input=[
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
            q.selcut_jet_veto,
        ],
        output=[q.presel_mask],
    )
    # Run 2 has no jet veto map
    presel_mask_Run2 = Producer(
        input=[
            q.selcut_presel_vsele_2,
            q.selcut_presel_vsmu_2,
            q.selcut_presel_trigger,
        ],
        output=[q.presel_mask],
    )

    # --- QCD fake factors ---
    ff_qcd_SRlike = Producer(
        input=[
            q.selcut_tau_iso_2,
            q.selcut_lep_iso,
            q.selcut_mt_lt_70,
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
            q.selcut_mt_lt_70,
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
            q.selcut_mt_lt_50_qcd_run2,
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
            q.selcut_mt_lt_50_qcd_run2,
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
    # Run 2: no jet veto map
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
# em -- preselection only, no fake factor regions implemented yet
# ---------------------------------------------------------------------------

with defaults(scopes=["em"], call='''event::CombineFlags({df}, {output}, {input}, "all_of")'''):
    presel_mask_em = Producer(
        input=[
            q.selcut_presel_pt_1,
            q.selcut_presel_trigger,
            q.selcut_jet_veto,
        ],
        output=[q.presel_mask],
    )
    # Run 2: no jet veto map
    presel_mask_em_Run2 = Producer(
        input=[
            q.selcut_presel_pt_1,
            q.selcut_presel_trigger,
        ],
        output=[q.presel_mask],
    )


##############################################################################
# ee, mm: hard OS + trigger cuts
#
# ee/mm carry no fake factor regions (there is no jet->tau fake background to
# measure), so unlike et/mt/tt there is no need to keep the anti-OS / anti-
# trigger / anti-iso events around behind a soft mask: the cuts are baked in
# directly as event filters. The era-dependent flag lists live in
# tau_triggersetup.py; the lepton isolation tightening is a plain config
# parameter change in config.py, not a producer.
##############################################################################


def _quoted_flag_list(flagnames):
    return ", ".join(f'"{name}"' for name in flagnames)


def build_trigger_or_flag(scope, flagnames, output, source_producer):
    call = 'event::CombineFlags({{df}}, {{output}}, {cols}, "any_of")'.format(
        cols=_quoted_flag_list(flagnames)
    )
    return _RawProducer(
        name=f"PreselTriggerFlagAnyOf_{scope}",
        call=call,
        input=[source_producer.output_group],
        output=output,
        scopes=[scope],
    )


def build_trigger_or_filter(scope, flagnames, source_producer):
    call = 'event::filter::Flags({{df}}, "TriggerFilter_{scope}", {cols}, "any_of")'.format(
        scope=scope, cols=_quoted_flag_list(flagnames)
    )
    return _RawBaseFilter(
        name=f"TriggerFilter_{scope}",
        call=call,
        input=[source_producer.output_group],
        scopes=[scope],
    )


with defaults(call='''event::filter::Flags({df}, "OppositeSignFilter", {input}, "all_of")''', input=[q.selcut_os]):
    OppositeSignFilter_mm = BaseFilter(scopes=["mm"])
    OppositeSignFilter_ee = BaseFilter(scopes=["ee"])


##############################################################################
# the opt-in preselection filter
##############################################################################

PreselectionFilter = BaseFilter(
    call='''event::filter::Flag({df}, "PreselectionFilter", {input})''',
    input=[q.presel_mask],
    scopes=["et", "mt", "tt", "em"],
)
