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

# data/embedding: constant no-op normalization and weight
with defaults(scopes=["et", "mt", "tt", "em"], call='''event::quantity::Define<float>({df}, {output}, 1.0f)''', input=[]):
    ConstantCrossSectionPerEventWeight = Producer(output=[q.crossSectionPerEventWeight])
    ConstantNumberGeneratedEventsWeight = Producer(output=[q.numberGeneratedEventsWeight])
    ConstantNegativeEventsFraction = Producer(output=[q.negative_events_fraction])

# data/embedding and mm/ee: constant no-op weight
with defaults(scopes=["et", "mt", "tt", "em", "mm", "ee"], call='''event::quantity::Define<double>({df}, {output}, 1.0)''', input=[]):
    ConstantWeight = Producer(output=[q.weight])

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
        NormPileup = Producer(input=[q.weight_norm_lumi, q.puweight], output=[q.weight_norm_pileup])

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
    Weight_ettt_Run2 = Producer(input=[q.weight_vsele_2, q.weight_campaign_split], output=[q.weight])
with defaults(scopes=["em"], call='''event::quantity::Product<double,double>({df}, {output}, {input})'''):
    Trigger_em = Producer(input=[q.weight_mu_iso, q.trg_wgt], output=[q.weight_trigger])
    Weight_em_Run2 = Producer(input=[q.weight_mu_iso, q.weight_campaign_split], output=[q.weight])
with defaults(scopes=["et", "mt", "tt", "em"]):
    Btag = Producer(call='''event::quantity::Product<double,float>({df}, {output}, {input})''', input=[q.weight_trigger, q.btag_weight], output=[q.weight_btag])
    Weight_Run3 = Producer(
        call='''event::quantity::Product<double,double>({df}, {output}, {input})''', input=[q.weight_btag, q.weight_campaign_split], output=[q.weight]
    )

with defaults(call=None, input=None, output=None):
    with defaults(scopes=["et"]):
        _norm = [GenWeightSign, Lumi, MCCampaignSplit, NormXsecNgen, NormSigned, NormLumi, NormPileup]
        _tau_2 = [GenuineTau_2, VsJetSF_2]
        WeightET_Run3 = ProducerGroup(subproducers=_norm + _tau_2 + [EleID_et, VsJet_et, VsMu_et, VsEle_2, Trigger_ettt, Btag, Weight_Run3])
        WeightET_Run2 = ProducerGroup(subproducers=_norm + _tau_2 + [EleID_et, VsJet_et, VsMu_et, VsEle_2, Weight_ettt_Run2])
    with defaults(scopes=["mt"]):
        WeightMT_Run3 = ProducerGroup(subproducers=_norm + _tau_2 + [MuID_mt, MuIso_mt, VsJet_mt, VsMu_mt, VsEle_2, Trigger_ettt, Btag, Weight_Run3])
        WeightMT_Run2 = ProducerGroup(subproducers=_norm + _tau_2 + [MuID_mt, MuIso_mt, VsJet_mt, VsMu_mt, VsEle_2, Weight_ettt_Run2])
    with defaults(scopes=["tt"]):
        _tau_12 = [GenuineTau_1, VsJetSF_1, GenuineTau_2, VsJetSF_2]
        _ids_tt = [VsJet_tt_1, VsJet_tt_2, VsMu_tt_1, VsMu_tt_2, VsEle_tt_1, VsEle_tt_2]
        WeightTT_Run3 = ProducerGroup(subproducers=_norm + _tau_12 + _ids_tt + [Trigger_ettt, Btag, Weight_Run3])
        WeightTT_Run2 = ProducerGroup(subproducers=_norm + _tau_12 + _ids_tt + [Weight_ettt_Run2])
    with defaults(scopes=["em"]):
        WeightEM_Run3 = ProducerGroup(subproducers=_norm + [EleID_em, MuID_em, MuIso_em, Trigger_em, Btag, Weight_Run3])
        WeightEM_Run2 = ProducerGroup(subproducers=_norm + [EleID_em, MuID_em, MuIso_em, Weight_em_Run2])

class WeightETSwitch(SwitchProducer):
    run2 = WeightET_Run2
    run3 = WeightET_Run3

class WeightMTSwitch(SwitchProducer):
    run2 = WeightMT_Run2
    run3 = WeightMT_Run3

class WeightTTSwitch(SwitchProducer):
    run2 = WeightTT_Run2
    run3 = WeightTT_Run3

class WeightEMSwitch(SwitchProducer):
    run2 = WeightEM_Run2
    run3 = WeightEM_Run3
