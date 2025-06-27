from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import jets as jets
from .scripts.CROWNWrapper import defaults, get_adjusted_add_shift_SystematicShift


def add_jetCorrectionData(configuration: Configuration, era: str):
    #########################
    # Jet energy corrections for data
    #########################

    add_shift = get_addjusted_add_shift_SystematicShift(configuration)

    with defaults(
        scopes="global",
        shift_key="jet_jes_tag_data",
        producers=[jets.JetEnergyCorrection_data],
        samples=["data"],
    ):
        if era == "2018":
            add_shift(name="jec2018A", shift_map={"": '"Summer19UL18_RunA_V5_DATA"'})
            add_shift(name="jec2018B", shift_map={"": '"Summer19UL18_RunB_V5_DATA"'})
            add_shift(name="jec2018C", shift_map={"": '"Summer19UL18_RunC_V5_DATA"'})
            add_shift(name="jec2018D", shift_map={"": '"Summer19UL18_RunD_V5_DATA"'})
        if era == "2017":
            add_shift(name="jec2017B", shift_map={"": '"Summer19UL17_RunB_V5_DATA"'})
            add_shift(name="jec2017C", shift_map={"": '"Summer19UL17_RunC_V5_DATA"'})
            add_shift(name="jec2017D", shift_map={"": '"Summer19UL17_RunD_V5_DATA"'})
            add_shift(name="jec2017E", shift_map={"": '"Summer19UL17_RunE_V5_DATA"'})
            add_shift(name="jec2017F", shift_map={"": '"Summer19UL17_RunF_V5_DATA"'})
        if era == "2016postVFP":
            add_shift(name="jec2016FGHpostVFP", shift_map={"": '"Summer19UL16_RunFGH_V7_DATA"'})
        if era == "2016preVFP":
            add_shift(name="jec2016BCDpreVFP", shift_map={"": '"Summer19UL16APV_RunBCD_V7_DATA"'})
            add_shift(name="jec2016EFpreVFP", shift_map={"": '"Summer19UL16APV_RunEF_V7_DATA"'})
