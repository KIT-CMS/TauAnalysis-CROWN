from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, defaults

class Inputs:
    raw_fakefactor_lt = [
        q.pt_2, 
        q.njets, 
        q.mt_1,
    ]
    fakefactor_lt = [
        q.pt_2,
        q.njets,
        q.mt_1,
        q.deltaR_ditaupair,
        q.tau_decaymode_2,
        q.mass_2,
        q.iso_1,
        q.pt_tt,
    ]
    raw_fakefactor_tt = [
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ]
    fakefactor_tt = [
        q.pt_1,
        q.pt_2,
        q.mass_1,
        q.mass_2,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
        q.njets,
        q.deltaR_ditaupair,
        q.pt_tt,
        q.m_vis,
    ]

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
        input=Inputs.raw_fakefactor_lt,
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
        input=Inputs.fakefactor_lt,
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
        input=Inputs.fakefactor_lt,
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
    RawFakeFactors_sm_tt_1 = Producer(
        call='fakefactors::sm::raw_fakefactor_tt({df}, correctionManager, {output}, 0, {input}, "{QCD_variation}", "{fraction_variation}", "{file}")',
        input=Inputs.raw_fakefactor_tt,
        output=[q.raw_fake_factor_1],
    )
    RawFakeFactors_sm_tt_2 = Producer(
        call='fakefactors::sm::raw_fakefactor_tt({df}, correctionManager, {output}, 1, {input}, "{QCD_subleading_variation}", "{fraction_variation_subleading}", "{file}")',
        input=Inputs.raw_fakefactor_tt,
        output=[q.raw_fake_factor_2],
    )

    FakeFactors_sm_tt_1 = Producer(
        call='fakefactors::sm::fakefactor_tt({df}, correctionManager, {output}, 0, {input}, "{QCD_variation}", "{fraction_variation}", "{QCD_non_closure_correction}", "{QCD_DR_SR_correction}", "{file}", "{corr_file}")',
        input=Inputs.fakefactor_tt,
        output=[q.fake_factor_1],
    )
    FakeFactors_sm_tt_2 = Producer(
        call='fakefactors::sm::fakefactor_tt({df}, correctionManager, {output}, 1, {input}, "{QCD_subleading_variation}", "{fraction_variation_subleading}", "{QCD_subleading_non_closure_correction}", "{QCD_subleading_DR_SR_correction}", "{file}", "{corr_file}")',
        input=Inputs.fakefactor_tt,
        output=[q.fake_factor_2],
    )

    FakeFactors_sm_tt_split_info_1 = Producer(
        call='''fakefactors::sm::fakefactor_tt_split_info({df}, correctionManager, {output_vec}, 0, {input}, "{QCD_variation}", "{fraction_variation}", "{QCD_non_closure_correction}", "{QCD_DR_SR_correction}", "{file}", "{corr_file}")''',
        input=Inputs.fakefactor_tt,
        output=[
            q.raw_qcd_fake_factor_1,
            q.qcd_fake_factor_fraction_1,
            q.qcd_DR_SR_correction_1,
            q.qcd_correction_wo_DR_SR_1,
            q.qcd_fake_factor_correction_1,
            q.qcd_fake_factor_1,
        ],
    )
    FakeFactors_sm_tt_split_info_2 = Producer(
        call='''fakefactors::sm::fakefactor_tt_split_info({df}, correctionManager, {output_vec}, 1, {input}, "{QCD_subleading_variation}", "{fraction_variation_subleading}", "{QCD_subleading_non_closure_correction}", "{QCD_subleading_DR_SR_correction}", "{file}", "{corr_file}")''',
        input=Inputs.fakefactor_tt,
        output=[
            q.raw_qcd_fake_factor_2,
            q.qcd_fake_factor_fraction_2,
            q.qcd_DR_SR_correction_2,
            q.qcd_correction_wo_DR_SR_2,
            q.qcd_fake_factor_correction_2,
            q.qcd_fake_factor_2,
        ],
    )
