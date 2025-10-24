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
            const std::string &tau_pt,
            const std::string &njets,
            //const std::string &delta_r,
            // for fraction
            const std::string &lep_mt,
            //
            const std::string &fraction_variation,
            const std::string &QCD_variation,
            const std::string &Wjets_variation,
            //const std::string &ttbar_variation,
            //
            const std::string &ff_file
        ) {
            Logger::get("SM RawFakeFactor (lt)")->debug("Setting up functions for raw fake factor (without corrections) evaluation with correctionlib");
            Logger::get("SM RawFakeFactor (lt)")->debug("Fraction variations: fraction={}, QCD={}, Wjets={}", fraction_variation, QCD_variation, Wjets_variation);

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            //auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto calc_fake_factor = [
                qcd, wjets, fractions,
                QCD_variation, Wjets_variation, fraction_variation](
                const float &pt_2, const int &njets, const float &mt_1) {

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0;

                if (pt_2 >= 0.) {
                    Logger::get("SM RawFakeFactor (lt)")->debug("pt_tau={}, njets={}, mt={}", pt_2, njets, mt_1);

                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, Wjets_variation});
                    //ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM RawFakeFactor (lt)")->debug("RawFakeFactor (lt) - QCD={}, Wjets={}", qcd_ff, wjets_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    //ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM RawFakeFactor (lt)")->debug("Fractions: QCD={}, Wjets={}", qcd_frac, wjets_frac);

                    ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) + 
                        std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.);
                        //std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.);
                }

                Logger::get("SM RawFakeFactor (lt)")->debug("Event Fake Factor {}", ff);

                return ff;
            };

            auto df1 = df.Define(outputname, calc_fake_factor, {tau_pt, njets, lep_mt});

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
            //const std::string &ttbar_variation,
            //
            const std::string &QCD_DR_SR_correction_variation,
            const std::string &QCD_non_closure_correction_variation,
            //
            //const std::string &Wjets_DR_SR_correction_variation,
            const std::string &Wjets_non_closure_correction_variation,
            //
            //const std::string &ttbar_non_closure_correction_variation,
            //
            const std::string &ff_file,
            const std::string &ff_corr_file
            ) {

            Logger::get("SM FaceFactor (lt)")->debug("Setting up functions for fake factor evaluation with correctionlib");

            Logger::get("SM FaceFactor (lt)")->debug("Fraction variations: fraction={}, QCD={}, Wjets={})", fraction_variation, QCD_variation, Wjets_variation);
            Logger::get("SM FaceFactor (lt)")->debug("Correction variations: QCD_DR_SR={}, QCD_non_closure={})", QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation);
            //Logger::get("SM FaceFactor (lt)")->debug("Correction variations: Wjets_DR_SR={}, Wjets_non_closure={})", Wjets_DR_SR_correction_variation, Wjets_non_closure_correction_variation);
            //Logger::get("SM FaceFactor (lt)")->debug("Correction variations: ttbar_non_closure={})", ttbar_non_closure_correction_variation);

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            //auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
            auto qcd_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "QCD_compound_correction");

            //auto wjets_DR_SR = correctionManager.loadCorrection(ff_corr_file, "Wjets_DR_SR_correction");
            auto wjets_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "Wjets_compound_correction");

            //auto ttbar_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "ttbar_compound_correction");

            auto calc_fake_factor = [
                qcd, wjets, fractions,
                QCD_variation, Wjets_variation, fraction_variation,
                qcd_DR_SR, qcd_non_closure,
                QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation,
                wjets_non_closure,
                Wjets_non_closure_correction_variation](
                const float &pt_2,
                const int &njets,
                const float &delta_r,
                const float &mt_1,
                const float &pt_1,
                const int &tau_decaymode,
                const float &m_vis,
                const float &lep_iso,
                const float &tau_mass) {

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0;

                if (pt_2 >= 0.) {
                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, Wjets_variation});
                    //ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fake factors: QCD={}, Wjets={}", qcd_ff, wjets_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    //ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}", qcd_frac, wjets_frac);

                    qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, (float)njets, QCD_DR_SR_correction_variation});
                    //qcd_DR_SR_corr = 1.0;  // Ignoring QCD DR_SR correction for now
                    qcd_non_closure_corr = qcd_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            QCD_non_closure_correction_variation
                        }
                    );

                    Logger::get("SM FaceFactor (lt)")->debug("QCD: DR_SR={}, non_closure={}", qcd_DR_SR_corr, qcd_non_closure_corr);

                    // wjets_DR_SR_corr = wjets_DR_SR->evaluate({m_vis, (float)njets, Wjets_DR_SR_correction_variation});
                    wjets_DR_SR_corr = 1.0;  // Ignoring Wjets DR_SR correction for now
                    wjets_non_closure_corr = wjets_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            Wjets_non_closure_correction_variation
                        }
                    );

                    Logger::get("SM FaceFactor (lt)")->debug("Wjets: DR_SR={}, non_closure={}", wjets_DR_SR_corr, wjets_non_closure_corr);

                    /*ttbar_non_closure_corr = ttbar_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            ttbar_non_closure_correction_variation
                        }
                    );*/

                    //Logger::get("SM FaceFactor (lt)")->debug("ttbar: non_closure={}", ttbar_non_closure_corr);

                    qcd_correction = std::max(qcd_DR_SR_corr, (float)0.) * std::max(qcd_non_closure_corr, (float)0.);
                    wjets_correction = std::max(wjets_DR_SR_corr, (float)0.) * std::max(wjets_non_closure_corr, (float)0.);
                    //ttbar_correction = std::max(ttbar_non_closure_corr, (float)0.);

                    ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * qcd_correction +
                        std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) * wjets_correction;
                        //std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.) * ttbar_correction;

                }

                Logger::get("SM FaceFactor (lt)")->debug("Event Fake Factor {}", ff);
                
                return ff;
            };

            auto df1 = df.Define(outputname, calc_fake_factor, {tau_pt, njets, delta_r, lep_mt, lep_pt, tau_decaymode, m_vis, lep_iso, tau_mass});

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
            //const std::string &ttbar_variation,
            //
            const std::string &QCD_DR_SR_correction_variation,
            const std::string &QCD_non_closure_correction_variation,
            //
            //const std::string &Wjets_DR_SR_correction_variation,
            const std::string &Wjets_non_closure_correction_variation,
            //
            //const std::string &ttbar_non_closure_correction_variation,
            //
            const std::string &ff_file,
            const std::string &ff_corr_file
            ) {

            auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
            auto wjets = correctionManager.loadCorrection(ff_file, "Wjets_fake_factors");
            //auto ttbar = correctionManager.loadCorrection(ff_file, "ttbar_fake_factors");
            auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");

            auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
            auto qcd_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "QCD_compound_correction");

            //auto wjets_DR_SR = correctionManager.loadCorrection(ff_corr_file, "Wjets_DR_SR_correction");
            auto wjets_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "Wjets_compound_correction");

            //auto ttbar_non_closure = correctionManager.loadCompoundCorrection(ff_corr_file, "ttbar_compound_correction");

            auto calc_fake_factor = [
                qcd, wjets, fractions,
                QCD_variation, Wjets_variation, fraction_variation,
                qcd_DR_SR, qcd_non_closure,
                QCD_DR_SR_correction_variation, QCD_non_closure_correction_variation,
                wjets_non_closure,
                Wjets_non_closure_correction_variation](
                const float &pt_2,
                const int &njets,
                const float &delta_r,
                const float &mt_1,
                const float &pt_1,
                const int &tau_decaymode,
                const float &m_vis,
                const float &lep_iso,
                const float &tau_mass) {

                float qcd_ff = 0.0, wjets_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0;

                if (pt_2 >= 0.) {
                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, Wjets_variation});
                    //ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fake factors: QCD={}, Wjets={}", qcd_ff, wjets_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    //ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}", qcd_frac, wjets_frac);

                    qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, (float)njets, QCD_DR_SR_correction_variation});
                    qcd_non_closure_corr = qcd_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            QCD_non_closure_correction_variation
                        }
                    );

                    Logger::get("SM FaceFactor (lt)")->debug("QCD: DR_SR={}, non_closure={}", qcd_DR_SR_corr, qcd_non_closure_corr);

                    //wjets_DR_SR_corr = wjets_DR_SR->evaluate({m_vis, (float)njets, Wjets_DR_SR_correction_variation});
                    wjets_DR_SR_corr = 1.0;
                    wjets_non_closure_corr = wjets_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            Wjets_non_closure_correction_variation
                        }
                    );

                    Logger::get("SM FaceFactor (lt)")->debug("Wjets: DR_SR={}, non_closure={}", wjets_DR_SR_corr, wjets_non_closure_corr);

                    /*ttbar_non_closure_corr = ttbar_non_closure->evaluate(
                        {
                            m_vis,
                            tau_mass,
                            delta_r,
                            lep_iso,
                            (float)tau_decaymode,
                            (float)njets,
                            ttbar_non_closure_correction_variation
                        }
                    );

                    Logger::get("SM FaceFactor (lt)")->debug("ttbar: non_closure={}", ttbar_non_closure_corr);*/

                    qcd_correction = std::max(qcd_DR_SR_corr, (float)0.) * std::max(qcd_non_closure_corr, (float)0.);
                    wjets_correction = std::max(wjets_DR_SR_corr, (float)0.) * std::max(wjets_non_closure_corr, (float)0.);
                    //ttbar_correction = std::max(ttbar_non_closure_corr, (float)0.);
                }

                // all of them process wise
                // raw_ff, factions, DR_SR, correction_wo_DR_SR, combined_correction, ff
                std::vector<float> result = {
                    std::max(qcd_ff, (float)0.),
                    std::max(wjets_ff, (float)0.),
                    //std::max(ttbar_ff, (float)0.),
                    //
                    std::max(qcd_frac, (float)0.),
                    std::max(wjets_frac, (float)0.),
                    //std::max(ttbar_frac, (float)0.),
                    //
                    std::max(qcd_DR_SR_corr, (float)0.),
                    std::max(wjets_DR_SR_corr, (float)0.),
                    //std::max(ttbar_DR_SR_corr, (float)0.),
                    //
                    std::max(qcd_non_closure_corr, (float)0.),
                    std::max(wjets_non_closure_corr, (float)0.),
                    //std::max(ttbar_non_closure_corr, (float)0.),
                    //
                    std::max(qcd_correction, (float)0.),
                    std::max(wjets_correction, (float)0.),
                    //std::max(ttbar_correction, (float)0.),
                    //
                    std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_correction, (float)0.),
                    std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) * std::max(wjets_correction, (float)0.)};
                    //std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.) * std::max(ttbar_correction, (float)0.)};
        
                return result;
            };

            std::vector<std::string> strings = {
                "fakefactor_lt_split_info",
                fraction_variation,
                QCD_variation,
                Wjets_variation,
                //ttbar_variation,
                QCD_DR_SR_correction_variation,
                QCD_non_closure_correction_variation,
                //Wjets_DR_SR_correction_variation,
                Wjets_non_closure_correction_variation,
                //ttbar_non_closure_correction_variation,
                ff_file,
                ff_corr_file};
        
            std::string shifted_collection_identifier =  fakefactors::joinAndReplace(strings, "_");

            auto df1 = df.Define(shifted_collection_identifier, calc_fake_factor, {tau_pt, njets, delta_r, lep_mt, lep_pt, tau_decaymode, m_vis, lep_iso, tau_mass});
            auto df2 = event::quantity::Unroll<float>(df1, outputname, shifted_collection_identifier);

            return df2;
        }
    } // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
