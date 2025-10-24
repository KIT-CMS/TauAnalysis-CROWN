from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults


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
    TauDMCut = Producer(
        call="physicsobject::CutQuantity<UChar_t>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
        input=[nanoAOD.Tau_decayMode],
    )

with defaults(scopes=["et", "mt", "tt"]):
    with defaults(output=[]):  # Tau ID cuts
        VsJetTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsjet_tau_wp_cut})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSjet],
        )
        VsElectronTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsele_tau_wp_cut})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSe],
        )
        VsMuonTauIDCut = Producer(
            call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {vsmu_tau_wp_cut})",
            input=[nanoAOD.Tau_idDeepTau2018v2p5VSmu],
        )

    ####################
    # Set of producers used for selection of good taus
    ####################

    TauPtCorrection_byValue = Producer(
        call="embedding::tau::PtCorrection_byValue({df}, {output}, {input}, {tau_ES_shift_DM0}, {tau_ES_shift_DM1}, {tau_ES_shift_DM10}, {tau_ES_shift_DM11})",
        input=[nanoAOD.Tau_pt, nanoAOD.Tau_decayMode],
        output=[q.Tau_pt_corrected],
    )
    RenameTauPt = Producer(
        call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
        input=[nanoAOD.Tau_pt],
        output=[q.Tau_pt_corrected],
    )
    TauPtCorrection_MC = Producer(
        call="physicsobject::tau::PtCorrectionMC({df}, correctionManager, {output}, {input}, {tau_sf_file}, {tau_ES_json_name}, {tau_id_algorithm}, {tau_elefake_es_DM0_barrel}, {tau_elefake_es_DM1_barrel}, {tau_elefake_es_DM0_endcap}, {tau_elefake_es_DM1_endcap}, {tau_mufake_es}, {tau_ES_shift_DM0}, {tau_ES_shift_DM1}, {tau_ES_shift_DM10}, {tau_ES_shift_DM11}, {tau_vsjet_wp}, {tau_vsele_wp})",
        input=[nanoAOD.Tau_pt, nanoAOD.Tau_eta, nanoAOD.Tau_decayMode, nanoAOD.Tau_genPartFlav],
        output=[q.Tau_pt_corrected],
    )
    TauPtCorrection_data = Producer(
        call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
        input=[nanoAOD.Tau_pt],
        output=[q.Tau_pt_corrected],
    )
    TauMassCorrection_data = Producer(
        call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
        input=[nanoAOD.Tau_mass],
        output=[q.Tau_mass_corrected],
    )
    TauMassCorrection = Producer(
        call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
        input=[
            nanoAOD.Tau_mass,
            nanoAOD.Tau_pt,
            q.Tau_pt_corrected,
        ],
        output=[q.Tau_mass_corrected],
    )

    with defaults(call=None, input=None, output=None):
        TauEnergyCorrection_byValue = ProducerGroup(
            subproducers=[
                TauPtCorrection_MC,
                TauPtCorrection_byValue,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection = ProducerGroup(
            subproducers=[
                TauPtCorrection_MC,
                TauMassCorrection,
            ],
        )
        TauEnergyCorrection_Embedding = ProducerGroup(
            subproducers=[
                TauPtCorrection_byValue,
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
        GoodTauDMCut = Producer(
            call="physicsobject::CutQuantity<UChar_t>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
            input=[nanoAOD.Tau_decayMode],
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
