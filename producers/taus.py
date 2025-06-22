from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..helper.ProducerWarapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    scopes,
)

with scopes(["global"]):
    TauPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})",
        input=[q.Tau_pt_corrected],
        output=[],
    )
    TauEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})",
        input=[nanoAOD.Tau_eta],
        output=[],
    )
    TauDzCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})",
        input=[nanoAOD.Tau_dz],
        output=[],
    )
    TauDMCut = Producer(
        call="physicsobject::CutQuantity<int>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
        input=[nanoAOD.Tau_decayMode],
        output=[],
    )

with scopes(["et", "mt", "tt"]):
    VsJetTauIDCut = Producer(
        name="VsJetTauIDCut",
        call="physicsobject::CutBitmask({df}, {output}, {input}, {vsjet_tau_id_bit})",
        input=[nanoAOD.Tau_ID_vsJet],
        output=[],
        scopes=["et", "mt", "tt"],
    )
    VsElectronTauIDCut = Producer(
        call="physicsobject::CutBitmask({df}, {output}, {input}, {vsele_tau_id_bit})",
        input=[nanoAOD.Tau_ID_vsEle],
        output=[],
    )
    VsMuonTauIDCut = Producer(
        call="physicsobject::CutBitmask({df}, {output}, {input}, {vsmu_tau_id_bit})",
        input=[nanoAOD.Tau_ID_vsMu],
        output=[],
    )

    ####################
    # Set of producers used for selection of good taus
    ####################

    TauPtCorrection_byValue = Producer(
        call="embedding::tau::PtCorrection_byValue({df}, {output}, {input}, {tau_ES_shift_DM0}, {tau_ES_shift_DM1}, {tau_ES_shift_DM10}, {tau_ES_shift_DM11})",
        input=[
            nanoAOD.Tau_pt,
            nanoAOD.Tau_decayMode,
        ],
        output=[q.Tau_pt_corrected],
    )
    TauPtCorrection_eleFake = Producer(
        call='physicsobject::tau::PtCorrectionMC_eleFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_elefake_es_DM0_barrel}", "{tau_elefake_es_DM1_barrel}", "{tau_elefake_es_DM0_endcap}", "{tau_elefake_es_DM1_endcap}")',
        input=[
            nanoAOD.Tau_pt,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_decayMode,
            nanoAOD.Tau_genMatch,
        ],
        output=[q.Tau_pt_ele_corrected],
    )
    TauPtCorrection_muFake = Producer(
        call='physicsobject::tau::PtCorrectionMC_muFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_mufake_es}")',
        input=[
            q.Tau_pt_ele_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_decayMode,
            nanoAOD.Tau_genMatch,
        ],
        output=[q.Tau_pt_ele_mu_corrected],
    )
    TauPtCorrection_genTau = Producer(
        call='physicsobject::tau::PtCorrectionMC_genuineTau({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_ES_shift_DM0}", "{tau_ES_shift_DM1}", "{tau_ES_shift_DM10}", "{tau_ES_shift_DM11}")',
        input=[
            q.Tau_pt_ele_mu_corrected,
            nanoAOD.Tau_eta,
            nanoAOD.Tau_decayMode,
            nanoAOD.Tau_genMatch,
        ],
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
    TauEnergyCorrection_byValue = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[TauPtCorrection_eleFake, TauPtCorrection_byValue, TauMassCorrection],
    )
    TauEnergyCorrection = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauPtCorrection_eleFake,
            TauPtCorrection_muFake,
            TauPtCorrection_genTau,
            TauMassCorrection,
        ],
    )
    TauEnergyCorrection_Embedding = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauPtCorrection_byValue,
            TauMassCorrection,
        ],
    )
    TauEnergyCorrection_data = ProducerGroup(
        call=None,
        input=None,
        output=None,
        subproducers=[
            TauPtCorrection_data,
            TauMassCorrection_data,
        ],
    )

    ######
    # Good taus selection for nonglobal scope
    ######

    GoodTauPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_tau_pt})",
        input=[q.Tau_pt_corrected],
        output=[],
    )
    GoodTauEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_eta})",
        input=[nanoAOD.Tau_eta],
        output=[],
    )
    GoodTauDzCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_tau_dz})",
        input=[nanoAOD.Tau_dz],
        output=[],
    )
    GoodTauDMCut = Producer(
        call="physicsobject::CutQuantity<int>({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
        input=[nanoAOD.Tau_decayMode],
        output=[],
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
