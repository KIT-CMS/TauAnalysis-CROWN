#ifndef GUARDFAKEFACTORS_H
#define GUARDFAKEFACTORS_H

#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include "../../../../include/utility/CorrectionManager.hxx"

#include <string>
#include <vector>

namespace fakefactors_run3 {

ROOT::RDF::RNode build_model_input_column(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::vector<std::string> &input_columns
);

std::string joinAndReplace(const std::vector<std::string> &strings,
                           const std::string &delimiter);

/**
 * @brief This function creates the fake factor weight of the fully hadronic
 * anti-isolated region, where exactly one of the two taus fails the
 * isolation: `0.5 * (ff_1 * [id_1 == 0] + ff_2 * [id_2 == 0])`, i.e. half of
 * the fake factor of the failing tau.
 *
 * @param df input dataframe
 * @param outputname name of the new column
 * @param ff_1 name of the fake factor column of the leading tau (`float`)
 * @param ff_2 name of the fake factor column of the subleading tau (`float`)
 * @param id_1 name of the isolation flag column of the leading tau (`int`)
 * @param id_2 name of the isolation flag column of the subleading tau (`int`)
 *
 * @return a dataframe with the new column of type `double`
 */
inline ROOT::RDF::RNode
AntiIsoFakeFactor(ROOT::RDF::RNode df, const std::string &outputname,
                  const std::string &ff_1, const std::string &ff_2,
                  const std::string &id_1, const std::string &id_2) {
    return df.Define(
        outputname,
        [](float fake_factor_1, float fake_factor_2, int id1, int id2) {
            return 0.5 *
                   (fake_factor_1 * (id1 == 0) + fake_factor_2 * (id2 == 0));
        },
        {ff_1, ff_2, id_1, id_2});
}

namespace sm{

    struct NonClosureHandler {
        std::string prefix;
        const correction::CompoundCorrection *compound;
        std::vector<std::string> variables;

        NonClosureHandler(const std::string &proc, const std::string &file,
                          const correction::CompoundCorrection *c);

        float evaluate(const std::string &systematic,
                       std::vector<correction::Variable::Type> args);
    };

    ROOT::RDF::RNode
    raw_fakefactor_lt(
        ROOT::RDF::RNode df,
        correctionManager::CorrectionManager &correctionManager,
        const std::string &outputname,
        const std::string &pt_2,
        const std::string &njets,
        const std::string &mt_1,
        const std::string &fraction_variation,
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        const std::string &ff_file);
    ROOT::RDF::RNode
        fakefactor_lt(
            ROOT::RDF::RNode df,
            correctionManager::CorrectionManager &correctionManager,
            const std::vector<std::string> &outputnames,
            const std::string &pt_2,
            const std::string &ff_input,
            const std::string &fractions_input,
            const std::string &DR_SR_input,
            const std::string &non_closure_input,
            const std::string &fraction_variation,
            const std::string &QCD_variation,
            const std::string &Wjets_variation,
            const std::string &ttbar_variation,
            const std::string &QCD_DR_SR_correction_variation,
            const std::string &QCD_non_closure_correction_variation,
            const std::string &Wjets_DR_SR_correction_variation,
            const std::string &Wjets_non_closure_correction_variation,
            const std::string &ttbar_non_closure_correction_variation,
            const std::string &ff_file,
            const std::string &ff_corr_file,
            const bool split_info);
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
            const std::vector<std::string> &outputnames,
            const int &tau_idx, 
            const std::string &pt_1_input,
            const std::string &pt_2_input,
            const std::string &qcd_ff_input,
            const std::string &qcd_sub_ff_input,
            const std::string &fractions_input,
            const std::string &DR_SR_input,
            const std::string &non_closure_QCD_input,
            const std::string &non_closure_QCD_sub_input,
            const std::string &fraction_variation,
            const std::string &QCD_variation,
            const std::string &QCD_DR_SR_correction_variation,
            const std::string &QCD_non_closure_correction_variation,
            const std::string &ff_file,
            const std::string &ff_corr_file,
            const bool split_info);
}  // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
