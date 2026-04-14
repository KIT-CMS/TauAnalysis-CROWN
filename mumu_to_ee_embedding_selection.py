from __future__ import annotations

from typing import List

from .producers import genparticles as genparticles
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import event as event
from .producers import electrons as electrons
from .producers import embedding as embedding
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import AppendProducer, RemoveProducer
from .scripts.CROWNWrapper import BaseFilter, Producer, Filter
from .producers import triggers as triggers
from .tau_triggersetup import add_diTauTriggerSetup

def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
) -> Configuration:
    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )
    configuration.add_config_parameters(
        "global",
        {
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                    "2024": "data/golden_json/Cert_Collisions2024_378981_386951_Golden.json",
                }
            ),
        },
    )
    configuration.add_config_parameters(
        "global",
        {
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                    "2024": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-02/puWeights_BCDEFGHI.json.gz",
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2016preVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2016postVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
                    "2024": "Collisions24_BCDEFGHI_goldenJSON",
                }
            ),
            "PU_reweighting_variation": "nominal",
        },
    )

    configuration.add_outputs(
        scopes,
        [
            nanoAOD.run,
            nanoAOD.luminosityBlock,
            nanoAOD.event,
        ],
    )
    configuration.add_config_parameters(
        ["global", "ee"],
        {
            "min_ele_pt": 10.0,
            "max_ele_eta": 2.4,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "ele_iso_cut": 0.15,
        },
    )

    configuration.add_config_parameters(
        ["ee"],
        {
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 1,
            "pairselection_min_dR": 0.001,
            "truegen_mother_pdgid": 23,
            "truegen_daughter_1_pdgid": 11,
            "truegen_daugher_2_pdgid": 11,
        }
    )

    ########################## Stuff for my Matching Algo ##########################
    # Require that the true-gen pair found by EmbeddingGenPair is really ee.
    TrueGenElectron1Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "TrueGenElectron1", {input}, {vec_open}-11,11{vec_close})',
        input=[q.gen_pdgid_1],
    )

    TrueGenElectron2Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "TrueGenElectron2", {input}, {vec_open}-11,11{vec_close})',
        input=[q.gen_pdgid_2],
    )

    # q.gen_match_1 / q.gen_match_2 are produced by genparticles.GenMatching in
    # analysis_configurations/tau/producers/genparticles.py. That producer calls
    # genparticles::tau::GenMatching(...) from src/genparticles.cxx, which matches
    # the reco p4 to nearby gen particles and returns an integer code describing
    # the gen origin. Here we require code 1, i.e. "prompt electron".
    GenMatchElectron1Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "GenMatchElectron1", {input}, {vec_open}1{vec_close})',
        input=[q.gen_match_1],
    )

    GenMatchElectron2Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "GenMatchElectron2", {input}, {vec_open}1{vec_close})',
        input=[q.gen_match_2],
    )
    # First keep only events where each reco electron can be assigned to an
    # original embedding muon by charge.
    RecoEmbeddingDirectionMatch1Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "RecoEmbeddingDirectionMatch1", {input}, {vec_open}1{vec_close})',
        input=[q.reco_emb_found_match_1],
    )

    RecoEmbeddingDirectionMatch2Filter = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<int>({df}, "RecoEmbeddingDirectionMatch2", {input}, {vec_open}1{vec_close})',
        input=[q.reco_emb_found_match_2],
    )

    RecoEmbeddingDeltaRFilter1 = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<bool>({df}, "RecoEmbeddingDeltaRFilter1", {input}, {vec_open}true{vec_close})',
        input=[q.reco_emb_match_1],
    )

    RecoEmbeddingDeltaRFilter2 = BaseFilter(
        scopes=["ee"],
        call='event::filter::Quantity<bool>({df}, "RecoEmbeddingDeltaRFilter2", {input}, {vec_open}true{vec_close})',
        input=[q.reco_emb_match_2],
    )

    # Build p4 vectors for the original embedding muons. These are only the two
    # seed muons stored in the embedding input and are not yet matched to reco.
    EmbMuonP4_1 = Producer(
        name="EmbMuonP4_1",
        call="lorentzvector::Build({df}, {output}, {input})",
        input=[
            q.emb_muon_pt_1,
            q.emb_muon_eta_1,
            q.emb_muon_phi_1,
            q.emb_muon_mass_1,
        ],
        output=[q.emb_muon_p4_1],
        scopes=["ee"],
    )

    EmbMuonP4_2 = Producer(
        name="EmbMuonP4_2",
        call="lorentzvector::Build({df}, {output}, {input})",
        input=[
            q.emb_muon_pt_2,
            q.emb_muon_eta_2,
            q.emb_muon_phi_2,
            q.emb_muon_mass_2,
        ],
        output=[q.emb_muon_p4_2],
        scopes=["ee"],
    )
    # MatchEmbeddingMuonP4ByCharge is declared in include/event.hxx and
    # implemented in src/event.cxx inside the namespace event::quantity.
    #
    # What it does:
    # - takes the reco charge q.q_1 (or q.q_2)
    # - compares it to the charges of the two original embedding muons
    #   q.emb_muon_q_1 and q.emb_muon_q_2
    # - returns the p4 of the embedding muon whose charge matches the reco one
    #
    # The result is a new column q.matched_emb_muon_p4_1 (or _2), i.e. the
    # embedding-muon Lorentz vector that should be compared to the reco electron.
    # This is the step that turns the two stored embedding muons into the
    # specific "partner" used later in the reco-to-embedding DeltaR matching.
    MatchedEmbMuonP4_1 = Producer(
        name="MatchedEmbMuonP4_1",
        call="event::quantity::MatchEmbeddingMuonP4ByCharge({df}, {output}, {input})",
        input=[
            q.q_1,
            q.emb_muon_q_1,
            q.emb_muon_q_2,
            q.emb_muon_p4_1,
            q.emb_muon_p4_2,
        ],
        output=[q.matched_emb_muon_p4_1],
        scopes=["ee"],
    )

    MatchedEmbMuonP4_2 = Producer(
        name="MatchedEmbMuonP4_2",
        call="event::quantity::MatchEmbeddingMuonP4ByCharge({df}, {output}, {input})",
        input=[
            q.q_2,
            q.emb_muon_q_1,
            q.emb_muon_q_2,
            q.emb_muon_p4_1,
            q.emb_muon_p4_2,
        ],
        output=[q.matched_emb_muon_p4_2],
        scopes=["ee"],
    )
    # Keep the old "found match" logic explicit before applying the DeltaR cut.
    # HasEmbeddingMuonChargeMatch is also defined in event::quantity in
    # src/event.cxx. It returns 1 if the reco charge matches at least one of the
    # two embedding-muon charges and 0 otherwise.
    #
    # This is intentionally kept as a separate step from
    # MatchEmbeddingMuonP4ByCharge:
    # - MatchEmbeddingMuonP4ByCharge gives us the p4 to use for DeltaR
    # - HasEmbeddingMuonChargeMatch keeps the old selection logic explicit:
    #   events without a valid charge match must fail before the DeltaR cut
    RecoEmbFoundMatch_1 = Producer(
        name="RecoEmbFoundMatch_1",
        call="event::quantity::HasEmbeddingMuonChargeMatch({df}, {output}, {input})",
        input=[q.q_1, q.emb_muon_q_1, q.emb_muon_q_2],
        output=[q.reco_emb_found_match_1],
        scopes=["ee"],
    )

    RecoEmbFoundMatch_2 = Producer(
        name="RecoEmbFoundMatch_2",
        call="event::quantity::HasEmbeddingMuonChargeMatch({df}, {output}, {input})",
        input=[q.q_2, q.emb_muon_q_1, q.emb_muon_q_2],
        output=[q.reco_emb_found_match_2],
        scopes=["ee"],
    )
    # Compute the actual angular distance between the reco electron and the
    # charge-matched embedding muon. This calls quantities::DeltaR(...) from
    # src/quantities.cxx on:
    # - q.p4_1 / q.p4_2           : reco electron Lorentz vector from the ee pair
    # - q.matched_emb_muon_p4_1/2 : embedding muon selected by charge above
    RecoEmbDeltaR_1 = Producer(
        name="RecoEmbDeltaR_1",
        call="quantities::DeltaR({df}, {output}, {input})",
        input=[q.p4_1, q.matched_emb_muon_p4_1],
        output=[q.reco_emb_deltaR_1],
        scopes=["ee"],
    )

    RecoEmbDeltaR_2 = Producer(
        name="RecoEmbDeltaR_2",
        call="quantities::DeltaR({df}, {output}, {input})",
        input=[q.p4_2, q.matched_emb_muon_p4_2],
        output=[q.reco_emb_deltaR_2],
        scopes=["ee"],
    )
    # Convert DeltaR < 0.1 into a simple filterable flag. The final reco->embedding
    # direction selection is therefore split into:
    # 1. valid charge match exists
    # 2. DeltaR(reco electron, matched embedding muon) < 0.1
    RecoEmbMatchFlag_1 = Producer(
        name="RecoEmbMatchFlag_1",
        call="event::quantity::MaxFlag<float>({df}, {output}, {input}, 0.1f)",
        input=[q.reco_emb_deltaR_1],
        output=[q.reco_emb_match_1],
        scopes=["ee"],
    )

    RecoEmbMatchFlag_2 = Producer(
        name="RecoEmbMatchFlag_2",
        call="event::quantity::MaxFlag<float>({df}, {output}, {input}, 0.1f)",
        input=[q.reco_emb_deltaR_2],
        output=[q.reco_emb_match_2],
        scopes=["ee"],
    )
#####################################################################################################
    
    
    # Read out the reco-electron ID flag for the two electrons stored in
    # q.dileptonpair.
    #
    # event::quantity::Get<bool>(..., 0) means:
    # - take the first index from q.dileptonpair
    # - use that index on the NanoAOD collection Electron_mvaIso_WP90
    # - store the resulting boolean in q.electron_id_wp90_1
    #
    # Therefore q.electron_id_wp90_1 is not the ID of "any electron in the
    # event", but specifically the WP90 ID flag of the first selected electron
    # from the reco ee pair. RecoElectronID_2 does the same for the second pair
    # electron using index 1 from q.dileptonpair.
    RecoElectronID_1 = Producer(
        name="RecoElectronID_1",
        call="event::quantity::Get<bool>({df}, {output}, {input}, 0)",
        input=[nanoAOD.Electron_mvaIso_WP90, q.dileptonpair],
        output=[q.electron_id_wp90_1],
        scopes=["ee"],
    )

    RecoElectronID_2 = Producer(
        name="RecoElectronID_2",
        call="event::quantity::Get<bool>({df}, {output}, {input}, 1)",
        input=[nanoAOD.Electron_mvaIso_WP90, q.dileptonpair],
        output=[q.electron_id_wp90_2],
        scopes=["ee"],
    )
    RecoElectronIDWP90Filter = BaseFilter( # prüft auf true 
        scopes=["ee"],
        call='event::filter::Flags({df}, "RecoElectronIDWP90", {input}, "all_of")',
        input=[q.electron_id_wp90_1, q.electron_id_wp90_2],
    )

    
    

    
    """
    SingleElectronTriggerFilter = Filter(
        name="SingleElectronTriggerFilter",
        call='event::filter::Flags({df}, "SingleElectronTrigger", {input}, "any_of")',
        input=[],
        scopes=["ee"],
        subproducers=[triggers.ElElGenerateSingleElectronTriggerFlags],
    )"""
    """DoubleElectronTriggerFilter = Filter(
        name="DoubleElectronTriggerFilter",
        call='event::filter::Flags({df}, "DoubleElectronTrigger", {input}, "any_of")',
        input=[],
        scopes=["ee"],
        subproducers=[triggers.ElElGenerateDoubleMuonTriggerFlags],
    )"""


    
       
    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            event.Lumi,
            electrons.RenameElectronPt,
            electrons.BaseElectrons, # hier läuft Electron_mvaIso_WP90 schon
        ],
    )

    configuration.add_producers(
        "ee",
        [
            electrons.GoodElectrons,
            electrons.NumberOfGoodElectrons,
            pairselection.ElElPairSelection,
            pairselection.GoodElElPairFilter,
            RecoElectronID_1,
            RecoElectronID_2,
            RecoElectronIDWP90Filter,
            pairselection.LVEl1,
            pairselection.LVEl2,
            pairquantities.ElElPairQuantities,
            #SingleElectronTriggerFilter,
            #DoubleElectronTriggerFilter,
            # Build and validate the true-gen ee pair.
            genparticles.EmbeddingGenPair,
            genparticles.LVGenParticle1,
            genparticles.LVGenParticle2,
            genparticles.UnrollGenElLV1,
            genparticles.UnrollGenElLV2,
            genparticles.gen_m_vis,
            # This runs the reco->gen matching for q.p4_1 and q.p4_2. The Python
            # wiring is in analysis_configurations/tau/producers/genparticles.py,
            # while the matching logic itself is implemented in
            # src/genparticles.cxx as genparticles::tau::GenMatching(...).
            genparticles.GenMatching,
            # Build the embedding-muon p4s and compare them to the reco electrons.
            embedding.EmbeddingQuantities,
            EmbMuonP4_1,
            EmbMuonP4_2,
            MatchedEmbMuonP4_1,
            MatchedEmbMuonP4_2,
            RecoEmbFoundMatch_1,
            RecoEmbFoundMatch_2,
            RecoEmbDeltaR_1,
            RecoEmbDeltaR_2,
            RecoEmbMatchFlag_1,
            RecoEmbMatchFlag_2,
            TrueGenElectron1Filter,
            TrueGenElectron2Filter,
            GenMatchElectron1Filter,
            GenMatchElectron2Filter,
            RecoEmbeddingDirectionMatch1Filter,
            RecoEmbeddingDirectionMatch2Filter,
            RecoEmbeddingDeltaRFilter1,
            RecoEmbeddingDeltaRFilter2,
        ],
    )
    configuration.add_outputs(
        "ee",
        [
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_diboson,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.mass_1,
            q.mass_2,
            q.electron_mass_nano_1,
            q.electron_mass_nano_2,
            q.q_1,
            q.q_2,
            q.electron_id_wp90_1,# bestehen meine Teilchen aus dem Elektronenpaar die WP90-ID, wenn beides true dann schreibe ich Event raus
            q.electron_id_wp90_2,
            q.dxy_1,
            q.dxy_2,
            q.dz_1,
            q.dz_2,
            q.iso_1,
            q.iso_2,
            q.m_vis,
            q.gen_pt_1,
            q.gen_eta_1,
            q.gen_phi_1,
            q.gen_mass_1,
            q.gen_pdgid_1,
            q.gen_pt_2,
            q.gen_eta_2,
            q.gen_phi_2,
            q.gen_mass_2,
            q.gen_pdgid_2,
            q.gen_m_vis,
            q.gen_match_1,
            q.gen_match_2,
            q.deltaR_ditaupair,
            q.deltaPhi_ditaupair,
            q.deltaEta_ditaupair,
            q.emb_muon_pt_1,
            q.emb_muon_eta_1,
            q.emb_muon_phi_1,
            q.emb_muon_mass_1,
            q.emb_muon_q_1,
            q.emb_muon_db_1,
            q.emb_muon_vtxX_1,
            q.emb_muon_vtxY_1,
            q.emb_muon_vtxZ_1,
            q.emb_muon_pt_2,
            q.emb_muon_eta_2,
            q.emb_muon_phi_2,
            q.emb_muon_mass_2,
            q.emb_muon_q_2,
            q.emb_muon_db_2,
            q.emb_muon_vtxX_2,
            q.emb_muon_vtxY_2,
            q.emb_muon_vtxZ_2,
            q.emb_isMediumLeadingMuon,
            q.emb_isMediumTrailingMuon,
            q.emb_isTightLeadingMuon,
            q.emb_isTightTrailingMuon,
            q.emb_initialMETEt,
            q.emb_initialMETphi,
            q.emb_initialPuppiMETEt,
            q.emb_initialPuppiMETphi,
            q.puweight,

        ],
    )

    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=[event.JSONFilter],
            samples=["data", "embedding"],
        ),
    )
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data", "embedding"],
        ),
    )



    #########################
    # Finalize and validate the configuration
    #########################
    #configuration = add_diTauTriggerSetup(configuration)
    #double trigger läuft noch nicht....
    """configuration.add_config_parameters(
        ["ee"],
        {
            "doubleelectron_trigger": [
                {
                    "flagname": "trg_double_ele24",
                    "hlt_path": "HLT_DoubleEle24_eta2p1_WPTight_Gsf",
                    "p1_ptcut": 24,
                    "p2_ptcut": 24,
                    "p1_etacut": 2.1,
                    "p1_filterbit": 4,
                    "p1_trigger_particle_id": 11,
                    "p2_etacut": 2.1,
                    "p2_filterbit": 4,
                    "p2_trigger_particle_id": 11,
                    "max_deltaR_triggermatch": 0.4,
                },
            ],
        },
    )"""

    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
