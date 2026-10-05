#ifndef GUARDFAKEFACTORS_GENERIC_CXX
#define GUARDFAKEFACTORS_GENERIC_CXX

#include "../include/fakefactors_generic.hxx"
#include "../../../../include/event.hxx"
#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "correction.h"

#include <algorithm>
#include <cmath>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace fakefactors {
namespace generic {

ArgBuilder::ArgBuilder(const std::string &correction_name,
                       const std::vector<correction::Variable> &inputs,
                       const std::vector<std::string> &layout,
                       const std::string &proc)
    : process(proc) {
    bool has_syst = false;
    for (const auto &var : inputs) {
        const std::string name = var.name();
        if (name == "process") {
            slots.push_back({Kind::Process, 0, var.type()});
        } else if (name == "syst") {
            syst_pos = slots.size();
            has_syst = true;
            slots.push_back({Kind::Syst, 0, var.type()});
        } else {
            auto it = std::find(layout.begin(), layout.end(), name);
            if (it == layout.end()) {
                throw std::runtime_error("fakefactors::generic: input '" + name + "' of correction '" +
                                         correction_name + "' is not in the input layout");
            }
            slots.push_back({Kind::Value, static_cast<size_t>(it - layout.begin()), var.type()});
        }
    }
    if (!has_syst) {
        throw std::runtime_error("fakefactors::generic: correction '" + correction_name + "' has no 'syst' input");
    }
}

std::vector<correction::Variable::Type>
ArgBuilder::build(const std::vector<float> &values, const std::string &syst) const {
    std::vector<correction::Variable::Type> args;
    args.reserve(slots.size());
    for (const auto &slot : slots) {
        switch (slot.kind) {
        case Kind::Process: args.emplace_back(process); break;
        case Kind::Syst: args.emplace_back(syst); break;
        case Kind::Value:
            if (slot.type == correction::Variable::VarType::integer) {
                args.emplace_back(static_cast<int>(values.at(slot.index)));
            } else {
                args.emplace_back(static_cast<double>(values.at(slot.index)));
            }
        }
    }
    return args;
}

NonClosureHandler::NonClosureHandler(const std::string &p, const std::vector<std::string> &vars,
                                     const correction::CompoundCorrection *c, size_t pos)
    : prefix(p), compound(c), syst_pos(pos), variables(vars) {}

float NonClosureHandler::evaluate(const std::string &systematic,
                                  std::vector<correction::Variable::Type> args) const {
    args[syst_pos] = "nominal";
    float nominal_value = compound->evaluate(args);

    bool is_target_variation = (systematic != "nominal") &&
                               (systematic.find(prefix) == 0) &&
                               (systematic.find("non_closure_Corr") != std::string::npos);

    if (!is_target_variation) {
        if (systematic == "nominal") {
            return nominal_value;
        }
        args[syst_pos] = systematic;
        return compound->evaluate(args);
    }

    std::string coarse_correction = systematic.substr(prefix.length());

    double sum_sq_diff = 0.0;
    for (const auto &variable : variables) {
        args[syst_pos] = prefix + variable + "_" + coarse_correction;
        float diff = nominal_value - static_cast<float>(compound->evaluate(args));
        sum_sq_diff += (diff * diff);
    }

    float total_uncertainty = std::sqrt(sum_sq_diff);
    bool is_up = (systematic.compare(systematic.length() - 2, 2, "Up") == 0);

    return is_up ? (nominal_value + total_uncertainty) : (nominal_value - total_uncertainty);
}

namespace {

size_t layout_index(const std::vector<std::string> &layout, const std::string &name) {
    auto it = std::find(layout.begin(), layout.end(), name);
    if (it == layout.end()) {
        throw std::runtime_error("fakefactors::generic: guard '" + name + "' is not in the input layout");
    }
    return static_cast<size_t>(it - layout.begin());
}

struct ProcessEval {
    Process cfg;
    const correction::Correction *ff;
    ArgBuilder ff_args, frac_args;
    const correction::Correction *dr = nullptr;
    std::unique_ptr<ArgBuilder> dr_args;
    std::shared_ptr<NonClosureHandler> nc;
    std::unique_ptr<ArgBuilder> nc_args;
};

// Everything needed at event level for one leg, built once at setup
struct LegEval {
    const correction::Correction *fractions;
    std::string fraction_variation;
    std::vector<ProcessEval> processes;
    size_t guard;

    LegEval(correctionManager::CorrectionManager &cm, const std::vector<std::string> &layout,
            const std::string &guard_name, const Leg &leg, const std::string &ff_file,
            const std::string *ff_corr_file)
        : fractions(cm.loadCorrection(ff_file, leg.fractions)),
          fraction_variation(leg.fraction_variation),
          guard(layout_index(layout, guard_name)) {
        processes.reserve(leg.processes.size());
        for (const auto &p : leg.processes) {
            auto ff = cm.loadCorrection(ff_file, p.ff);
            processes.push_back(ProcessEval{
                p, ff,
                ArgBuilder(p.ff, ff->inputs(), layout, p.name),
                ArgBuilder(leg.fractions, fractions->inputs(), layout, p.name)});
            auto &pe = processes.back();
            if (!ff_corr_file) continue;
            if (!p.dr_sr.empty()) {
                pe.dr = cm.loadCorrection(*ff_corr_file, p.dr_sr);
                pe.dr_args = std::make_unique<ArgBuilder>(p.dr_sr, pe.dr->inputs(), layout, p.name);
            }
            if (!p.non_closure.empty()) {
                auto compound = cm.loadCompoundCorrection(*ff_corr_file, p.non_closure);
                pe.nc_args = std::make_unique<ArgBuilder>(p.non_closure, compound->inputs(), layout, p.name);
                pe.nc = std::make_shared<NonClosureHandler>(p.non_closure_prefix, p.non_closure_variables, compound,
                                                            pe.nc_args->syst_pos);
            }
        }
    }
};

} // namespace

ROOT::RDF::RNode build_inputs(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::vector<std::string> &input_columns) {
    if (input_columns.empty()) {
        throw std::runtime_error("fakefactors::generic::build_inputs requires at least one input column");
    }
    std::string expression = "std::vector<float>{";
    for (size_t i = 0; i < input_columns.size(); ++i) {
        expression += "static_cast<float>(" + input_columns[i] + ")";
        if (i + 1 < input_columns.size()) expression += ", ";
    }
    expression += "}";
    return df.Define(outputname, expression);
}

ROOT::RDF::RNode raw_fakefactor(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname,
    const std::string &inputs_column,
    const std::vector<std::string> &layout,
    const std::string &guard,
    const Leg &leg,
    const std::string &ff_file) {

    Logger::get("GenericRawFakeFactor")->debug("Setting up raw fake factor for {} ({} processes)", leg.fractions, leg.processes.size());

    auto eval = std::make_shared<LegEval>(correctionManager, layout, guard, leg, ff_file, nullptr);

    auto calc = [eval](const std::vector<float> &in) {
        float ff = 0.0f;
        if (in.at(eval->guard) >= 0.0f) {
            for (const auto &p : eval->processes) {
                float ff_val = p.ff->evaluate(p.ff_args.build(in, p.cfg.ff_variation));
                float frac = eval->fractions->evaluate(p.frac_args.build(in, eval->fraction_variation));
                ff += std::max(frac, 0.0f) * std::max(ff_val, 0.0f);
            }
        }
        Logger::get("GenericRawFakeFactor")->debug("Event raw fake factor {}", ff);
        return ff;
    };

    return df.Define(outputname, calc, {inputs_column});
}

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
    const bool split_info) {

    Logger::get("GenericFakeFactor")->debug("Setting up fake factor for {} ({} processes)", leg.fractions, leg.processes.size());

    auto eval = std::make_shared<LegEval>(correctionManager, layout, guard, leg, ff_file, &ff_corr_file);

    constexpr size_t n_split = 6;

    auto calc = [eval, split_info](const std::vector<float> &in) {
        std::vector<float> split;
        float ff_sum = 0.0f;
        if (split_info) split.assign(n_split * eval->processes.size(), 0.0f);

        if (in.at(eval->guard) > 0.0f) {
            size_t i = 0;
            for (const auto &p : eval->processes) {
                float ff = p.ff->evaluate(p.ff_args.build(in, p.cfg.ff_variation));
                float frac = eval->fractions->evaluate(p.frac_args.build(in, eval->fraction_variation));
                float dr = p.dr ? static_cast<float>(p.dr->evaluate(p.dr_args->build(in, p.cfg.dr_sr_variation))) : 1.0f;
                float nc = p.nc ? p.nc->evaluate(p.cfg.non_closure_variation, p.nc_args->build(in, "nominal")) : 1.0f;

                ff = std::max(ff, 0.0f);
                frac = std::max(frac, 0.0f);
                dr = std::max(dr, 0.0f);
                nc = std::max(nc, 0.0f);
                ff_sum += frac * ff * dr * nc;

                if (split_info) {
                    float corr = dr * nc;
                    float *out = &split[i * n_split];
                    out[0] = ff; out[1] = frac; out[2] = dr; out[3] = nc; out[4] = corr;
                    out[5] = frac * ff * corr;
                }
                ++i;
            }
        }
        return split_info ? split : std::vector<float>{ff_sum};
    };

    if (split_info) {
        std::vector<std::string> strings = {"fakefactor_generic_split_info", leg.fractions, leg.fraction_variation};
        for (const auto &p : leg.processes) {
            strings.insert(strings.end(), {p.name, p.ff_variation, p.dr_sr_variation, p.non_closure_variation});
        }
        strings.push_back(ff_file);
        strings.push_back(ff_corr_file);
        std::string identifier = fakefactors::joinAndReplace(strings, "_");

        auto df1 = df.Define(identifier, calc, {inputs_column});
        return event::quantity::Unroll<float>(df1, outputnames, identifier);
    }

    auto extract_ff = [](const std::vector<float> &v) { return v[0]; };
    auto df1 = df.Define(outputnames[0] + "_tmp_ff_vec", calc, {inputs_column});
    return df1.Define(outputnames[0], extract_ff, {outputnames[0] + "_tmp_ff_vec"});
}

} // namespace generic
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_GENERIC_CXX */
