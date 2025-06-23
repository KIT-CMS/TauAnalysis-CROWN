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
    namespace nmssm {
    /**
     * @brief Function to calculate raw fake factors without corrections with
     * correctionlib for the semileptonic channels
     *
     * @param df the input dataframe
     * @param outputname name of the output column for the fake factor
     * @param tau_pt pt of the hadronic tau in the tau pair
     * @param njets number of good jets in the event
     * @param lep_mt transverse mass of the leptonic tau in the tau pair
     * @param nbtags number of good b-tagged jets in the event
     * @param variation name of the uncertainty variation or nominal
     * @param ff_file correctionlib json file with the fake factors
     * @returns a dataframe with the fake factors
     */
    ROOT::RDF::RNode
    raw_fakefactor_lt(ROOT::RDF::RNode df, const std::string &outputname,
                            const std::string &tau_pt, const std::string &njets,
                            const std::string &lep_mt, const std::string &nbtags,
                            const std::string &variation,
                            const std::string &ff_file) {
        Logger::get("RawFakeFactor")
            ->debug("Setting up functions for raw fake factor (without "
                    "corrections) evaluation with correctionlib");
        Logger::get("RawFakeFactor")->debug("Variation - Name {}", variation);
        auto qcd =
            correction::CorrectionSet::from_file(ff_file)->at("QCD_fake_factors");
        auto wjets =
            correction::CorrectionSet::from_file(ff_file)->at("Wjets_fake_factors");
        auto ttbar =
            correction::CorrectionSet::from_file(ff_file)->at("ttbar_fake_factors");
        auto fractions =
            correction::CorrectionSet::from_file(ff_file)->at("process_fractions");
        auto calc_fake_factor = [variation, qcd, wjets, ttbar,
                                fractions](const float &pt_2, const int &njets,
                                            const float &mt_1, const int &nbtag) {
            float ff = -1.;
            if (pt_2 >= 0.) {
                Logger::get("RawFakeFactor")->debug("Tau pt - value {}", pt_2);
                Logger::get("RawFakeFactor")->debug("N jets - value {}", njets);

                float qcd_ff = qcd->evaluate({pt_2, (float)njets, variation});
                Logger::get("RawFakeFactor")->debug("QCD - value {}", qcd_ff);
                float wjets_ff = wjets->evaluate({pt_2, (float)njets, variation});
                Logger::get("RawFakeFactor")->debug("Wjets - value {}", wjets_ff);
                float ttbar_ff = ttbar->evaluate({pt_2, (float)njets, variation});
                Logger::get("RawFakeFactor")->debug("ttbar - value {}", ttbar_ff);

                Logger::get("RawFakeFactor")->debug("Lep mt - value {}", mt_1);
                Logger::get("RawFakeFactor")->debug("N b-jets - value {}", nbtag);

                float qcd_frac =
                    fractions->evaluate({"QCD", mt_1, (float)nbtag, variation});
                Logger::get("RawFakeFactor")->debug("QCD - fraction {}", qcd_frac);
                float wjets_frac =
                    fractions->evaluate({"Wjets", mt_1, (float)nbtag, variation});
                Logger::get("RawFakeFactor")
                    ->debug("Wjets - fraction {}", wjets_frac);
                float ttbar_frac =
                    fractions->evaluate({"ttbar", mt_1, (float)nbtag, variation});
                Logger::get("RawFakeFactor")
                    ->debug("ttbar - fraction {}", ttbar_frac);

                ff = qcd_frac * qcd_ff + wjets_frac * wjets_ff +
                    ttbar_frac * ttbar_ff;
            }

            Logger::get("RawFakeFactor")->debug("Event Fake Factor {}", ff);
            return ff;
        };
        auto df1 = df.Define(outputname, calc_fake_factor,
                            {tau_pt, njets, lep_mt, nbtags});
        return df1;
    }
    /**
     * @brief Function to calculate raw fake factors without corrections with
     * correctionlib for the full hadronic channel
     *
     * @param df the input dataframe
     * @param outputname name of the output column for the fake factor
     * @param tau_idx index of the tau, leading/subleading
     * @param tau_pt_1 pt of the leading hadronic tau in the tau pair
     * @param tau_pt_2 pt of the subleading hadronic tau in the tau pair
     * @param njets number of good jets in the event
     * @param variation name of the uncertainty variation or nominal
     * @param ff_file correctionlib json file with the fake factors
     * @returns a dataframe with the fake factors
     */
    ROOT::RDF::RNode
    raw_fakefactor_tt(ROOT::RDF::RNode df, const std::string &outputname,
                            const int &tau_idx, const std::string &tau_pt_1,
                            const std::string &tau_pt_2, const std::string &njets,
                            const std::string &variation,
                            const std::string &ff_file) {

        Logger::get("RawFakeFactor")
            ->debug("Setting up functions for raw fake factor (without "
                    "corrections) evaluation with correctionlib");
        Logger::get("RawFakeFactor")->debug("Variation - Name {}", variation);

        auto qcd =
            correction::CorrectionSet::from_file(ff_file)->at("QCD_fake_factors");

        auto qcd_subleading = correction::CorrectionSet::from_file(ff_file)->at(
            "QCD_subleading_fake_factors");

        auto calc_fake_factor = [tau_idx, variation, qcd, qcd_subleading](
                                    const float &pt_1, const float &pt_2,
                                    const int &njets) {
            float ff = -1.;
            if (pt_2 >= 0.) {
                Logger::get("RawFakeFactor")
                    ->debug("Leading Tau pt - value {}", pt_1);
                Logger::get("RawFakeFactor")
                    ->debug("Subleading Tau pt - value {}", pt_2);
                Logger::get("RawFakeFactor")->debug("N jets - value {}", njets);

                float qcd_ff = -1.;
                if (tau_idx == 0) {
                    float qcd_ff = qcd->evaluate({pt_1, (float)njets, variation});
                    Logger::get("RawFakeFactor")->debug("QCD - value {}", qcd_ff);
                    ff = qcd_ff;
                } else if (tau_idx == 1) {
                    float qcd_ff =
                        qcd_subleading->evaluate({pt_2, (float)njets, variation});
                    Logger::get("RawFakeFactor")->debug("QCD - value {}", qcd_ff);
                    ff = qcd_ff;
                }
            }

            Logger::get("RawFakeFactor")->debug("Event Fake Factor {}", ff);
            return ff;
        };
        auto df1 =
            df.Define(outputname, calc_fake_factor, {tau_pt_1, tau_pt_2, njets});
        return df1;
    }
    /**
     * @brief Function to calculate fake factors with correctionlib for the
     * semileptonic channels
     *
     * @param df the input dataframe
     * @param outputname name of the output column for the fake factor
     * @param tau_pt pt of the hadronic tau in the tau pair
     * @param njets number of good jets in the event
     * @param lep_mt transverse mass of the leptonic tau in the tau pair
     * @param nbtags number of good b-tagged jets in the event
     * @param lep_pt pt of the leptonic tau in the tau pair
     * @param lep_iso isolation of the leptonic tau in the tau pair
     * @param m_vis visible mass of the tau pair
     * @param variation name of the uncertainty variation or nominal
     * @param ff_file correctionlib json file with the fake factors
     * @param ff_corr_file correctionlib json file with corrections for the fake
     * factors
     * @returns a dataframe with the fake factors
     */
    ROOT::RDF::RNode
    fakefactor_lt(ROOT::RDF::RNode df, const std::string &outputname,
                        const std::string &tau_pt, const std::string &njets,
                        const std::string &lep_mt, const std::string &nbtags,
                        const std::string &lep_pt, const std::string &lep_iso,
                        const std::string &m_vis, const std::string &variation,
                        const std::string &ff_file,
                        const std::string &ff_corr_file) {

        Logger::get("FakeFactor")
            ->debug("Setting up functions for fake factor evaluation with "
                    "correctionlib");
        Logger::get("FakeFactor")->debug("Variation - Name {}", variation);
        auto qcd =
            correction::CorrectionSet::from_file(ff_file)->at("QCD_fake_factors");
        auto wjets =
            correction::CorrectionSet::from_file(ff_file)->at("Wjets_fake_factors");
        auto ttbar =
            correction::CorrectionSet::from_file(ff_file)->at("ttbar_fake_factors");
        auto fractions =
            correction::CorrectionSet::from_file(ff_file)->at("process_fractions");

        auto qcd_lep_pt_closure = correction::CorrectionSet::from_file(ff_corr_file)
                                    ->at("QCD_non_closure_lep_pt_correction");
        auto qcd_lep_iso_closure =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("QCD_non_closure_lep_iso_correction");
        auto qcd_DR_SR = correction::CorrectionSet::from_file(ff_corr_file)
                            ->at("QCD_DR_SR_correction");
        auto wjets_lep_pt_closure =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("Wjets_non_closure_lep_pt_correction");
        auto wjets_DR_SR = correction::CorrectionSet::from_file(ff_corr_file)
                            ->at("Wjets_DR_SR_correction");
        auto ttbar_lep_pt_closure =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("ttbar_non_closure_lep_pt_correction");
        auto calc_fake_factor = [variation, qcd, wjets, ttbar, fractions,
                                qcd_lep_pt_closure, qcd_lep_iso_closure, qcd_DR_SR,
                                wjets_lep_pt_closure, wjets_DR_SR,
                                ttbar_lep_pt_closure](
                                    const float &pt_2, const int &njets,
                                    const float &mt_1, const int &nbtag,
                                    const float &pt_1, const float &iso_1,
                                    const float &m_vis) {
            float ff = -1.;
            if (pt_2 >= 0.) {
                Logger::get("FakeFactor")->debug("Tau pt - value {}", pt_2);
                Logger::get("FakeFactor")->debug("N jets - value {}", njets);

                float qcd_ff = qcd->evaluate({pt_2, (float)njets, variation});
                Logger::get("FakeFactor")->debug("QCD - value {}", qcd_ff);
                float wjets_ff = wjets->evaluate({pt_2, (float)njets, variation});
                Logger::get("FakeFactor")->debug("Wjets - value {}", wjets_ff);
                float ttbar_ff = ttbar->evaluate({pt_2, (float)njets, variation});
                Logger::get("FakeFactor")->debug("ttbar - value {}", ttbar_ff);

                Logger::get("FakeFactor")->debug("Lep mt - value {}", mt_1);
                Logger::get("FakeFactor")->debug("N b-jets - value {}", nbtag);

                float qcd_frac =
                    fractions->evaluate({"QCD", mt_1, (float)nbtag, variation});
                Logger::get("FakeFactor")->debug("QCD - fraction {}", qcd_frac);
                float wjets_frac =
                    fractions->evaluate({"Wjets", mt_1, (float)nbtag, variation});
                Logger::get("FakeFactor")->debug("Wjets - fraction {}", wjets_frac);
                float ttbar_frac =
                    fractions->evaluate({"ttbar", mt_1, (float)nbtag, variation});
                Logger::get("FakeFactor")->debug("ttbar - fraction {}", ttbar_frac);

                Logger::get("FakeFactor")->debug("Lep pt - value {}", pt_1);
                Logger::get("FakeFactor")->debug("Lep iso - value {}", iso_1);
                Logger::get("FakeFactor")->debug("m_vis - value {}", m_vis);

                float qcd_lep_pt_corr =
                    qcd_lep_pt_closure->evaluate({pt_1, variation});
                Logger::get("FakeFactor")
                    ->debug("QCD - lep pt correction {}", qcd_lep_pt_corr);
                float qcd_lep_iso_corr =
                    qcd_lep_iso_closure->evaluate({iso_1, variation});
                Logger::get("FakeFactor")
                    ->debug("QCD - lep iso correction {}", qcd_lep_iso_corr);
                float qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, variation});
                Logger::get("FakeFactor")
                    ->debug("QCD - DR to SR correction {}", qcd_DR_SR_corr);
                float wjets_lep_pt_corr =
                    wjets_lep_pt_closure->evaluate({pt_1, variation});
                Logger::get("FakeFactor")
                    ->debug("Wjets - lep pt correction {}", wjets_lep_pt_corr);
                float wjets_DR_SR_corr = wjets_DR_SR->evaluate({m_vis, variation});
                Logger::get("FakeFactor")
                    ->debug("Wjets - DR to SR correction {}", wjets_DR_SR_corr);
                float ttbar_lep_pt_corr =
                    ttbar_lep_pt_closure->evaluate({pt_1, variation});
                Logger::get("FakeFactor")
                    ->debug("ttbar - lep pt correction {}", ttbar_lep_pt_corr);

                ff = qcd_frac * qcd_ff * qcd_lep_pt_corr * qcd_lep_iso_corr *
                        qcd_DR_SR_corr +
                    wjets_frac * wjets_ff * wjets_lep_pt_corr * wjets_DR_SR_corr +
                    ttbar_frac * ttbar_ff * ttbar_lep_pt_corr;
            }

            Logger::get("FakeFactor")->debug("Event Fake Factor {}", ff);
            return ff;
        };
        auto df1 =
            df.Define(outputname, calc_fake_factor,
                    {tau_pt, njets, lep_mt, nbtags, lep_pt, lep_iso, m_vis});
        return df1;
    }
    /**
     * @brief Function to calculate fake factors with correctionlib for the full
     * hadronic channel
     *
     * @param df the input dataframe
     * @param outputname name of the output column for the fake factor
     * @param tau_idx index of the tau, leading/subleading
     * @param tau_pt_1 pt of the leading hadronic tau in the tau pair
     * @param tau_pt_2 pt of the subleading hadronic tau in the tau pair
     * @param njets number of good jets in the event
     * @param m_vis visible mass of the tau pair
     * @param variation name of the uncertainty variation or nominal
     * @param ff_file correctionlib json file with the fake factors
     * @param ff_corr_file correctionlib json file with corrections for the fake
     * factors
     * @returns a dataframe with the fake factors
     */
    ROOT::RDF::RNode
    fakefactor_tt(ROOT::RDF::RNode df, const std::string &outputname,
                        const int &tau_idx, const std::string &tau_pt_1,
                        const std::string &tau_pt_2, const std::string &njets,
                        const std::string &m_vis, const std::string &variation,
                        const std::string &ff_file,
                        const std::string &ff_corr_file) {

        Logger::get("FakeFactor")
            ->debug("Setting up functions for fake factor evaluation with "
                    "correctionlib");
        Logger::get("FakeFactor")->debug("Variation - Name {}", variation);

        auto qcd =
            correction::CorrectionSet::from_file(ff_file)->at("QCD_fake_factors");

        auto qcd_tau_pt_closure =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("QCD_non_closure_subleading_lep_pt_correction");
        auto qcd_m_vis_closure = correction::CorrectionSet::from_file(ff_corr_file)
                                    ->at("QCD_non_closure_m_vis_correction");
        auto qcd_DR_SR = correction::CorrectionSet::from_file(ff_corr_file)
                            ->at("QCD_DR_SR_correction");

        auto qcd_subleading = correction::CorrectionSet::from_file(ff_file)->at(
            "QCD_subleading_fake_factors");

        auto qcd_tau_pt_closure_subleading =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("QCD_subleading_non_closure_leading_lep_pt_correction");
        auto qcd_m_vis_closure_subleading =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("QCD_subleading_non_closure_m_vis_correction");
        auto qcd_DR_SR_subleading =
            correction::CorrectionSet::from_file(ff_corr_file)
                ->at("QCD_subleading_DR_SR_correction");

        auto calc_fake_factor = [tau_idx, variation, qcd, qcd_tau_pt_closure,
                                qcd_m_vis_closure, qcd_DR_SR, qcd_subleading,
                                qcd_tau_pt_closure_subleading,
                                qcd_m_vis_closure_subleading,
                                qcd_DR_SR_subleading](
                                    const float &pt_1, const float &pt_2,
                                    const int &njets, const float &m_vis) {
            float ff = -1.;
            if (pt_2 >= 0.) {
                Logger::get("FakeFactor")->debug("Leading Tau pt - value {}", pt_1);
                Logger::get("FakeFactor")
                    ->debug("Subleading Tau pt - value {}", pt_2);
                Logger::get("FakeFactor")->debug("m_vis - value {}", m_vis);
                Logger::get("FakeFactor")->debug("N jets - value {}", njets);

                float qcd_ff = -1.;
                float qcd_tau_pt_corr = -1.;
                float qcd_m_vis_corr = -1.;
                float qcd_DR_SR_corr = -1.;
                if (tau_idx == 0) {
                    float qcd_ff = qcd->evaluate({pt_1, (float)njets, variation});
                    Logger::get("FakeFactor")->debug("QCD - value {}", qcd_ff);
                    float qcd_tau_pt_corr =
                        qcd_tau_pt_closure->evaluate({pt_2, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD - lep pt correction {}", qcd_tau_pt_corr);
                    float qcd_m_vis_corr =
                        qcd_m_vis_closure->evaluate({m_vis, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD - visible mass correction {}", qcd_m_vis_corr);
                    float qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD - DR to SR correction {}", qcd_DR_SR_corr);
                    ff = qcd_ff * qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr;
                } else if (tau_idx == 1) {
                    float qcd_ff =
                        qcd_subleading->evaluate({pt_2, (float)njets, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD(subleading) - value {}", qcd_ff);
                    float qcd_tau_pt_corr =
                        qcd_tau_pt_closure_subleading->evaluate({pt_1, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD(subleading) - lep pt correction {}",
                                qcd_tau_pt_corr);
                    float qcd_m_vis_corr =
                        qcd_m_vis_closure_subleading->evaluate({m_vis, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD(subleading) - visible mass correction {}",
                                qcd_m_vis_corr);
                    float qcd_DR_SR_corr =
                        qcd_DR_SR_subleading->evaluate({m_vis, variation});
                    Logger::get("FakeFactor")
                        ->debug("QCD(subleading) - DR to SR correction {}",
                                qcd_DR_SR_corr);
                    ff = qcd_ff * qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr;
                }
            }

            Logger::get("FakeFactor")->debug("Event Fake Factor {}", ff);
            return ff;
        };
        auto df1 = df.Define(outputname, calc_fake_factor,
                            {tau_pt_1, tau_pt_2, njets, m_vis});
        return df1;
    }
} // namespace nmssm
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
            const std::string &delta_r,
            // for fraction
            const std::string &lep_mt,
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
                const float &pt_2, const int &njets, const float &mt_1, const float &delta_r) {

                float ff = 0.0;

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;

                if (pt_2 >= 0.) {
                    Logger::get("SM RawFakeFactor (lt)")->debug("pt_tau={}, njets={}, mt={}, delta_r={}", pt_2, njets, mt_1, delta_r);

                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, delta_r, Wjets_variation});
                    ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM RawFakeFactor (lt)")->debug("RawFakeFactor (lt) - QCD={}, Wjets={}, ttbar={}", qcd_ff, wjets_ff, ttbar_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM RawFakeFactor (lt)")->debug("Fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                    ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) + 
                        std::max(wjets_frac, (float)0.) * std::max(wjets_ff, (float)0.) +
                        std::max(ttbar_frac, (float)0.) * std::max(ttbar_ff, (float)0.);
                }

                Logger::get("SM RawFakeFactor (lt)")->debug("Event Fake Factor {}", ff);

                return ff;
            };

            auto df1 = df.Define(outputname, calc_fake_factor, {tau_pt, njets, lep_mt, delta_r});

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

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;
                float ttbar_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (pt_2 >= 0.) {
                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, pt_1, Wjets_variation});
                    ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fake factors: QCD={}, Wjets={}, ttbar={}", qcd_ff, wjets_ff, ttbar_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

                    // qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, (float)njets, QCD_DR_SR_correction_variation});
                    qcd_DR_SR_corr = 1.0;  // Ignoring QCD DR_SR correction for now
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

                    ttbar_non_closure_corr = ttbar_non_closure->evaluate(
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
                const float &pt_2,
                const int &njets,
                const float &delta_r,
                const float &mt_1,
                const float &pt_1,
                const int &tau_decaymode,
                const float &m_vis,
                const float &lep_iso,
                const float &tau_mass) {

                float qcd_ff = 0.0, wjets_ff = 0.0, ttbar_ff = 0.0;
                float qcd_frac = 0.0, wjets_frac = 0.0, ttbar_frac = 0.0;
                float qcd_DR_SR_corr = 0., qcd_non_closure_corr = 0.;
                float wjets_DR_SR_corr = 0., wjets_non_closure_corr = 0.;
                float ttbar_DR_SR_corr = 1., ttbar_non_closure_corr = 0.;

                float qcd_correction = 0.0, wjets_correction = 0.0, ttbar_correction = 0.0;

                if (pt_2 >= 0.) {
                    qcd_ff = qcd->evaluate({pt_2, (float)njets, QCD_variation});
                    wjets_ff = wjets->evaluate({pt_2, (float)njets, pt_1, Wjets_variation});
                    ttbar_ff = ttbar->evaluate({pt_2, (float)njets, ttbar_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fake factors: QCD={}, Wjets={}, ttbar={}", qcd_ff, wjets_ff, ttbar_ff);

                    qcd_frac = fractions->evaluate({"QCD", mt_1, (float)njets, fraction_variation});
                    wjets_frac = fractions->evaluate({"Wjets", mt_1, (float)njets, fraction_variation});
                    ttbar_frac = fractions->evaluate({"ttbar", mt_1, (float)njets, fraction_variation});

                    Logger::get("SM FaceFactor (lt)")->debug("fractions: QCD={}, Wjets={}, ttbar={}", qcd_frac, wjets_frac, ttbar_frac);

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

                    wjets_DR_SR_corr = wjets_DR_SR->evaluate({m_vis, (float)njets, Wjets_DR_SR_correction_variation});
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

                    ttbar_non_closure_corr = ttbar_non_closure->evaluate(
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

            auto df1 = df.Define(shifted_collection_identifier, calc_fake_factor, {tau_pt, njets, delta_r, lep_mt, lep_pt, tau_decaymode, m_vis, lep_iso, tau_mass});
            auto df2 = event::quantity::Unroll<float>(df1, outputname, shifted_collection_identifier);

            return df2;
        }
    } // namespace sm
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
