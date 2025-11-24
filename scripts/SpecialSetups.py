from dataclasses import dataclass
from ..producers import taus, embedding

@dataclass
class _Embedding_ES_ID_Scheme_dm_binned:
    producerES = taus.TauPtCorrection_emb_genTau_dm_binned
    producerGroupES = taus.TauEnergyCorrection_Embedding_ES_dm_binned
    producerID = embedding.Tau_2_VsJetTauID_lt_SF_dm_binned
    json_name = "tau_energy_scale_dm_binned"
    vsjet_sf_dependence = "dm"
    pt_binning = [""]



@dataclass
class _Embedding_ES_ID_Scheme_dm_pt_binned:
    producerES = taus.TauPtCorrection_emb_genTau_dm_pt_binned
    producerGroupES = taus.TauEnergyCorrection_Embedding_ES_dm_pt_binned
    producerID = embedding.Tau_2_VsJetTauID_lt_SF_dm_pt_binned
    json_name = "tau_energy_scale"
    vsjet_sf_dependence = "pt"
    pt_binning = ["20to40", "40toInf"]


@dataclass
class _MC_ES_ID_Scheme_dm_binned:
    pass


@dataclass
class _MC_ES_ID_Scheme_dm_pt_binned:
    pass


class ES_ID_SCHEME:
    def __init__(self, scheme: str = "dm_pt_binned"):
        self.scheme = scheme
        self.is_dm_binned = scheme == "dm_binned"
        self.is_dm_pt_binned = scheme == "dm_pt_binned"

        if self.is_dm_binned:
            self.embedding = _Embedding_ES_ID_Scheme_dm_binned()
            self.mc = _MC_ES_ID_Scheme_dm_binned()
        elif self.is_dm_pt_binned:
            self.embedding = _Embedding_ES_ID_Scheme_dm_pt_binned()
            self.mc = _MC_ES_ID_Scheme_dm_pt_binned()
        else:
            raise ValueError(f"Unknown ES/ID scheme: {scheme}, known schemes are 'dm_binned' and 'dm_pt_binned'")


class __ES_ID_SCHEME:
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
