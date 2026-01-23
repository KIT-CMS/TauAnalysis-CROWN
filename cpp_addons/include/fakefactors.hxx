#ifndef GUARDFAKEFACTORS_H
#define GUARDFAKEFACTORS_H

namespace fakefactors {
namespace sm{
    ROOT::RDF::RNode
    raw_fakefactor_lt(
        ROOT::RDF::RNode df,
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        // for ff
        const std::string &pt_2,
        const std::string &njets,
        const std::string &pt_1,
        // for fraction
        const std::string &mt_1,
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
        const std::vector<std::string> &outputnames,
        //
        const std::string &pt_2,
        const std::string &njets,
        const std::string &pt_1,
        const std::string &mt_1,
        const std::string &tau_decaymode_2,
        const std::string &iso_1,
        const std::string &mass_2,
        const std::string &eta_1,
        const std::string &eta_2,
        const std::string &jpt_1,
        const std::string &jeta_1,
        const std::string &jpt_2,
        const std::string &jeta_2,
        const std::string &met,
        const std::string &deltaEta_ditaupair,
        const std::string &pt_tt,
        const std::string &pt_ttjj,
        const std::string &deltaR_ditaupair,
        const std::string &mt_tot,
        const std::string &deltaR_jj,
        const std::string &deltaR_1j1,
        const std::string &deltaR_12j1,
        const std::string &m_vis,
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
        const std::string &ff_corr_file,
        const bool split_info
    );

    ROOT::RDF::RNode
    raw_fakefactor_tt(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        const int &tau_idx, 
        const std::string &pt_1,
        const std::string &pt_2, 
        const std::string &njets, 
        const std::string &m_vis, 
        const std::string &qcd_variation,
        const std::string &fraction_variation, 
        const std::string &ff_file);

    ROOT::RDF::RNode
    fakefactor_tt(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        const int &tau_idx, 
        const std::string &tau_pt_1,
        const std::string &tau_pt_2,
        const std::string &njets,
        const std::string &m_vis,
        const std::string &decaymode_1,
        const std::string &decaymode_2,
        const std::string &mass_1,
        const std::string &mass_2,
        const std::string &met,
        const std::string &pt_tt,
        const std::string &qcd_variation, 
        const std::string &fraction_variation, const std::string &qcd_non_closure_correction_variation,
        const std::string &qcd_DR_SR_correction_variation,
        const std::string &ff_file, const std::string &ff_corr_file);

    ROOT::RDF::RNode
    fakefactor_tt_split_info(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::vector<std::string> &outputname,
        const int &tau_idx, 
        const std::string &tau_pt_1,
        const std::string &tau_pt_2,
        const std::string &njets,
        const std::string &m_vis,
        const std::string &decaymode_1,
        const std::string &decaymode_2,
        const std::string &mass_1,
        const std::string &mass_2,
        const std::string &met,
        const std::string &pt_tt,
        const std::string &qcd_variation, 
        const std::string &fraction_variation, 
        const std::string &qcd_non_closure_correction_variation,
        const std::string &qcd_DR_SR_correction_variation,
        const std::string &ff_file, 
        const std::string &ff_corr_file);
}  // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
