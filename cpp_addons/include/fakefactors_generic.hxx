#ifndef GUARDFAKEFACTORS_GENERIC_H
#define GUARDFAKEFACTORS_GENERIC_H

#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include "../../../../include/utility/CorrectionManager.hxx"
#include "fakefactors.hxx"

#include <string>
#include <vector>

namespace fakefactors {
namespace generic {

// One fake-factor process of a hadronic tau leg; empty dr_sr / non_closure fields mean "absent".
// non_closure_prefix is the part of the non-closure variation names before the variable, e.g. "CMS_fake_t_QCD_non_closure_"
struct Process {
    std::string name;
    std::string ff, ff_variation;
    std::string dr_sr, dr_sr_variation;
    std::string non_closure, non_closure_prefix, non_closure_variation;
    std::vector<std::string> non_closure_variables;
};

struct Leg {
    std::string fractions, fraction_variation;
    std::vector<Process> processes;
};

// Maps the packed input column onto the inputs declared by a correction
struct ArgBuilder {
    enum class Kind { Value, Process, Syst };
    struct Slot {
        Kind kind;
        size_t index;
        correction::Variable::VarType type;
    };
    std::vector<Slot> slots;
    size_t syst_pos = 0;
    std::string process;

    ArgBuilder(const std::string &correction_name,
               const std::vector<correction::Variable> &inputs,
               const std::vector<std::string> &layout,
               const std::string &process);

    std::vector<correction::Variable::Type>
    build(const std::vector<float> &values, const std::string &syst) const;
};

struct NonClosureHandler {
    std::string prefix;
    const correction::CompoundCorrection *compound;
    size_t syst_pos;
    std::vector<std::string> variables;

    NonClosureHandler(const std::string &prefix, const std::vector<std::string> &variables,
                      const correction::CompoundCorrection *c, size_t syst_pos);

    float evaluate(const std::string &systematic,
                   std::vector<correction::Variable::Type> args) const;
};

// Packs the columns into one std::vector<float>, casting each (int, short, double, ...) to float
ROOT::RDF::RNode build_inputs(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::vector<std::string> &input_columns);

ROOT::RDF::RNode raw_fakefactor(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname,
    const std::string &inputs_column,
    const std::vector<std::string> &layout,
    const std::string &guard,
    const Leg &leg,
    const std::string &ff_file);

ROOT::RDF::RNode fakefactor(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::vector<std::string> &outputnames,
    const std::string &inputs_column,
    const std::vector<std::string> &layout,
    const std::string &guard,
    const Leg &leg,
    const std::string &ff_file,
    const std::string &ff_corr_file,
    const bool split_info);

} // namespace generic
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_GENERIC_H */
