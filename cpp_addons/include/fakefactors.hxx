#ifndef GUARDFAKEFACTORS_H
#define GUARDFAKEFACTORS_H

namespace fakefactors {
namespace sm{
    ROOT::RDF::RNode
    raw_fakefactor_lt(
        ROOT::RDF::RNode df,
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        const std::string &tau_pt,
        const std::string &njets,
        const std::string &delta_r,
        const std::string &lep_mt,
        //
        const std::string &fraction_variation,
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        //
        const std::string &ff_file
    );
    ROOT::RDF::RNode
    fakefactor_lt(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        // for ff
        const std::string &tau_pt,
        const std::string &njets,
        const std::string &delta_r,
        // for fraction 
        const std::string &lep_mt,
        // for DR SR corrections
        const std::string &m_vis,
        // for non closure corrections
        const std::string &lep_pt,
        const std::string &tau_decaymode,
        const std::string &lep_iso,
        const std::string &tau_mass,
        // for corrections
        const std::string &fraction_variation,
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        //
        const std::string &QCD_DR_SR_correction_variation,
        const std::string &QCD_non_closure_correction_variation,
        //
        const std::string &Wjets_DR_SR_correction_variation,
        const std::string &Wjets_non_closure_correction_variation,
        //
        const std::string &ttbar_non_closure_correction_variation,
        //
        const std::string &ff_file,
        const std::string &ff_corr_file
    );
    ROOT::RDF::RNode
    fakefactor_lt_split_info(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::vector<std::string> &outputname,
        // for ff
        const std::string &tau_pt,
        const std::string &njets,
        const std::string &delta_r,
        // for fraction 
        const std::string &lep_mt,
        // for DR SR corrections
        const std::string &m_vis,
        // for non closure corrections
        const std::string &lep_pt,
        const std::string &tau_decaymode,
        const std::string &lep_iso,
        const std::string &tau_mass,
        // for corrections
        const std::string &fraction_variation,
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        //
        const std::string &QCD_DR_SR_correction_variation,
        const std::string &QCD_non_closure_correction_variation,
        //
        const std::string &Wjets_DR_SR_correction_variation,
        const std::string &Wjets_non_closure_correction_variation,
        //
        const std::string &ttbar_non_closure_correction_variation,
        //
        const std::string &ff_file,
        const std::string &ff_corr_file
    );
}  // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
