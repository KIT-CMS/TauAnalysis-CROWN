#ifndef GUARDFAKEFACTORS_CXX
#define GUARDFAKEFACTORS_CXX

/// The namespace that contains the fake factor function.
#include "../include/fakefactors.hxx"
#include "../../../../include/event.hxx"
#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include <vector>
#include <string>
#include <sstream>
#include <iterator>
#include <iostream>
#include <random>
#include <string_view>
#include <array>

#include <regex>
#include <cmath>
#include <stdexcept>

namespace fakefactors {
    ROOT::RDF::RNode build_model_input_column(
        ROOT::RDF::RNode df,
        const std::string &outputname,
        const std::vector<std::string> &input_columns
    ) {
        if (input_columns.empty()) {
            throw std::runtime_error(
                "fakefactors::build_model_input_column requires at least one input column");
        }

        std::string define_expression = "std::vector<float>{";
        for (size_t i = 0; i < input_columns.size(); ++i) {
            define_expression += input_columns[i];
            if (i + 1 < input_columns.size()) {
                define_expression += ", ";
            }
        }
        define_expression += "}";

        return df.Define(outputname, define_expression);
    }

    /**
     * @brief Function to join and replace characters in a vector of strings
     * and return a single string.
     * 
     * @param strings Vector of strings to join.
     * @param delimiter Delimiter to use for joining the strings.
     * @return A single string with the joined and modified strings.
     */
    std::string joinAndReplace(const std::vector<std::string>& strings, const std::string& delimiter) {
        static std::unordered_map<std::string, int> seen_strings;
        std::ostringstream os;

        for (const auto& str : strings) {
            std::string modified_str = str;
            std::replace(modified_str.begin(), modified_str.end(), '/', '_');
            std::replace(modified_str.begin(), modified_str.end(), '.', '_');

            os << modified_str << delimiter;
        }

        std::string result = os.str();
        result = result.substr(0, result.size() - delimiter.size()); // Remove the trailing delimiter

        if (seen_strings.find(result) != seen_strings.end()) {
            seen_strings[result]++;
            result += "_" + std::to_string(seen_strings[result]);
        } else {
            seen_strings[result] = 0;
        }

        return result;
    }
    namespace sm {
        std::vector<correction::Variable::Type>
        to_correction_args(const std::vector<float> &values) {
            return std::vector<correction::Variable::Type>(values.begin(), values.end());
        }

        std::vector<correction::Variable::Type>
        with_suffix(const std::vector<float> &values, const std::string &suffix) {
            auto args = to_correction_args(values);
            args.emplace_back(suffix);
            return args;
        }

        std::vector<correction::Variable::Type>
        with_prefix_and_suffix(const std::string &prefix,
                               const std::vector<float> &values,
                               const std::string &suffix) {
            std::vector<correction::Variable::Type> args;
            args.reserve(values.size() + 2);
            args.emplace_back(prefix);
            args.insert(args.end(), values.begin(), values.end());
            args.emplace_back(suffix);
            return args;
        }

        NonClosureHandler::NonClosureHandler(const std::string& proc,
                                             const std::string& file,
                                             const correction::CompoundCorrection* c)
            : compound(c) {
            prefix = proc + "_non_closure_";
            std::string pattern_str = prefix + "(.*)_correction";
            std::regex pattern(pattern_str);
            std::smatch match;

            auto cset = correction::CorrectionSet::from_file(file);

            for (const auto& [name, _] : *cset) {
                if (std::regex_match(name, match, pattern)) {
                    variables.push_back(match[1].str());
                }
            }
        }

        float NonClosureHandler::evaluate(
            const std::string& systematic,
            std::vector<correction::Variable::Type> args
        ) {
            args.push_back("nominal");
            float nominal_value = compound->evaluate(args);

            bool is_target_variation = (systematic != "nominal") &&
                                       (systematic.find(prefix) == 0) &&
                                       (systematic.find("non_closure_Corr") != std::string::npos);

            if (!is_target_variation) {
                if (systematic == "nominal") {
                    return nominal_value;
                }

                args.back() = systematic;
                return compound->evaluate(args);
            }

            std::string coarse_correction = systematic.substr(prefix.length());

            double sum_sq_diff = 0.0;

            for (const auto& variable : variables) {
                std::string specific_key = prefix + variable + "_" + coarse_correction;
                args.back() = specific_key;

                float variation_val = compound->evaluate(args);
                float diff = nominal_value - variation_val;

                sum_sq_diff += (diff * diff);
            }

            float total_uncertainty = std::sqrt(sum_sq_diff);
            bool is_up = (systematic.compare(systematic.length() - 2, 2, "Up") == 0);

            return is_up ? (nominal_value + total_uncertainty) : (nominal_value - total_uncertainty);
        }

        /**
         * @brief Function to calculate raw fake factors without corrections with
         * correctionlib for the semileptonic channels
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param pt_2_input scalar event validity guard (negative values short-circuit to 0)
         * @param qcd_ff_input correctionlib inputs [pt_2, njets]
         * @param wjets_ff_input correctionlib inputs [pt_2, njets, pt_1]
         * @param ttbar_ff_input correctionlib inputs [pt_2, njets]
         * @param fractions_input correctionlib inputs [mt_1, njets]
         * @param fraction_variation name of the uncertainty variation or nominal
         * @param QCD_variation name of the uncertainty variation or nominal for QCD
         * @param Wjets_variation name of the uncertainty variation or nominal for Wjets
         * @param ttbar_variation name of the uncertainty variation or nominal for ttbar
         * @param ff_file correctionlib json file with the fake factors
         * @returns a dataframe with the fake factors
         */
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
            //
            const std::string &fraction_variation,
            const std::string &QCD_variation,
            const std::string &Wjets_variation,
            const std::string &ttbar_variation,
            //
            const std::string &ff_file
        ) {
            Logger::get("SM RawFakeFactor (lt)")->debug("Setting up functions for raw fake factor (without corrections) evaluation with correctionlib");
            Logger::get("SM RawFakeFactor (lt)")->debug("Fraction variations: fraction={}, QCD={}, Wjets={}, ttbar={})", fraction_variation, QCD_variation, Wjets_variation, ttbar_variation);

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto calc_fake_factor = [
                qcd, wjets, ttbar, fractions,
                QCD_variation, Wjets_variation, ttbar_variation, fraction_variation](
                const float &_pt_2,
                const std::vector<float> &_qcd_ff_input,
                const std::vector<float> &_wjets_ff_input,
                const std::vector<float> &_ttbar_ff_input,
                const std::vector<float> &_fractions_input
            ) {
                if (_pt_2 < 0.0f) {
                    return 0.0f;
                }

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                

                qcd_ff = qcd->evaluate(with_suffix(_qcd_ff_input, QCD_variation));
                wjets_ff = wjets->evaluate(with_suffix(_wjets_ff_input, Wjets_variation));
                ttbar_ff = ttbar->evaluate(with_suffix(_ttbar_ff_input, ttbar_variation));

                qcd_frac = fractions->evaluate(with_prefix_and_suffix("QCD", _fractions_input, fraction_variation));
                wjets_frac = fractions->evaluate(with_prefix_and_suffix("Wjets", _fractions_input, fraction_variation));
                ttbar_frac = fractions->evaluate(with_prefix_and_suffix("ttbar", _fractions_input, fraction_variation));

                Logger::get("SM RawFakeFactor (lt)")->debug("RawFakeFactor (lt) - QCD={}, Wjets={}, ttbar={}", qcd_ff, wjets_ff, ttbar_ff);

                Logger::get("SM RawFakeFactor (lt)")->debug("Fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) + 
                    std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) +
                    std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.);

                Logger::get("SM RawFakeFactor (lt)")->debug("Event Fake Factor {}", ff);

                return ff;
            };

            auto df1 = df.Define(
                outputname,
                calc_fake_factor,
                {
                    pt_2_input,
                    qcd_ff_input,
                    wjets_ff_input,
                    ttbar_ff_input,
                    fractions_input
                }
            );

            return df1;
        }
        /**
         * @brief Function to calculate fake factors with corrections with correctionlib
         * for the semileptonic channels, optionally splitting the information for further analysis
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param pt_2_input scalar event validity guard (negative values short-circuit to 0)
         * @param qcd_ff_input correctionlib inputs [pt_2, njets]
         * @param wjets_ff_input correctionlib inputs [pt_2, njets, pt_1]
         * @param ttbar_ff_input correctionlib inputs [pt_2, njets]
         * @param fractions_input correctionlib inputs [mt_1, njets]
         * @param qcd_DR_SR_input correctionlib inputs [mt_1, njets]
         * @param wjets_DR_SR_input correctionlib inputs [mt_1, njets]
         * @param qcd_non_closure_input correctionlib non-closure inputs (QCD ordering)
         * @param wjets_non_closure_input correctionlib non-closure inputs (Wjets ordering)
         * @param ttbar_non_closure_input correctionlib non-closure inputs (ttbar ordering)
         * @param fraction_variation name of the uncertainty variation or nominal
         * @param QCD_variation name of the uncertainty variation or nominal for QCD
         * @param Wjets_variation name of the uncertainty variation or nominal for Wjets
         * @param ttbar_variation name of the uncertainty variation or nominal for ttbar
         * @param QCD_DR_SR_correction_variation name of the uncertainty variation or nominal
         * for the QCD DR to SR correction
         * @param QCD_non_closure_correction_variation name of the uncertainty variation or
         * nominal for the QCD non-closure correction
         * @param Wjets_DR_SR_correction_variation name of the uncertainty variation or nominal
         * for the Wjets DR to SR correction
         * @param Wjets_non_closure_correction_variation name of the uncertainty variation or
         * nominal for the Wjets non-closure correction
         * @param ttbar_non_closure_correction_variation name of the uncertainty variation or
         * nominal for the ttbar non-closure correction
         * @param ff_file correctionlib json file with the fake factors
         * @param ff_corr_file correctionlib json file with corrections for the fake factors
         * @param split_info bool to define the level of splitting of the information
         0: only fake factor
         1: raw components (ff and fractions and corrections per process)
         * @returns a dataframe with the fake factors and additional split information
         */
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
            ) {

            Logger::get("SM FakeFactor (lt)")->debug("Setting up functions for fake factor evaluation with correctionlib");
            
            Logger::get("SM FakeFactor (lt)")->debug("Fraction variations: fraction={}, QCD={}, Wjets={}, ttbar={})", fraction_variation, QCD_variation, Wjets_variation, ttbar_variation);
            Logger::get("SM FakeFactor (lt)")->debug("Correction variations: QCD_DR_SR={}, QCD_non_closure={})", QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation);
            Logger::get("SM FakeFactor (lt)")->debug("Correction variations: Wjets_DR_SR={}, Wjets_non_closure={})", Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation);
            Logger::get("SM FakeFactor (lt)")->debug("Correction variations: ttbar_non_closure={})", ttbar_non_closure_correction_variation);

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
            auto qcd_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "QCD_compound_correction");

            auto wjets_DR_SR = correctionManager.loadCorrection(ff_corr_file, "Wjets_DR_SR_correction");
            auto wjets_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "Wjets_compound_correction");

            auto ttbar_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "ttbar_compound_correction");

            // ---

            auto qcd_handler = std::make_shared<NonClosureHandler>("QCD", ff_corr_file, qcd_non_closure);
            auto wjets_handler = std::make_shared<NonClosureHandler>("Wjets", ff_corr_file, wjets_non_closure);
            auto ttbar_handler = std::make_shared<NonClosureHandler>("ttbar", ff_corr_file, ttbar_non_closure);

            const auto input_columns = {
                pt_2_input,
                qcd_ff_input,
                wjets_ff_input,
                ttbar_ff_input,
                fractions_input,
                qcd_DR_SR_input,
                wjets_DR_SR_input,
                qcd_non_closure_input,
                wjets_non_closure_input,
                ttbar_non_closure_input
            };

            auto calc_fake_factor = [
                qcd_handler, wjets_handler, ttbar_handler,
                qcd, wjets, ttbar, fractions,
                QCD_variation, Wjets_variation, ttbar_variation, fraction_variation,
                qcd_DR_SR, qcd_non_closure,
                QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation,
                wjets_DR_SR, wjets_non_closure,
                Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation,
                ttbar_non_closure,
                ttbar_non_closure_correction_variation,
                split_info](
                const float &_pt_2,
                const std::vector<float> &_qcd_ff_input,
                const std::vector<float> &_wjets_ff_input,
                const std::vector<float> &_ttbar_ff_input,
                const std::vector<float> &_fractions_input,
                const std::vector<float> &_qcd_DR_SR_input,
                const std::vector<float> &_wjets_DR_SR_input,
                const std::vector<float> &_qcd_non_closure_input,
                const std::vector<float> &_wjets_non_closure_input,
                const std::vector<float> &_ttbar_non_closure_input
            ) {
                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                float qcd_DR_SR_corr = 0.0, qcd_non_closure_corr = 0.0;
                float wjets_DR_SR_corr = 0.0, wjets_non_closure_corr = 0.0;
                float ttbar_DR_SR_corr = 1.0, ttbar_non_closure_corr = 0.0;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (_pt_2 < 0.0f) {
                    if (split_info) {
                        return std::vector<float>{
                            0.0f,
                            0.0f,
                            0.0f,
                            //
                            0.0f,
                            0.0f,
                            0.0f,
                            //
                            0.0f,
                            0.0f,
                            0.0f,
                            //
                            0.0f,
                            0.0f,
                            0.0f,
                            //
                            0.0f,
                            0.0f,
                            0.0f,
                            //
                            0.0f,
                            0.0f,
                            0.0f
                        };
                    }
                    return std::vector<float>{0.0f};
                }

                qcd_ff = qcd->evaluate(with_suffix(_qcd_ff_input, QCD_variation));
                wjets_ff = wjets->evaluate(with_suffix(_wjets_ff_input, Wjets_variation));
                ttbar_ff = ttbar->evaluate(with_suffix(_ttbar_ff_input, ttbar_variation));

                qcd_frac = fractions->evaluate(with_prefix_and_suffix("QCD", _fractions_input, fraction_variation));
                wjets_frac = fractions->evaluate(with_prefix_and_suffix("Wjets", _fractions_input, fraction_variation));
                ttbar_frac = fractions->evaluate(with_prefix_and_suffix("ttbar", _fractions_input, fraction_variation));

                qcd_DR_SR_corr = qcd_DR_SR->evaluate(with_suffix(_qcd_DR_SR_input, QCD_DR_SR_correction_variation));
                wjets_DR_SR_corr = wjets_DR_SR->evaluate(with_suffix(_wjets_DR_SR_input, Wjets_DR_SR_correction_variation));

                std::vector<correction::Variable::Type> qcd_nc_args(_qcd_non_closure_input.begin(), _qcd_non_closure_input.end());
                std::vector<correction::Variable::Type> wjets_nc_args(_wjets_non_closure_input.begin(), _wjets_non_closure_input.end());
                std::vector<correction::Variable::Type> ttbar_nc_args(_ttbar_non_closure_input.begin(), _ttbar_non_closure_input.end());

                qcd_non_closure_corr = qcd_handler->evaluate(QCD_non_closure_correction_variation, qcd_nc_args);
                wjets_non_closure_corr = wjets_handler->evaluate(Wjets_non_closure_correction_variation, wjets_nc_args);
                ttbar_non_closure_corr = ttbar_handler->evaluate(ttbar_non_closure_correction_variation, ttbar_nc_args);

                qcd_correction = std::max(qcd_DR_SR_corr, 0.0f) * std::max(qcd_non_closure_corr, 0.0f);
                wjets_correction = std::max(wjets_DR_SR_corr, 0.0f) * std::max(wjets_non_closure_corr, 0.0f);
                ttbar_correction = std::max(ttbar_non_closure_corr, 0.0f);

                if (split_info) {
                    return std::vector<float>{
                        std::max(qcd_ff, 0.0f),
                        std::max(wjets_ff, 0.0f),
                        std::max(ttbar_ff, 0.0f),
                        //
                        std::max(qcd_frac, 0.0f),
                        std::max(wjets_frac, 0.0f),
                        std::max(ttbar_frac, 0.0f),
                        //
                        std::max(qcd_DR_SR_corr, 0.0f),
                        std::max(wjets_DR_SR_corr, 0.0f),
                        std::max(ttbar_DR_SR_corr, 0.0f),
                        //
                        std::max(qcd_non_closure_corr, 0.0f),
                        std::max(wjets_non_closure_corr, 0.0f),
                        std::max(ttbar_non_closure_corr, 0.0f),
                        //
                        std::max(qcd_correction, 0.0f),
                        std::max(wjets_correction, 0.0f),
                        std::max(ttbar_correction, 0.0f),
                        //
                        std::max(qcd_frac, 0.0f) * std::max(qcd_ff, 0.0f) * std::max(qcd_correction, 0.0f),
                        std::max(wjets_frac, 0.0f) * std::max(wjets_ff, 0.0f) * std::max(wjets_correction, 0.0f),
                        std::max(ttbar_frac, 0.0f) * std::max(ttbar_ff, 0.0f) * std::max(ttbar_correction, 0.0f)
                    };
                }

                // If not splitting info, return a vector with a single element: the combined fake factor.
                float ff = std::max(qcd_frac, 0.0f) * std::max(qcd_ff, 0.0f) * std::max(qcd_DR_SR_corr, 0.0f) * std::max(qcd_non_closure_corr, 0.0f) +
                           std::max(wjets_frac, 0.0f) * std::max(wjets_ff, 0.0f) * std::max(wjets_DR_SR_corr, 0.0f) * std::max(wjets_non_closure_corr, 0.0f) +
                           std::max(ttbar_frac, 0.0f) * std::max(ttbar_ff, 0.0f) * std::max(ttbar_non_closure_corr, 0.0f);
                return std::vector<float>{ff};
            };

            if (split_info) {
                 std::vector<std::string> strings = {
                    "fakefactor_lt_split_info",
                    fraction_variation,
                    QCD_variation,
                    Wjets_variation,
                    ttbar_variation,
                    QCD_DR_SR_correction_variation,
                    QCD_non_closure_correction_variation,
                    Wjets_DR_SR_correction_variation,
                    Wjets_non_closure_correction_variation,
                    ttbar_non_closure_correction_variation,
                    ff_file,
                    ff_corr_file
                };
                std::string shifted_collection_identifier = fakefactors::joinAndReplace(strings, "_");

                auto df1 = df.Define(shifted_collection_identifier, calc_fake_factor, input_columns);
                return event::quantity::Unroll<float>(df1, outputnames, shifted_collection_identifier);
            } else {
                auto extract_ff = [](const std::vector<float>& ff_vec) { return ff_vec[0]; };
                auto df1 = df.Define(outputnames[0] + "_tmp_ff_vec", calc_fake_factor, input_columns);
                return df1.Define(outputnames[0], extract_ff, {outputnames[0] + "_tmp_ff_vec"});
            }
        }
    } // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_CXX */
