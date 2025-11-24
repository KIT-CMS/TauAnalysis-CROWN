from ..producers import taus, embedding


class ES_ID_SCHEME:
    def __init__(self, scheme: str = "dm_pt_binned"):
        self.scheme = scheme

    @property
    def ProducerES(self):
        return taus.TauPtCorrection_emb_genTau_dm_binned if self.scheme == "dm_binned" else taus.TauPtCorrection_emb_genTau_dm_pt_binned

    @property
    def ProducerGroupES(self):
        return taus.TauEnergyCorrection_Embedding_ES_dm_binned if self.scheme == "dm_binned" else taus.TauEnergyCorrection_Embedding_ES_dm_pt_binned

    @property
    def ProducerID(self):
        return embedding.Tau_2_VsJetTauID_lt_SF_dm_binned if self.scheme == "dm_binned" else embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned

    @property
    def tau_emb_ES_json_name(self):
        return "tau_energy_scale_dm_binned" if self.scheme == "dm_binned" else "tau_energy_scale"

    @property
    def tau_emb_vsjet_sf_dependence(self):
        return "dm" if self.scheme == "dm_binned" else "pt"

    @property
    def pt_binning(self):
        return ["20to40", "40toInf"] if self.scheme == "dm_pt_binned" else [""]
