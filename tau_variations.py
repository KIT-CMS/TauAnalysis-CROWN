from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import scalefactors as scalefactors
from .producers import pairselection as pairselection
from .producers import muons as muons
from .producers import electrons as electrons
from .producers import taus as taus
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


def add_tauVariations(configuration: Configuration, sample: str, era: str) -> Configuration:
    if sample == "embedding" or sample == "embedding_mc" or sample == "data":
        return configuration

    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    with defaults(shift_map={"Up": "up", "Down": "down"}):
        with defaults(scopes=("et", "mt")):
            with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerID]):
                for dm in ["1prong0pizero", "1prong1pizero", "3prong0pizero", "3prong1pizero"]:
                    for pt in configuration.ES_ID_SCHEME.pt_binning:
                        add_shift(name=f"vsJetTau{dm}{pt}", shift_key=f"tau_sf_vsjet_{dm}{pt}")
            with defaults(producers=[scalefactors.Tau_2_VsEleTauID_SF]):
                add_shift(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel")
                add_shift(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap")
            with defaults(producers=[scalefactors.Tau_2_VsMuTauID_SF]):
                for wheel in range(1, 6):
                    add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}")
        # --- TES shifts ---
        with defaults(scopes=("et", "mt", "tt")):
            with defaults(producers=[configuration.ES_ID_SCHEME.mc.producerES]):
                for dm in ["1prong0pizero", "1prong1pizero", "3prong0pizero", "3prong1pizero"]:
                    for pt in configuration.ES_ID_SCHEME.pt_binning:
                        add_shift(name=f"tauEs{dm}{pt}", shift_key=f"tau_ES_shift_{dm}{pt}")

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

    return configuration
