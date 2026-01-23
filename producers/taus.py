from ..quantities import output as q
from ..quantities import nanoAOD, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults


with defaults(scopes=["global"], output=[]):
    TauPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})",
        input=[q.Tau_pt_corrected],
    )
    TauEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})",
        input=[nanoAOD.Tau_eta],
    )
    TauDzCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})",
        input=[nanoAOD.Tau_dz],
    )
    # int for v9, UChar_t from v12
    TauDMCut = Producer(
        call="physicsobject::CutQuantity<UChar_t>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
        input=[nanoAOD.Tau_decayMode],
    )

with defaults(scopes=["et", "mt", "tt"]):
    with defaults(output=[q.Tau_IDvsEle]):
        TauID_vsEle_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSe],
        )
        TauID_vsEle_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSe],
        )
    with defaults(output=[q.Tau_IDvsMu]):
        TauID_vsMu_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSmu],
        )
        TauID_vsMu_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSmu],
        )
    with defaults(output=[q.Tau_IDvsJet]):
        TauID_vsJet_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSjet],
        )
        TauID_vsJet_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSjet],
        )

    with defaults(output=[q.Tau_rawIDvsEle]):
        TauIDraw_vsEle_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_rawDeepTau2018v2p5VSe],
        )
        TauIDraw_vsEle_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSe],
        )
    with defaults(output=[q.Tau_rawIDvsMu]):
        TauIDraw_vsMu_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_rawDeepTau2018v2p5VSmu],
        )
        TauIDraw_vsMu_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSmu],
        )

    with defaults(output=[q.Tau_rawIDvsJet]):
        TauIDraw_vsJet_2p5 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_rawDeepTau2018v2p5VSjet],
        )
        TauIDraw_vsJet_2p1 = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSjet],
        )


    with defaults(output=[]):  # Tau ID cuts
        VsJetTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsjet_tau_wp_cut})",
            input=[q.Tau_IDvsJet],
        )
        VsElectronTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsele_tau_wp_cut})",
            input=[q.Tau_IDvsEle],
        )
        VsMuonTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsmu_tau_wp_cut})",
            input=[q.Tau_IDvsMu],
        )
    

    ####################
    # Set of producers used for selection of good taus
    ####################

    TauPtCorrection_eleFake = Producer(
        call='''physicsobject::tau::PtCorrectionMC_eleFake(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_ES_json_name}",
            "{tau_id_algorithm}",
            "{tau_elefake_es_DM0_barrel}",
            "{tau_elefake_es_DM1_barrel}",
            "{tau_elefake_es_DM0_endcap}",
            "{tau_elefake_es_DM1_endcap}")''',
        input=[
            nanoAOD.Tau_pt,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_decayMode,
            nanoAOD.Tau_genPartFlav,
        ],
        output=[q.Tau_pt_ele_corrected],
    )
    TauPtCorrection_muFake = Producer(
        call='physicsobject::tau::PtCorrectionMC_muFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_mufake_es}")',
        input=[
            q.Tau_pt_ele_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_decayMode,
            nanoAOD.Tau_genPartFlav,
        ],
        output=[q.Tau_pt_ele_mu_corrected],
    )
    
    with defaults(output=[q.Tau_pt_corrected]):
        # legacy implementation kept for reference
        TauPtCorrection_genTau = Producer(
            call='''physicsobject::tau::PtCorrectionMC_genuineTau(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_sf_file}",
                "{tau_ES_json_name}",
                "{tau_id_algorithm}",
                "{tau_ES_shift_DM0}",
                "{tau_ES_shift_DM1}",
                "{tau_ES_shift_DM10}",
                "{tau_ES_shift_DM11}")''',
            input=[
                q.Tau_pt_ele_mu_corrected,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_decayMode,
                nanoAOD.Tau_genPartFlav,
            ],
        )
        # MC Genuine Tau ES Corrections
        TauPtCorrection_genTau_dm_binned = Producer(
            call='''physicsobject::tau::PtCorrectionMC_genuineTau(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_sf_file}",
                "{tau_ES_json_name}",
                "{tau_id_algorithm}",
                "{tau_ES_shift_1prong0pizero}",
                "{tau_ES_shift_1prong1pizero}",
                "{tau_ES_shift_3prong0pizero}",
                "{tau_ES_shift_3prong1pizero}")''',
            input=[
                q.Tau_pt_ele_mu_corrected,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_decayMode,
                nanoAOD.Tau_genPartFlav,
            ],
        )
        TauPtCorrection_genTau_dm_pt_binned = Producer(
            call='''physicsobject::tau::PtCorrectionMC_genuineTau(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_sf_file}",
                "{tau_ES_json_name}",
                "{tau_id_algorithm}",
                "{tau_ES_shift_1prong0pizero20to40}",
                "{tau_ES_shift_1prong0pizero40toInf}",
                "{tau_ES_shift_1prong1pizero20to40}",
                "{tau_ES_shift_1prong1pizero40toInf}",
                "{tau_ES_shift_3prong0pizero20to40}",
                "{tau_ES_shift_3prong0pizero40toInf}",
                "{tau_ES_shift_3prong1pizero20to40}",
                "{tau_ES_shift_3prong1pizero40toInf}")''',
            input=[
                q.Tau_pt_ele_mu_corrected,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_decayMode,
                nanoAOD.Tau_genPartFlav,
            ],
            scopes=["et", "mt", "tt"],
        )
        # Embedding Genuine Tau ES Corrections
        TauPtCorrection_emb_genTau_dm_binned = Producer(
            call='''physicsobject::tau::PtCorrectionMC_genuineTau(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_emb_sf_file}",
                "{tau_emb_ES_json_name}",
                "{tau_id_algorithm}",
                "{tau_emb_ES_WP}",
                "{tau_vsjet_vseleWP}",
                "{tau_ES_shift_1prong0pizero}",
                "{tau_ES_shift_1prong1pizero}",
                "{tau_ES_shift_3prong0pizero}",
                "{tau_ES_shift_3prong1pizero}")''',
            input=[
                nanoAOD.Tau_pt,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_decayMode,
                nanoAOD.Tau_genPartFlav,
            ],
        )
        TauPtCorrection_emb_genTau_dm_pt_binned = Producer(
            call='''physicsobject::tau::PtCorrectionMC_genuineTau(
                {df},
                correctionManager,
                {output},
                {input},
                "{tau_emb_sf_file}",
                "{tau_emb_ES_json_name}",
                "{tau_id_algorithm}",
                "{tau_emb_ES_WP}",
                "{tau_vsjet_vseleWP}",
                "{tau_ES_shift_1prong0pizero20to40}",
                "{tau_ES_shift_1prong0pizero40toInf}",
                "{tau_ES_shift_1prong1pizero20to40}",
                "{tau_ES_shift_1prong1pizero40toInf}",
                "{tau_ES_shift_3prong0pizero20to40}",
                "{tau_ES_shift_3prong0pizero40toInf}",
                "{tau_ES_shift_3prong1pizero20to40}",
                "{tau_ES_shift_3prong1pizero40toInf}")''',
            input=[
                nanoAOD.Tau_pt,
                nanoAOD.Tau_eta,
                nanoAOD.Tau_decayMode,
                nanoAOD.Tau_genPartFlav,
            ],
        )
        # Run 3
        TauPtCorrection_byValue = Producer(
            call='embedding::tau::PtCorrection_byValue({df}, {output}, {input}, "{tau_ES_shift_DM0}", "{tau_ES_shift_DM1}", "{tau_ES_shift_DM10}", "{tau_ES_shift_DM11}")',
            input=[nanoAOD.Tau_pt, nanoAOD.Tau_decayMode],
        )
        RenameTauPt = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_pt],
        )
        TauPtCorrection_MC = Producer(
            call='''physicsobject::tau::PtCorrectionMC(
                {df}, 
                correctionManager, 
                {output}, 
                {input}, 
                "{tau_sf_file}", 
                "{tau_ES_json_name}", 
                "{tau_id_algorithm}", 
                "{tau_elefake_es_DM0_barrel}", 
                "{tau_elefake_es_DM1_barrel}", 
                "{tau_elefake_es_DM0_endcap}", 
                "{tau_elefake_es_DM1_endcap}", 
                "{tau_mufake_es}", 
                "{tau_ES_shift_DM0}", 
                "{tau_ES_shift_DM1}", 
                "{tau_ES_shift_DM10}", 
                "{tau_ES_shift_DM11}", 
                {tau_vsjet_wp}, 
                {tau_vsele_wp})''',
            input=[nanoAOD.Tau_pt, nanoAOD.Tau_eta, nanoAOD.Tau_decayMode, nanoAOD.Tau_genPartFlav],
        )
        TauPtCorrection_data = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_pt],
        )

    with defaults(output=[q.Tau_mass_corrected]):
        TauMassCorrection_data = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Tau_mass],
        )
        TauMassCorrection = Producer(
            call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
            input=[
                nanoAOD.Tau_mass,
                nanoAOD.Tau_pt,
                q.Tau_pt_corrected,
            ],
        )

    with defaults(call=None, input=None, output=None):
        TauEnergyCorrection_byValue = ProducerGroup(
            subproducers=[
                TauPtCorrection_eleFake,
                TauPtCorrection_byValue,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_ES_dm_binned = ProducerGroup(
            subproducers=[
                TauPtCorrection_eleFake,
                TauPtCorrection_muFake,
                TauPtCorrection_genTau_dm_binned,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_ES_dm_pt_binned = ProducerGroup(
            subproducers=[
                TauPtCorrection_eleFake,
                TauPtCorrection_muFake,
                TauPtCorrection_genTau_dm_pt_binned,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_Embedding = ProducerGroup(
            subproducers=[
                TauPtCorrection_byValue,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_Embedding_ES_dm_binned = ProducerGroup(
            subproducers=[
                TauPtCorrection_emb_genTau_dm_binned,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_Embedding_ES_dm_pt_binned = ProducerGroup(
            subproducers=[
                TauPtCorrection_emb_genTau_dm_pt_binned,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection = ProducerGroup(
            subproducers=[
                TauPtCorrection_MC,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_data = ProducerGroup(
            subproducers=[
                TauPtCorrection_data,
                TauMassCorrection_data,
            ],
        )

    #########################################
    # Good taus selection for nonglobal scope
    #########################################

    with defaults(output=[]):
        GoodTauPtCut = Producer(
            call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})",
            input=[q.Tau_pt_corrected],
        )
        GoodTauEtaCut = Producer(
            call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})",
            input=[nanoAOD.Tau_eta],
        )
        GoodTauDzCut = Producer(
            call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})",
            input=[nanoAOD.Tau_dz],
        )
        #int for v9, UChart_t for v12 and v15
        GoodTauDMCut = Producer(
            call="physicsobject::CutQuantity<UChar_t>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
            input=[nanoAOD.Tau_decayMode],
        )

    BaseTaus = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauID_vsEle_2p5,
            TauID_vsMu_2p5,
            TauID_vsJet_2p5,
            TauIDraw_vsEle_2p5,
            TauIDraw_vsMu_2p5,
            TauIDraw_vsJet_2p5,
        ],
    )

    GoodTaus = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.good_taus_mask],
        subproducers=[
            GoodTauPtCut,
            GoodTauEtaCut,
            GoodTauDzCut,
            GoodTauDMCut,
            VsJetTauIDCut,
            VsElectronTauIDCut,
            VsMuonTauIDCut,
        ],
    )
    NumberOfGoodTaus = Producer(
        call="physicsobject::Count({df}, {output}, {input})",
        input=[q.good_taus_mask],
        output=[q.ntaus],
    )
