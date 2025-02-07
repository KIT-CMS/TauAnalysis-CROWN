# TauAnalysis-CROWN
The repository holding the CROWN configurations for tau related analyses

## Available Configurations

* `config.py` - The main configuration to be used for the Standard Model H->𝜏𝜏 Measurement. Works for all main final states (mt, et, tt, em, mm, ee)
* `tauembedding_tagandprobe.py` - Configuration used for the measurement of TagAndProbe Scale Factors for Electrons and Muons (available scopes are ee and mm)
* `embedding_selection.py` - Configuration used for control plots of the Muon selection of Tau-Embedding

* `sm_bbtautau_config.py` - Config for HH -> bb𝜏𝜏 nonresonant measurement. First implementation plans to do 2018UL with nanoAODv12 and DeepTau2.5 .

## Available Friend Configurations

* `fastmtt.py` - Produce FastMTT friends
* `nmssm_fake_factors.py` - Produce FakeFactor Friends for the NMSSM Analysis
