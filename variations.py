from __future__ import annotations 
from typing import List

from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity

from .producers import electrons as electrons
from .producers import event as event
from .producers import jets as jets
from .producers import met as met
from .producers import muons as muons
from .producers import scalefactors as scalefactors
from .producers import taus as taus
from .quantities import nanoAODv15, nanoAODv9
from .scripts.CROWNWrapper import (defaults,
                                   get_adjusted_add_shift_SystematicShift)
from .tau_triggersetup import RUN2_ERAS, DOUBLETAU_HPS_ERAS

# Map internal era names to JERC JSON era names for JERC sources
ERA_MAP = {
    "2016preVFP":"2016",
    "2016postVFP":"2016", 
    "2017":"2017", 
    "2018":"2018",
    "2022preEE": "2022",
    "2022postEE": "2022EE",
    "2023preBPix": "2023",
    "2023postBPix": "2023BPix",
    "2024": "2024",
    "2025": "2025",
    "2026": "2026",
}

def add_Variations(configuration: Configuration, sample: str, era: str) -> Configuration:
    add_shift = get_adjusted_add_shift_SystematicShift(configuration)
    era_tag = ERA_MAP[era]  
    shift_era_tag = era if era in ("2016preVFP", "2016postVFP") else era_tag  # keeps 2016 sub-eras
    
    #########################
    # LHE Scale Weight variations
    #########################
    lhe_scale_production_mode_postfixes = {
        "ggh": ["ggH"],
        "vbf": ["qqH"],
        "rem": ["VH", "ttH"],
    }
    lhe_scale_postfixes: List[str] = next(
        (postfixes for tag, postfixes in lhe_scale_production_mode_postfixes.items() if tag in sample),
        [],
    )
    if lhe_scale_postfixes:
        with defaults(scopes="global"):
            with defaults(shift_map={"Up": 2.0, "Down": 0.5}):
                for postfix in lhe_scale_postfixes:
                    add_shift(name=f"QCDscale_ren_{postfix}", shift_key="muR", producers=[event.LHE_Scale_weight])
                    add_shift(name=f"QCDscale_fac_{postfix}", shift_key="muF", producers=[event.LHE_Scale_weight])
                    add_shift(name=f"ps_fsr_{postfix}", shift_key="fsr", producers=[event.PS_weight])
                    add_shift(name=f"ps_isr_{postfix}", shift_key="isr", producers=[event.PS_weight])
            with defaults(shift_map={"Up": "up", "Down": "down"}):
                for postfix in lhe_scale_postfixes:
                    add_shift(name=f"pdf_Higgs_{postfix}", shift_key="pdf_variation", producers=[event.LHE_PDF_weight])
                    add_shift(name=f"pdf_alphas_{postfix}", shift_key="pdf_alphaS_variation", producers=[event.LHE_alphaS_weight])

    #########################
    # Pileup Shifts
    #########################
    # if era == "2025":
    #     add_shift(
    #         name=f"PileUp",
    #         shift_key="PU_reweighting_variation",
    #         shift_map={"Up": "data/root_pileup/Data_PileUp_2025_72p3832.root", "Down": "data/root_pileup/Data_PileUp_2025_66p0168.root"},
    #         scopes="global",
    #         producers=[event.PUweights],
    #         exclude_samples=["data", "embedding", "embedding_mc"],
    #     )
    # else:
    add_shift(
        name=f"CMS_pileup_{shift_era_tag}",
        shift_key="PU_reweighting_variation",
        shift_map={"Up": "up", "Down": "down"},
        scopes="global",
        producers=[event.PUweights],
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    #########################
    # Prefiring Shifts
    #########################
    if int(era[:4]) < 2018:
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="CMS_l1_ecal_prefiringDown",
                quantity_change={
                    nanoAODv9.L1PreFiringWeight_Nom: "L1PreFiringWeight_Dn",
                },
                scopes=["global"],
            )
        )
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="CMS_l1_ecal_prefiringUp",
                quantity_change={
                    nanoAODv9.L1PreFiringWeight_Nom: "L1PreFiringWeight_Up",
                },
                scopes=["global"],
            )
        )

    #########################
    # Muon scale and resolution correction shifts
    #########################
    with defaults(
        scopes="global",
        shift_key="muon_sr_shift",
        producers=[muons.MuonPtCorrection],
        exclude_samples=["data", "embedding", "embedding_mc"],
    ):
        add_shift(name=f"CMS_scale_m_stat", shift_map={"Up": "ScaleStatUp", "Down": "ScaleStatDown"})
        add_shift(name=f"CMS_scale_m_syst{shift_era_tag}", shift_map={"Up": "ScaleSystUp", "Down": "ScaleSystDown"})
        add_shift(name=f"CMS_res_m_stat", shift_map={"Up": "ResoStatUp", "Down": "ResoStatDown"})
        add_shift(name=f"CMS_res_m_syst_{shift_era_tag}", shift_map={"Up": "ResoSystUp", "Down": "ResoSystDown"})

    #########################
    # Muon ID shifts
    #########################
    for muon_scopes, muon_producer in [
        (("mt", "mm"), scalefactors.Muon_1_ID_SF),
        (("mm", "em"), scalefactors.Muon_2_ID_SF),
    ]:
        with defaults(scopes=muon_scopes, producers=[muon_producer]):
            add_shift(
                name="CMS_eff_m_id_syst",
                shift_key="muon_id_variation",
                shift_map={"Up":"systup", "Down":"systdown"},
            )
            add_shift(
                name=f"CMS_eff_m_id_stat_{shift_era_tag}",
                shift_key="muon_id_variation",
                shift_map={"Up":"statup", "Down":"statdown"},
            )

    #########################
    # Muon iso shifts
    #########################
    for muon_scopes, muon_producer in [
        (("mt", "mm"), scalefactors.Muon_1_ID_SF),
        (("mm", "em"), scalefactors.Muon_2_ID_SF),
    ]:
        with defaults(scopes=muon_scopes, producers=[muon_producer]):
            add_shift(
                name="CMS_eff_m_iso_syst",
                shift_key="muon_iso_variation",
                shift_map={"Up":"systup", "Down":"systdown"},
            )
            add_shift(
                name=f"CMS_eff_m_iso_stat_{shift_era_tag}",
                shift_key="muon_iso_variation",
                shift_map={"Up":"statup", "Down":"statdown"},
            )

    #########################
    # Electron energy correction shifts
    #########################
    if int(era[:4]) < 2022:
        with defaults(
            scopes="global",
            shift_key="ele_es_variation",
            producers=[electrons.ElectronPtCorrectionMC_v9],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ):
            add_shift(name="CMS_res_e", shift_map={"Up": "resolutionUp", "Down": "resolutionDown"})
            add_shift(name="CMS_scale_e", shift_map={"Up": "scaleUp", "Down": "scaleDown"})
    else:
        with defaults(
            scopes="global",
            shift_key="ele_es_variation",
            producers=[electrons.ElectronPtCorrectionMC],
            exclude_samples=["data", "embedding", "embedding_mc"],
        ):
            add_shift(name="CMS_res_e", shift_map={"Up": "resolutionUp", "Down": "resolutionDown"})
            add_shift(name="CMS_scale_e", shift_map={"Up": "scaleUp", "Down": "scaleDown"})

    #########################
    # Electron ID shifts
    #########################
    add_shift(
        name="CMS_eff_e_id",
        scopes=("et", "ee", "em"),
        shift_key="ele_sf_variation",
        shift_map={"Up":"sfup", "Down":"sfdown"},
        producers=[scalefactors.EleID_SF],
    )

    #########################
    # MET Shifts
    #########################
    configuration.add_shift(
        SystematicShiftByQuantity(
            name=f"CMS_scale_met_unclustered_energyUp_{shift_era_tag}",
            quantity_change={
                nanoAODv15.PuppiMET_pt: "PuppiMET_ptUnclusteredUp",
                nanoAODv15.PuppiMET_phi: "PuppiMET_phiUnclusteredUp",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShiftByQuantity(
            name=f"CMS_scale_met_unclustered_energyDown_{shift_era_tag}",
            quantity_change={
                nanoAODv15.PuppiMET_pt: "PuppiMET_ptUnclusteredDown",
                nanoAODv15.PuppiMET_phi: "PuppiMET_phiUnclusteredDown",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    #########################
    # MET Recoil Shifts
    #########################
    if int(era[:4]) < 2022:
        with defaults(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[met.ApplyRecoilCorrections_Run2],
            exclude_samples=["data", "embedding", "embedding_mc"],
            shift_key=[
                "apply_recoil_resolution_systematic",  # set either to True or False
                "apply_recoil_response_systematic",  # set either to True or False
                "recoil_systematic_shift_up",  # set either to True or False upon variation
                "recoil_systematic_shift_down",  # set either to True or False upon variation
            ]
        ):
            add_shift(
                name="CMS_scale_met_recoil_response",
                shift_map={
                    "Up": [False, True, True, False],
                    "Down": [False, True, False, True],
                }
            )
            add_shift(
                name="CMS_res_met_recoil_resolution",
                shift_map={
                    "Up": [True, False, True, False],
                    "Down": [True, False, False, True],
                },
            )
    else:
        with defaults(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[met.ApplyRecoilCorrections],
            exclude_samples=["data", "embedding", "embedding_mc"],
            shift_key="recoil_variation",
        ):
            add_shift(
                name=f"CMS_scale_met_recoil_response_{shift_era_tag}",
                shift_map={"Up":"RespUp", "Down":"RespDown"}
            )
            add_shift(
                name=f"CMS_res_met_recoil_resolution_{shift_era_tag}",
                shift_map={"Up":"ResolUp", "Down":"ResolDown"}
            )

    #########################
    # Z pt DY uncertainties
    #########################
    if int(era[:4]) >= 2022:
        add_shift(
            scopes=("et", "mt", "tt", "em", "ee", "mm"),
            producers=[event.ZPtReweighting],
            shift_key="zpt_variation",
            name=f"CMS_htt_zptReweight_{shift_era_tag}",
            shift_map={"Up": "up", "Down": "down"},
            samples=["dyjets_powheg", "dyjets_amcatnlo", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "electroweak_boson"],
        )
    
    #########################
    # Tau energy scale shifts  #
    #########################
    with defaults(shift_map={"Down": "down", "Up": "up"}, exclude_samples=["data", "embedding", "embedding_mc"]):
        if ("dyjets" in sample or "electroweak_boson" in sample) and int(era[:4]) < 2022:
            add_shift(
                name="CMS_scale_t_genMuon",
                shift_key="tau_mufake_es",
                scopes="mt",
                producers=[taus.TauPtCorrection_muFake],
            )
            with defaults(
                scopes="et",
                producers=[taus.TauPtCorrection_eleFake],
            ):
                add_shift(name="CMS_scale_t_DM0_genElectron_barrel", shift_key="tau_elefake_es_DM0_barrel")
                add_shift(name="CMS_scale_t_DM0_genElectron_endcap", shift_key="tau_elefake_es_DM0_endcap")
                add_shift(name="CMS_scale_t_DM1_genElectron_barrel", shift_key="tau_elefake_es_DM1_barrel")
                add_shift(name="CMS_scale_t_DM1_genElectron_endcap", shift_key="tau_elefake_es_DM1_endcap")
        elif int(era[:4]) < 2022:
            with defaults(scopes=("et", "mt", "tt")):
                # dm and pt scheme
                with defaults(producers=[taus.TauEnergyCorrection_ES_dm_pt_binned]):
                    for dm, dm_num in [
                        ("1prong0pizero", "0"),
                        ("1prong1pizero", "1"),
                        ("3prong0pizero", "10"),
                        ("3prong1pizero", "11"),
                    ]:
                        for pt in ["20to40", "40toInf"]:
                            add_shift(name=f"CMS_scale_t_DM{dm_num}_genTau_pT{pt}", shift_key=f"tau_ES_shift_{dm}{pt}")

        elif int(era[:4]) >= 2022 and int(era[:4]) < 2024:
            with defaults(scopes=("et", "mt", "tt")):
                with defaults(producers=[taus.TauEnergyCorrection_v12]): # propagate to mass too
                    for dm in ["0", "1", "10", "11"]:
                        # genuine tau
                        add_shift(name=f"CMS_scale_t_DM{dm}_genTau_{shift_era_tag}", shift_key=f"tau_es_DM{dm}")
                        # ele fake
                        add_shift(name=f"CMS_scale_t_DM{dm}_genElectron_barrel_{shift_era_tag}", shift_key=f"tau_elefake_es_DM{dm}_barrel")
                        add_shift(name=f"CMS_scale_t_DM{dm}_genElectron_endcap_{shift_era_tag}", shift_key=f"tau_elefake_es_DM{dm}_endcap")
                        # muon fake
                        add_shift(name=f"CMS_scale_t_DM{dm}_genMuon_{shift_era_tag}", shift_key=f"tau_mufake_es_DM{dm}")
        elif int(era[:4]) >= 2024:
            with defaults(scopes=("et", "mt", "tt")): #is there a reason not to apply this everywhere?
                with defaults(producers=[taus.TauEnergyCorrection]): # propagate to mass too
                    for dm in ["0", "1", "10", "11"]:
                        # genuine tau
                        for pt in ["20to40", "40to60", "60toInf"]:
                            add_shift(name=f"CMS_scale_t_DM{dm}_genTau_pT{pt}_{shift_era_tag}", shift_key=f"tau_es_DM{dm}_pt{pt}")
                        # ele fake
                        add_shift(name=f"CMS_scale_t_DM{dm}_genElectron_barrel_{shift_era_tag}", shift_key=f"tau_elefake_es_DM{dm}_barrel")
                        add_shift(name=f"CMS_scale_t_DM{dm}_genElectron_endcap_{shift_era_tag}", shift_key=f"tau_elefake_es_DM{dm}_endcap")
                        # muon fake
                        add_shift(name=f"CMS_scale_t_DM{dm}_genMuon_{shift_era_tag}", shift_key=f"tau_mufake_es_DM{dm}")

    #########################
    # TauID scale factor shifts
    #########################
    with defaults(
        exclude_samples=["data", "embedding", "embedding_mc"],
        shift_map={"Up": "up", "Down": "down"}
        ):

        if int(era[:4]) < 2022:
            with defaults(scopes=("et", "mt")):
                #dm and pt scheme
                with defaults(producers=[scalefactors.Tau_2_VsJetTauID_lt_SF_dm_pt_binned]):
                    for dm, dm_num in [
                        ("1prong0pizero", "0"),
                        ("1prong1pizero", "1"),
                        ("3prong0pizero", "10"),
                        ("3prong1pizero", "11"),
                    ]:
                        for pt in ["20to40", "40toInf"]:
                            add_shift(name=f"CMS_eff_t_DeepTau2017v2p1_VSjet_DM{dm_num}_pT{pt}", shift_key=f"tau_id_vsjet_{dm}{pt}")
                with defaults(producers=[scalefactors.Tau_2_VsEleTauID_SF_Run2]):
                    add_shift(name="CMS_fake_t_DeepTau2017v2p1_VSe_barrel", shift_key="tau_id_vsele_barrel")
                    add_shift(name="CMS_fake_t_DeepTau2017v2p1_VSe_endcap", shift_key="tau_id_vsele_endcap")
                with defaults(producers=[scalefactors.Tau_2_VsMuTauID_SF]):
                    for wheel in range(1, 6):
                        add_shift(name=f"CMS_fake_t_DeepTau2017v2p1_VSmu_wheel{wheel}", shift_key=f"tau_id_vsmu_wheel{wheel}")
            with defaults(scopes="tt"):
                with defaults(producers=[scalefactors.Tau_1_VsJetTauID_SF_v12, scalefactors.Tau_2_VsJetTauID_tt_SF]):
                    add_shift(name="CMS_eff_t_DeepTau2017v2p1_VSjet_DM0", shift_key="tau_id_vsjet_DM0")
                    add_shift(name="CMS_eff_t_DeepTau2017v2p1_VSjet_DM1", shift_key="tau_id_vsjet_DM1")
                    add_shift(name="CMS_eff_t_DeepTau2017v2p1_VSjet_DM10", shift_key="tau_id_vsjet_DM10")
                    add_shift(name="CMS_eff_t_DeepTau2017v2p1_VSjet_DM11", shift_key="tau_id_vsjet_DM11")
                with defaults(producers=[scalefactors.Tau_1_VsEleTauID_SF_Run2, scalefactors.Tau_2_VsEleTauID_SF_Run2]):
                    add_shift(name="CMS_fake_t_DeepTau2017v2p1_VSe_barrel", shift_key="tau_id_vsele_barrel")
                    add_shift(name="CMS_fake_t_DeepTau2017v2p1_VSe_endcap", shift_key="tau_id_vsele_endcap")
                with defaults(producers=[scalefactors.Tau_1_VsMuTauID_SF, scalefactors.Tau_2_VsMuTauID_SF]):
                    for wheel in range(1, 6):
                        add_shift(name=f"CMS_fake_t_DeepTau2017v2p1_VSmu_wheel{wheel}", shift_key=f"tau_id_vsmu_wheel{wheel}")
            
        else:
            # Naming convention of the eras used inside the TAU POG correctionlib
            # json files for the DM-binned "DeepTau2018v2p5VSjet" SFs (2022-2023),
            # see https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun3
            TAU_JSON_ERA_MAP = {
                "2022preEE": "2022_preEE",
                "2022postEE": "2022_postEE",
                "2023preBPix": "2023_preBPix",
                "2023postBPix": "2023_postBPix",
            }
            vsjet_dms = ["0", "1", "10", "11"]
            for dm in vsjet_dms:
                # vs Ele
                with defaults(name=f"CMS_fake_t_DeepTau2018v2p5_VSe_DM{dm}_barrel_{shift_era_tag}", shift_key=f"tau_id_vsele_DM{dm}_barrel"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsEleTauID_SF])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                with defaults(name=f"CMS_fake_t_DeepTau2018v2p5_VSe_DM{dm}_endcap_{shift_era_tag}", shift_key=f"tau_id_vsele_DM{dm}_endcap"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsEleTauID_SF])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                # vs Jet
                if int(era[:4]) < 2024:
                    # 2022-2023 (NanoAODv12): DM-dependent ("dm" flag) SFs. Per the
                    # TauPOG recommendation the uncertainty is split into:
                    #  - 2 stat. uncertainties per DM, uncorrelated across DM and era
                    #  - 1 syst. uncertainty fully correlated across DM and era ("alleras")
                    #  - 1 syst. uncertainty correlated across DM, uncorrelated across era
                    #  - 1 syst. (TES-induced) uncertainty per DM, uncorrelated across DM and era
                    json_era_tag = TAU_JSON_ERA_MAP[era]
                    with defaults(scopes=("et", "mt", "tt"), producers=[scalefactors.Tau_2_VsJetTauID_SF_v12], shift_key=f"tau_id_vsjet_DM{dm}"):
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_stat1_DM{dm}_{shift_era_tag}", shift_map={"Up": f"stat1_dm{dm}_up", "Down": f"stat1_dm{dm}_down"})
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_stat2_DM{dm}_{shift_era_tag}", shift_map={"Up": f"stat2_dm{dm}_up", "Down": f"stat2_dm{dm}_down"})
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_syst_TES_DM{dm}_{shift_era_tag}", shift_map={"Up": f"syst_TES_{json_era_tag}_dm{dm}_up", "Down": f"syst_TES_{json_era_tag}_dm{dm}_down"})
                    with defaults(scopes=("tt"), producers=[scalefactors.Tau_1_VsJetTauID_SF_v12], shift_key=f"tau_id_vsjet_DM{dm}"):
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_stat1_DM{dm}_{shift_era_tag}", shift_map={"Up": f"stat1_dm{dm}_up", "Down": f"stat1_dm{dm}_down"})
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_stat2_DM{dm}_{shift_era_tag}", shift_map={"Up": f"stat2_dm{dm}_up", "Down": f"stat2_dm{dm}_down"})
                        add_shift(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_syst_TES_DM{dm}_{shift_era_tag}", shift_map={"Up": f"syst_TES_{json_era_tag}_dm{dm}_up", "Down": f"syst_TES_{json_era_tag}_dm{dm}_down"})
                else:
                    for pt in ["20to40", "40to60", "60toInf"]:
                        with defaults(name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_DM{dm}_pT{pt}_{shift_era_tag}", shift_key=f"tau_id_vsjet_DM{dm}_pt{pt}"):
                            add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsJetTauID_SF])
                            add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsJetTauID_SF])

            if int(era[:4]) < 2024:
                # vs Jet uncertainties correlated across decay modes (2022-2023):
                # shift all DM-binned config keys simultaneously.
                json_era_tag = TAU_JSON_ERA_MAP[era]
                with defaults(shift_key=[f"tau_id_vsjet_DM{dm}" for dm in vsjet_dms]):
                    with defaults(scopes=("et", "mt", "tt"), producers=[scalefactors.Tau_2_VsJetTauID_SF_v12]):
                        add_shift(
                            name="CMS_eff_t_DeepTau2018v2p5_VSjet_syst_alleras",
                            shift_map={"Up": ["syst_alleras_up"] * len(vsjet_dms), "Down": ["syst_alleras_down"] * len(vsjet_dms)},
                        )
                        add_shift(
                            name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_syst_{shift_era_tag}",
                            shift_map={"Up": [f"syst_{json_era_tag}_up"] * len(vsjet_dms), "Down": [f"syst_{json_era_tag}_down"] * len(vsjet_dms)},
                        )
                    with defaults(scopes=("tt"), producers=[scalefactors.Tau_1_VsJetTauID_SF_v12]):
                        add_shift(
                            name="CMS_eff_t_DeepTau2018v2p5_VSjet_syst_alleras",
                            shift_map={"Up": ["syst_alleras_up"] * len(vsjet_dms), "Down": ["syst_alleras_down"] * len(vsjet_dms)},
                        )
                        add_shift(
                            name=f"CMS_eff_t_DeepTau2018v2p5_VSjet_syst_{shift_era_tag}",
                            shift_map={"Up": [f"syst_{json_era_tag}_up"] * len(vsjet_dms), "Down": [f"syst_{json_era_tag}_down"] * len(vsjet_dms)},
                        )
            # vs Muon
            for wheel in range(1, 6):
                with defaults(name=f"CMS_fake_t_DeepTau2018v2p5_VSmu_wheel{wheel}_{shift_era_tag}", shift_key=f"tau_id_vsmu_wheel{wheel}"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsMuTauID_SF])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsMuTauID_SF])

    ##########################
    #### Jet variations ######
    #########################
    
    class JES_CONFIG:
        REGROUPED = True
        jet_pt_correction_producer = jets.JetEnergyCorrection_Run2 if int(era[:4])<2022 else jets.JetEnergyCorrection

    with defaults(exclude_samples=["data", "embedding", "embedding_mc"]):
        if int(era[:4]) < 2022:
            with defaults(
                scopes=("mt", "et", "tt"),
                shift_key="btag_sf_variation",
                producers=[scalefactors.btagging_SF],
            ):
                add_shift(name="CMS_btag_fullShape_hf", shift_map={"Up": "up_hf", "Down": "down_hf"})
                add_shift(name=f"CMS_btag_fullShape_hfstats1_{era_tag}", shift_map={"Up": "up_hfstats1", "Down": "down_hfstats1"})
                add_shift(name=f"CMS_btag_fullShape_hfstats2_{era_tag}", shift_map={"Up": "up_hfstats2", "Down": "down_hfstats2"})
                add_shift(name="CMS_btag_fullShape_lf", shift_map={"Up": "up_lf", "Down": "down_lf"})
                add_shift(name=f"CMS_btag_fullShape_lfstats1_{era_tag}", shift_map={"Up": "up_lfstats1", "Down": "down_lfstats1"})
                add_shift(name=f"CMS_btag_fullShape_lfstats2_{era_tag}", shift_map={"Up": "up_lfstats2", "Down": "down_lfstats2"})
                add_shift(name="CMS_btag_fullShape_cferr1", shift_map={"Up": "up_cferr1", "Down": "down_cferr1"})
                add_shift(name="CMS_btag_fullShape_cferr2", shift_map={"Up": "up_cferr2", "Down": "down_cferr2"})
        else:
            with defaults(
                scopes=("mt", "et", "tt"),
                producers=[scalefactors.btaggingWP_SF],
            ):
                add_shift(
                    name="CMS_btag_fixedWP_bc_correlated",
                    shift_key=["btag_sf_variation_bc", "btag_sf_variation_lf"],
                    shift_map={"Up": ["up_correlated", "central"], "Down": ["down_correlated", "central"]},
                )
                add_shift(
                    name=f"CMS_btag_fixedWP_bc_uncorrelated_{era_tag}",
                    shift_key=["btag_sf_variation_bc", "btag_sf_variation_lf"],
                    shift_map={"Up": ["up_uncorrelated", "central"], "Down": ["down_uncorrelated", "central"]},
                )
                add_shift(
                    name="CMS_btag_fixedWP_light_correlated",
                    shift_key=["btag_sf_variation_bc", "btag_sf_variation_lf"],
                    shift_map={"Up": ["central", "up_correlated"], "Down": ["central", "down_correlated"]},
                )
                add_shift(
                    name=f"CMS_btag_fixedWP_light_uncorrelated_{era_tag}",
                    shift_key=["btag_sf_variation_bc", "btag_sf_variation_lf"],
                    shift_map={"Up": ["central", "up_uncorrelated"], "Down": ["central", "down_uncorrelated"]},
                )

        with defaults(scopes="global", producers=[JES_CONFIG.jet_pt_correction_producer]):
            add_shift(name=f"CMS_res_j_{era_tag}", shift_key="jet_jer_shift", shift_map={"Up": "up", "Down": "down"})
            if era == "2018":  # --- HEM 15/16 issue ---
                add_shift(
                    name="CMS_scale_j_HEMIssue_2018",
                    shift_key=["jet_jes_shift", "jet_jes_source"],
                    shift_map={"Up": [1, "HEMIssue"], "Down": [-1, "HEMIssue"]},
                )

        with defaults(name="CMS_scale_j_Total"):  # two components of CMS_scale_j_Total
            add_shift(
                shift_key=["jet_jes_shift", "jet_jes_source"],
                shift_map={"Up": [1, "Total"], "Down": [-1, "Total"]},
                scopes="global",
                producers=[JES_CONFIG.jet_pt_correction_producer]
            )
            if int(era[:4]) < 2022:
                add_shift(
                    shift_key="btag_sf_variation",
                    shift_map={"Up": "up_jes", "Down": "down_jes"},
                    scopes=("mt", "et", "tt"),
                    producers=[scalefactors.btagging_SF]
                )

        if not JES_CONFIG.REGROUPED:
            for name in [
                # --- CMS_scale_j_Absolute ---
                "SinglePionECAL",
                "SinglePionHCAL",
                "AbsoluteMPFBias",
                "AbsoluteScale",
                "Fragmentation",
                "PileUpDataMC",
                "RelativeFSR",
                "PileUpPtRef",
                # --- CMS_scale_j_Absolute_{era} ---
                "AbsoluteStat",
                "TimePtEta",
                "RelativeStatFSR",
                # --- CMS_scale_j_FlavorQCD ---
                "FlavorQCD",
                # --- CMS_scale_j_BBEC1 ---
                "PileUpPtEC1",
                "PileUpPtBB",
                "RelativePtBB",
                # --- CMS_scale_j_BBEC1_{era} ---
                "RelativeJEREC1",
                "RelativePtEC1",
                "RelativeStatEC",
                # --- CMS_scale_j_HF ---
                "RelativePtHF",
                "PileUpPtHF",
                "RelativeJERHF",
                # --- CMS_scale_j_HF_{era} ---
                "RelativeStatHF",
                # --- CMS_scale_j_EC2 ---
                "PileUpPtEC2",
                # --- CMS_scale_j_EC2_{era} ---
                "RelativeJEREC2",
                "RelativePtEC2",
                # --- CMS_scale_j_RelativeBal ---
                "RelativeBal",
                # --- CMS_scale_j_RelativeSample_{era} ---
                "RelativeSample",
            ]:
                # two components of CMS_scale_j_{name}
                with defaults(name=f"CMS_scale_j_{name}"):
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_source"],
                        shift_map={"Up": [1, name], "Down": [-1, name]},
                        scopes="global",
                        producers=[JES_CONFIG.jet_pt_correction_producer]
                    )
                    if int(era[:4]) < 2022:
                        add_shift(
                            shift_key="btag_sf_variation",
                            shift_map={"Up": f"up_jes{name}", "Down": f"down_jes{name}"},
                            scopes=("mt", "et", "tt"),
                            producers=[scalefactors.btagging_SF]
                        )

        else:  # preferred configuration
            for name, JES_source, *is_yearly in [
                ("Absolute", "Regrouped_Absolute"),
                ("FlavorQCD", "Regrouped_FlavorQCD"),
                ("BBEC1", "Regrouped_BBEC1"),
                ("HF", "Regrouped_HF"),
                ("EC2", "Regrouped_EC2"),
                ("RelativeBal", "Regrouped_RelativeBal"),
                # --- Yearly variations ---
                ("Absolute", lambda era: f"Regrouped_Absolute_{ERA_MAP[era]}", era),
                ("BBEC1", lambda era: f"Regrouped_BBEC1_{ERA_MAP[era]}", era),
                ("HF", lambda era: f"Regrouped_HF_{ERA_MAP[era]}", era),
                ("EC2", lambda era: f"Regrouped_EC2_{ERA_MAP[era]}", era),
                ("RelativeSample", lambda era: f"Regrouped_RelativeSample_{ERA_MAP[era]}", era),
            ]:
                with defaults(name=f"CMS_scale_j_{name}_{era_tag}" if is_yearly else f"CMS_scale_j_{name}"):
                    JES_source_val = JES_source(era) if is_yearly else JES_source
                    add_shift(
                        shift_key=["jet_jes_shift", "jet_jes_source"],
                        shift_map={"Up": [1, JES_source_val], "Down": [-1, JES_source_val]},
                        scopes="global",
                        producers=[JES_CONFIG.jet_pt_correction_producer],
                    )

                    if int(era[:4]) < 2022:
                        btag_variation_source = f"{name}_{era}" if is_yearly else name
                        add_shift(
                            shift_key="btag_sf_variation",
                            shift_map={"Up": f"up_jes{btag_variation_source}", "Down": f"down_jes{btag_variation_source}"},
                            scopes=("mt", "et", "tt"),
                            producers=[scalefactors.btagging_SF]
                        )

    #########################
    # Trigger scale factor shifts (Run 3)
    #########################
    for variation in ["up", "down"]:
        configuration.add_shift(
            SystematicShift(
                name=f"CMS_eff_e_trigger{variation.upper()}",
                shift_config={
                    ("et"): {
                        "singleelectron_trigger_sf": [
                            {
                                "singleelectron_trigger_flagname": "trg_wgt_single_ele30",
                                "singleelectron_trigger_flag": "trg_single_ele30",
                                "singleelectron_trigger_sf_name": "Electron-HLT-SF",
                                "singleelectron_trigger_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                                "singleelectron_trigger_variation": f"sf{variation}",
                            },
                        ],
                    }
                },
                producers={("et"): scalefactors.SingleEleTriggerSF},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"CMS_trig_etau_cross{variation.upper()}",
                shift_config={
                    ("et"): {
                        "eletau_cross_trigger_leg1_sf": [
                            {
                                "eletau_cross_trigger_leg1_flagname": "trg_wgt_ele24tau30_leg1",
                                "eletau_cross_trigger_flag": EraModifier(
                                    {"2025": "trg_cross_ele24tau30_pnet", "2026": "trg_cross_ele24tau30_pnet"},
                                    default="trg_cross_ele24tau30_hps",
                                ),
                                "eletau_cross_trigger_leg1_sf_name": "Electron-HLT-SF",
                                "eletau_cross_trigger_leg1_path_id_name": "HLT_SF_Ele24_TightID",
                                "eletau_cross_trigger_leg1_variation": f"sf{variation}",
                            },
                        ],
                        "eletau_cross_trigger_leg2_sf": [
                            {
                                "eletau_cross_trigger_leg2_flagname": "trg_wgt_ele24tau30_leg2",
                                "eletau_cross_trigger_flag": EraModifier(
                                    {"2025": "trg_cross_ele24tau30_pnet", "2026": "trg_cross_ele24tau30_pnet"},
                                    default="trg_cross_ele24tau30_hps",
                                ),
                                "eletau_cross_trigger_leg2_sf_name": "etau",
                                "eletau_cross_trigger_leg2_variation": variation,
                            },
                        ]
                    },
                },
                producers={
                    ("et"): [
                        scalefactors.EleTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
                SystematicShift(
                    name=f"CMS_eff_m_trigger_syst{variation.upper()}",
                    shift_config={
                        ("mt"): {
                            "singlemuon_trigger_sf": [
                                {
                                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                                    "singlemuon_trigger_flag": "trg_single_mu24",
                                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "singlemuon_trigger_variation": f"syst{variation}",
                                },
                            ],
                        }
                    },
                    producers={("mt"): scalefactors.SingleMuTriggerSF},
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )
        configuration.add_shift(
                SystematicShift(
                    name=f"CMS_eff_m_trigger_stat_{shift_era_tag}{variation.upper()}",
                    shift_config={
                        ("mt"): {
                            "singlemuon_trigger_sf": [
                                {
                                    "singlemuon_trigger_flagname": "trg_wgt_single_mu24",
                                    "singlemuon_trigger_flag": "trg_single_mu24",
                                    "singlemuon_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "singlemuon_trigger_variation": f"stat{variation}",
                                },
                            ],
                        }
                    },
                    producers={("mt"): scalefactors.SingleMuTriggerSF},
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )
        configuration.add_shift(
            SystematicShift(
                name=f"CMS_trig_mutau_cross_syst{variation.upper()}",
                shift_config={
                    ("mt"): {
                        "mutau_trigger_leg1_sf": [
                            {
                                "mutau_cross_trigger_flag": EraModifier(
                                    {"2025": "trg_cross_mu20tau27_pnet", "2026": "trg_cross_mu20tau27_pnet"},
                                    default="trg_cross_mu20tau27_hps",
                                ),
                                "mutau_cross_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                                "mutau_cross_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                                "mutau_cross_trigger_leg1_variation": f"syst{variation}",
                            },
                        ],
                        "mutau_trigger_leg2_sf": [
                            {
                                "mutau_cross_trigger_flag": EraModifier(
                                    {"2025": "trg_cross_mu20tau27_pnet", "2026": "trg_cross_mu20tau27_pnet"},
                                    default="trg_cross_mu20tau27_hps",
                                ),
                                "mutau_cross_trigger_leg2_flagname": "trg_wgt_mu20tau27_leg2",
                                "mutau_cross_trigger_leg2_sf_name": "mutau",
                                "mutau_cross_trigger_leg2_variation": variation,
                            },
                        ],
                    },
                },
                producers={
                    ("mt"): [
                        scalefactors.MuTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"CMS_trig_mutau_cross_stat_{shift_era_tag}{variation.upper()}",
                shift_config={
                    ("mt"): {
                        "mutau_trigger_leg1_sf": [
                            {
                                "mutau_cross_trigger_flag": EraModifier(
                                    {"2025": "trg_cross_mu20tau27_pnet", "2026": "trg_cross_mu20tau27_pnet"},
                                    default="trg_cross_mu20tau27_hps",
                                ),
                                "mutau_cross_trigger_leg1_flagname": "trg_wgt_mu20tau27_leg1",
                                "mutau_cross_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                                "mutau_cross_trigger_leg1_variation": f"stat{variation}",
                            },
                        ],
                    },
                },
                producers={
                    ("mt"): [
                        scalefactors.MuTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name=f"CMS_trig_t_ditau_cross{variation.upper()}",
                shift_config={
                    ("tt"): {
                        "doubletau_trigger_leg1_sf": [
                            {
                                "doubletau_trigger_leg1_flagname": EraModifier(
                                    {
                                        **{era: '""' for era in RUN2_ERAS},
                                        **{era: "trg_wgt_doubletau35_leg1" for era in DOUBLETAU_HPS_ERAS},
                                    },
                                    default="trg_wgt_doubletau30_leg1",  # 2024, 2025, 2026
                                ),
                                "doubletau_trigger_flag": EraModifier(
                                    {
                                        **{era: '""' for era in RUN2_ERAS},
                                        **{era: "trg_double_tau35_mediumiso_hps" for era in DOUBLETAU_HPS_ERAS},
                                    },
                                    default="trg_double_tau30_mediumiso_pnet",  # 2024, 2025, 2026
                                ),
                                "doubletau_trigger_leg1_sf_name": EraModifier(
                                    {era: '""' for era in RUN2_ERAS},
                                    default="ditau",  # all Run 3 eras
                                ),
                                "doubletau_trigger_leg1_variation": variation,
                            },
                        ],
                        "doubletau_trigger_leg2_sf": [
                            {
                                "doubletau_trigger_leg2_flagname": EraModifier(
                                    {
                                        **{era: '""' for era in RUN2_ERAS},
                                        **{era: "trg_wgt_doubletau35_leg2" for era in DOUBLETAU_HPS_ERAS},
                                    },
                                    default="trg_wgt_doubletau30_leg2",  # 2024, 2025, 2026
                                ),
                                "doubletau_trigger_flag": EraModifier(
                                    {
                                        **{era: '""' for era in RUN2_ERAS},
                                        **{era: "trg_double_tau35_mediumiso_hps" for era in DOUBLETAU_HPS_ERAS},
                                    },
                                    default="trg_double_tau30_mediumiso_pnet",  # 2024, 2025, 2026
                                ),
                                "doubletau_trigger_leg2_sf_name": EraModifier(
                                    {era: '""' for era in RUN2_ERAS},
                                    default="ditau",  # all Run 3 eras
                                ),
                                "doubletau_trigger_leg2_variation": variation,
                            },
                        ],
                    },
                },
                producers={
                    ("tt"): [
                        scalefactors.DoubleTauTriggerSF,
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )

    #########################
    # Trigger scale factor shifts (Run 2, embedding framework)
    #########################
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFUp",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": EraModifier(
                        {
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_ele32orele35",
                                        "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele32",
                                        "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele35",
                                        "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele27orele32orele35",
                                        "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                ]
                                for era in ["2017", "2018"]
                            },
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_ele25",
                                        "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    }
                                ]
                                for era in ["2016preVFP", "2016postVFP"]
                            },
                        },
                        default=[  ## TODO: not implemented, here as a placeholder (2022preEE, 2022postEE, 2023preBPix, 2023postBPix, 2024, 2025, 2026)
                            {
                                "flagname": '""',
                                "mc_trigger_sf": '""',
                                "mc_trg_extrapolation": 1.0,  # for nominal case
                            },
                        ],
                    )
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleElectronTriggerSFDown",
            shift_config={
                ("et"): {
                    "singlelectron_trigger_sf_mc": EraModifier(
                        {
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_ele32orele35",
                                        "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele32",
                                        "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele35",
                                        "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_ele27orele32orele35",
                                        "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                ]
                                for era in ["2017", "2018"]
                            },
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_ele25",
                                        "mc_trigger_sf": "Trg25_Iso_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    }
                                ]
                                for era in ["2016preVFP", "2016postVFP"]
                            },
                        },
                        default=[  ## TODO: not implemented, here as a placeholder (2022preEE, 2022postEE, 2023preBPix, 2023postBPix, 2024, 2025, 2026)
                            {
                                "flagname": '""',
                                "mc_trigger_sf": '""',
                                "mc_trg_extrapolation": 1.0,  # for nominal case
                            },
                        ],
                    )
                }
            },
            producers={("et"): scalefactors.ETGenerateSingleElectronTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFUp",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_mu24",
                                        "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_mu27",
                                        "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_mu24ormu27",
                                        "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                ]
                                for era in ["2017", "2018"]
                            },
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_mu22",
                                        "mc_trigger_sf": "Trg_pt_eta_bins",
                                        "mc_trg_extrapolation": 1.02,
                                    },
                                ]
                                for era in ["2016preVFP", "2016postVFP"]
                            },
                        },
                        default=[  ## TODO: not implemented, here as a placeholder (2022preEE, 2022postEE, 2023preBPix, 2023postBPix, 2024, 2025, 2026)
                            {
                                "flagname": '""',
                                "mc_trigger_sf": '""',
                                "mc_trg_extrapolation": 1.0,  # for nominal case
                            },
                        ],
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="singleMuonTriggerSFDown",
            shift_config={
                ("mt"): {
                    "singlemuon_trigger_sf_mc": EraModifier(
                        {
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_mu24",
                                        "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_mu27",
                                        "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                    {
                                        "flagname": "trg_wgt_single_mu24ormu27",
                                        "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                ]
                                for era in ["2017", "2018"]
                            },
                            **{
                                era: [
                                    {
                                        "flagname": "trg_wgt_single_mu22",
                                        "mc_trigger_sf": "Trg_pt_eta_bins",
                                        "mc_trg_extrapolation": 0.98,
                                    },
                                ]
                                for era in ["2016preVFP", "2016postVFP"]
                            },
                        },
                        default=[  ## TODO: not implemented, here as a placeholder (2022preEE, 2022postEE, 2023preBPix, 2023postBPix, 2024, 2025, 2026)
                            {
                                "flagname": '""',
                                "mc_trigger_sf": '""',
                                "mc_trg_extrapolation": 1.0,  # for nominal case
                            },
                        ],
                    )
                }
            },
            producers={("mt"): scalefactors.MTGenerateSingleMuonTriggerSF_MC},
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    return configuration
