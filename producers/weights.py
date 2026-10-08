from ..quantities import output as q
from ..quantities import nanoAODv15 as nanoAOD
from code_generation.helpers import defaults
from code_generation.producer import Producer, ProducerGroup, SwitchProducer
from code_generation.quantity import Quantity

# per-era luminosity in pb^-1; "2025" is 2025+2026 data combined
LUMI_PB = {
    "2016preVFP": 19500.0, "2016postVFP": 16800.0, "2017": 41500.0, "2018": 59830.0,
    "2022preEE": 8086.069205, "2022postEE": 26674.924045,
    "2023preBPix": 17964.217998, "2023postBPix": 9676.737966,
    "2024": 109816.515335, "2025": 135047.093128, "2026": 25148.977841,
}
# 2024/2025/2026 Summer24 campaigns split in half, one per era (EvenIDFilter/OddIDFilter)
MC_CAMPAIGN_SPLIT_FACTOR = {"2024": 2.0, "2025": 2.0, "2026": 2.0}

# {norm_table_path} set by shapes_preparation.py's build_norm_table()
SampleNormalization = Producer(
    call='''event::quantity::SampleNormalization({df}, correctionManager, {output}, "{norm_table_path}")''',
    input=[],
    output=[
        q.crossSectionPerEventWeight, 
        q.numberGeneratedEventsWeight, 
        q.negative_events_fraction
    ],
    scopes=["et", "mt", "tt", "em"],
)

# signal samples: per-bin STXS normalization, family code and per-bin normalized LHE scale weights
STXSNormalization = Producer(
    call='''event::quantity::STXSNormalization({df}, correctionManager, {output}, "{norm_table_path}", {input})''',
    input=[nanoAOD.HTXS_stage1_2_cat_pTjet30GeV, q.lhe_scale_up, q.lhe_scale_down],
    output=[q.stxs_family, q.stxs_norm_weight, q.lhe_scale_norm_up, q.lhe_scale_norm_down],
    scopes=["et", "mt", "tt", "em"],
)

# data/embedding: constant no-op normalization and weight
with defaults(scopes=["et", "mt", "tt", "em"], call='''event::quantity::Define<float>({df}, {output}, 1.0f)''', input=[]):
    ConstantCrossSectionPerEventWeight = Producer(output=[q.crossSectionPerEventWeight])
    ConstantNumberGeneratedEventsWeight = Producer(output=[q.numberGeneratedEventsWeight])
    ConstantNegativeEventsFraction = Producer(output=[q.negative_events_fraction])

with defaults(scopes=["et", "mt", "tt", "em"], call='''event::quantity::Define<double>({df}, {output}, 1.0)''', input=[]):
    ConstantSTXSNormWeight = Producer(output=[q.stxs_norm_weight])

# data/embedding and mm/ee: constant no-op weight
with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"], call='''event::quantity::Define<double>({df}, {output}, 1.0)''', input=[]):
    ConstantWeight = Producer(output=[q.weight])
    ConstantWeightNoBtag = Producer(scopes=["et", "mt", "tt", "em"], output=[q.weight_no_btag])

##############################################################################
# normalization: xsec / nevents * sign(genWeight) / negative fraction * lumi * pileup
##############################################################################

with defaults(scopes=["et", "mt", "tt", "em"]):
    GenWeightSign = Producer(
        call='''event::quantity::NormalizedGenWeightSign({df}, {output}, {input})''',
        input=[nanoAOD.genWeight, q.negative_events_fraction],
        output=[q.weight_gen_sign],
    )
    Lumi = Producer(call='''event::quantity::Define<double>({df}, {output}, {luminosity_pb})''', input=[], output=[q.weight_lumi])
    MCCampaignSplit = Producer(call='''event::quantity::Define<double>({df}, {output}, {mc_campaign_split_factor})''', input=[], output=[q.weight_campaign_split])
    
    with defaults(call='''event::quantity::Product<double,double>({df}, {output}, {input})'''):
        NormXsecNgen = Producer(input=[q.crossSectionPerEventWeight, q.numberGeneratedEventsWeight], output=[q.weight_xsec_ngen])
        NormSigned = Producer(input=[q.weight_xsec_ngen, q.weight_gen_sign], output=[q.weight_norm_signed])
        NormLumi = Producer(input=[q.weight_norm_signed, q.weight_lumi], output=[q.weight_norm_lumi])
        NormStxs = Producer(input=[q.weight_norm_lumi, q.stxs_norm_weight], output=[q.weight_norm_stxs])
        NormPileup = Producer(input=[q.weight_norm_stxs, q.puweight], output=[q.weight_norm_pileup])

##############################################################################
# lepton and tau ID scale factors
##############################################################################

with defaults(scopes=["et", "mt", "tt"]):
    GenuineTau_2 = Producer(call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 5)''', input=[q.gen_match_2], output=[q.weight_genuine_tau_2])
    VsJetSF_2 = Producer(
        call='''event::quantity::Gate<double>({df}, {output}, {input})''',
        input=[q.weight_genuine_tau_2, Quantity("id_wgt_tau_vsJet_{vs_jet_wp}_2")],
        output=[q.weight_vsjet_sf_2],
    )
with defaults(scopes=["tt"]):
    GenuineTau_1 = Producer(call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 5)''', input=[q.gen_match_1], output=[q.weight_genuine_tau_1])
    VsJetSF_1 = Producer(
        call='''event::quantity::Gate<double>({df}, {output}, {input})''',
        input=[q.weight_genuine_tau_1, Quantity("id_wgt_tau_vsJet_{vs_jet_wp}_1")],
        output=[q.weight_vsjet_sf_1],
    )

with defaults(call='''event::quantity::Product<double,double>({df}, {output}, {input})'''):
    with defaults(scopes=["et"]):
        EleID_et = Producer(input=[q.weight_norm_pileup, q.id_wgt_ele_wp90iso_1], output=[q.weight_ele_id])
        VsJet_et = Producer(input=[q.weight_ele_id, q.weight_vsjet_sf_2], output=[q.weight_vsjet_2])
        VsMu_et = Producer(input=[q.weight_vsjet_2, Quantity("id_wgt_tau_vsMu_VLoose_{vs_ele_wp}_2")], output=[q.weight_vsmu_2])
    with defaults(scopes=["mt"]):
        MuID_mt = Producer(input=[q.weight_norm_pileup, q.id_wgt_mu_1], output=[q.weight_mu_id])
        MuIso_mt = Producer(input=[q.weight_mu_id, q.iso_wgt_mu_1], output=[q.weight_mu_iso])
        VsJet_mt = Producer(input=[q.weight_mu_iso, q.weight_vsjet_sf_2], output=[q.weight_vsjet_2])
        VsMu_mt = Producer(input=[q.weight_vsjet_2, Quantity("id_wgt_tau_vsMu_Tight_{vs_ele_wp}_2")], output=[q.weight_vsmu_2])
    with defaults(scopes=["et", "mt"]):
        VsEle_2 = Producer(input=[q.weight_vsmu_2, Quantity("id_wgt_tau_vsEle_{vs_ele_wp}_2")], output=[q.weight_vsele_2])
    with defaults(scopes=["tt"]):
        VsJet_tt_1 = Producer(input=[q.weight_norm_pileup, q.weight_vsjet_sf_1], output=[q.weight_vsjet_1])
        VsJet_tt_2 = Producer(input=[q.weight_vsjet_1, q.weight_vsjet_sf_2], output=[q.weight_vsjet_2])
        VsMu_tt_1 = Producer(input=[q.weight_vsjet_2, Quantity("id_wgt_tau_vsMu_VLoose_{vs_ele_wp}_1")], output=[q.weight_vsmu_1])
        VsMu_tt_2 = Producer(input=[q.weight_vsmu_1, Quantity("id_wgt_tau_vsMu_VLoose_{vs_ele_wp}_2")], output=[q.weight_vsmu_2])
        VsEle_tt_1 = Producer(input=[q.weight_vsmu_2, Quantity("id_wgt_tau_vsEle_{vs_ele_wp}_1")], output=[q.weight_vsele_1])
        VsEle_tt_2 = Producer(input=[q.weight_vsele_1, Quantity("id_wgt_tau_vsEle_{vs_ele_wp}_2")], output=[q.weight_vsele_2])
    with defaults(scopes=["em"]):
        EleID_em = Producer(input=[q.weight_norm_pileup, q.id_wgt_ele_wp90iso_1], output=[q.weight_ele_id])
        MuID_em = Producer(input=[q.weight_ele_id, q.id_wgt_mu_2], output=[q.weight_mu_id])
        MuIso_em = Producer(input=[q.weight_mu_id, q.iso_wgt_mu_2], output=[q.weight_mu_iso])

# producers with a templated input quantity, resolved by shapes_preparation.py
TEMPLATED_QUANTITY_PRODUCERS = [VsJetSF_1, VsJetSF_2, VsMu_et, VsMu_mt, VsEle_2, VsMu_tt_1, VsMu_tt_2, VsEle_tt_1, VsEle_tt_2]

##############################################################################
# trigger and b-tag scale factors (Run 3 only) and the final weight
##############################################################################

with defaults(scopes=["et", "mt", "tt"], call='''event::quantity::Product<double,double>({df}, {output}, {input})'''):
    Trigger_ettt = Producer(input=[q.weight_vsele_2, q.trg_wgt], output=[q.weight_trigger])
    # Run 2 has no trigger SF: weight_trigger is the weight entering the reweighting step
    NoTrigger_ettt = Producer(input=[q.weight_vsele_2, q.weight_one], output=[q.weight_trigger])
    Weight_ettt_Run2 = Producer(input=[q.weight_reweighted, q.weight_campaign_split], output=[q.weight])
with defaults(scopes=["em"], call='''event::quantity::Product<double,double>({df}, {output}, {input})'''):
    Trigger_em = Producer(input=[q.weight_mu_iso, q.trg_wgt], output=[q.weight_trigger])
    NoTrigger_em = Producer(input=[q.weight_mu_iso, q.weight_one], output=[q.weight_trigger])
    Weight_em_Run2 = Producer(input=[q.weight_reweighted, q.weight_campaign_split], output=[q.weight])
with defaults(scopes=["et", "mt", "tt", "em"]):
    # process-dependent reweighting: Z pT of the DY-like samples (Run 3), top pT of ttbar, 1 for the others
    ZPtReweight = Producer(call='''event::quantity::Product<double,float>({df}, {output}, {input})''', input=[q.weight_trigger, q.zPtReweightWeight], output=[q.weight_reweighted])
    # top pT: the nominal factor to the power top_pt_exponent (1 nominal, 2 up, 0 down)
    TopPtFactor = Producer(call='''event::quantity::Power<float>({df}, {output}, {input}, {top_pt_exponent})''', input=[q.topPtReweightWeight], output=[q.weight_top_pt])
    TopPtReweight = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_trigger, q.weight_top_pt], output=[q.weight_reweighted])
    ConstantReweight = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_trigger, q.weight_one], output=[q.weight_reweighted])
    ConstantOne = Producer(call='''event::quantity::Define<double>({df}, {output}, 1.0)''', input=[], output=[q.weight_one])
    # signal samples: ggH NNLOPS reweighting of the ggH family (stxs_family 1), then the LHEScaleWeight factor of the shifted nuisance
    IsGGHFamily = Producer(call='''event::quantity::EqualFlag<int>({df}, {output}, {input}, 1)''', input=[q.stxs_family], output=[q.stxs_is_ggh])
    GGHNNLOFactor = Producer(call='''event::quantity::Gate<double>({df}, {output}, {input})''', input=[q.stxs_is_ggh, q.ggh_NNLO_weight], output=[q.weight_ggh_nnlo])
    GGHReweight = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_trigger, q.weight_ggh_nnlo], output=[q.weight_signal_nnlo])
    LHEScale = Producer(
        call='''event::quantity::STXSLheScale({df}, correctionManager, {output}, "{lhe_scale_table_path}", "{lhe_scale_variation}", {input})''',
        input=[q.stxs_family, nanoAOD.HTXS_stage1_2_cat_pTjet30GeV, q.lhe_scale_norm_up, q.lhe_scale_norm_down],
        output=[q.weight_lhe_scale],
    )
    LHEScaleReweight = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_trigger, q.weight_lhe_scale], output=[q.weight_reweighted])
    LHEScaleReweightGGH = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_signal_nnlo, q.weight_lhe_scale], output=[q.weight_reweighted])
    # weight_no_btag: the weight the b-tag efficiencies are measured with
    NoBtag = Producer(call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_reweighted, q.weight_campaign_split], output=[q.weight_no_btag])
    Btag = Producer(call='''event::quantity::Product<double,float>({df}, {output}, {input})''', input=[q.weight_no_btag, q.btag_weight], output=[q.weight])

_norm = [GenWeightSign, Lumi, MCCampaignSplit, ConstantOne, NormXsecNgen, NormSigned, NormLumi, NormStxs, NormPileup]
_tau_2 = [GenuineTau_2, VsJetSF_2]
_tau_12 = [GenuineTau_1, VsJetSF_1, GenuineTau_2, VsJetSF_2]
_ids = {
    "et": _tau_2 + [EleID_et, VsJet_et, VsMu_et, VsEle_2],
    "mt": _tau_2 + [MuID_mt, MuIso_mt, VsJet_mt, VsMu_mt, VsEle_2],
    "tt": _tau_12 + [VsJet_tt_1, VsJet_tt_2, VsMu_tt_1, VsMu_tt_2, VsEle_tt_1, VsEle_tt_2],
    "em": [EleID_em, MuID_em, MuIso_em],
}
_trigger = {"et": Trigger_ettt, "mt": Trigger_ettt, "tt": Trigger_ettt, "em": Trigger_em}
_no_trigger = {"et": NoTrigger_ettt, "mt": NoTrigger_ettt, "tt": NoTrigger_ettt, "em": NoTrigger_em}
_run2_weight = {"et": Weight_ettt_Run2, "mt": Weight_ettt_Run2, "tt": Weight_ettt_Run2, "em": Weight_em_Run2}


def weight_switches(reweight):
    """Era-switched weight chain per scope; the sample dependent `reweight` producers (which read weight_trigger) are part of the
    groups, right after the trigger step, since the call order inside a group is not visible to producers outside of it."""
    switches = {}
    with defaults(call=None, input=None, output=None):
        for scope in ("et", "mt", "tt", "em"):
            run3 = ProducerGroup(
                name=f"Weight{scope.upper()}_Run3", scopes=[scope],
                subproducers=_norm + _ids[scope] + [_trigger[scope], *reweight, NoBtag, Btag],
            )
            run2 = ProducerGroup(
                name=f"Weight{scope.upper()}_Run2", scopes=[scope],
                subproducers=_norm + _ids[scope] + [_no_trigger[scope], *reweight, _run2_weight[scope]],
            )
            switches[scope] = type(f"Weight{scope.upper()}Switch", (SwitchProducer,), {"run2": run2, "run3": run3})
    return switches
