from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import fakefactors as fakefactors
from .producers import scalefactors as scalefactors
from .producers import pairquantities as pairquantities
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):
    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    # fake factor configurations
    configuration.add_config_parameters(
        ["et"],
        {
            "qcd_ff_variation": "nominal",
            "wjets_ff_variation": "nominal",
            "ttbar_ff_variation": "nominal",
            "fraction_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/fake_factors_et.json.gz",
                }
            ),
            "ff_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/fake_factors_et.json.gz",
                }
            ),
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_taumass_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            "wjets_ff_corr_leppt_variation": "nominal",
            "wjets_ff_corr_taumass_variation": "nominal",
            "wjets_ff_corr_drsr_variation": "nominal",
            "ttbar_ff_corr_leppt_variation": "nominal",
            "ttbar_ff_corr_taumass_variation": "nominal",
            "ff_corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/FF_corrections_et.json.gz",
                }
            ),       
            "qcd_ff_corr_lepmt_variation": "nominal",     
            "ff_corr_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/FF_corrections_et.json.gz",
                }
            ),
            # "pNetXbb_sf_file": EraModifier(
            #     {
            #         "2016preVFP": "",
            #         "2016postVFP": "",
            #         "2017": "",
            #         "2018": "payloads/particleNet/pNet_Xbb_SF_2018.json.gz",
            #     }
            # ),
            # "pNetXbb_sf_variation": "nominal",
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "qcd_ff_variation": "nominal",
            "wjets_ff_variation": "nominal",
            "ttbar_ff_variation": "nominal",
            "fraction_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/fake_factors_mt.json.gz",
                }
            ),
            "ff_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/fake_factors_mt.json.gz",
                }
            ),
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_taumass_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            "wjets_ff_corr_leppt_variation": "nominal",
            "wjets_ff_corr_taumass_variation": "nominal",
            "wjets_ff_corr_drsr_variation": "nominal",
            "ttbar_ff_corr_leppt_variation": "nominal",
            "ttbar_ff_corr_taumass_variation": "nominal",
            "ff_corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/FF_corrections_mt.json.gz",
                }
            ),
            "qcd_ff_corr_lepmt_variation": "nominal",
            "ff_corr_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/FF_corrections_mt.json.gz",
                }
            ),
            # "pNetXbb_sf_file": EraModifier(
            #     {
            #         "2016preVFP": "",
            #         "2016postVFP": "",
            #         "2017": "",
            #         "2018": "payloads/particleNet/pNet_Xbb_SF_2018.json.gz",
            #     }
            # ),
            # "pNetXbb_sf_variation": "nominal",
        },
    )
    configuration.add_config_parameters(
        ["tt"],
        {
            "qcd_ff_variation": "nominal",
            "qcd_subleading_ff_variation": "nominal",
            "ttbar_ff_variation": "nominal",
            "ttbar_subleading_ff_variation": "nominal",
            "fraction_variation": "nominal",
            "fraction_subleading_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/fake_factors_tt.json.gz",
                }
            ),
            "ff_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/fake_factors_tt.json.gz",
                }
            ),
            "qcd_ff_corr_leppt_variation": "nominal",
            "qcd_ff_corr_taumass_variation": "nominal",
            "qcd_ff_corr_drsr_variation": "nominal",
            "qcd_subleading_ff_corr_leppt_variation": "nominal",
            "qcd_subleading_ff_corr_taumass_variation": "nominal",
            "qcd_subleading_ff_corr_drsr_variation": "nominal",
            "ttbar_ff_corr_leppt_variation": "nominal",
            "ttbar_ff_corr_taumass_variation": "nominal",
            "ttbar_subleading_ff_corr_leppt_variation": "nominal",
            "ttbar_subleading_ff_corr_taumass_variation": "nominal",
            "ff_corr_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/resolved/FF_corrections_tt.json.gz",
                }
            ),
            "ff_corr_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/fake_factors/nmssm/2018/boosted/FF_corrections_tt.json.gz",
                }
            ),
            # "pNetXbb_sf_file": EraModifier(
            #     {
            #         "2016preVFP": "",
            #         "2016postVFP": "",
            #         "2017": "",
            #         "2018": "payloads/particleNet/pNet_Xbb_SF_2018.json.gz",
            #     }
            # ),
            # "pNetXbb_sf_variation": "nominal",
        },
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            fakefactors.RawFakeFactors_nmssm_lt,
            fakefactors.FakeFactors_nmssm_lt,
            fakefactors.RawFakeFactors_nmssm_boosted_lt,
            fakefactors.FakeFactors_nmssm_boosted_lt,
            # scalefactors.Xbb_tagging_SF,
            # scalefactors.Xbb_tagging_SF_boosted,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.raw_fake_factor,
            q.fake_factor,
            q.raw_fake_factor_boosted,
            q.fake_factor_boosted,
            # q.pNet_Xbb_weight_flv,
            # q.pNet_Xbb_weight_flv_boosted,
        ],
    )

    configuration.add_producers(
        ["tt"],
        [
            fakefactors.RawFakeFactors_nmssm_tt_1,
            fakefactors.RawFakeFactors_nmssm_tt_2,
            fakefactors.FakeFactors_nmssm_tt_1,
            fakefactors.FakeFactors_nmssm_tt_2,
            fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
            fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
            fakefactors.FakeFactors_nmssm_tt_boosted_1,
            fakefactors.FakeFactors_nmssm_tt_boosted_2,
            # scalefactors.Xbb_tagging_SF,
            # scalefactors.Xbb_tagging_SF_boosted,
        ],
    )

    configuration.add_outputs(
        ["tt"],
        [
            q.raw_fake_factor_1,
            q.raw_fake_factor_2,
            q.fake_factor_1,
            q.fake_factor_2,
            q.raw_fake_factor_boosted_1,
            q.raw_fake_factor_boosted_2,
            q.fake_factor_boosted_1,
            q.fake_factor_boosted_2,
            # q.pNet_Xbb_weight_flv,
            # q.pNet_Xbb_weight_flv_boosted,
        ],
    )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="pNetXbbSFUp",
    #         shift_config={
    #             ("mt", "et", "tt"): {"pNetXbb_sf_variation": "up"},
    #         },
    #         producers={
    #             ("mt", "et", "tt"): {
    #                 scalefactors.Xbb_tagging_SF,
    #                 scalefactors.Xbb_tagging_SF_boosted,
    #             }
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="pNetXbbSFDown",
    #         shift_config={
    #             ("mt", "et", "tt"): {"pNetXbb_sf_variation": "down"},
    #         },
    #         producers={
    #             ("mt", "et", "tt"): {
    #                 scalefactors.Xbb_tagging_SF,
    #                 scalefactors.Xbb_tagging_SF_boosted,
    #             }
    #         },
    #     ),
    #     exclude_samples=["data", "embedding", "embedding_mc"],
    # )
    # configuration.add_modification_rule(
    #     ["et", "mt", "tt"],
    #     RemoveProducer(
    #         producers=[
    #             scalefactors.Xbb_tagging_SF,
    #             scalefactors.Xbb_tagging_SF_boosted,
    #         ],
    #         samples=["data", "embedding"],
    #     ),
    # )
    # QCD FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDFFslopeUncUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFslopeUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFslopeUncDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFslopeUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFnormUncUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFnormUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFnormUncDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFnormUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFmcSubUncUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFmcSubUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFmcSubUncDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_variation": "QCDFFmcSubUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # Wjets FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFslopeUncUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFslopeUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFslopeUncDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFslopeUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFnormUncUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFnormUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFnormUncDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFnormUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFmcSubUncUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFmcSubUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsFFmcSubUncDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_variation": "WjetsFFmcSubUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # ttbar FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFslopeUncUp",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_variation": "ttbarFFslopeUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFslopeUncDown",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_variation": "ttbarFFslopeUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFnormUncUp",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_variation": "ttbarFFnormUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFnormUncDown",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_variation": "ttbarFFnormUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # Process fractions related shifts
    configuration.add_shift(
        SystematicShift(
            name="fracQCDUncUp",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracQCDUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracQCDUncDown",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracQCDUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsUncUp",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracWjetsUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsUncDown",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracWjetsUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarUncUp",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracTTbarUncUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarUncDown",
            shift_config={
                ("et", "mt"): {
                    "fraction_variation": "process_fractionsfracTTbarUncDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.RawFakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.RawFakeFactors_nmssm_boosted_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # QCD FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureLeadingLepPtCorrUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_leppt_variation": "QCDnonClosureLeadingLepPtCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureLeadingLepPtCorrDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_leppt_variation": "QCDnonClosureLeadingLepPtCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureSubleadingTauMassCorrUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_taumass_variation": "QCDnonClosureSubleadingLepMassCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureSubleadingTauMassCorrDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_taumass_variation": "QCDnonClosureSubleadingLepMassCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="QCDClosureLepMTCorrUp",
    #         shift_config={
    #             ("et", "mt"): {
    #                 "qcd_ff_corr_lepmt_variation": "QCDnonClosureLepMTCorrUp",
    #             }
    #         },
    #         producers={
    #             ("et", "mt"): [
    #                 fakefactors.FakeFactors_nmssm_boosted_lt,
    #             ]
    #         },
    #     ),
    # )
    # configuration.add_shift(
    #     SystematicShift(
    #         name="QCDClosureLepMTCorrDown",
    #         shift_config={
    #             ("et", "mt"): {
    #                 "qcd_ff_corr_lepmt_variation": "QCDnonClosureLepMTCorrDown",
    #             }
    #         },
    #         producers={
    #             ("et", "mt"): [
    #                 fakefactors.FakeFactors_nmssm_boosted_lt,
    #             ]
    #         },
    #     ),
    # )
    configuration.add_shift(
        SystematicShift(
            name="QCDDRtoSRCorrUp",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_drsr_variation": "QCDDRtoSRCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDDRtoSRCorrDown",
            shift_config={
                ("et", "mt"): {
                    "qcd_ff_corr_drsr_variation": "QCDDRtoSRCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # Wjets FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="WjetsClosureLeadingLepPtCorrUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_leppt_variation": "WjetsnonClosureLeadingLepPtCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsClosureLeadingLepPtCorrDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_leppt_variation": "WjetsnonClosureLeadingLepPtCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsClosureSubleadingTauMassCorrUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_taumass_variation": "WjetsnonClosureSubleadingLepMassCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsClosureSubleadingTauMassCorrDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_taumass_variation": "WjetsnonClosureSubleadingLepMassCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsDRtoSRCorrUp",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_drsr_variation": "WjetsDRtoSRCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="WjetsDRtoSRCorrDown",
            shift_config={
                ("et", "mt"): {
                    "wjets_ff_corr_drsr_variation": "WjetsDRtoSRCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    # ttbar FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureLeadingLepPtCorrUp",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_corr_leppt_variation": "ttbarnonClosureLeadingLepPtCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureLeadingLepPtCorrDown",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_corr_leppt_variation": "ttbarnonClosureLeadingLepPtCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureSubleadingTauMassCorrUp",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_corr_taumass_variation": "ttbarnonClosureSubleadingLepMassCorrUp",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureSubleadingTauMassCorrDown",
            shift_config={
                ("et", "mt"): {
                    "ttbar_ff_corr_taumass_variation": "ttbarnonClosureSubleadingLepMassCorrDown",
                }
            },
            producers={
                ("et", "mt"): [
                    fakefactors.FakeFactors_nmssm_lt,
                    fakefactors.FakeFactors_nmssm_boosted_lt,
                ]
            },
        ),
    )
    
    ## tt channel
    # QCD FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDFFslopeUncUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFslopeUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFslopeUncDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFslopeUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFnormUncUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFnormUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFnormUncDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFnormUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFmcSubUncUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFmcSubUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDFFmcSubUncDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_variation": "QCDFFmcSubUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    
    # QCD subleading tau FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFslopeUncUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFslopeUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFslopeUncDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFslopeUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFnormUncUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFnormUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFnormUncDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFnormUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFmcSubUncUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFmcSubUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingFFmcSubUncDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_variation": "QCD_subleadingFFmcSubUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    
    # ttbar FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFslopeUncUp",
            shift_config={
                ("tt"): {
                    "ttbar_ff_variation": "ttbarFFslopeUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFslopeUncDown",
            shift_config={
                ("tt"): {
                    "ttbar_ff_variation": "ttbarFFslopeUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFnormUncUp",
            shift_config={
                ("tt"): {
                    "ttbar_ff_variation": "ttbarFFnormUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarFFnormUncDown",
            shift_config={
                ("tt"): {
                    "ttbar_ff_variation": "ttbarFFnormUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    
    # ttbar subleading tau FF related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingFFslopeUncUp",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_variation": "ttbar_subleadingFFslopeUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingFFslopeUncDown",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_variation": "ttbar_subleadingFFslopeUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingFFnormUncUp",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_variation": "ttbar_subleadingFFnormUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingFFnormUncDown",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_variation": "ttbar_subleadingFFnormUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    
    # Process fractions leading tau related shifts
    configuration.add_shift(
        SystematicShift(
            name="fracQCDUncUp",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracQCDUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracQCDUncDown",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracQCDUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsUncUp",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracWjetsUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsUncDown",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracWjetsUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarUncUp",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracTTbarUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarUncDown",
            shift_config={
                ("tt"): {
                    "fraction_variation": "process_fractionsfracTTbarUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    
    # Process fractions subleading tau related shifts
    configuration.add_shift(
        SystematicShift(
            name="fracQCDSubleadingUncUp",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracQCDUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracQCDSubleadingUncDown",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracQCDUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsSubleadingUncUp",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracWjetsUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracWjetsSubleadingUncDown",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracWjetsUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarSubleadingUncUp",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracTTbarUncUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="fracTTbarSubleadingUncDown",
            shift_config={
                ("tt"): {
                    "fraction_subleading_variation": "process_fractions_subleadingfracTTbarUncDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.RawFakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.RawFakeFactors_nmssm_tt_boosted_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    
    ## tt channel
    # QCD FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureSubleadingLepPtCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_leppt_variation": "QCDnonClosureSubleadingLepPtCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureSubleadingLepPtCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_leppt_variation": "QCDnonClosureSubleadingLepPtCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureLeadingTauMassCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_taumass_variation": "QCDnonClosureLeadingLepMassCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDClosureLeadingTauMassCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_taumass_variation": "QCDnonClosureLeadingLepMassCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDDRtoSRCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_drsr_variation": "QCDDRtoSRCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDDRtoSRCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_ff_corr_drsr_variation": "QCDDRtoSRCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    
    # QCD subleading tau FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingClosureLeadingLepPtCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_leppt_variation": "QCD_subleadingnonClosureLeadingLepPtCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingClosureLeadingLepPtCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_leppt_variation": "QCD_subleadingnonClosureLeadingLepPtCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingClosureSubleadingTauMassCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_taumass_variation": "QCD_subleadingnonClosureSubleadingLepMassCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingClosureSubleadingTauMassCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_taumass_variation": "QCD_subleadingnonClosureSubleadingLepMassCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingDRtoSRCorrUp",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_drsr_variation": "QCD_subleadingDRtoSRCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="QCDSubleadingDRtoSRCorrDown",
            shift_config={
                ("tt"): {
                    "qcd_subleading_ff_corr_drsr_variation": "QCD_subleadingDRtoSRCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    
    # ttbar FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureSubleadingLepPtCorrUp",
            shift_config={
                ("tt"): {
                    "ttbar_ff_corr_leppt_variation": "ttbarnonClosureSubleadingLepPtCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureSubleadingLepPtCorrDown",
            shift_config={
                ("tt"): {
                    "ttbar_ff_corr_leppt_variation": "ttbarnonClosureSubleadingLepPtCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureLeadingTauMassCorrUp",
            shift_config={
                ("tt"): {
                    "ttbar_ff_corr_taumass_variation": "ttbarnonClosureLeadingLepMassCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarClosureLeadingTauMassCorrDown",
            shift_config={
                ("tt"): {
                    "ttbar_ff_corr_taumass_variation": "ttbarnonClosureLeadingLepMassCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_1,
                    fakefactors.FakeFactors_nmssm_tt_boosted_1,
                ]
            },
        ),
    )
    
    # ttbar subleading tau FF corrections related shifts
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingClosureLeadingLepPtCorrUp",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_corr_leppt_variation": "ttbar_subleadingnonClosureLeadingLepPtCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingClosureLeadingLepPtCorrDown",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_corr_leppt_variation": "ttbar_subleadingnonClosureLeadingLepPtCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingClosureSubleadingTauMassCorrUp",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_corr_taumass_variation": "ttbar_subleadingnonClosureSubleadingLepMassCorrUp",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )
    configuration.add_shift(
        SystematicShift(
            name="ttbarSubleadingClosureSubleadingTauMassCorrDown",
            shift_config={
                ("tt"): {
                    "ttbar_subleading_ff_corr_taumass_variation": "ttbar_subleadingnonClosureSubleadingLepMassCorrDown",
                }
            },
            producers={
                ("tt"): [
                    fakefactors.FakeFactors_nmssm_tt_2,
                    fakefactors.FakeFactors_nmssm_tt_boosted_2,
                ]
            },
        ),
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
