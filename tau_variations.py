from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import scalefactors as scalefactors
from .producers import pairselection as pairselection
from .producers import muons as muons
from .producers import electrons as electrons
from .producers import taus as taus
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


def add_tauVariations(configuration: Configuration, sample: str, era: str, run2_v15: bool) -> Configuration:

    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    with defaults(
        shift_map={"Up": "up", "Down": "down"}
        ):
        
        #########################
        # Lepton to tau fakes energy scalefactor shifts  #
        #########################
        if int(era[:4]) < 2022:
            if ("dyjets" in sample or "electroweak_boson" in sample):
                add_shift(
                    name="tauMuFakeEs",
                    shift_key="tau_mufake_es",
                    scopes="mt",
                    producers=[taus.TauPtCorrection_muFake_v15],
                )
                with defaults(
                    scopes="et",
                    producers=[taus.TauPtCorrection_eleFake_v15],
                ):
                    add_shift(name="tauEleFakeEsDM0Barrel", shift_key="tau_elefake_es_DM0_barrel")
                    add_shift(name="tauEleFakeEsDM0Endcap", shift_key="tau_elefake_es_DM0_endcap")
                    add_shift(name="tauEleFakeEsDM1Barrel", shift_key="tau_elefake_es_DM1_barrel")
                    add_shift(name="tauEleFakeEsDM1Endcap", shift_key="tau_elefake_es_DM1_endcap")
            with defaults(scopes=("et", "mt", "tt")):
                with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerGroupES],
                              exclude_samples=["data", "embedding", "embedding_mc"]): 
                    for dm in ["DM0", "DM1", "DM10", "DM11"]:
                        for pt in configuration.ES_ID_SCHEME.pt_binning:
                            add_shift(name=f"tauEs{dm}{pt}", shift_key=f"tau_ES_shift_{dm}{pt}")

        elif int(era[:4]) >= 2022:
            with defaults(scopes=("et", "mt", "tt")): # This is not doing anything ... ?
                with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerGroupES]): # propagate to mass too
                    for dm in ["0", "1", "10", "11"]:
                        # genuine tau
                        add_shift(name=f"tauEsDM{dm}", shift_key=f"tau_ES_shift_DM{dm}")
                        # ele fake
                        add_shift(name=f"tauEleFakeEsDM{dm}", shift_key=f"tau_elefake_es_DM{dm}")
                    # muon fake
                    add_shift(name="tauMuFakeEs", shift_key="tau_mufake_es")

        #########################
        # TauID scale factor shifts
        #########################
        with defaults(
            exclude_samples=["data", "embedding", "embedding_mc"]
            ):

            if int(era[:4]) < 2022:
                with defaults(scopes=("et", "mt")):
                    with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerID]):
                        for dm in ["DM0", "DM1", "DM10", "DM11"]:
                            for pt in configuration.ES_ID_SCHEME.pt_binning:
                                add_shift(name=f"vsJetTau{dm}{pt}", shift_key=f"tau_sf_vsjet_{dm}{pt}")
                    with defaults(producers=[scalefactors.Tau_2_VsEleTauID_SF]):
                        add_shift(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel")
                        add_shift(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap")
                    with defaults(producers=[scalefactors.Tau_2_VsMuTauID_SF]):
                        for wheel in range(1, 6):
                            add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}")
                with defaults(scopes="tt"):
                    with defaults(producers=[scalefactors.Tau_1_VsJetTauID_SF, scalefactors.Tau_2_VsJetTauID_tt_SF]):
                        add_shift(name="vsJetTauDM0", shift_key="tau_sf_vsjet_tauDM0")
                        add_shift(name="vsJetTauDM1", shift_key="tau_sf_vsjet_tauDM1")
                        add_shift(name="vsJetTauDM10", shift_key="tau_sf_vsjet_tauDM10")
                        add_shift(name="vsJetTauDM11", shift_key="tau_sf_vsjet_tauDM11")
                    with defaults(producers=[scalefactors.Tau_1_VsEleTauID_SF, scalefactors.Tau_2_VsEleTauID_SF]):
                        add_shift(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel")
                        add_shift(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap")
                    with defaults(producers=[scalefactors.Tau_1_VsMuTauID_SF, scalefactors.Tau_2_VsMuTauID_SF]):
                        for wheel in range(1, 6):
                            add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}")
                
            else:
                # vs Ele
                with defaults(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsEleTauID_SF])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                with defaults(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsEleTauID_SF])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                # vs Muon
                for wheel in range(1, 6):
                    with defaults(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}"):
                        add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsMuTauID_SF])
                        add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsMuTauID_SF])
                # vs Jet
                with defaults(
                    name="tau_vsjet_variation",
                    shift_key="tau_sf_vsjet_variation",
                ):
                    add_shift(scopes=("et", "mt", "tt"),producers=[configuration.ES_ID_SCHEME.mc.producerID]) #scalefactors.Tau_2_VsJetTauID_SF
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsJetTauID_SF])














        #### OLD ####
        # if int(era[:4]) < 2022 and not run2_v15:
        #     with defaults(scopes=("et", "mt")):
        #         with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerID]):
        #             for dm in ["DM0", "DM1", "DM10", "DM11"]:
        #                 for pt in configuration.ES_ID_SCHEME.pt_binning:
        #                     add_shift(name=f"vsJetTau{dm}{pt}", shift_key=f"tau_sf_vsjet_{dm}{pt}")
        #         with defaults(producers=[scalefactors.Tau_2_VsEleTauID_SF]):
        #             add_shift(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel")
        #             add_shift(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap")
        #         with defaults(producers=[scalefactors.Tau_2_VsMuTauID_SF]):
        #             for wheel in range(1, 6):
        #                 add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}")
        #     with defaults(scopes="tt"):
        #         with defaults(producers=[scalefactors.Tau_1_VsJetTauID_SF, scalefactors.Tau_2_VsJetTauID_tt_SF]):
        #             add_shift(name="vsJetTauDM0", shift_key="tau_sf_vsjet_tauDM0")
        #             add_shift(name="vsJetTauDM1", shift_key="tau_sf_vsjet_tauDM1")
        #             add_shift(name="vsJetTauDM10", shift_key="tau_sf_vsjet_tauDM10")
        #             add_shift(name="vsJetTauDM11", shift_key="tau_sf_vsjet_tauDM11")
        #         with defaults(producers=[scalefactors.Tau_1_VsEleTauID_SF, scalefactors.Tau_2_VsEleTauID_SF]):
        #             add_shift(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel")
        #             add_shift(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap")
        #         with defaults(producers=[scalefactors.Tau_1_VsMuTauID_SF, scalefactors.Tau_2_VsMuTauID_SF]):
        #             for wheel in range(1, 6):
        #                 add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}")
        #     # --- TES shifts ---
        #     with defaults(scopes=("et", "mt", "tt")):
        #         with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerES]):
        #             for dm in ["DM0", "DM1", "DM10", "DM11"]:
        #                 for pt in configuration.ES_ID_SCHEME.pt_binning:
        #                     add_shift(name=f"tauEs{dm}{pt}", shift_key=f"tau_ES_shift_{dm}{pt}")
    
        # # else:
        #     # ES variation
        #     add_shift(
        #         name="tau_es_variation_run3",
        #         shift_key="tau_es_variation",
        #         scopes=("et", "mt", "tt"),
        #         producers=[configuration.ES_ID_SCHEME.mc.producerGroupES],
        #     )
        #     # ID SF variations
        #     with defaults(
        #         name="tau_vsele_variation",
        #         shift_key="tau_sf_vsele_variation",
        #     ):
        #         add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsEleTauID_SF])
        #         add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
            
        #     with defaults(
        #         name="tau_vsmu_variation",
        #         shift_key="tau_sf_vsmu_variation",
        #     ):
        #         add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.Tau_2_VsMuTauID_SF])
        #         add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsMuTauID_SF])
            
        #     with defaults(
        #         name="tau_vsjet_variation",
        #         shift_key="tau_sf_vsjet_variation",
        #     ):
        #         add_shift(scopes=("et", "mt", "tt"),producers=[configuration.ES_ID_SCHEME.mc.producerID]) #scalefactors.Tau_2_VsJetTauID_SF
        #         add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsJetTauID_SF])

    return configuration
