from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, defaults

with defaults(scopes=["mt", "et"]):
    RawFakeFactors_sm_lt = Producer(
        call='''fakefactors::sm::raw_fakefactor_lt(
            {df},
            correctionManager,
            {output},
            {input},
            "{fraction_variation}",
            "{QCD_variation}",
            "{Wjets_variation}",
            "{ttbar_variation}",
            "{file}")''',
        input=[q.pt_2, q.njets, q.deltaR_ditaupair, q.mt_1],
        output=[q.raw_fake_factor_2],
    )
    FakeFactors_sm_lt = Producer(
        call='''fakefactors::sm::fakefactor_lt(
            {df},
            correctionManager,
            {output},
            {input},
            "{fraction_variation}",
            "{QCD_variation}",
            "{Wjets_variation}",
            "{ttbar_variation}",
            "{QCD_DR_SR_correction}",
            "{QCD_non_closure_correction}",
            "{Wjets_DR_SR_correction}",
            "{Wjets_non_closure_correction}",
            "{ttbar_non_closure_correction}",
            "{file}",
            "{corr_file}")''',
        input=[
            q.pt_2,
            q.njets,
            q.deltaR_ditaupair,
            q.mt_1,
            q.m_vis,
            q.pt_1,
            q.tau_decaymode_2,
            q.iso_1,
            q.mass_2,
        ],
        output=[q.fake_factor_2],
    )
    FakeFactors_sm_lt_split_info = Producer(
        call='''fakefactors::sm::fakefactor_lt_split_info(
            {df},
            correctionManager,
            {output_vec},
            {input},
            "{fraction_variation}",
            "{QCD_variation}",
            "{Wjets_variation}",
            "{ttbar_variation}",
            "{QCD_DR_SR_correction}",
            "{QCD_non_closure_correction}",
            "{Wjets_DR_SR_correction}",
            "{Wjets_non_closure_correction}",
            "{ttbar_non_closure_correction}",
            "{file}",
            "{corr_file}")''',
        input=[
            q.pt_2,
            q.njets,
            q.deltaR_ditaupair,
            q.mt_1,
            q.m_vis,
            q.pt_1,
            q.tau_decaymode_2,
            q.iso_1,
            q.mass_2,
        ],
        output=[
            q.raw_qcd_fake_factor_2,
            q.raw_wjets_fake_factor_2,
            q.raw_ttbar_fake_factor_2,
            # ---
            q.qcd_fake_factor_fraction_2,
            q.wjets_fake_factor_fraction_2,
            q.ttbar_fake_factor_fraction_2,
            # ---
            q.qcd_DR_SR_correction_2,
            q.wjets_DR_SR_correction_2,
            q.ttbar_DR_SR_correction_2,
            # ---
            q.qcd_correction_wo_DR_SR_2,
            q.wjets_correction_wo_DR_SR_2,
            q.ttbar_correction_wo_DR_SR_2,
            # ---
            q.qcd_fake_factor_correction_2,
            q.wjets_fake_factor_correction_2,
            q.ttbar_fake_factor_correction_2,
            # ---
            q.qcd_fake_factor_2,
            q.wjets_fake_factor_2,
            q.ttbar_fake_factor_2,
        ],
    )

with defaults(scopes=["tt"]):
    pass
