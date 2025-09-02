#ifndef GUARDFAKEFACTORS_H
#define GUARDFAKEFACTORS_H
/// The namespace that contains the fake factor function.
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

namespace fakefactors {
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
        namespace config {
            // Define all unique variable names as constexpr string_views
            inline constexpr std::string_view pt_2 {"pt_2"};
            inline constexpr std::string_view njets {"njets"};
            inline constexpr std::string_view deltaR_ditaupair {"deltaR_ditaupair"};
            inline constexpr std::string_view mt_1 {"mt_1"};
            inline constexpr std::string_view m_vis {"m_vis"};
            inline constexpr std::string_view pt_1 {"pt_1"};
            inline constexpr std::string_view tau_decaymode_2 {"tau_decaymode_2"};
            inline constexpr std::string_view iso_1 {"iso_1"};
            inline constexpr std::string_view mass_2 {"mass_2"};
            //
            inline constexpr std::array qcd_ff_inputs = {pt_2, njets};
            inline constexpr std::array wjets_ff_inputs = {pt_2, njets, pt_1};
            inline constexpr std::array ttbar_ff_inputs = {pt_2, njets};
            //
            inline constexpr std::array fraction_inputs = {mt_1, njets};
            //
            inline constexpr std::array DR_SR_inputs = {m_vis, njets};
            inline constexpr std::array qcd_DR_SR_inputs = DR_SR_inputs;
            inline constexpr std::array wjets_DR_SR_inputs = DR_SR_inputs;
            //
            inline constexpr std::array non_closure_inputs = {
                m_vis,
                mass_2,
                deltaR_ditaupair,
                iso_1,
                tau_decaymode_2,
                njets
            };
            inline constexpr std::array qcd_non_closure_inputs = non_closure_inputs;
            inline constexpr std::array wjets_non_closure_inputs = non_closure_inputs;
            inline constexpr std::array ttbar_non_closure_inputs = non_closure_inputs;
        }
        template <size_t N>
        std::vector<correction::Variable::Type>
        build_eval_vector(
            const std::unordered_map<std::string, float>& available_vars,
            const std::array<std::string_view, N>& required_vars
        ) {
            std::vector<correction::Variable::Type> eval_args;
            eval_args.reserve(N);

            for (const auto& var_name_sv : required_vars) {
                std::string var_name(var_name_sv);
                try {
                    float value = available_vars.at(var_name);
                    eval_args.push_back(static_cast<double>(value));
                } catch (const std::out_of_range& e) {
                    Logger::get("build_eval_vector")->critical("Required variable '{}' not found in available variables map!", var_name);
                    throw; // Re-throw the exception
                }
            }
            return eval_args;
        }
        template <typename CorrectionType, size_t N>
        float evaluate(
            const std::unordered_map<std::string, float>& available_vars,
            const CorrectionType* corr,
            const std::array<std::string_view, N>& inputs,
            const std::string& variation,
            const std::string& process_name = "" // Optional: for insertion at the beginning
        ) {
            auto args = build_eval_vector(available_vars, inputs);
            args.push_back(variation);
            
            if (!process_name.empty()) {
                args.insert(args.begin(), process_name);
            }
            
            return corr->evaluate(args);
        }
        /**
         * @brief Function to calculate raw fake factors without corrections with
         * correctionlib for the semileptonic channels
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param tau_pt pt of the hadronic tau in the tau pair
         * @param njets number of jets in the event
         * @param delta_r delta R between the leptonic tau and the hadronic tau
         * @param lep_mt transverse mass of the leptonic tau in the tau pair
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
                const int &_njets,
                const float &_mt_1,
                const float &_pt_1
            ) {

                const std::unordered_map<std::string, float> available_vars = {
                    {"pt_2", _pt_2},
                    {"njets", static_cast<float>(_njets)},
                    {"pt_1", _pt_1},
                    {"mt_1", _mt_1},
                };

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                if (_pt_2 >= 0.) {

                    wjets_ff = evaluate(available_vars, wjets, config::wjets_ff_inputs, Wjets_variation);
                    qcd_ff = evaluate(available_vars, qcd, config::qcd_ff_inputs, QCD_variation);
                    ttbar_ff = evaluate(available_vars, ttbar, config::ttbar_ff_inputs, ttbar_variation);

                    qcd_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "QCD");
                    wjets_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "Wjets");
                    ttbar_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "ttbar");

                    Logger::get("SM RawFakeFactor (lt)")->debug("RawFakeFactor (lt) - QCD={}, Wjets={}, ttbar={}", qcd_ff, wjets_ff, ttbar_ff);

                    Logger::get("SM RawFakeFactor (lt)")->debug("Fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                    ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) + 
                        std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) +
                        std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.);
                }

                Logger::get("SM RawFakeFactor (lt)")->debug("Event Fake Factor {}", ff);

                return ff;
            };

            auto df1 = df.Define(outputname, calc_fake_factor, {pt_2, njets, mt_1, pt_1});

            return df1;
        }
        /**
         * @brief Function to calculate fake factors with corrections with correctionlib
         * for the semileptonic channels
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param tau_pt pt of the hadronic tau in the tau pair
         * @param njets number of jets in the event
         * @param delta_r delta R between the leptonic tau and the hadronic tau
         * @param lep_mt transverse mass of the leptonic tau in the tau pair
         * @param lep_pt pt of the leptonic tau in the tau pair
         * @param tau_decaymode decay mode of the hadronic tau in the tau pair
         * @param lep_iso isolation of the leptonic tau in the tau pair
         * @param tau_mass mass of the hadronic tau in the tau pair
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
         * @returns a dataframe with the fake factors
         */
        ROOT::RDF::RNode
        fakefactor_lt(
            ROOT::RDF::RNode df, 
            correctionManager::CorrectionManager &correctionManager,
            const std::string &outputname,
            // for ff
            const std::string &pt_2,
            const std::string &njets,
            const std::string &deltaR_ditaupair,
            // for fraction 
            const std::string &mt_1,
            // for DR SR corrections
            const std::string &m_vis,
            // for non closure corrections
            const std::string &pt_1,
            const std::string &tau_decaymode_2,
            const std::string &iso_1,
            const std::string &mass_2,
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
            ) {

            Logger::get("SM FaceFactor (lt)")->debug("Setting up functions for fake factor evaluation with correctionlib");

            Logger::get("SM FaceFactor (lt)")->debug("Fraction variations: fraction={}, QCD={}, Wjets={}, ttbar={})", fraction_variation, QCD_variation, Wjets_variation, ttbar_variation);
            Logger::get("SM FaceFactor (lt)")->debug("Correction variations: QCD_DR_SR={}, QCD_non_closure={})", QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation);
            Logger::get("SM FaceFactor (lt)")->debug("Correction variations: Wjets_DR_SR={}, Wjets_non_closure={})", Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation);
            Logger::get("SM FaceFactor (lt)")->debug("Correction variations: ttbar_non_closure={})", ttbar_non_closure_correction_variation);

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
            auto qcd_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "QCD_compound_correction");

            auto wjets_DR_SR = correctionManager.loadCorrection(ff_corr_file, "Wjets_DR_SR_correction");
            auto wjets_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "Wjets_compound_correction");

            auto ttbar_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "ttbar_compound_correction");

            auto calc_fake_factor = [
                qcd, wjets, ttbar, fractions,
                QCD_variation, Wjets_variation, ttbar_variation, fraction_variation,
                qcd_DR_SR, qcd_non_closure,
                QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation,
                wjets_DR_SR, wjets_non_closure,
                Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation,
                ttbar_non_closure,
                ttbar_non_closure_correction_variation](
                const float &_pt_2,
                const int &_njets,
                const float &_deltaR_ditaupair,
                const float &_mt_1,
                const float &_pt_1,
                const int &_tau_decaymode_2,
                const float &_m_vis,
                const float &_iso_1,
                const float &_mass_2
            ) {

                const std::unordered_map<std::string, float> available_vars = {
                    {"pt_2", _pt_2},
                    {"njets", static_cast<float>(_njets)},
                    {"deltaR_ditaupair", _deltaR_ditaupair},
                    {"mt_1", _mt_1},
                    {"pt_1", _pt_1},
                    {"tau_decaymode_2", static_cast<float>(_tau_decaymode_2)},
                    {"m_vis", _m_vis},
                    {"iso_1", _iso_1},
                    {"mass_2", _mass_2}
                };

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;
                float ttbar_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (_pt_2 >= 0.) {
                    qcd_ff = evaluate(available_vars, qcd, config::qcd_ff_inputs, QCD_variation);
                    wjets_ff = evaluate(available_vars, wjets, config::wjets_ff_inputs, Wjets_variation);
                    ttbar_ff = evaluate(available_vars, ttbar, config::ttbar_ff_inputs, ttbar_variation);

                    qcd_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "QCD");
                    wjets_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "Wjets");
                    ttbar_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "ttbar");

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                    qcd_DR_SR_corr = 1.0f;  // evaluate(available_vars, qcd_DR_SR, config::qcd_DR_SR_inputs, QCD_DR_SR_correction_variation);  // ignore for now
                    wjets_DR_SR_corr = 1.0f;  // evaluate(available_vars, wjets_DR_SR, config::wjets_DR_SR_inputs, Wjets_DR_SR_correction_variation);  // ignore for now

                    qcd_non_closure_corr = evaluate(available_vars, qcd_non_closure, config::qcd_non_closure_inputs, QCD_non_closure_correction_variation);
                    wjets_non_closure_corr = evaluate(available_vars, wjets_non_closure, config::wjets_non_closure_inputs, Wjets_non_closure_correction_variation);
                    ttbar_non_closure_corr = evaluate(available_vars, ttbar_non_closure, config::ttbar_non_closure_inputs, ttbar_non_closure_correction_variation);

                    // ---------------------

                    Logger::get("SM FaceFactor (lt)")->debug("QCD: DR_SR={}, non_closure={}", qcd_DR_SR_corr, qcd_non_closure_corr);
                    Logger::get("SM FaceFactor (lt)")->debug("Wjets: DR_SR={}, non_closure={}", wjets_DR_SR_corr, wjets_non_closure_corr);
                    Logger::get("SM FaceFactor (lt)")->debug("ttbar: non_closure={}", ttbar_non_closure_corr);

                    qcd_correction = std::max(qcd_DR_SR_corr, (float)0.) * std::max(qcd_non_closure_corr, (float)0.);
                    wjets_correction = std::max(wjets_DR_SR_corr, (float)0.) * std::max(wjets_non_closure_corr, (float)0.);
                    ttbar_correction = std::max(ttbar_non_closure_corr, (float)0.);

                    ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * qcd_correction +
                        std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) * wjets_correction +
                        std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.) * ttbar_correction;

                }

                Logger::get("SM FaceFactor (lt)")->debug("Event Fake Factor {}", ff);

                return ff;
            };

            auto df1 = df.Define(outputname, calc_fake_factor, {pt_2, njets, deltaR_ditaupair, mt_1, pt_1, tau_decaymode_2, m_vis, iso_1, mass_2});

            return df1;
        }
        /**
         * @brief Function to calculate fake factors with corrections with correctionlib
         * for the semileptonic channels, splitting the information for further analysis
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param tau_pt pt of the hadronic tau in the tau pair
         * @param njets number of jets in the event
         * @param delta_r delta R between the leptonic tau and the hadronic tau
         * @param lep_mt transverse mass of the leptonic tau in the tau pair
         * @param lep_pt pt of the leptonic tau in the tau pair
         * @param tau_decaymode decay mode of the hadronic tau in the tau pair
         * @param lep_iso isolation of the leptonic tau in the tau pair
         * @param tau_mass mass of the hadronic tau in the tau pair
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
         * @returns a dataframe with the fake factors and additional split information
         */
        ROOT::RDF::RNode
        fakefactor_lt_split_info(
            ROOT::RDF::RNode df, 
            correctionManager::CorrectionManager &correctionManager,
            const std::vector<std::string> &outputname,
                // for ff
            const std::string &pt_2,
            const std::string &njets,
            const std::string &deltaR_ditaupair,
            // for fraction 
            const std::string &mt_1,
            // for DR SR corrections
            const std::string &m_vis,
            // for non closure corrections
            const std::string &pt_1,
            const std::string &tau_decaymode_2,
            const std::string &iso_1,
            const std::string &mass_2,
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
            ) {

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
            auto qcd_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "QCD_compound_correction");

            auto wjets_DR_SR = correctionManager.loadCorrection(ff_corr_file, "Wjets_DR_SR_correction");
            auto wjets_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "Wjets_compound_correction");

            auto ttbar_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "ttbar_compound_correction");

            auto calc_fake_factor = [
                qcd, wjets, ttbar, fractions,
                QCD_variation, Wjets_variation, ttbar_variation, fraction_variation,
                qcd_DR_SR, qcd_non_closure,
                QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation,
                wjets_DR_SR, wjets_non_closure,
                Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation,
                ttbar_non_closure,
                ttbar_non_closure_correction_variation](
                const float &_pt_2,
                const int &_njets,
                const float &_deltaR_ditaupair,
                const float &_mt_1,
                const float &_pt_1,
                const int &_tau_decaymode_2,
                const float &_m_vis,
                const float &_iso_1,
                const float &_mass_2
            ) {
                const std::unordered_map<std::string, float> available_vars = {
                    {"pt_2", _pt_2},
                    {"njets", static_cast<float>(_njets)},
                    {"deltaR_ditaupair", _deltaR_ditaupair},
                    {"mt_1", _mt_1},
                    {"pt_1", _pt_1},
                    {"tau_decaymode_2", static_cast<float>(_tau_decaymode_2)},
                    {"m_vis", _m_vis},
                    {"iso_1", _iso_1},
                    {"mass_2", _mass_2}
                };

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;
                float ttbar_DR_SR_corr = 1., ttbar_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (_pt_2 >= 0.) {
                    qcd_ff = evaluate(available_vars, qcd, config::qcd_ff_inputs, QCD_variation);
                    wjets_ff = evaluate(available_vars, wjets, config::wjets_ff_inputs, Wjets_variation);
                    ttbar_ff = evaluate(available_vars, ttbar, config::ttbar_ff_inputs, ttbar_variation);

                    qcd_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "QCD");
                    wjets_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "Wjets");
                    ttbar_frac = evaluate(available_vars, fractions, config::fraction_inputs, fraction_variation, "ttbar");

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                    qcd_DR_SR_corr = evaluate(available_vars, qcd_DR_SR, config::qcd_DR_SR_inputs, QCD_DR_SR_correction_variation);  // ignore for now
                    wjets_DR_SR_corr = evaluate(available_vars, wjets_DR_SR, config::wjets_DR_SR_inputs, Wjets_DR_SR_correction_variation);  // ignore for now

                    qcd_non_closure_corr = evaluate(available_vars, qcd_non_closure, config::qcd_non_closure_inputs, QCD_non_closure_correction_variation);
                    wjets_non_closure_corr = evaluate(available_vars, wjets_non_closure, config::wjets_non_closure_inputs, Wjets_non_closure_correction_variation);
                    ttbar_non_closure_corr = evaluate(available_vars, ttbar_non_closure, config::ttbar_non_closure_inputs, ttbar_non_closure_correction_variation);

                    // ---------------------

                    Logger::get("SM FaceFactor (lt)")->debug("QCD: DR_SR={}, non_closure={}", qcd_DR_SR_corr, qcd_non_closure_corr);
                    Logger::get("SM FaceFactor (lt)")->debug("Wjets: DR_SR={}, non_closure={}", wjets_DR_SR_corr, wjets_non_closure_corr);
                    Logger::get("SM FaceFactor (lt)")->debug("ttbar: non_closure={}", ttbar_non_closure_corr);

                    qcd_correction = std::max(qcd_DR_SR_corr, (float)0.) * std::max(qcd_non_closure_corr, (float)0.);
                    wjets_correction = std::max(wjets_DR_SR_corr, (float)0.) * std::max(wjets_non_closure_corr, (float)0.);
                    ttbar_correction = std::max(ttbar_non_closure_corr, (float)0.);
                }

                // all of them process wise
                // raw_ff, factions, DR_SR, correction_wo_DR_SR, combined_correction, ff
                std::vector<float> result = {
                    std::max(qcd_ff, (float)0.),
                    std::max(wjets_ff, (float)0.),
                    std::max(ttbar_ff, (float)0.),
                    //
                    std::max(qcd_frac, (float)0.),
                    std::max(wjets_frac, (float)0.),
                    std::max(ttbar_frac, (float)0.),
                    //
                    std::max(qcd_DR_SR_corr, (float)0.),
                    std::max(wjets_DR_SR_corr, (float)0.),
                    std::max(ttbar_DR_SR_corr, (float)0.),
                    //
                    std::max(qcd_non_closure_corr, (float)0.),
                    std::max(wjets_non_closure_corr, (float)0.),
                    std::max(ttbar_non_closure_corr, (float)0.),
                    //
                    std::max(qcd_correction, (float)0.),
                    std::max(wjets_correction, (float)0.),
                    std::max(ttbar_correction, (float)0.),
                    //
                    std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_correction, (float)0.),
                    std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) * std::max(wjets_correction, (float)0.),
                    std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.) * std::max(ttbar_correction, (float)0.)};

                return result;
            };

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
                ff_corr_file};

            std::string shifted_collection_identifier =  fakefactors::joinAndReplace(strings, "_");

            auto df1 = df.Define(shifted_collection_identifier, calc_fake_factor, {pt_2, njets, deltaR_ditaupair, mt_1, pt_1, tau_decaymode_2, m_vis, iso_1, mass_2});
            auto df2 = event::quantity::Unroll<float>(df1, outputname, shifted_collection_identifier);

            return df2;
        }
    } // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
