from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

RawFakeFactors_nmssm_lt = Producer(
    name="RawFakeFactors_nmssm_lt",
    call='fakefactors::raw_fakefactor_nmssm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.nbtag,
    ],
    output=[q.raw_fake_factor],
    scopes=["mt", "et"],
)
RawFakeFactors_nmssm_tt_1 = Producer(
    name="RawFakeFactors_nmssm_tt_1",
    call='fakefactors::raw_fakefactor_nmssm_tt({df}, {output}, 0, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
    ],
    output=[q.raw_fake_factor_1],
    scopes=["tt"],
)
RawFakeFactors_nmssm_tt_2 = Producer(
    name="RawFakeFactors_nmssm_tt_2",
    call='fakefactors::raw_fakefactor_nmssm_tt({df}, {output}, 1, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
    ],
    output=[q.raw_fake_factor_2],
    scopes=["tt"],
)
FakeFactors_nmssm_tt_1 = Producer(
    name="FakeFactors_nmssm_tt_1",
    call='fakefactors::fakefactor_nmssm_tt({df}, {output}, 0, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.fake_factor_1],
    scopes=["tt"],
)
FakeFactors_nmssm_tt_2 = Producer(
    name="FakeFactors_nmssm_tt_2",
    call='fakefactors::fakefactor_nmssm_tt({df}, {output}, 1, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.fake_factor_2],
    scopes=["tt"],
)

FakeFactors_nmssm_lt = Producer(
    name="FakeFactors_nmssm_lt",
    call='fakefactors::fakefactor_nmssm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.nbtag,
        q.pt_1,
        q.iso_1,
        q.m_vis,
    ],
    output=[q.fake_factor],
    scopes=["mt", "et"],
)

RawFakeFactors_sm_lt = Producer(
    name="RawFakeFactors_sm_lt",
    call='fakefactors::raw_fakefactor_sm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.deltaR_ditaupair,
    ],
    output=[q.raw_fake_factor, q.raw_qcd_fake_factor, q.raw_wjets_fake_factor, q.raw_ttbar_fake_factor],
    scopes=["mt", "et"],
)
FakeFactors_sm_lt = Producer(
    name="FakeFactors_sm_lt",
    call='fakefactors::fakefactor_sm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.pt_1,
        q.iso_1,
        q.m_vis,
        q.deltaR_ditaupair,
    ],
    output=[q.fake_factor, q.qcd_fake_factor, q.wjets_fake_factor, q.ttbar_fake_factor],
    scopes=["mt", "et"],
)
FakeFactors_sm_lt_nodR = Producer(
    name="FakeFactors_sm_lt_nodR",
    call='fakefactors::fakefactor_sm_lt_no_deltaR({df}, {output}, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.pt_1,
        q.iso_1,
        q.m_vis,
    ],
    output=[q.fake_factor, q.qcd_fake_factor, q.wjets_fake_factor, q.ttbar_fake_factor],
    scopes=["mt", "et"],
)
