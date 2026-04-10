from ..quantities import output as q
from ..scripts.CROWNWrapper import Producer, defaults


with defaults(scopes=["mt", "et"]):
    with defaults(call='''fakefactors::build_model_input_column({df}, {output}, {input_vec})'''):
        FFInput_Wjets_2018_mt = Producer(input=[q.pt_2, q.njets_float, q.pt_1], output=[q.ff_sm_wjets_model_input_2])
        with defaults(input=[q.pt_2, q.njets_float]):
            FFInput_QCD_2018_mt = Producer(output=[q.ff_sm_qcd_model_input_2])
            FFInput_ttbar_2018_mt = Producer(output=[q.ff_sm_ttbar_model_input_2])
        with defaults(input=[q.mt_1, q.njets_float]):
            FFInput_fractions_2018_mt = Producer(output=[q.ff_sm_fractions_model_input_2])
            FFInput_DR_QCD_2018_mt = Producer(output=[q.ff_sm_dr_qcd_model_input_2])
            FFInput_DR_Wjets_2018_mt = Producer(output=[q.ff_sm_dr_wjets_model_input_2])
        with defaults(
            input=[
                q.tau_decaymode_2_float,
                q.eta_1,
                q.eta_2,
                q.jeta_1,
                q.jeta_2,
                q.jpt_1,
                q.jpt_2,
                q.met,
                q.pt_tt,
                q.deltaEta_ditaupair,
                q.deltaR_ditaupair,
                q.deltaR_1j1,
                q.deltaR_12j1,
                q.pt_ttjj,
                q.mass_2,
                q.mt_tot,
                q.m_vis,
                q.iso_1,
                q.njets_float,
            ],
        ):
            FFInput_NC_QCD_2018_mt = Producer(output=[q.ff_sm_nc_qcd_model_input_2])
            FFInput_NC_Wjets_2018_mt = Producer(output=[q.ff_sm_nc_wjets_model_input_2])
            FFInput_NC_ttbar_2018_mt = Producer(output=[q.ff_sm_nc_ttbar_model_input_2])

    RawFakeFactors_sm_2018_mt = Producer(
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
        input=[
            q.pt_2,
            q.ff_sm_qcd_model_input_2,
            q.ff_sm_wjets_model_input_2,
            q.ff_sm_ttbar_model_input_2,
            q.ff_sm_fractions_model_input_2,
        ],
        output=[q.raw_fake_factor_2],
    )
    with defaults(
        input=[
                q.pt_2,
                q.ff_sm_qcd_model_input_2,
                q.ff_sm_wjets_model_input_2,
                q.ff_sm_ttbar_model_input_2,
                q.ff_sm_fractions_model_input_2,
                q.ff_sm_dr_qcd_model_input_2,
                q.ff_sm_dr_wjets_model_input_2,
                q.ff_sm_nc_qcd_model_input_2,
                q.ff_sm_nc_wjets_model_input_2,
                q.ff_sm_nc_ttbar_model_input_2,
        ],
    ):
        FakeFactors_sm_lt = Producer(
            call='''fakefactors::sm::fakefactor_lt(
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
        FakeFactors_sm_lt_split_info = Producer(
            call='''fakefactors::sm::fakefactor_lt(
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
                true)''',
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
