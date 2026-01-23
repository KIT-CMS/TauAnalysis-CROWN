from ..quantities import output as q
from ..quantities import nanoAOD, nanoAODv9
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for loosest selection of electrons
####################

with defaults(scopes=["global"]):
    # event seed for initializing the smearing
    ElectronPtSmearingSeed = Producer(
        call="event::quantity::GenerateSeed({df}, {output}, {input}, {ele_es_master_seed})",
        input=[
            nanoAOD.luminosityBlock,
            nanoAOD.run,
            nanoAOD.event,
        ],
        output=[],
    )

    with defaults(output=[q.Electron_pt_corrected]):
        ElectronPtCorrectionEmbedding = Producer(
           call='embedding::electron::PtCorrection({df}, correctionManager, {output}, {input}, "{embedding_electron_es_sf_file}", "{ele_ES_json_name}", "{ele_energyscale_barrel}", "{ele_energyscale_endcap}")',
           input=[nanoAOD.Electron_pt, nanoAOD.Electron_eta],
        )
        ElectronPtCorrectionMC_Run2 = Producer(
            call='physicsobject::electron::PtCorrectionMC({df}, correctionManager, {output}, {input}, "{ele_es_file}", "{ele_es_name}", "{ele_es_era}", "{ele_es_variation}")',
            input=[nanoAOD.Electron_pt, nanoAOD.Electron_eta, nanoAOD.Electron_seedGain, nanoAODv9.Electron_dEsigmaUp, nanoAODv9.Electron_dEsigmaDown],
        )
        ElectronPtCorrectionMC_Run3 = ProducerGroup(
            call='physicsobject::electron::PtCorrectionMC({df}, correctionManager, {output}, {input}, {ele_es_file}, {ele_es_mc_name}, "{ele_es_variation}")',
            input=[nanoAOD.Electron_pt, nanoAOD.Electron_eta, nanoAOD.Electron_deltaEtaSC, nanoAOD.Electron_r9,],
            subproducers=[ElectronPtSmearingSeed],
        )
        ElectronPtCorrectionData = Producer(
            call='physicsobject::electron::PtCorrectionData({df}, correctionManager, {output}, {input}, {ele_es_file}, {ele_es_data_name})',
            input=[nanoAOD.Electron_pt, nanoAOD.Electron_eta, nanoAOD.Electron_deltaEtaSC, nanoAOD.Electron_seedGain, nanoAOD.Electron_r9, nanoAOD.run],
        )
        RenameElectronPt = Producer(
            call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
            input=[nanoAOD.Electron_pt],
        )

    ElectronEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_ele_eta})",
        input=[nanoAOD.Electron_eta],
        output=[q._ElectronEtaCut],
    )
    ElectronDxyCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_ele_dxy})",
        input=[nanoAOD.Electron_dxy],
        output=[q._ElectronDxyCut],
    )
    ElectronDzCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_ele_dz})",
        input=[nanoAOD.Electron_dz],
        output=[q._ElectronDzCut],
    )
    ElectronPtCut= Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_ele_pt})",
        input=[q.Electron_pt_corrected],
        output=[q._ElectronPtCut],
    )
    with defaults(output=[q._ElectronIDCut], call='physicsobject::CutEqual<bool>({df}, {output}, {input}, true)',):
        ElectronIDCut = Producer(
            input=[nanoAOD.Electron_mvaIso_WP90],
        )
        ElectronIDCut_v9 = Producer(
            input=[nanoAODv9.Electron_mvaFall17V2noIso_WP90],
        )

    ElectronIsoCut = Producer(
        call="physicsobject::CutMax<float>({df}, {output}, {input}, {ele_iso_cut})",
        input=[nanoAOD.Electron_pfRelIso03_all],
        output=[q._ElectronIsoCut],
    )

    with defaults(output=[]):
        DiElectronVetoPtCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_dielectronveto_pt})", input=[q.Electron_pt_corrected])
        # int for v9, UChar_t for v12 and v15
        DiElectronVetoIDCut = Producer(call='physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {dielectronveto_id_wp})', input=[nanoAOD.Electron_cutBased])
        DiElectronVetoElectrons = ProducerGroup(
            call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
            input=[q._ElectronEtaCut, q._ElectronDxyCut, q._ElectronDzCut, q._ElectronIsoCut],
            subproducers=[DiElectronVetoPtCut, DiElectronVetoIDCut],
        )

    BaseElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_electrons_mask],
        subproducers=[
            ElectronPtCut,
            ElectronEtaCut,
            ElectronDxyCut,
            ElectronDzCut,
            ElectronIDCut,
            ElectronIsoCut,
        ],
    )

    BaseElectrons_v9 = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_electrons_mask],
        subproducers=[
            ElectronPtCut,
            ElectronEtaCut,
            ElectronDxyCut,
            ElectronDzCut,
            ElectronIDCut_v9,
            ElectronIsoCut,
        ],
    )

    DiElectronVeto = ProducerGroup(
        call="physicsobject::LeptonPairVeto({df}, {output}, {input}, {dileptonveto_dR})",
        input=[
            q.Electron_pt_corrected,
            nanoAOD.Electron_eta,
            nanoAOD.Electron_phi,
            nanoAOD.Electron_mass,
            nanoAOD.Electron_charge,
        ],
        output=[q.dielectron_veto],
        subproducers=[DiElectronVetoElectrons],
    )


####################
# Set of producers used for more specific selection of electrons in channels
####################

with defaults(scopes=["em", "et", "ee"]):
    with defaults(output=[]):
        GoodElectronPtCut = Producer(call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_ele_pt})", input=[q.Electron_pt_corrected])
        GoodElectronEtaCut = Producer(call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_ele_eta})", input=[nanoAOD.Electron_eta])
        GoodElectronIsoCut = Producer(call="physicsobject::CutMax<float>({df}, {output}, {input}, {ele_iso_cut})", input=[nanoAOD.Electron_pfRelIso03_all])

    GoodElectrons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[q.base_electrons_mask],
        output=[q.good_electrons_mask],
        subproducers=[
            GoodElectronPtCut,
            GoodElectronEtaCut,
            GoodElectronIsoCut,
        ],
    )
    NumberOfGoodElectrons = Producer(
        call="physicsobject::Count({df}, {output}, {input})",
        input=[q.good_electrons_mask],
        output=[q.nelectrons],
    )

    VetoElectrons = Producer(
        call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
        input=[q.base_electrons_mask, q.dileptonpair],
        output=[q.veto_electrons_mask],
    )

VetoSecondElectron = Producer(
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {second_electron_index_in_pair})",
    input=[q.veto_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask_2],
    scopes=["ee"],
)
ExtraElectronsVeto = Producer(
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "em": [q.veto_electrons_mask],
        "et": [q.veto_electrons_mask],
        "mt": [q.base_electrons_mask],
        "tt": [q.base_electrons_mask],
        "mm": [q.base_electrons_mask],
        "ee": [q.veto_electrons_mask_2],
    },
    output=[q.extraelec_veto],
    scopes=["em", "et", "mt", "tt", "mm", "ee"],
)
