from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of photons
####################


PhotonPtCut = Producer(
    name="PhotonPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_photon_pt})",
    input=[nanoAOD.Photon_pt],
    output=[],
    scopes=["global"],
)
PhotonEtaCut = Producer(
    name="PhotonEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_photon_eta})",
    input=[nanoAOD.Photon_eta],
    output=[],
    scopes=["global"],
)
PhotonElectronVeto = Producer(
    name="PhotonElectronVeto",
    call="physicsobject::CutEqual<bool>({df}, {output}, {input}, true)",
    input=[nanoAOD.Photon_electronVeto],
    output=[],
    scopes=["global"],
)

BasePhotons = ProducerGroup(
    name="BasePhotons",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[q.base_photons_mask],
    scopes=["global"],
    subproducers=[
        PhotonPtCut,
        PhotonEtaCut,
        PhotonElectronVeto,
    ],
)
