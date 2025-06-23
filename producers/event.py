from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from .electrons import DiElectronVeto
from .muons import DiMuonVeto

from ..scripts.ProducerWrapper import (
    AutoBaseFilter as BaseFilter,
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    AutoVectorProducer as VectorProducer,
    scopes,
)

####################
# Set of general producers for event quantities
####################

with scopes(["global"]):
    RunLumiEventFilter = VectorProducer(
        call='event::filter::Quantity<{RunLumiEventFilter_Quantity_Types}>({df}, "RunLumiEventFilter", "{RunLumiEventFilter_Quantities}", {vec_open}{RunLumiEventFilter_Selections}{vec_close})',
        input=[],
        output=None,
        vec_configs=[
            "RunLumiEventFilter_Quantities",
            "RunLumiEventFilter_Quantity_Types",
            "RunLumiEventFilter_Selections",
        ],
    )
    JSONFilter = BaseFilter(
        call='event::filter::GoldenJSON({df}, correctionManager, "GoldenJSONFilter",  {input}, "{golden_json_file}")',
        input=[nanoAOD.run, nanoAOD.luminosityBlock],
    )
    PrefireWeight = Producer(
        call="event::quantity::Rename<float>({df}, {output}, {input})",
        input=[nanoAOD.prefireWeight],
        output=[q.prefireweight],
    )
    is_data = Producer(
        input=[],
        call="event::quantity::Define({df}, {output}, {is_data})",
        output=[q.is_data],
    )
    is_embedding = Producer(
        call="event::quantity::Define({df}, {output}, {is_embedding})",
        input=[],
        output=[q.is_embedding],
    )
    is_ttbar = Producer(
        call="event::quantity::Define({df}, {output}, {is_ttbar})",
        input=[],
        output=[q.is_ttbar],
    )
    is_dyjets = Producer(
        call="event::quantity::Define({df}, {output}, {is_dyjets})",
        input=[],
        output=[q.is_dyjets],
    )
    is_wjets = Producer(
        call="event::quantity::Define({df}, {output}, {is_wjets})",
        input=[],
        output=[q.is_wjets],
    )
    is_ggh_htautau = Producer(
        call="event::quantity::Define({df}, {output}, {is_ggh_htautau})",
        input=[],
        output=[q.is_ggh_htautau],
    )
    is_vbf_htautau = Producer(
        call="event::quantity::Define({df}, {output}, {is_vbf_htautau})",
        input=[],
        output=[q.is_vbf_htautau],
    )
    is_diboson = Producer(
        call="event::quantity::Define({df}, {output}, {is_diboson})",
        input=[],
        output=[q.is_diboson],
    )
    is_ggh_hbb = Producer(
        call="event::quantity::Define({df}, {output}, {is_ggh_hbb})",
        input=[],
        output=[q.is_ggh_hbb],
    )
    is_vbf_hbb = Producer(
        call="event::quantity::Define({df}, {output}, {is_vbf_hbb})",
        input=[],
        output=[q.is_vbf_hbb],
    )
    is_rem_hbb = Producer(
        call="event::quantity::Define({df}, {output}, {is_rem_hbb})",
        input=[],
        output=[q.is_rem_hbb],
    )
    is_embedding_mc = Producer(
        call="event::quantity::Define({df}, {output}, {is_embedding_mc})",
        input=[],
        output=[q.is_embedding_mc],
    )
    is_singletop = Producer(
        call="event::quantity::Define({df}, {output}, {is_singletop})",
        input=[],
        output=[q.is_singletop],
    )
    is_rem_htautau = Producer(
        call="event::quantity::Define({df}, {output}, {is_rem_htautau})",
        input=[],
        output=[q.is_rem_htautau],
    )
    is_electroweak_boson = Producer(
        call="event::quantity::Define({df}, {output}, {is_electroweak_boson})",
        input=[],
        output=[q.is_electroweak_boson],
    )
    SampleFlags = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            is_data,
            is_embedding,
            is_ttbar,
            is_dyjets,
            is_wjets,
            is_ggh_htautau,
            is_vbf_htautau,
            is_diboson,
            is_ggh_hbb,
            is_vbf_hbb,
            is_rem_hbb,
            is_embedding_mc,
            is_singletop,
            is_rem_htautau,
            is_electroweak_boson,
        ],
    )
    MetFilter = VectorProducer(
        call='event::filter::Flag({df}, "{met_filters}", "{met_filters}")',
        input=[],
        output=None,
        vec_configs=["met_filters"],
    )
    Lumi = Producer(
        call="event::quantity::Rename<UInt_t>({df}, {output}, {input})",
        input=[nanoAOD.luminosityBlock],
        output=[q.lumi],
    )
    npartons = Producer(
        call="event::quantity::Rename<UChar_t>({df}, {output}, {input})",
        input=[nanoAOD.LHE_Njets],
        output=[q.npartons],
    )
    PUweights = Producer(
        call='reweighting::puweights({df}, correctionManager, {output}, {input}, "{PU_reweighting_file}", "{PU_reweighting_era}", "{PU_reweighting_variation}")',
        input=[nanoAOD.Pileup_nTrueInt],
        output=[q.puweight],
    )
    PUweightsFromHistogram = Producer(
        call='reweighting::puweights({df}, {output}, {input}, "{PU_reweighting_file}", "{PU_reweighting_hist}")',
        input=[nanoAOD.Pileup_nTrueInt],
        output=[q.puweight],
    )
    DiLeptonVeto = ProducerGroup(
        call='event::CombineFlags({df}, {output}, {input}, "any_of")',
        input=[],
        output=[q.dilepton_veto],
        subproducers=[DiElectronVeto, DiMuonVeto],
    )

# zptmass not used in 2016preVFP and 2016postVFP atm due to broken file.

with scopes(["global", "em", "et", "mt", "tt", "mm", "ee"]):
    ZPtMassReweighting = Producer(
        call='reweighting::zPtMassReweighting({df}, {output}, {input}, "{zptmass_file}", "{zptmass_functor}", "{zptmass_arguments}")',
        input=[
            q.recoil_genboson_p4_vec,
        ],
        output=[q.ZPtMassReweightWeight],
    )
    TopPtReweighting = Producer(
        call="reweighting::topptreweighting({df}, {output}, {input})",
        input=[
            nanoAOD.GenParticle_pdgId,
            nanoAOD.GenParticle_statusFlags,
            nanoAOD.GenParticle_pt,
        ],
        output=[q.topPtReweightWeight],
    )
    GGH_NNLO_Reweighting = Producer(
        call='htxs::ggHNNLOWeights({df}, {output}, "{ggHNNLOweightsRootfile}", "{ggH_generator}", {input})',
        input=[nanoAOD.HTXS_Higgs_pt, nanoAOD.HTXS_njets30],
        output=[q.ggh_NNLO_weight],
    )
    GGH_WG1_Uncertainties = Producer(
        call="htxs::ggH_WG1_uncertainties({df}, {output_vec}, {input})",
        input=[
            nanoAOD.HTXS_stage_1_pTjet30,
            nanoAOD.HTXS_Higgs_pt,
            nanoAOD.HTXS_njets30,
        ],  # using non-updated stage1 flag required by the used macro
        output=[
            q.THU_ggH_Mu,
            q.THU_ggH_Res,
            q.THU_ggH_Mig01,
            q.THU_ggH_Mig12,
            q.THU_ggH_VBF2j,
            q.THU_ggH_VBF3j,
            q.THU_ggH_PT60,
            q.THU_ggH_PT120,
            q.THU_ggH_qmtop,
        ],
    )
    QQH_WG1_Uncertainties = Producer(
        call="htxs::qqH_WG1_uncertainties({df}, {output_vec}, {input})",
        input=[
            nanoAOD.HTXS_stage1_1_fine_cat_pTjet30GeV
        ],  # using fine stage1.1 flag required by the used macro
        output=[
            q.THU_qqH_TOT,
            q.THU_qqH_PTH200,
            q.THU_qqH_Mjj60,
            q.THU_qqH_Mjj120,
            q.THU_qqH_Mjj350,
            q.THU_qqH_Mjj700,
            q.THU_qqH_Mjj1000,
            q.THU_qqH_Mjj1500,
            q.THU_qqH_25,
            q.THU_qqH_JET01,
        ],
    )
    LHE_Scale_weight = Producer(
        call="reweighting::lhe_scale_weights({df}, {output}, {input}, {muR}, {muF})",
        input=[nanoAOD.LHEScaleWeight],
        output=[q.lhe_scale_weight],
    )
