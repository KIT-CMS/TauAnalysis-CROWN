from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from ..scripts.CROWNWrapper import Producer, ProducerGroup, defaults

####################
# Set of producers used for loosest selection of photons
####################

with defaults(scopes=["global"]):
    with defaults(output=[]):
        PhotonPtCut = Producer(
            call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_photon_pt})",
            input=[nanoAOD.Photon_pt],
        )
        PhotonEtaCut = Producer(
            call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_photon_eta})",
            input=[nanoAOD.Photon_eta],
        )
        PhotonElectronVeto = Producer(
            call="physicsobject::CutEqual<bool>({df}, {output}, {input}, true)",
            input=[nanoAOD.Photon_electronVeto],
        )

    BasePhotons = ProducerGroup(
        call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
        input=[],
        output=[q.base_photons_mask],
        subproducers=[PhotonPtCut, PhotonEtaCut, PhotonElectronVeto],
    )
