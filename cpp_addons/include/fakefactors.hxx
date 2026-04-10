#ifndef GUARD_FAKEFACTORS_H
#define GUARD_FAKEFACTORS_H

#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include "../../../../include/utility/CorrectionManager.hxx"

#include <string>
#include <vector>

#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include "../../../../include/utility/CorrectionManager.hxx"

#include <string>
#include <vector>

namespace fakefactors {

// Builds a std::vector<float> column from scalar columns.
ROOT::RDF::RNode build_model_input_column(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::vector<std::string> &input_columns
);

std::string joinAndReplace(const std::vector<std::string> &strings,
                           const std::string &delimiter);

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
        // dedicated event validity input
        const std::string &pt_2_input,
        // pre-built correctionlib input vectors
        const std::string &qcd_ff_input,
        const std::string &wjets_ff_input,
        const std::string &ttbar_ff_input,
        const std::string &fractions_input,
        // ---
        const std::string &fraction_variation,
        // ---
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        // ---
        const std::string &ff_file
    );

    // Evaluates full SM fake factors (raw, fractions, DR/SR, non-closure).
    // Vector input contract:
    // - qcd_ff_input: [pt_2, njets]
    // - wjets_ff_input: [pt_2, njets, pt_1]
    // - ttbar_ff_input: [pt_2, njets]
    // - fractions_input: [mt_1, njets]
    // - qcd_DR_SR_input: [mt_1, njets]
    // - wjets_DR_SR_input: [mt_1, njets]
    // - *_non_closure_input: process-specific non-closure inputs
    ROOT::RDF::RNode
    fakefactor_lt(
        ROOT::RDF::RNode df, 
        correctionManager::CorrectionManager &correctionManager,
        const std::vector<std::string> &outputnames,
        // dedicated event validity input
        const std::string &pt_2_input,
        // pre-built correctionlib input vectors
        const std::string &qcd_ff_input,
        const std::string &wjets_ff_input,
        const std::string &ttbar_ff_input,
        const std::string &fractions_input,
        const std::string &qcd_DR_SR_input,
        const std::string &wjets_DR_SR_input,
        const std::string &qcd_non_closure_input,
        const std::string &wjets_non_closure_input,
        const std::string &ttbar_non_closure_input,
        // for corrections
        const std::string &fraction_variation,
        const std::string &QCD_variation,
        const std::string &Wjets_variation,
        const std::string &ttbar_variation,
        // ---
        const std::string &QCD_DR_SR_correction_variation,
        const std::string &QCD_non_closure_correction_variation,
        // ---
        const std::string &Wjets_DR_SR_correction_variation,
        const std::string &Wjets_non_closure_correction_variation,
        //
        const std::string &ttbar_non_closure_correction_variation,
        // ---
        const std::string &ff_file,
        const std::string &ff_corr_file,
        const bool split_info
    );
}  // namespace sm
} // namespace fakefactors
#endif /* GUARD_FAKEFACTORS_H */