from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, defaults

class Inputs:
    raw_fakefactor_lt = [
        q.pt_2, 
        q.njets, 
        q.mt_1,
    ]
    raw_fakefactor_tt = [
        q.pt_1,
        q.pt_2,
        q.njets,
        q.m_vis,
    ]
    
with defaults(scopes=["mt", "et"]):
    with defaults(call='''fakefactors_run3::build_model_input_column({df}, {output}, {input_vec})'''):
        FFInput_lt = Producer(
            input=[q.pt_2, q.njets_float],
            output=[q.ff_input_lt]
            )
        FFInput_fractions_lt = Producer(
            input=[q.mt_1, q.njets_float],
            output=[q.ff_input_fraction_lt]
            )
        FFInput_DR_lt = Producer(
            input=[q.pt_tt, q.njets_float],
            output=[q.ff_input_dr_lt]
            )
        FFInput_NC_lt = Producer(
            input=[
                q.tau_decaymode_2_float,
                q.mass_2,
                q.eta_2,
                q.pt_ttjj,
                q.njets_float,
            ],
            output=[q.ff_input_nc_lt]
            )

    RawFakeFactors_sm_lt = Producer(
        call='''fakefactors_run3::sm::raw_fakefactor_lt(
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
    with defaults(
        input=[
                q.pt_2,
                q.ff_input_lt,
                q.ff_input_fraction_lt,
                q.ff_input_dr_lt,
                q.ff_input_nc_lt,
        ],
    ):
        FakeFactors_sm_lt = Producer(
            call='''fakefactors_run3::sm::fakefactor_lt(
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
                "{corr_file}",
                false)''',
            output=[q.fake_factor_2],
        )
        
with defaults(scopes=["tt"]):
    with defaults(call='''fakefactors_run3::build_model_input_column({df}, {output}, {input_vec})'''):
        FFInput_QCD_tt = Producer(
            input=[q.pt_1, q.njets_float],
            output=[q.ff_input_qcd_tt]
            )
        FFInput_QCDsub_tt = Producer(
            input=[q.pt_2, q.njets_float],
            output=[q.ff_input_qcdsub_tt]
            )
        FFInput_fractions_tt = Producer(
            input=[q.m_vis, q.njets_float],
            output=[q.ff_input_fraction_tt]
            )
        FFInput_DR_tt = Producer(
            input=[q.pt_tt, q.njets_float],
            output=[q.ff_input_dr_tt]
            )
        FFInput_NC_QCD_tt = Producer(
            input=[
                q.tau_decaymode_1_float,
                q.mass_1,
                q.eta_1,
                q.pt_ttjj,
                q.njets_float,
            ],
            output=[q.ff_input_nc_qcd_tt]
            )
        FFInput_NC_QCDsub_tt = Producer(
            input=[
                q.tau_decaymode_2_float,
                q.mass_2,
                q.eta_2,
                q.pt_ttjj,
                q.njets_float,
            ],
            output=[q.ff_input_nc_qcdsub_tt]
            )
        
    with defaults(
        input=Inputs.raw_fakefactor_tt,
    ):
        RawFakeFactors_sm_tt_1 = Producer(
            call='''fakefactors_run3::sm::raw_fakefactor_tt({df}, correctionManager, {output}, 0, {input}, "{QCD_variation}", "{fraction_variation}", "{file}")''',
            output=[q.raw_fake_factor_1],)
        RawFakeFactors_sm_tt_2 = Producer(
            call='''fakefactors_run3::sm::raw_fakefactor_tt({df}, correctionManager, {output}, 1, {input}, "{QCD_subleading_variation}", "{fraction_variation_subleading}", "{file}")''',
            output=[q.raw_fake_factor_2],
        )

    with defaults(
        input=[
                q.pt_1,
                q.pt_2,
                q.ff_input_qcd_tt,
                q.ff_input_qcdsub_tt,
                q.ff_input_fraction_tt,
                q.ff_input_dr_tt,
                q.ff_input_nc_qcd_tt,
                q.ff_input_nc_qcdsub_tt,
        ],
    ):
        FakeFactors_sm_tt_1 = Producer(
            call='''fakefactors_run3::sm::fakefactor_tt(
                    {df},
                    correctionManager,
                    {output_vec},
                    0,
                    {input},
                    "{fraction_variation}",
                    "{QCD_variation}",
                    "{QCD_DR_SR_correction}",
                    "{QCD_non_closure_correction}",
                    "{file}",
                    "{corr_file}",
                    false)''',
            output=[q.fake_factor_1],)
        FakeFactors_sm_tt_2 = Producer(
            call='''fakefactors_run3::sm::fakefactor_tt(
                    {df},
                    correctionManager,
                    {output_vec},
                    1,
                    {input},
                    "{fraction_variation_subleading}",
                    "{QCD_subleading_variation}",
                    "{QCD_subleading_DR_SR_correction}",
                    "{QCD_subleading_non_closure_correction}",
                    "{file}",
                    "{corr_file}",
                    false)''',
            output=[q.fake_factor_2],)