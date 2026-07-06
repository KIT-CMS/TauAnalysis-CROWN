from ..quantities import output as q
from ..scripts.CROWNWrapper import Producer, defaults


model_inputs_with_nbtag = [
    q.event_parity_float,
    q.nbtag_float,
    q.pt_2,
    q.pt_1,
    q.deltaEta_12j1,
    q.deltaEta_12j2,
    q.deltaEta_1j1,
    q.deltaEta_1j2,
    q.deltaEta_2j1,
    q.deltaEta_2j2,
    q.deltaEta_ditaupair,
    q.deltaEta_jj,
    q.deltaR_12j1,
    q.deltaR_12j2,
    q.deltaR_1j1,
    q.deltaR_1j2,
    q.deltaR_2j1,
    q.deltaR_2j2,
    q.deltaR_ditaupair,
    q.deltaR_jj,
    q.eta_1,
    q.eta_2,
    q.jeta_1,
    q.jeta_2,
    q.jpt_1,
    q.jpt_2,
    q.m_vis,
    q.met,
    q.mjj,
    q.mt_2,
    q.mt_tot,
    q.pt_dijet,
    q.pt_tt,
    q.pt_ttjj,
    q.pt_vis,
    q.m_fastmtt,
    q.pt_fastmtt,
    q.mass_2,
    q.pzetamissvis_float,
    q.tau_decaymode_2_float,
    q.njets_float,
]
model_inputs_without_nbtag = [
    q.event_parity_float,
    q.pt_2,
    q.pt_1,
    q.deltaEta_12j1,
    q.deltaEta_12j2,
    q.deltaEta_1j1,
    q.deltaEta_1j2,
    q.deltaEta_2j1,
    q.deltaEta_2j2,
    q.deltaEta_ditaupair,
    q.deltaEta_jj,
    q.deltaR_12j1,
    q.deltaR_12j2,
    q.deltaR_1j1,
    q.deltaR_1j2,
    q.deltaR_2j1,
    q.deltaR_2j2,
    q.deltaR_ditaupair,
    q.deltaR_jj,
    q.eta_1,
    q.eta_2,
    q.jeta_1,
    q.jeta_2,
    q.jpt_1,
    q.jpt_2,
    q.m_vis,
    q.met,
    q.mjj,
    q.mt_2,
    q.mt_tot,
    q.pt_dijet,
    q.pt_tt,
    q.pt_ttjj,
    q.pt_vis,
    q.m_fastmtt,
    q.pt_fastmtt,
    q.mass_2,
    q.pzetamissvis_float,
    q.tau_decaymode_2_float,
    q.njets_float,
]

model_ff_QCD_input = model_inputs_with_nbtag
model_ff_ttbar_input = model_inputs_with_nbtag
model_fractions_input = model_inputs_with_nbtag
model_DR_SR_correction_QCD_input = model_inputs_with_nbtag
model_ff_Wjets_input = model_inputs_without_nbtag
model_DR_SR_correction_Wjets_input = model_inputs_with_nbtag

classic_non_closure_inputs = [
    q.tau_decaymode_2_float,
    q.deltaEta_ditaupair,
    q.deltaR_ditaupair,
    q.deltaR_1j1,
    q.pt_ttjj,
    q.mass_2,
    q.iso_1,
    q.njets_float,
]


with defaults(scopes=["mt"]):
    with defaults(call='''fakefactors::build_model_input_column({df}, {output}, {input_vec})'''):
        FFModelInput_QCD_lt = Producer(input=model_ff_QCD_input, output=[q.ff_ml_qcd_model_input_2])
        FFModelInput_Wjets_lt = Producer(input=model_ff_Wjets_input, output=[q.ff_ml_wjets_model_input_2])
        FFModelInput_ttbar_lt = Producer(input=model_ff_ttbar_input, output=[q.ff_ml_ttbar_model_input_2])
        FFModelInput_fractions_lt = Producer(input=model_fractions_input, output=[q.ff_ml_fractions_model_input_2])
        FFModelInput_DR_QCD_lt = Producer(input=model_DR_SR_correction_QCD_input, output=[q.ff_ml_dr_qcd_model_input_2])
        FFModelInput_DR_Wjets_lt = Producer(input=model_DR_SR_correction_Wjets_input, output=[q.ff_ml_dr_wjets_model_input_2])
        FFModelInput_NC_lt = Producer(input=classic_non_closure_inputs, output=[q.ff_ml_nc_model_input_2])
    with defaults(
        input=[
            q.pt_2,
            q.ff_ml_qcd_model_input_2,
            q.ff_ml_wjets_model_input_2,
            q.ff_ml_ttbar_model_input_2,
            q.ff_ml_fractions_model_input_2,
            q.ff_ml_dr_qcd_model_input_2,
            q.ff_ml_dr_wjets_model_input_2,
            q.ff_ml_nc_model_input_2,
        ],
    ):
        FakeFactors_ml_lt = Producer(
            call='''fakefactors::ml::fakefactor_lt(
                {df},
                correctionManager,
                onnxSessionManager,  // for now using own onnxSessionManager until the changes are merged
                {output_vec},
                {input},
                // ---
                "{model_ff_QCD}",
                "{model_ff_QCD_Up}",
                "{model_ff_QCD_Down}",
                "{model_ff_QCD_StatUp}",
                "{model_ff_QCD_StatDown}",
                "{model_ff_QCD_NormalizationUp}",
                "{model_ff_QCD_NormalizationDown}",
                "{ff_QCD_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_ff_Wjets}",
                "{model_ff_Wjets_Up}",
                "{model_ff_Wjets_Down}",
                "{model_ff_Wjets_StatUp}",
                "{model_ff_Wjets_StatDown}",
                "{model_ff_Wjets_NormalizationUp}",
                "{model_ff_Wjets_NormalizationDown}",
                "{ff_Wjets_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_ff_ttbar}",
                "{model_ff_ttbar_Up}",
                "{model_ff_ttbar_Down}",
                "{model_ff_ttbar_StatUp}",
                "{model_ff_ttbar_StatDown}",
                "{model_ff_ttbar_NormalizationUp}",
                "{model_ff_ttbar_NormalizationDown}",
                "{ff_ttbar_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_fractions}",
                "{model_fractions_QCD_Up}",
                "{model_fractions_QCD_Down}",
                "{model_fractions_Wjets_Up}",
                "{model_fractions_Wjets_Down}",
                "{model_fractions_ttbar_Up}",
                "{model_fractions_ttbar_Down}",
                "{model_fractions_QCD_StatUp}",
                "{model_fractions_QCD_StatDown}",
                "{model_fractions_Wjets_StatUp}",
                "{model_fractions_Wjets_StatDown}",
                "{model_fractions_ttbar_StatUp}",
                "{model_fractions_ttbar_StatDown}",
                "{ml_fractions_variation}",  // nominal, QCD_Up/Down, Wjets_Up/Down, ttbar_Up/Down, QCD_StatUp/Down, Wjets_StatUp/Down, ttbar_StatUp/Down
                // ---
                "{model_DR_SR_correction_QCD}",
                "{model_DR_SR_correction_QCD_Up}",
                "{model_DR_SR_correction_QCD_Down}",
                "{model_DR_SR_correction_QCD_StatUp}",
                "{model_DR_SR_correction_QCD_StatDown}",
                "{model_DR_SR_correction_QCD_NormalizationUp}",
                "{model_DR_SR_correction_QCD_NormalizationDown}",
                "{QCD_DR_SR_correction_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_DR_SR_correction_Wjets}",
                "{model_DR_SR_correction_Wjets_Up}",
                "{model_DR_SR_correction_Wjets_Down}",
                "{model_DR_SR_correction_Wjets_StatUp}",
                "{model_DR_SR_correction_Wjets_StatDown}",
                "{model_DR_SR_correction_Wjets_NormalizationUp}",
                "{model_DR_SR_correction_Wjets_NormalizationDown}",
                "{Wjets_DR_SR_correction_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{QCD_non_closure_correction}",
                "{Wjets_non_closure_correction}",
                "{ttbar_non_closure_correction}",
                "{corr_file}",
                false
            )''',
            output=[q.fake_factor_2],
        )
        FakeFactors_ml_lt_split_info = Producer(
            call='''fakefactors::ml::fakefactor_lt(
                {df},
                correctionManager,
                onnxSessionManager,  // for now using own onnxSessionManager until the changes are merged
                {output_vec},
                {input},
                // ---
                "{model_ff_QCD}",
                "{model_ff_QCD_Up}",
                "{model_ff_QCD_Down}",
                "{model_ff_QCD_StatUp}",
                "{model_ff_QCD_StatDown}",
                "{model_ff_QCD_NormalizationUp}",
                "{model_ff_QCD_NormalizationDown}",
                "{ff_QCD_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_ff_Wjets}",
                "{model_ff_Wjets_Up}",
                "{model_ff_Wjets_Down}",
                "{model_ff_Wjets_StatUp}",
                "{model_ff_Wjets_StatDown}",
                "{model_ff_Wjets_NormalizationUp}",
                "{model_ff_Wjets_NormalizationDown}",
                "{ff_Wjets_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_ff_ttbar}",
                "{model_ff_ttbar_Up}",
                "{model_ff_ttbar_Down}",
                "{model_ff_ttbar_StatUp}",
                "{model_ff_ttbar_StatDown}",
                "{model_ff_ttbar_NormalizationUp}",
                "{model_ff_ttbar_NormalizationDown}",
                "{ff_ttbar_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_fractions}",
                "{model_fractions_QCD_Up}",
                "{model_fractions_QCD_Down}",
                "{model_fractions_Wjets_Up}",
                "{model_fractions_Wjets_Down}",
                "{model_fractions_ttbar_Up}",
                "{model_fractions_ttbar_Down}",
                "{model_fractions_QCD_StatUp}",
                "{model_fractions_QCD_StatDown}",
                "{model_fractions_Wjets_StatUp}",
                "{model_fractions_Wjets_StatDown}",
                "{model_fractions_ttbar_StatUp}",
                "{model_fractions_ttbar_StatDown}",
                "{ml_fractions_variation}",  // nominal, QCD_Up/Down, Wjets_Up/Down, ttbar_Up/Down, QCD_StatUp/Down, Wjets_StatUp/Down, ttbar_StatUp/Down
                // ---
                "{model_DR_SR_correction_QCD}",
                "{model_DR_SR_correction_QCD_Up}",
                "{model_DR_SR_correction_QCD_Down}",
                "{model_DR_SR_correction_QCD_StatUp}",
                "{model_DR_SR_correction_QCD_StatDown}",
                "{model_DR_SR_correction_QCD_NormalizationUp}",
                "{model_DR_SR_correction_QCD_NormalizationDown}",
                "{QCD_DR_SR_correction_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{model_DR_SR_correction_Wjets}",
                "{model_DR_SR_correction_Wjets_Up}",
                "{model_DR_SR_correction_Wjets_Down}",
                "{model_DR_SR_correction_Wjets_StatUp}",
                "{model_DR_SR_correction_Wjets_StatDown}",
                "{model_DR_SR_correction_Wjets_NormalizationUp}",
                "{model_DR_SR_correction_Wjets_NormalizationDown}",
                "{Wjets_DR_SR_correction_variation}",  // nominal, Up, Down, StatUp, StatDown
                // ---
                "{QCD_non_closure_correction}",
                "{Wjets_non_closure_correction}",
                "{ttbar_non_closure_correction}",
                "{corr_file}",
                true
            )''',
            output=[
                q.fake_factor_2,
                q.raw_qcd_fake_factor_2,
                q.raw_wjets_fake_factor_2,
                q.raw_ttbar_fake_factor_2,
                q.qcd_fake_factor_fraction_2,
                q.wjets_fake_factor_fraction_2,
                q.ttbar_fake_factor_fraction_2,
                q.qcd_DR_SR_correction_2,
                q.wjets_DR_SR_correction_2,
                q.ttbar_DR_SR_correction_2,
                q.qcd_correction_wo_DR_SR_2,
                q.wjets_correction_wo_DR_SR_2,
                q.ttbar_correction_wo_DR_SR_2,
                q.qcd_fake_factor_correction_2,
                q.wjets_fake_factor_correction_2,
                q.ttbar_fake_factor_correction_2,
                q.qcd_fake_factor_2,
                q.wjets_fake_factor_2,
                q.ttbar_fake_factor_2,
            ],
        )
