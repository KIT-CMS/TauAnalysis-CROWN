#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H


namespace physicsobject {

namespace jet {

namespace quantities {

ROOT::RDF::RNode
CorrectJetIDRun3NanoV12(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_id,
    const std::string &jet_ne_hef,
    const std::string &jet_ne_em_ef,
    const std::string &jet_mu_ef,
    const std::string &jet_ch_em_ef
); 

} // end quantities

namespace vetoes {
    // function xyh::vetoes::jet_vetomap
ROOT::RDF::RNode jet_vetomap(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &output_mask,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_phi,
    const std::string &jet_id,
    const std::string &jet_ch_em_ef,
    const std::string &jet_n_em_ef,
    const std::string &jet_vetomap_file,
    const std::string &jet_vetomap_name,
    const std::string &jet_vetomap_type,
    const float &min_pt,
    const int &id_wp,
    const float &max_em_frac
);

} // end vetoes

} // end jet

} // end physicsobject


#endif