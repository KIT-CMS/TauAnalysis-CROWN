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
        /**
         * @brief Function to calculate raw fake factors without corrections with
         * correctionlib for the semileptonic channels
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param pt_2 pt of the hadronic tau in the tau pair
         * @param njets number of jets in the event
         * @param pt_1 pt of the leptonic tau in the tau pair
         * @param mt_1 transverse mass of the leptonic tau in the tau pair
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
                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                if (_pt_2 >= 0.) {
                    auto __njets = static_cast<float>(_njets);

                    qcd_ff = qcd->evaluate({_pt_2, __njets, QCD_variation});
                    wjets_ff = wjets->evaluate({_pt_2, __njets, _pt_1, Wjets_variation});
                    ttbar_ff = ttbar->evaluate({_pt_2, __njets, ttbar_variation});

                    qcd_frac = fractions->evaluate({"QCD", _mt_1, __njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", _mt_1, __njets, fraction_variation});
                    ttbar_frac = fractions->evaluate({"ttbar", _mt_1, __njets, fraction_variation});

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
         * for the semileptonic channels, optionally splitting the information for further analysis
         * 
         * @param df the input dataframe
         * @param correctionManager the correction manager to load corrections
         * @param outputname name of the output column for the fake factor
         * @param pt_2 pt of the hadronic tau in the tau pair
         * @param njets number of jets in the event
         * @param pt_1 pt of the leptonic tau in the tau pair
         * @param mt_1 transverse mass of the leptonic tau in the tau pair
         * @param tau_decaymode_2 decay mode of the hadronic tau in the tau pair
         * @param iso_1 isolation of the leptonic tau in the tau pair
         * @param mass_2 mass of the hadronic tau in the tau pair
         * @param eta_1 eta of the leptonic tau in the tau pair
         * @param eta_2 eta of the hadronic tau in the tau pair
         * @param jpt_1 pt of the leading jet in the event
         * @param jeta_1 eta of the leading jet in the event
         * @param jpt_2 pt of the subleading jet in the event
         * @param jeta_2 eta of the subleading jet in the event
         * @param met missing transverse energy in the event
         * @param deltaEta_ditaupair delta eta between the leptonic tau and the hadronic tau
         * @param pt_tt pt of the ditau system
         * @param pt_ttjj pt of the ditau + dijet system
         * @param deltaR_ditaupair delta R between the leptonic tau and the hadronic tau
         * @param mt_tot total transverse mass of the event
         * @param deltaR_jj delta R between the two leading jets in the event
         * @param deltaR_1j1 delta R between the leptonic tau and the leading jet
         * @param deltaR_12j1 delta R between the hadronic tau and the leading jet
         * @param m_vis visible mass of the ditau system
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
            // correctionlib kinematic variables
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

            const auto input_columns = {
                pt_2,
                njets,
                pt_1,
                mt_1,
                tau_decaymode_2,
                iso_1,
                mass_2,
                eta_1,
                eta_2,
                jpt_1,
                jeta_1,
                jpt_2,
                jeta_2,
                met,
                deltaEta_ditaupair,
                pt_tt,
                pt_ttjj,
                deltaR_ditaupair,
                mt_tot,
                deltaR_jj,
                deltaR_1j1,
                deltaR_12j1,
                m_vis
            };

            auto calc_fake_factor = [
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
                const int &_njets,
                const float &_pt_1,
                const float &_mt_1,
                const int &_tau_decaymode_2,
                const float &_iso_1,
                const float &_mass_2,
                const float &_eta_1,
                const float &_eta_2,
                const float &_jpt_1,
                const float &_jeta_1,
                const float &_jpt_2,
                const float &_jeta_2,
                const float &_met,
                const float &_deltaEta_ditaupair,
                const float &_pt_tt,
                const float &_pt_ttjj,
                const float &_deltaR_ditaupair,
                const float &_mt_tot,
                const float &_deltaR_jj,
                const float &_deltaR_1j1,
                const float &_deltaR_12j1,
                const float &_m_vis
            ) {
                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                float qcd_DR_SR_corr = 0.0, qcd_non_closure_corr = 0.0;
                float wjets_DR_SR_corr = 0.0, wjets_non_closure_corr = 0.0;
                float ttbar_DR_SR_corr = 1.0, ttbar_non_closure_corr = 0.0;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (_pt_2 >= 0.) {
                    auto __njets = static_cast<float>(_njets);
                    auto __tau_decaymode_2 = static_cast<float>(_tau_decaymode_2);

                    qcd_ff = qcd->evaluate({_pt_2, __njets, QCD_variation});
                    wjets_ff = wjets->evaluate({_pt_2, __njets, _pt_1, Wjets_variation});
                    ttbar_ff = ttbar->evaluate({_pt_2, __njets, ttbar_variation});

                    qcd_frac = fractions->evaluate({"QCD", _mt_1, __njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", _mt_1, __njets, fraction_variation});
                    ttbar_frac = fractions->evaluate({"ttbar", _mt_1, __njets, fraction_variation});

                    qcd_DR_SR_corr = qcd_DR_SR->evaluate({_pt_tt, __njets, QCD_DR_SR_correction_variation});
                    wjets_DR_SR_corr = wjets_DR_SR->evaluate({_pt_tt, __njets, Wjets_DR_SR_correction_variation});

                    std::vector<correction::Variable::Type> _non_closure_args = {
                        __tau_decaymode_2,
                        _eta_1,
                        _eta_2,
                        _jeta_1,
                        _jeta_2,
                        _jpt_1,
                        _jpt_2,
                        _met,
                        _deltaEta_ditaupair,
                        _deltaR_ditaupair,
                        _deltaR_1j1,
                        _deltaR_12j1,
                        _pt_ttjj,
                        _mass_2,
                        _mt_tot,
                        _m_vis,
                        _iso_1,
                        __njets
                    };

                    auto qcd_non_closure_args = _non_closure_args;
                    qcd_non_closure_args.push_back(QCD_non_closure_correction_variation);

                    auto wjets_non_closure_args = _non_closure_args;
                    wjets_non_closure_args.push_back(Wjets_non_closure_correction_variation);

                    auto ttbar_non_closure_args = _non_closure_args;
                    ttbar_non_closure_args.push_back(ttbar_non_closure_correction_variation);

                    qcd_non_closure_corr = qcd_non_closure->evaluate(qcd_non_closure_args);
                    wjets_non_closure_corr = wjets_non_closure->evaluate(wjets_non_closure_args);
                    ttbar_non_closure_corr = ttbar_non_closure->evaluate(ttbar_non_closure_args);

                    qcd_correction = std::max(qcd_DR_SR_corr, 0.0f) * std::max(qcd_non_closure_corr, 0.0f);
                    wjets_correction = std::max(wjets_DR_SR_corr, 0.0f) * std::max(wjets_non_closure_corr, 0.0f);
                    ttbar_correction = std::max(ttbar_non_closure_corr, 0.0f);
                }

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
#endif /* GUARDFAKEFACTORS_H */
