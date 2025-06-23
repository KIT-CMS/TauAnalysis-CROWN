from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD

from ..scripts.ProducerWrapper import (
    AutoProducer as Producer,
    AutoProducerGroup as ProducerGroup,
    scopes,
)

####################
# Set of producers used for loosest selection of photons
####################

with scopes(["global"]):
    PhotonPtCut = Producer(
        call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_photon_pt})",
        input=[nanoAOD.Photon_pt],
        output=[],
    )
    PhotonEtaCut = Producer(
        call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_photon_eta})",
        input=[nanoAOD.Photon_eta],
        output=[],
    )
    PhotonElectronVeto = Producer(
        call="physicsobject::CutEqual<bool>({df}, {output}, {input}, true)",
        input=[nanoAOD.Photon_electronVeto],
        output=[],
    )
    BasePhotons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_photons_mask],
        subproducers=[
            PhotonPtCut,
            PhotonEtaCut,
            PhotonElectronVeto,
        ],
    )
