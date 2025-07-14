from ..scripts.CROWNWrapper import NanoAODQuantity

# NanoAODQuantity name is set to the name of the variable automatically.
# If you want to set a different name explicitly, you can do so by passing an specific name as a string.


run = NanoAODQuantity()
luminosityBlock = NanoAODQuantity()
event = NanoAODQuantity()
LHE_Njets = NanoAODQuantity()
prefireWeight = NanoAODQuantity("L1PreFiringWeight_Nom")

Tau_pt = NanoAODQuantity()
Tau_eta = NanoAODQuantity()
Tau_phi = NanoAODQuantity()
Tau_mass = NanoAODQuantity()
Tau_dz = NanoAODQuantity()
Tau_dxy = NanoAODQuantity()
Tau_charge = NanoAODQuantity()
Tau_decayMode = NanoAODQuantity()
Tau_genMatch = NanoAODQuantity("Tau_genPartFlav")
Tau_IDraw = NanoAODQuantity("Tau_rawDeepTau2017v2p1VSjet")
Tau_indexToGen = NanoAODQuantity("Tau_genPartIdx")
Tau_associatedJet = NanoAODQuantity("Tau_jetIdx")
Tau_ID_vsJet = NanoAODQuantity("Tau_idDeepTau2017v2p1VSjet")
Tau_ID_vsEle = NanoAODQuantity("Tau_idDeepTau2017v2p1VSe")
Tau_ID_vsMu = NanoAODQuantity("Tau_idDeepTau2017v2p1VSmu")

Muon_pt = NanoAODQuantity()
Muon_eta = NanoAODQuantity()
Muon_phi = NanoAODQuantity()
Muon_mass = NanoAODQuantity()
Muon_iso = NanoAODQuantity("Muon_pfRelIso04_all")
Muon_dz = NanoAODQuantity()
Muon_dxy = NanoAODQuantity()
Muon_charge = NanoAODQuantity()
Muon_genMatch = NanoAODQuantity("Muon_genPartFlav")
Muon_indexToGen = NanoAODQuantity("Muon_genPartIdx")
Muon_id_medium = NanoAODQuantity("Muon_mediumId")
Muon_id_tight = NanoAODQuantity("Muon_tightId")
Muon_id_loose = NanoAODQuantity("Muon_looseId")
Muon_isGlobal = NanoAODQuantity()
Muon_nStations = NanoAODQuantity()
Muon_nTrackerLayers = NanoAODQuantity()
Muon_ptErr = NanoAODQuantity()

Electron_pt = NanoAODQuantity()
Electron_eta = NanoAODQuantity()
Electron_dxy = NanoAODQuantity()
Electron_dz = NanoAODQuantity()
Electron_phi = NanoAODQuantity()
Electron_mass = NanoAODQuantity()
Electron_iso = NanoAODQuantity("Electron_pfRelIso03_all")
Electron_charge = NanoAODQuantity()
Electron_indexToGen = NanoAODQuantity("Electron_genPartIdx")
Electron_IDWP90 = NanoAODQuantity("Electron_mvaFall17V2noIso_WP90")
Electron_IDWP80 = NanoAODQuantity("Electron_mvaFall17V2noIso_WP80")
Electron_cutBased = NanoAODQuantity()
Electron_seedGain = NanoAODQuantity()
Electron_dEsigmaUp = NanoAODQuantity()
Electron_dEsigmaDown = NanoAODQuantity()

Photon_pt = NanoAODQuantity()
Photon_eta = NanoAODQuantity()
Photon_phi = NanoAODQuantity()
Photon_mass = NanoAODQuantity()
Photon_electronVeto = NanoAODQuantity()

GenJet_pt = NanoAODQuantity()
GenJet_eta = NanoAODQuantity()
GenJet_phi = NanoAODQuantity()

Jet_eta = NanoAODQuantity()
Jet_phi = NanoAODQuantity()
Jet_pt = NanoAODQuantity()
Jet_mass = NanoAODQuantity()
Jet_area = NanoAODQuantity()
Jet_flavor = NanoAODQuantity("Jet_hadronFlavour")
Jet_rawFactor = NanoAODQuantity()
Jet_ID = NanoAODQuantity("Jet_jetId")
Jet_PUID = NanoAODQuantity("Jet_puId")
Jet_associatedGenJet = NanoAODQuantity("Jet_genJetIdx")
BJet_discriminator = NanoAODQuantity("Jet_btagDeepFlavB")

Pileup_nTrueInt = NanoAODQuantity()
rho = NanoAODQuantity("fixedGridRhoFastjetAll")

GenParticle_eta = NanoAODQuantity("GenPart_eta")
GenParticle_phi = NanoAODQuantity("GenPart_phi")
GenParticle_pt = NanoAODQuantity("GenPart_pt")
GenParticle_mass = NanoAODQuantity("GenPart_mass")
GenParticle_pdgId = NanoAODQuantity("GenPart_pdgId")
GenParticle_status = NanoAODQuantity("GenPart_status")
GenParticle_statusFlags = NanoAODQuantity("GenPart_statusFlags")
GenParticle_motherid = NanoAODQuantity("GenPart_genPartIdxMother")

## Trigger Objects
TriggerObject_bit = NanoAODQuantity("TrigObj_filterBits")
TriggerObject_pt = NanoAODQuantity("TrigObj_pt")
TriggerObject_eta = NanoAODQuantity("TrigObj_eta")
TriggerObject_phi = NanoAODQuantity("TrigObj_phi")
TriggerObject_id = NanoAODQuantity("TrigObj_id")

## HTXS quantities
HTXS_Higgs_pt = NanoAODQuantity()                           # Float_t   pt of the Higgs boson as identified in HTXS
HTXS_Higgs_y = NanoAODQuantity()                            # Float_t   rapidity of the Higgs boson as identified in HTXS
HTXS_njets25 = NanoAODQuantity()                            # UChar_t   number of jets with pt>25 GeV as identified in HTXS
HTXS_njets30 = NanoAODQuantity()                            # UChar_t   number of jets with pt>30 GeV as identified in HTXS
HTXS_stage1_1_cat_pTjet25GeV = NanoAODQuantity()            # Int_t     HTXS stage-1.1 category(jet pt>25 GeV)
HTXS_stage1_1_cat_pTjet30GeV = NanoAODQuantity()            # Int_t     HTXS stage-1.1 category(jet pt>30 GeV)
HTXS_stage1_1_fine_cat_pTjet25GeV = NanoAODQuantity()       # Int_t     HTXS stage-1.1-fine category(jet pt>25 GeV)
HTXS_stage1_1_fine_cat_pTjet30GeV = NanoAODQuantity()       # Int_t     HTXS stage-1.1-fine category(jet pt>30 GeV)
HTXS_stage1_2_cat_pTjet25GeV = NanoAODQuantity()            # Int_t     HTXS stage-1.2 category(jet pt>25 GeV)
HTXS_stage1_2_cat_pTjet30GeV = NanoAODQuantity()            # Int_t     HTXS stage-1.2 category(jet pt>30 GeV)
HTXS_stage1_2_fine_cat_pTjet25GeV = NanoAODQuantity()       # Int_t     HTXS stage-1.2-fine category(jet pt>25 GeV)
HTXS_stage1_2_fine_cat_pTjet30GeV = NanoAODQuantity()       # Int_t     HTXS stage-1.2-fine category(jet pt>30 GeV)
HTXS_stage_0 = NanoAODQuantity()                            # Int_t     HTXS stage-0 category
HTXS_stage_1_pTjet25 = NanoAODQuantity()                    # Int_t     HTXS stage-1 category (jet pt>25 GeV)
HTXS_stage_1_pTjet30 = NanoAODQuantity()                    # Int_t     HTXS stage-1 category (jet pt>30 GeV)

# Theory weights
LHEScaleWeight = NanoAODQuantity()
LHEPdfWeight = NanoAODQuantity()
PSWeight = NanoAODQuantity()

## MET quantities
## TODO Swich to Puppi versions for METCOV and Signifiance as soon as they are in the nanoAOD
MET_covXX = NanoAODQuantity()
MET_covXY = NanoAODQuantity()
MET_covYY = NanoAODQuantity()
MET_significance = NanoAODQuantity()

MET_phi = NanoAODQuantity("PuppiMET_phi")
MET_pt = NanoAODQuantity("PuppiMET_pt")
MET_sumEt = NanoAODQuantity("PuppiMET_sumEt")

PFMET_phi = NanoAODQuantity("MET_phi")
PFMET_pt = NanoAODQuantity("MET_pt")
PFMET_sumEt = NanoAODQuantity("MET_sumEt")

## Embedding Quantities
genWeight = NanoAODQuantity()
TauEmbedding_initialMETEt = NanoAODQuantity()
TauEmbedding_initialMETphi = NanoAODQuantity()
TauEmbedding_initialPuppiMETEt = NanoAODQuantity()
TauEmbedding_initialPuppiMETphi = NanoAODQuantity()
TauEmbedding_isMediumLeadingMuon = NanoAODQuantity()
TauEmbedding_isMediumTrailingMuon = NanoAODQuantity()
TauEmbedding_isTightLeadingMuon = NanoAODQuantity()
TauEmbedding_isTightTrailingMuon = NanoAODQuantity()
TauEmbedding_InitialPairCandidates = NanoAODQuantity("TauEmbedding_nInitialPairCandidates")
TauEmbedding_SelectionOldMass = NanoAODQuantity()
TauEmbedding_SelectionNewMass = NanoAODQuantity()

HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ = NanoAODQuantity()
