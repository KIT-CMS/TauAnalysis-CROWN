# from code_generation.quantity import Quantity
from ..scripts.CROWNWrapper import Quantity

# Quantity name is set to the name of the variable automatically.
# If you want to set a different name explicitly, you can do so by passing an specific name as a string.

# DY flavor bug selection
gen_dyflavor = Quantity()
gen_dyfilter = Quantity()

#### Jet

Jet_ID = Quantity()
Jet_pt_corrected = Quantity()
Jet_mass_corrected = Quantity()
jet_id_mask = Quantity()
jet_puid_mask = Quantity()
good_jet_collection = Quantity()
good_bjet_collection = Quantity()
good_jets_mask_loose = Quantity()
good_jets_mask_tight = Quantity()
loose_jets_mask_loweta = Quantity()
loose_jets_mask_higheta = Quantity()
good_jets_mask = Quantity()
good_bjets_mask = Quantity()
Jet_pt_cut_loose = Quantity()
Jet_vetomap = Quantity()
jet_overlap_veto_mask = Quantity()
njets = Quantity()
nbtag = Quantity()
jet_p4_1 = Quantity()
jpt_1 = Quantity()
jeta_1 = Quantity()
jphi_1 = Quantity()
jtag_value_1 = Quantity()
jet_p4_2 = Quantity()
jpt_2 = Quantity()
jeta_2 = Quantity()
jphi_2 = Quantity()
jtag_value_2 = Quantity()
mjj = Quantity()
bjet_p4_1 = Quantity()
bpt_1 = Quantity()
beta_1 = Quantity()
bphi_1 = Quantity()
btag_value_1 = Quantity()
bjet_p4_2 = Quantity()
bpt_2 = Quantity()
beta_2 = Quantity()
bphi_2 = Quantity()
btag_value_2 = Quantity()

# working points

id_wgt_mu_1 = Quantity()
id_wgt_mu_2 = Quantity()
iso_wgt_mu_1 = Quantity()
iso_wgt_mu_2 = Quantity()
id_wgt_ele_wp90iso_1 = Quantity()
id_wgt_ele_wp90iso_2 = Quantity()
id_wgt_ele_wp80iso_1 = Quantity()
id_wgt_ele_wp80iso_2 = Quantity()
id_wgt_ele_1 = Quantity()
id_wgt_ele_2 = Quantity()
iso_wgt_ele_1 = Quantity()
iso_wgt_ele_2 = Quantity()

btag_weight = Quantity()

#### event

# HTXS quantities 
ggh_NNLO_weight = Quantity()
THU_ggH_Mu = Quantity()
THU_ggH_Res = Quantity()
THU_ggH_Mig01 = Quantity()
THU_ggH_Mig12 = Quantity()
THU_ggH_VBF2j = Quantity()
THU_ggH_VBF3j = Quantity()
THU_ggH_PT60 = Quantity()
THU_ggH_PT120 = Quantity()
THU_ggH_qmtop = Quantity()
THU_qqH_TOT = Quantity()
THU_qqH_PTH200 = Quantity()
THU_qqH_Mjj60 = Quantity()
THU_qqH_Mjj120 = Quantity()
THU_qqH_Mjj350 = Quantity()
THU_qqH_Mjj700 = Quantity()
THU_qqH_Mjj1000 = Quantity()
THU_qqH_Mjj1500 = Quantity()
THU_qqH_25 = Quantity()
THU_qqH_JET01 = Quantity()

# SampleFlags
is_data = Quantity()
is_data_all = Quantity()
is_data_E = Quantity()
is_data_F = Quantity()
is_data_G = Quantity()
is_ttbar = Quantity()
is_dyjets = Quantity()
is_dyjets_powheg = Quantity()
is_dyjets_amcatnlo = Quantity()
is_wjets = Quantity()
is_wjets_amcatnlo = Quantity()
is_wjets_temp = Quantity()
is_ggh_htautau = Quantity()
is_vbf_htautau = Quantity()
is_diboson = Quantity()
is_vbf_hbb = Quantity()
is_ggh_hbb = Quantity()
is_rem_hbb = Quantity()
is_singletop = Quantity()
is_rem_htautau = Quantity()
is_electroweak_boson = Quantity()
is_embedding = Quantity()
is_embedding_mc = Quantity()

lumi = Quantity()
npartons = Quantity()
puweight = Quantity()
lhe_scale_weight = Quantity()
lhe_pdf_weight = Quantity()
lhe_alphaS_weight = Quantity()
ps_weight = Quantity()

#### MET 

# MetBasics
met_mask = Quantity()
met_p4 = Quantity()
recoil_genboson_p4_vec = Quantity()
genboson_p4 = Quantity()
visgenboson_p4 = Quantity()
genbosonmass = Quantity()
met_p4_leptoncorrected = Quantity()
met_p4_jetcorrected = Quantity()
met_p4_recoilcorrected = Quantity()
met = Quantity()
metphi = Quantity()
metSumEt = Quantity()
metcov00 = Quantity()
metcov01 = Quantity()
metcov10 = Quantity()
metcov11 = Quantity()
met_uncorrected = Quantity()
metphi_uncorrected = Quantity()
pfmet = Quantity()
pfmet_p4 = Quantity()
pfmetphi = Quantity()
pfmet_uncorrected = Quantity()
pfmetphi_uncorrected = Quantity()
pfmet_p4_leptoncorrected = Quantity()
pfmet_p4_jetcorrected = Quantity()
pfmet_p4_recoilcorrected = Quantity()

#### Electrons

# RenameElectronPt
Electron_pt_corrected = Quantity()

# BaseElectrons
_ElectronEtaCut = Quantity()
_ElectronDxyCut = Quantity()
_ElectronDzCut = Quantity()
_ElectronPtCutMin = Quantity()
_ElectronPtCutMax = Quantity()
_ElectronIDCut = Quantity()
_ElectronIsoCut = Quantity()
base_electrons_mask = Quantity()

# ExtraElectronsVeto
extraelec_veto = Quantity()

# DiLeptonVeto->DiElectronVeto
dilepton_veto = Quantity()
dielectron_veto = Quantity()

# GoodElectrons
good_electrons_mask = Quantity()

# NumberOfGoodElectrons
nelectrons = Quantity()

# VetoElectrons
veto_electrons_mask = Quantity()
veto_electrons_mask_2 = Quantity()

#### Muons

# BaseMuons
base_muons_mask = Quantity()
good_muons_mask = Quantity()
_MuonEtaCut = Quantity()
_MuonDxyCut = Quantity()
_MuonDzCut = Quantity()
_MuonPtCut = Quantity()
_MuonIDCut = Quantity()
_MuonIsoCut = Quantity()

# NumberGoodMuons
nmuons = Quantity()

# VetoMuons
veto_muons_mask = Quantity()

# ExtraMuonsVeto
veto_muons_mask_2 = Quantity()
extramuon_veto = Quantity()

# DiMuonVeto
dimuon_veto = Quantity()

#### Taus

# GoodTaus
good_taus_mask = Quantity()

# NumberOfGoodTaus
ntaus = Quantity()

# TauPtCorrection_muFake
Tau_pt_corrected = Quantity()
Tau_mass_corrected = Quantity()
Tau_pt_ele_corrected = Quantity()
Tau_pt_ele_mu_corrected = Quantity()

#### pairselection

# MTPairSelection
dileptonpair = Quantity()

# LV...
p4_1 = Quantity()
p4_1_uncorrected = Quantity()
p4_2 = Quantity()
p4_2_uncorrected = Quantity()

#### pairquantities

# MTDiTauPairQuantities
pt_1 = Quantity()
eta_1 = Quantity()
phi_1 = Quantity()
pt_2 = Quantity()
eta_2 = Quantity()
phi_2 = Quantity()
mass_1 = Quantity()
mass_2 = Quantity()
m_vis = Quantity()
pt_vis = Quantity()
deltaR_ditaupair = Quantity()
dxy_1 = Quantity()
dxy_2 = Quantity()
dz_1 = Quantity()
dz_2 = Quantity()
q_1 = Quantity()
q_2 = Quantity()
iso_1 = Quantity()
iso_2 = Quantity()
is_global_1 = Quantity()
is_global_2 = Quantity()
tau_decaymode_1 = Quantity()
tau_decaymode_2 = Quantity()

# DiTauPairMETQuantities
pzetamissvis = Quantity()
mTdileptonMET = Quantity()
mt_1 = Quantity()
mt_2 = Quantity()
pt_tt = Quantity()
pt_ttjj = Quantity()
mt_tot = Quantity()
pzetamissvis_pf = Quantity()
mTdileptonMET_pf = Quantity()
mt_1_pf = Quantity()
mt_2_pf = Quantity()
pt_tt_pf = Quantity()
pt_ttjj_pf = Quantity()
mt_tot_pf = Quantity()
pt_dijet = Quantity()
jet_hemisphere = Quantity()
zPtReweightWeight = Quantity()
topPtReweightWeight = Quantity()

p4_fastmtt = Quantity()
m_fastmtt = Quantity()
pt_fastmtt = Quantity()
eta_fastmtt = Quantity()
phi_fastmtt = Quantity()
p4_dilepton = Quantity()
muon_pterr_1 = Quantity()
muon_pterr_2 = Quantity()
muon_nstations_1 = Quantity()
muon_nstations_2 = Quantity()
muon_ntrackerlayers_1 = Quantity()
muon_ntrackerlayers_2 = Quantity()

#### scalefactors

gen_match_1 = Quantity()
gen_match_2 = Quantity()
gen_tau_pt_1 = Quantity()
gen_tau_pt_2 = Quantity()
gen_tau_eta_1 = Quantity()
gen_tau_eta_2 = Quantity()
gen_tau_phi_1 = Quantity()
gen_tau_phi_2 = Quantity()
taujet_pt_1 = Quantity()
taujet_pt_2 = Quantity()
gen_taujet_pt_1 = Quantity()
gen_taujet_pt_2 = Quantity()
gen_dileptonpair = Quantity()
truegenpair = Quantity()

#### genparticles

# GenMatching
gen_p4_1 = Quantity()
gen_pt_1 = Quantity()
gen_eta_1 = Quantity()
gen_phi_1 = Quantity()
gen_mass_1 = Quantity()
gen_pdgid_1 = Quantity()
gen_p4_2 = Quantity()
gen_pt_2 = Quantity()
gen_eta_2 = Quantity()
gen_phi_2 = Quantity()
gen_mass_2 = Quantity()
gen_pdgid_2 = Quantity()
gen_m_vis = Quantity()

# MTGenDiTauPairQuantities
hadronic_gen_taus = Quantity()

# fake factors
raw_fake_factor = Quantity()
raw_fake_factor_1 = Quantity()
raw_fake_factor_2 = Quantity()

fake_factor = Quantity()
fake_factor_1 = Quantity()
fake_factor_2 = Quantity()

raw_qcd_fake_factor_1 = Quantity()
raw_qcd_fake_factor_2 = Quantity()
raw_wjets_fake_factor_1 = Quantity()
raw_wjets_fake_factor_2 = Quantity()
raw_ttbar_fake_factor_1 = Quantity()
raw_ttbar_fake_factor_2 = Quantity()

qcd_fake_factor_1 = Quantity()
qcd_fake_factor_2 = Quantity()
wjets_fake_factor_1 = Quantity()
wjets_fake_factor_2 = Quantity()
ttbar_fake_factor_1 = Quantity()
ttbar_fake_factor_2 = Quantity()

qcd_fake_factor_fraction_1 = Quantity()
qcd_fake_factor_fraction_2 = Quantity()
wjets_fake_factor_fraction_1 = Quantity()
wjets_fake_factor_fraction_2 = Quantity()
ttbar_fake_factor_fraction_1 = Quantity()
ttbar_fake_factor_fraction_2 = Quantity()

qcd_fake_factor_correction_1 = Quantity()
qcd_fake_factor_correction_2 = Quantity()
wjets_fake_factor_correction_1 = Quantity()
wjets_fake_factor_correction_2 = Quantity()
ttbar_fake_factor_correction_1 = Quantity()
ttbar_fake_factor_correction_2 = Quantity()

qcd_DR_SR_correction_1 = Quantity()
qcd_DR_SR_correction_2 = Quantity()
wjets_DR_SR_correction_1 = Quantity()
wjets_DR_SR_correction_2 = Quantity()
ttbar_DR_SR_correction_1 = Quantity()
ttbar_DR_SR_correction_2 = Quantity()

qcd_correction_wo_DR_SR_1 = Quantity()
qcd_correction_wo_DR_SR_2 = Quantity()
wjets_correction_wo_DR_SR_1 = Quantity()
wjets_correction_wo_DR_SR_2 = Quantity()
ttbar_correction_wo_DR_SR_1 = Quantity()
ttbar_correction_wo_DR_SR_2 = Quantity()

## embedding quantities
emb_genweight = Quantity()
emb_initialMETEt = Quantity()
emb_initialMETphi = Quantity()
emb_initialPuppiMETEt = Quantity()
emb_initialPuppiMETphi = Quantity()
emb_isMediumLeadingMuon = Quantity()
emb_isMediumTrailingMuon = Quantity()
emb_isTightLeadingMuon = Quantity()
emb_isTightTrailingMuon = Quantity()
emb_InitialPairCandidates = Quantity()
emb_SelectionOldMass = Quantity()
emb_SelectionNewMass = Quantity()
emb_triggersel_wgt = Quantity()
emb_idsel_wgt_1 = Quantity()
emb_idsel_wgt_2 = Quantity()
emb_trg_wgt_1 = Quantity()
emb_trg_wgt_2 = Quantity()