from ..quantities import output as q
from ..quantities import nanoAODv15, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, ExtendedVectorProducer, defaults


with defaults(scopes=["global"], output=[]):
    TauPtCut = Producer(
        call='''physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})''',
        input=[q.tau_pt_corrected],
    )
    TauEtaCut = Producer(
        call='''physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})''',
        input=[nanoAODv15.Tau_eta],
    )
    TauDzCut = Producer(
        call='''physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})''',
        input=[nanoAODv15.Tau_dz],
    )

with defaults(scopes=["et", "mt", "tt"]):
    with defaults(output=[q.tau_IDvsEle]):
        TauID_vsEle_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_idDeepTau2018v2p5VSe],
        )
        TauID_vsEle_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSe],
        )
    with defaults(output=[q.tau_IDvsMu]):
        TauID_vsMu_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_idDeepTau2018v2p5VSmu],
        )
        TauID_vsMu_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSmu],
        )
    with defaults(output=[q.tau_IDvsJet]):
        TauID_vsJet_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_idDeepTau2018v2p5VSjet],
        )
        TauID_vsJet_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_idDeepTau2017v2p1VSjet],
        )

    with defaults(output=[q.tau_rawIDvsEle]):
        TauIDraw_vsEle_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_rawDeepTau2018v2p5VSe],
        )
        TauIDraw_vsEle_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSe],
        )
    with defaults(output=[q.tau_rawIDvsMu]):
        TauIDraw_vsMu_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_rawDeepTau2018v2p5VSmu],
        )
        TauIDraw_vsMu_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSmu],
        )

    with defaults(output=[q.tau_rawIDvsJet]):
        TauIDraw_vsJet_2p5 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_rawDeepTau2018v2p5VSjet],
        )
        TauIDraw_vsJet_2p1 = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv9.Tau_rawDeepTau2017v2p1VSjet],
        )


    with defaults(output=[]):  # Tau ID cuts
        VsJetTauIDCut = Producer(
            call='''physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsjet_tau_wp_cut})''',
            input=[q.tau_IDvsJet],
        )
        VsElectronTauIDCut = Producer(
            call='''physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsele_tau_wp_cut})''',
            input=[q.tau_IDvsEle],
        )
        VsMuonTauIDCut = Producer(
            call='''physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsmu_tau_wp_cut})''',
            input=[q.tau_IDvsMu],
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
            nanoAODv15.Tau_pt,
            nanoAODv15.Tau_eta,
            nanoAODv15.Tau_decayMode,
            nanoAODv15.Tau_genPartFlav,
        ],
        output=[q.tau_pt_ele_corrected],
    )
    TauPtCorrection_muFake = Producer(
        call='''physicsobject::tau::PtCorrectionMC_muFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_mufake_es}")''',
        input=[
            q.tau_pt_ele_corrected,
            nanoAODv15.Tau_eta,
            nanoAODv15.Tau_decayMode,
            nanoAODv15.Tau_genPartFlav,
        ],
        output=[q.tau_pt_ele_mu_corrected],
    )
    
    with defaults(output=[q.tau_pt_corrected]):
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
                q.tau_pt_ele_mu_corrected,
                nanoAODv15.Tau_eta,
                nanoAODv15.Tau_decayMode,
                nanoAODv15.Tau_genPartFlav,
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
                q.tau_pt_ele_mu_corrected,
                nanoAODv15.Tau_eta,
                nanoAODv15.Tau_decayMode,
                nanoAODv15.Tau_genPartFlav,
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
                q.tau_pt_ele_mu_corrected,
                nanoAODv15.Tau_eta,
                nanoAODv15.Tau_decayMode,
                nanoAODv15.Tau_genPartFlav,
            ],
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
                nanoAODv15.Tau_pt,
                nanoAODv15.Tau_eta,
                nanoAODv15.Tau_decayMode,
                nanoAODv15.Tau_genPartFlav,
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
                nanoAODv15.Tau_pt,
                nanoAODv15.Tau_eta,
                nanoAODv15.Tau_decayMode,
                nanoAODv15.Tau_genPartFlav,
            ],
        )
        # Run 3
        TauPtCorrection_byValue = Producer(
            call='''embedding::tau::PtCorrection_byValue({df}, {output}, {input}, "{tau_ES_shift_DM0}", "{tau_ES_shift_DM1}", "{tau_ES_shift_DM10}", "{tau_ES_shift_DM11}")''',
            input=[nanoAODv15.Tau_pt, nanoAODv15.Tau_decayMode],
        )
        RenameTauPt = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_pt],
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
                {vec_open}{tau_dms}{vec_close},
                "{tau_elefake_es_DM0}", 
                "{tau_elefake_es_DM1}", 
                "{tau_elefake_es_DM10}", 
                "{tau_elefake_es_DM11}", 
                "{tau_mufake_es}", 
                "{tau_ES_shift_DM0}", 
                "{tau_ES_shift_DM1}", 
                "{tau_ES_shift_DM10}", 
                "{tau_ES_shift_DM11}", 
                "{tau_vsjet_wp}", 
                "{tau_vsele_wp}")''',
            input=[nanoAODv15.Tau_pt, nanoAODv15.Tau_eta, nanoAODv15.Tau_decayMode, nanoAODv15.Tau_genPartFlav],
        )
        TauPtCorrection_MC_toremove = Producer(
            call='''physicsobject::tau::PtCorrectionMC(
                {df}, 
                correctionManager, 
                {output}, 
                {input}, 
                "{tau_sf_file}", 
                "{tau_ES_json_name}", 
                "{tau_id_algorithm}", 
                {vec_open}{tau_dms}{vec_close},
                "{tau_es_variation}", 
                "{tau_vsjet_wp}", 
                "{tau_vsele_wp}")''',
            input=[nanoAODv15.Tau_pt, nanoAODv15.Tau_eta, nanoAODv15.Tau_decayMode, nanoAODv15.Tau_genPartFlav],
        )
        TauPtCorrection_data = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_pt],
        )

    with defaults(output=[q.tau_mass_corrected]):
        TauMassCorrection_data = Producer(
            call='''event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})''',
            input=[nanoAODv15.Tau_mass],
        )
        TauMassCorrection = Producer(
            call='''physicsobject::MassCorrectionWithPt({df}, {output}, {input})''',
            input=[
                nanoAODv15.Tau_mass,
                nanoAODv15.Tau_pt,
                q.tau_pt_corrected,
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
            call='''physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})''',
            input=[q.tau_pt_corrected],
        )
        GoodTauEtaCut = Producer(
            call='''physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})''',
            input=[nanoAODv15.Tau_eta],
        )
        GoodTauDzCut = Producer(
            call='''physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})''',
            input=[nanoAODv15.Tau_dz],
        )
        GoodTauDMCut = Producer(
            call='''physicsobject::CutQuantity<UChar_t>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})''',
            input=[nanoAODv15.Tau_decayMode],
        )
        GoodTauDMCut_v9 = Producer(
            call='''physicsobject::CutQuantity<int>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})''',
            input=[nanoAODv15.Tau_decayMode],
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

    BaseTaus_v9 = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauID_vsEle_2p1,
            TauID_vsMu_2p1,
            TauID_vsJet_2p1,
            TauIDraw_vsEle_2p1,
            TauIDraw_vsMu_2p1,
            TauIDraw_vsJet_2p1,
        ],
    )

    GoodTaus = ProducerGroup(
        call='''physicsobject::CombineMasks({df}, {output}, {input}, "all_of")''',
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
    GoodTaus_v9 = ProducerGroup(
        call='''physicsobject::CombineMasks({df}, {output}, {input}, "all_of")''',
        input=[],
        output=[q.good_taus_mask],
        subproducers=[
            GoodTauPtCut,
            GoodTauEtaCut,
            GoodTauDzCut,
            GoodTauDMCut_v9,
            VsJetTauIDCut,
            VsElectronTauIDCut,
            VsMuonTauIDCut,
        ],
    )
    NumberOfGoodTaus = Producer(
        call='''physicsobject::Count({df}, {output}, {input})''',
        input=[q.good_taus_mask],
        output=[q.ntaus],
    )
