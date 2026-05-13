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
        q.tau_decaymode_2,
        q.mass_2,
        q.eta_2,
        q.pt_1,
        # q.jpt_1,
        # q.jpt_2,
        q.deltaR_ditaupair,
        q.deltaR_1j1,
        q.pt_ttjj,
        q.met,
        q.m_vis,
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
        q.njets,
        q.m_vis,
        q.tau_decaymode_1,
        q.tau_decaymode_2,
        q.mass_1,
        q.mass_2,
        q.eta_1,
        q.eta_2,
        # q.jpt_1,
        # q.jpt_2,
        q.deltaR_ditaupair,
        q.deltaR_1j1,
        q.deltaR_2j1,
        q.pt_ttjj,
        q.met,
        q.pt_tt,
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