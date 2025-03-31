#ifndef GUARDFAKEFACTORS_TAU_H
#define GUARDFAKEFACTORS_TAU_H
/// The namespace that contains the fake factor function.
#include "../../../../include/basefunctions.hxx"
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

ROOT::RDF::RNode
raw_fakefactor_sm_lt(
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

ROOT::RDF::RNode
fakefactor_sm_lt(
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

ROOT::RDF::RNode
fakefactor_sm_lt_split_info(
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
        "fakefactor_sm_lt_split_info",
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
    auto df2 = basefunctions::UnrollVectorQuantity<float>(df1, shifted_collection_identifier, outputname);

    return df2;
}

ROOT::RDF::RNode
raw_fakefactor_sm_tt(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname,
    const int &tau_idx,
    const std::string &tau_pt_1,
    const std::string &tau_pt_2,
    const std::string &njets,
    const std::string &m_vis,
    //
    const std::string &fraction_variation,
    const std::string &QCD_variation,
    //
    const std::string &ff_file
) {

    Logger::get("SM RawFakeFactor (tt)")->debug("Setting up functions for raw fake factor (without corrections) evaluation with correctionlib");

    Logger::get("SM RawFakeFactor (tt)")->debug("Fraction variations: fraction={}, QCD={})", fraction_variation, QCD_variation);

    auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
    auto qcd_subleading = correctionManager.loadCorrection(ff_file, "QCD_subleading_fake_factors");

    auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");
    auto fractions_subleading = correctionManager.loadCorrection(ff_file, "process_fractions_subleading");

    auto calc_fake_factor = [
        tau_idx, 
        qcd, qcd_subleading, fractions, fractions_subleading, 
        QCD_variation, fraction_variation](
        const float &pt_1, const float &pt_2,
        const int &njets, const float &m_vis) {

        float ff = 0.0;

        float qcd_ff = 0.0;
        float qcd_frac = 0.0;

        if (pt_2 >= 0.) {
            Logger::get("SM RawFakeFactor (tt)")->debug("pt_tau_1={}, pt_tau_2={}, njets={}, m_vis={}", pt_1, pt_2, njets, m_vis);            

            if (tau_idx == 0) {
                qcd_ff = qcd->evaluate({pt_1, (float)njets, QCD_variation});
                qcd_frac = fractions->evaluate({"QCD", m_vis, (float)njets, fraction_variation});

                Logger::get("SM RawFakeFactor (tt)")->debug("tau_idx={}", tau_idx);
                Logger::get("SM RawFakeFactor (tt)")->debug("fake factors: QCD={}", qcd_ff);
                Logger::get("SM RawFakeFactor (tt)")->debug("fractions: QCD={}", qcd_frac);

                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.);
            } else if (tau_idx == 1) {
                qcd_ff = qcd_subleading->evaluate({pt_2, (float)njets, QCD_variation});
                qcd_frac = fractions_subleading->evaluate({"QCD", m_vis, (float)njets, fraction_variation});

                Logger::get("SM RawFakeFactor (tt)")->debug("tau_idx={}", tau_idx);
                Logger::get("SM RawFakeFactor (tt)")->debug("fake factors: QCD={}", qcd_ff);
                Logger::get("SM RawFakeFactor (tt)")->debug("fractions: QCD={}", qcd_frac);

                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.);
            }
        }

        Logger::get("SM RawFakeFactor (tt)")->debug("Event Fake Factor {}", ff);

        return ff;
    };

    auto df1 = df.Define(outputname, calc_fake_factor, {tau_pt_1, tau_pt_2, njets, m_vis});

    return df1;
}

ROOT::RDF::RNode
fakefactor_sm_tt(
    ROOT::RDF::RNode df, 
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname,
    const int &tau_idx,
    const std::string &tau_pt_1,
    const std::string &tau_pt_2,
    const std::string &njets,
    const std::string &m_vis,
    //
    const std::string &fraction_variation,
    const std::string &QCD_variation,
    //
    const std::string &QCD_DR_SR_correction_variation,
    //
    const std::string &QCD_non_closure_lep_pt_correction_variation,
    //
    const std::string &QCD_non_closure_m_vis_correction_variation,
    //
    const std::string &ff_file,
    const std::string &ff_corr_file
) {

    Logger::get("SM FakeFactor (tt)")->debug("Setting up functions for fake factor evaluation with correctionlib");
    
    Logger::get("SM FakeFactor (tt)")->debug("Fraction variations: fraction={}, QCD={})", fraction_variation, QCD_variation);
    Logger::get("SM FakeFactor (tt)")->debug("QCD variations: DR_SR={}, leading_lep_pt={}, m_vis={}", QCD_DR_SR_correction_variation, QCD_non_closure_lep_pt_correction_variation, QCD_non_closure_m_vis_correction_variation);

    auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
    auto qcd_subleading = correctionManager.loadCorrection(ff_file, "QCD_subleading_fake_factors");

    auto qcd_tau_pt_closure = correctionManager.loadCorrection(ff_corr_file, "QCD_non_closure_subleading_lep_pt_correction");
    auto qcd_tau_pt_closure_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_non_closure_leading_lep_pt_correction");
    
    auto qcd_m_vis_closure = correctionManager.loadCorrection(ff_corr_file, "QCD_non_closure_m_vis_correction");
    auto qcd_m_vis_closure_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_non_closure_m_vis_correction");
    
    auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
    auto qcd_DR_SR_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_DR_SR_correction");

    auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");
    auto fractions_subleading = correctionManager.loadCorrection(ff_file, "process_fractions_subleading");

    auto calc_fake_factor = [
        tau_idx, 
        qcd, qcd_subleading, fractions, fractions_subleading,
        qcd_tau_pt_closure, qcd_tau_pt_closure_subleading,
        qcd_m_vis_closure, qcd_m_vis_closure_subleading,
        qcd_DR_SR, qcd_DR_SR_subleading,
        QCD_variation, fraction_variation,                     
        QCD_non_closure_lep_pt_correction_variation, 
        QCD_DR_SR_correction_variation, 
        QCD_non_closure_m_vis_correction_variation](
        const float &pt_1, const float &pt_2,
        const int &njets, const float &m_vis) {

        float ff = 0.0;

        float qcd_ff = 0.0;
        float qcd_frac = 0.0;
        float qcd_tau_pt_corr = 0.0;
        float qcd_m_vis_corr = 0.0;
        float qcd_DR_SR_corr = 0.0;

        if (pt_2 >= 0.) {

            Logger::get("SM FakeFactor (tt)")->debug("pt_tau_1={}, pt_tau_2={}, njets={}, m_vis={}", pt_1, pt_2, njets, m_vis);

            if (tau_idx == 0) {
                qcd_ff = qcd->evaluate({pt_1, (float)njets, QCD_variation});
                qcd_frac = fractions->evaluate({"QCD", m_vis, (float)njets, fraction_variation});

                Logger::get("SM RawFakeFactor (tt)")->debug("tau_idx={}", tau_idx);
                Logger::get("SM FakeFactor (tt)")->debug("fake factors: QCD={}", qcd_ff);
                Logger::get("SM FakeFactor (tt)")->debug("fractions: QCD={}", qcd_frac);

                qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, QCD_DR_SR_correction_variation});
                qcd_tau_pt_corr = qcd_tau_pt_closure->evaluate({pt_2, QCD_non_closure_lep_pt_correction_variation});
                qcd_m_vis_corr = qcd_m_vis_closure->evaluate({m_vis, QCD_non_closure_m_vis_correction_variation});

                Logger::get("SM FakeFactor (tt)")->debug("QCD: DR_SR={}, lep_pt={}, m_vis={}", qcd_DR_SR_corr, qcd_tau_pt_corr, qcd_m_vis_corr);
                
                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr, (float)0.);

            } else if (tau_idx == 1) {
                qcd_ff = qcd_subleading->evaluate({pt_2, (float)njets, QCD_variation});
                qcd_frac = fractions_subleading->evaluate({"QCD", m_vis, (float)njets, fraction_variation});
                
                Logger::get("SM RawFakeFactor (tt)")->debug("tau_idx={}", tau_idx);
                Logger::get("SM FakeFactor (tt)")->debug("fake factors: QCD={}", qcd_ff);
                Logger::get("SM FakeFactor (tt)")->debug("fractions: QCD={}", qcd_frac);

                qcd_tau_pt_corr = qcd_tau_pt_closure_subleading->evaluate({pt_1, QCD_non_closure_lep_pt_correction_variation});
                qcd_m_vis_corr = qcd_m_vis_closure_subleading->evaluate({m_vis, QCD_non_closure_m_vis_correction_variation});
                qcd_DR_SR_corr = qcd_DR_SR_subleading->evaluate({m_vis, QCD_DR_SR_correction_variation});

                Logger::get("SM FakeFactor (tt)")->debug("QCD: DR_SR={}, lep_pt={}, m_vis={}", qcd_DR_SR_corr, qcd_tau_pt_corr, qcd_m_vis_corr);

                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr, (float)0.);
            }
        }

        Logger::get("SM FakeFactor (tt)")->debug("Event Fake Factor {}", ff);
        
        return ff;
    };

    auto df1 = df.Define(outputname, calc_fake_factor, {tau_pt_1, tau_pt_2, njets, m_vis});
    
    return df1;
}

ROOT::RDF::RNode
fakefactor_sm_tt_split_info(
    ROOT::RDF::RNode df, 
    correctionManager::CorrectionManager &correctionManager,
    const std::vector<std::string> &outputname,
    const int &tau_idx,
    const std::string &tau_pt_1,
    const std::string &tau_pt_2,
    const std::string &njets,
    const std::string &m_vis,
    //
    const std::string &fraction_variation,
    const std::string &QCD_variation,
    //
    const std::string &QCD_DR_SR_correction_variation,
    //
    const std::string &QCD_non_closure_lep_pt_correction_variation,
    //
    const std::string &QCD_non_closure_m_vis_correction_variation,
    //
    const std::string &ff_file,
    const std::string &ff_corr_file
) {

    auto qcd = correctionManager.loadCorrection(ff_file, "QCD_fake_factors");
    auto qcd_subleading = correctionManager.loadCorrection(ff_file, "QCD_subleading_fake_factors");

    auto qcd_tau_pt_closure = correctionManager.loadCorrection(ff_corr_file, "QCD_non_closure_subleading_lep_pt_correction");
    auto qcd_tau_pt_closure_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_non_closure_leading_lep_pt_correction");

    auto qcd_m_vis_closure = correctionManager.loadCorrection(ff_corr_file, "QCD_non_closure_m_vis_correction");
    auto qcd_m_vis_closure_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_non_closure_m_vis_correction");

    auto qcd_DR_SR = correctionManager.loadCorrection(ff_corr_file, "QCD_DR_SR_correction");
    auto qcd_DR_SR_subleading = correctionManager.loadCorrection(ff_corr_file, "QCD_subleading_DR_SR_correction");

    auto fractions = correctionManager.loadCorrection(ff_file, "process_fractions");
    auto fractions_subleading = correctionManager.loadCorrection(ff_file, "process_fractions_subleading");

    auto calc_fake_factor = [
        tau_idx, 
        qcd, qcd_subleading, fractions, fractions_subleading,
        qcd_tau_pt_closure, qcd_tau_pt_closure_subleading,
        qcd_m_vis_closure, qcd_m_vis_closure_subleading,
        qcd_DR_SR, qcd_DR_SR_subleading,
        QCD_variation, fraction_variation,                     
        QCD_non_closure_lep_pt_correction_variation, 
        QCD_DR_SR_correction_variation, 
        QCD_non_closure_m_vis_correction_variation](
        const float &pt_1, const float &pt_2,
        const int &njets, const float &m_vis) {

        float ff = 0.0;

        float qcd_ff = 0.0;
        float qcd_frac = 0.0;
        float qcd_tau_pt_corr = 0.0;
        float qcd_m_vis_corr = 0.0;
        float qcd_DR_SR_corr = 0.0;

        if (pt_2 >= 0.) {
            if (tau_idx == 0) {
                qcd_ff = qcd->evaluate({pt_1, (float)njets, QCD_variation});
                qcd_frac = fractions->evaluate({"QCD", m_vis, (float)njets, fraction_variation});

                qcd_tau_pt_corr = qcd_tau_pt_closure->evaluate({pt_2, QCD_non_closure_lep_pt_correction_variation});
                qcd_m_vis_corr = qcd_m_vis_closure->evaluate({m_vis, QCD_non_closure_m_vis_correction_variation});
                qcd_DR_SR_corr = qcd_DR_SR->evaluate({m_vis, QCD_DR_SR_correction_variation});

                ff = std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr, (float)0.);

            } else if (tau_idx == 1) {
                qcd_ff = qcd_subleading->evaluate({pt_2, (float)njets, QCD_variation});
                qcd_frac = fractions_subleading->evaluate({"QCD", m_vis, (float)njets, fraction_variation});

                qcd_tau_pt_corr = qcd_tau_pt_closure_subleading->evaluate({pt_1, QCD_non_closure_lep_pt_correction_variation});
                qcd_m_vis_corr = qcd_m_vis_closure_subleading->evaluate({m_vis, QCD_non_closure_m_vis_correction_variation});
                qcd_DR_SR_corr = qcd_DR_SR_subleading->evaluate({m_vis, QCD_DR_SR_correction_variation});
            }
        }
        // raw_ff_split, ff_split, frac_split, correction_split
        std::vector<float> result = {
            std::max(qcd_ff, (float)0.),
            std::max(qcd_frac, (float)0.) * std::max(qcd_ff, (float)0.) * std::max(qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr, (float)0.),
            std::max(qcd_frac, (float)0.),
            std::max(qcd_tau_pt_corr * qcd_m_vis_corr * qcd_DR_SR_corr, (float)0.)};

        return result;
    };

    std::vector<std::string> strings = {
        "fakefactor_sm_tt_split_info",
        fraction_variation,
        QCD_variation,
        QCD_DR_SR_correction_variation,
        QCD_non_closure_lep_pt_correction_variation,
        QCD_non_closure_m_vis_correction_variation,
        ff_file,
        ff_corr_file};
    std::string shifted_collection_identifier =  fakefactors::joinAndReplace(strings, "_");

    auto df1 = df.Define(shifted_collection_identifier, calc_fake_factor, {tau_pt_1, tau_pt_2, njets, m_vis});
    auto df2 = basefunctions::UnrollVectorQuantity<float>(df1, shifted_collection_identifier, outputname);

    return df2;
}

} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_TAU_H */

