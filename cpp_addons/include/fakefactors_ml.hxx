#ifndef GUARD_FAKEFACTORS_ML_H
#define GUARD_FAKEFACTORS_ML_H

#include "ROOT/RDataFrame.hxx"
#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/utility/OnnxSessionManager.hxx"
#include <memory>
#include <onnxruntime_cxx_api.h>
#include <string>
#include <unordered_map>
#include <vector>

namespace fakefactors {
namespace ml {
    class FakeFactorsOnnxSessionManager {
      public:
        FakeFactorsOnnxSessionManager() {
            OrtLoggingLevel logging_level =
                ORT_LOGGING_LEVEL_WARNING; // ORT_LOGGING_LEVEL_VERBOSE

            env = Ort::Env(logging_level, "FakeFactorsML");
            session_options.SetInterOpNumThreads(1);
            session_options.SetIntraOpNumThreads(1);
            session_options.SetGraphOptimizationLevel(
                GraphOptimizationLevel::ORT_ENABLE_ALL);
        };

        Ort::Session *getSession(const std::string &modelPath) {
            if (sessions_map.count(modelPath) == 0) {
                sessions_map[modelPath] = std::make_unique<Ort::Session>(
                    env, modelPath.c_str(), session_options);
                Logger::get("FakeFactorsOnnxSessionManager")
                    ->info("Created session for model: {}", modelPath);
            } else {
                Logger::get("FakeFactorsOnnxSessionManager")
                    ->info("Session already exists for model: {}", modelPath);
            }
            return sessions_map[modelPath].get();
        };

      private:
        std::unordered_map<std::string, std::unique_ptr<Ort::Session>> sessions_map;
        Ort::Env env;
        Ort::SessionOptions session_options;
    };

    // Evaluates ML-based fake factors using ONNX for raw terms and correctionlib for
    // non-closure compound corrections. The first scalar input is a dedicated event
    // validity guard (pt_2_input), followed by pre-built vector inputs.
    ROOT::RDF::RNode fakefactor_lt(
        ROOT::RDF::RNode df,
        correctionManager::CorrectionManager &correctionManager,
        OnnxSessionManager &onnxSessionManager,  // for now using own onnxSessionManager until the changes are merged
        const std::vector<std::string> &outputnames,
        // dedicated event validity input
        const std::string &pt_2_input,
        // ---
        const std::string &model_ff_QCD_input,
        const std::string &model_ff_Wjets_input,
        const std::string &model_ff_ttbar_input,
        const std::string &model_fractions_input,
        const std::string &model_ff_QCD_DR_SR_correction_input,
        const std::string &model_ff_Wjets_DR_SR_correction_input,
        const std::string &model_non_closure_correction_input,    
        // ---
        const std::string &model_ff_QCD,
        const std::string &model_ff_QCD_Up,
        const std::string &model_ff_QCD_Down,
        const std::string &model_ff_QCD_StatUp,
        const std::string &model_ff_QCD_StatDown,
        const std::string &model_ff_QCD_NormalizationUp,
        const std::string &model_ff_QCD_NormalizationDown,
        const std::string &ff_QCD_variation,
        // ---
        const std::string &model_ff_Wjets,
        const std::string &model_ff_Wjets_Up,
        const std::string &model_ff_Wjets_Down,
        const std::string &model_ff_Wjets_StatUp,
        const std::string &model_ff_Wjets_StatDown,
        const std::string &model_ff_Wjets_NormalizationUp,
        const std::string &model_ff_Wjets_NormalizationDown,
        const std::string &ff_Wjets_variation,
        // ---
        const std::string &model_ff_ttbar,
        const std::string &model_ff_ttbar_Up,
        const std::string &model_ff_ttbar_Down,
        const std::string &model_ff_ttbar_StatUp,
        const std::string &model_ff_ttbar_StatDown,
        const std::string &model_ff_ttbar_NormalizationUp,
        const std::string &model_ff_ttbar_NormalizationDown,
        const std::string &ff_ttbar_variation,
        // ---
        const std::string &model_fractions,
        const std::string &model_fractions_QCD_Up,
        const std::string &model_fractions_QCD_Down,
        const std::string &model_fractions_Wjets_Up,
        const std::string &model_fractions_Wjets_Down,
        const std::string &model_fractions_ttbar_Up,
        const std::string &model_fractions_ttbar_Down,
        const std::string &model_fractions_QCD_StatUp,
        const std::string &model_fractions_QCD_StatDown,
        const std::string &model_fractions_Wjets_StatUp,
        const std::string &model_fractions_Wjets_StatDown,
        const std::string &model_fractions_ttbar_StatUp,
        const std::string &model_fractions_ttbar_StatDown,
        const std::string &ml_fractions_variation,
        // ---
        const std::string &model_DR_SR_correction_QCD,
        const std::string &model_DR_SR_correction_QCD_Up,
        const std::string &model_DR_SR_correction_QCD_Down,
        const std::string &model_DR_SR_correction_QCD_StatUp,
        const std::string &model_DR_SR_correction_QCD_StatDown,
        const std::string &model_DR_SR_correction_QCD_NormalizationUp,
        const std::string &model_DR_SR_correction_QCD_NormalizationDown,
        const std::string &QCD_DR_SR_correction_variation,
        // ---
        const std::string &model_DR_SR_correction_Wjets,
        const std::string &model_DR_SR_correction_Wjets_Up,
        const std::string &model_DR_SR_correction_Wjets_Down,
        const std::string &model_DR_SR_correction_Wjets_StatUp,
        const std::string &model_DR_SR_correction_Wjets_StatDown,
        const std::string &model_DR_SR_correction_Wjets_NormalizationUp,
        const std::string &model_DR_SR_correction_Wjets_NormalizationDown,
        const std::string &Wjets_DR_SR_correction_variation,
        // ---
        const std::string &QCD_non_closure_correction,
        const std::string &Wjets_non_closure_correction,
        const std::string &ttbar_non_closure_correction,
        // ---
        const std::string &corr_file,
        const bool split_info
    );

} // namespace ml
} // namespace fakefactors

#endif /* GUARD_FAKEFACTORS_ML_H */
