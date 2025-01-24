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
FakeFactors_nmssm_tt_1 = Producer(
    name="FakeFactors_nmssm_tt_1",
    call='''fakefactors::fakefactor_nmssm_tt(
        {df},
        {output},
        0,
        {input},
        "{ff_variation}",
        "{ff_file}",
        "{ff_corr_file}")''',
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

RawFakeFactors_sm_lt = Producer(
    name="RawFakeFactors_sm_lt",
    call='''fakefactors_sm::raw_fakefactor_sm_lt(
        {df},
        correctionManager,
        {output},
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{Wjets_variation}",
        "{ttbar_variation}",
        "{file}")''',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.deltaR_ditaupair,
    ],
    output=[q.raw_fake_factor_2],
    scopes=["mt", "et"],
)
RawFakeFactors_sm_tt_1 = Producer(
    name="RawFakeFactors_sm_tt_1",
    call='''fakefactors_sm::raw_fakefactor_sm_tt(
        {df},
        correctionManager,
        {output},
        0,
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.raw_fake_factor_1],
    scopes=["tt"],
)
RawFakeFactors_sm_tt_2 = Producer(
    name="RawFakeFactors_sm_tt_2",
    call='''fakefactors_sm::raw_fakefactor_sm_tt(
        {df},
        correctionManager,
        {output},
        1,
        {input},
        "{fraction_variation_subleading}",
        "{QCD_subleading_variation}",
        "{file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.raw_fake_factor_2],
    scopes=["tt"],
)

FakeFactors_sm_lt = Producer(
    name="FakeFactors_sm_lt",
    call='''fakefactors_sm::fakefactor_sm_lt(
        {df},
        correctionManager,
        {output},
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{Wjets_variation}",
        "{ttbar_variation}",
        "{QCD_DR_SR_correction}",
        "{QCD_non_closure_leading_lep_pt_correction}",
        "{QCD_non_closure_lep_iso_correction}",
        "{Wjets_DR_SR_correction}",
        "{Wjets_non_closure_leading_lep_pt_correction}",
        "{ttbar_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.deltaR_ditaupair,
        q.m_vis,
        q.pt_1,
        q.iso_1,
    ],
    output=[q.fake_factor_2],
    scopes=["mt", "et"],
)
FakeFactors_sm_tt_1 = Producer(
    name="FakeFactors_sm_tt_1",
    call='''fakefactors_sm::fakefactor_sm_tt(
        {df},
        correctionManager,
        {output},
        0,
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{QCD_DR_SR_correction}",
        "{QCD_non_closure_subleading_lep_pt_correction}",
        "{QCD_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.fake_factor_1],
    scopes=["tt"],
)
FakeFactors_sm_tt_2 = Producer(
    name="FakeFactors_sm_tt_2",
    call='''fakefactors_sm::fakefactor_sm_tt(
        {df},
        correctionManager,
        {output},
        1,
        {input},
        "{fraction_variation_subleading}",
        "{QCD_subleading_variation}",
        "{QCD_subleading_DR_SR_correction}",
        "{QCD_subleading_non_closure_leading_lep_pt_correction}",
        "{QCD_subleading_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[q.fake_factor_2],
    scopes=["tt"],
)

FakeFactors_sm_lt_split_info = Producer(
    name="FakeFactors_sm_lt_split_info",
    call='''fakefactors_sm::fakefactor_sm_lt_split_info(
        {df},
        correctionManager,
        {output_vec},
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{Wjets_variation}",
        "{ttbar_variation}",
        "{QCD_DR_SR_correction}",
        "{QCD_non_closure_leading_lep_pt_correction}",
        "{QCD_non_closure_lep_iso_correction}",
        "{Wjets_DR_SR_correction}",
        "{Wjets_non_closure_leading_lep_pt_correction}",
        "{ttbar_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.deltaR_ditaupair,
        q.m_vis,
        q.pt_1,
        q.iso_1,
    ],
    output=[
        q.qcd_fake_factor_2,
        q.wjets_fake_factor_2,
        q.ttbar_fake_factor_2,
        # ---
        q.raw_qcd_fake_factor_2,
        q.raw_wjets_fake_factor_2,
        q.raw_ttbar_fake_factor_2,
        # ---
        q.qcd_fake_factor_fraction_2,
        q.wjets_fake_factor_fraction_2,
        q.ttbar_fake_factor_fraction_2,
        # ---
        q.qcd_fake_factor_correction_2,
        q.wjets_fake_factor_correction_2,
        q.ttbar_fake_factor_correction_2,
    ],
    scopes=["mt", "et"],
)
FakeFactors_sm_tt_1_split_info = Producer(
    name="FakeFactors_sm_tt_1_split_info",
    call='''fakefactors_sm::fakefactor_sm_tt_split_info(
        {df},
        correctionManager,
        {output_vec},
        0,
        {input},
        "{fraction_variation}",
        "{QCD_variation}",
        "{QCD_DR_SR_correction}",
        "{QCD_non_closure_subleading_lep_pt_correction}",
        "{QCD_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[
        q.qcd_fake_factor_1,
        q.raw_qcd_fake_factor_1,
        q.qcd_fake_factor_fraction_1,
        q.qcd_fake_factor_correction_1,
    ],
    scopes=["tt"],
)
FakeFactors_sm_tt_2_split_info = Producer(
    name="FakeFactors_sm_tt_2_split_info",
    call='''fakefactors_sm::fakefactor_sm_tt_split_info(
        {df},
        correctionManager,
        {output_vec},
        1,
        {input},
        "{fraction_variation_subleading}",
        "{QCD_subleading_variation}",
        "{QCD_subleading_DR_SR_correction}",
        "{QCD_subleading_non_closure_leading_lep_pt_correction}",
        "{QCD_subleading_non_closure_m_vis_correction}",
        "{file}",
        "{corr_file}")''',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ],
    output=[
        q.qcd_fake_factor_2,
        q.raw_qcd_fake_factor_2,
        q.qcd_fake_factor_fraction_2,
        q.qcd_fake_factor_correction_2,
    ],
    scopes=["tt"],
)
