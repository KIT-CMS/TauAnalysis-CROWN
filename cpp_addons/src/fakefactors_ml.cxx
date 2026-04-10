#ifndef GUARDFAKEFACTORS_ML_CXX
#define GUARDFAKEFACTORS_ML_CXX

#include "../include/fakefactors_ml.hxx"
#include "../include/onnx_model_manager.hxx"
#include "../include/fakefactors.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/event.hxx"
#include "correction.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <cstring>
#include <initializer_list>
#include <memory>
#include <stdexcept>
#include <unordered_map>

namespace fakefactors {
namespace ml {

    struct CachedTensorBindings {
        bool initialized = false;
        const float *input_ptr = nullptr;
        float *output_ptr = nullptr;
        std::array<Ort::Value, 1> input_tensors;
        std::array<Ort::Value, 1> output_tensors;
        std::array<const char *, 1> input_names;
        std::array<const char *, 1> output_names;
    };

    struct CachedInferenceResult {
        bool initialized = false;
        std::vector<float> input_snapshot;
        std::vector<float> output_snapshot;
    };

    void run_onnx_model(const OnnxPreparedModelManager::PreparedOnnxModel &model,
                        const float *input_data,
                        const size_t input_size,
                        float *output_data,
                        const size_t output_size) {
        if (input_size != model.input_tensor_size) {
            throw std::runtime_error(
                "ONNX input size mismatch: got " + std::to_string(input_size) +
                ", expected " + std::to_string(model.input_tensor_size));
        }

        if (output_size != model.output_tensor_size) {
            throw std::runtime_error(
                "ONNX output size mismatch: got " + std::to_string(output_size) +
                ", expected " + std::to_string(model.output_tensor_size));
        }

        static const Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(
            OrtAllocatorType::OrtArenaAllocator, OrtMemType::OrtMemTypeDefault);

        static thread_local std::unordered_map<const OnnxPreparedModelManager::PreparedOnnxModel *, CachedTensorBindings>
            cached_bindings;
        auto &bindings = cached_bindings[&model];

        static thread_local std::unordered_map<const OnnxPreparedModelManager::PreparedOnnxModel *, CachedInferenceResult>
            cached_inference;
        auto &inference = cached_inference[&model];

        if (inference.initialized &&
            inference.input_snapshot.size() == input_size &&
            inference.output_snapshot.size() == output_size &&
            std::memcmp(inference.input_snapshot.data(), input_data,
                        input_size * sizeof(float)) == 0) {
            std::memcpy(output_data, inference.output_snapshot.data(),
                        output_size * sizeof(float));
            return;
        }

        if (!bindings.initialized ||
            bindings.input_ptr != input_data ||
            bindings.output_ptr != output_data) {
            bindings.input_ptr = input_data;
            bindings.output_ptr = output_data;
            bindings.input_names = {model.input_node_name.c_str()};
            bindings.output_names = {model.output_node_name.c_str()};
            bindings.input_tensors = {Ort::Value::CreateTensor<float>(
                memory_info,
                const_cast<float *>(input_data),
                input_size,
                model.input_node_dims.data(),
                model.input_node_dims.size())};
            bindings.output_tensors = {Ort::Value::CreateTensor<float>(
                memory_info,
                output_data,
                output_size,
                model.output_node_dims.data(),
                model.output_node_dims.size())};
            bindings.initialized = true;
        }

        model.session->Run(Ort::RunOptions{nullptr},
                           bindings.input_names.data(),
                           bindings.input_tensors.data(),
                           bindings.input_tensors.size(),
                           bindings.output_names.data(),
                           bindings.output_tensors.data(),
                           bindings.output_tensors.size());

        inference.input_snapshot.assign(input_data, input_data + input_size);
        inference.output_snapshot.assign(output_data, output_data + output_size);
        inference.initialized = true;
    }

    const std::string &select_model_path_or_throw(
        const std::string &variation,
        std::initializer_list<std::pair<const char *, const std::string *>> candidates,
        const std::string &variation_key) {

        for (const auto &entry : candidates) {
            if (variation == entry.first) {
                return *entry.second;
            }
        }

        throw std::runtime_error("Unknown variation '" + variation + "' for " + variation_key);
    }

    struct ModelEvaluationResult {
        float qcd_ff;
        float wjets_ff;
        float ttbar_ff;
        float qcd_frac;
        float wjets_frac;
        float ttbar_frac;
        float qcd_DR_SR_corr;
        float wjets_DR_SR_corr;
        float ttbar_DR_SR_corr;
        float qcd_nc_corr;
        float wjets_nc_corr;
        float ttbar_nc_corr;
        float qcd_correction;
        float wjets_correction;
        float ttbar_correction;
    };

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
        const std::string &ff_QCD_variation,
        // ---
        const std::string &model_ff_Wjets,
        const std::string &model_ff_Wjets_Up,
        const std::string &model_ff_Wjets_Down,
        const std::string &model_ff_Wjets_StatUp,
        const std::string &model_ff_Wjets_StatDown,
        const std::string &ff_Wjets_variation,
        // ---
        const std::string &model_ff_ttbar,
        const std::string &model_ff_ttbar_Up,
        const std::string &model_ff_ttbar_Down,
        const std::string &model_ff_ttbar_StatUp,
        const std::string &model_ff_ttbar_StatDown,
        const std::string &ff_ttbar_variation,
        // ---
        const std::string &model_fractions,
        const std::string &model_fractions_QCD_Up,
        const std::string &model_fractions_QCD_Down,
        const std::string &model_fractions_Wjets_Up,
        const std::string &model_fractions_Wjets_Down,
        const std::string &model_fractions_ttbar_Up,
        const std::string &model_fractions_ttbar_Down,
        const std::string &model_fractions_StatUp,
        const std::string &model_fractions_StatDown,
        const std::string &ml_fractions_variation,
        // ---
        const std::string &model_DR_SR_correction_QCD,
        const std::string &model_DR_SR_correction_QCD_Up,
        const std::string &model_DR_SR_correction_QCD_Down,
        const std::string &model_DR_SR_correction_QCD_StatUp,
        const std::string &model_DR_SR_correction_QCD_StatDown,
        const std::string &QCD_DR_SR_correction_variation,
        // ---
        const std::string &model_DR_SR_correction_Wjets,
        const std::string &model_DR_SR_correction_Wjets_Up,
        const std::string &model_DR_SR_correction_Wjets_Down,
        const std::string &model_DR_SR_correction_Wjets_StatUp,
        const std::string &model_DR_SR_correction_Wjets_StatDown,
        const std::string &Wjets_DR_SR_correction_variation,
        // ---
        const std::string &QCD_non_closure_correction,
        const std::string &Wjets_non_closure_correction,
        const std::string &ttbar_non_closure_correction,
        // ---
        const std::string &corr_file,
        const bool split_info
    ) {
        Logger::get("FakeFactorsML")->debug("Setting up ML-based fake factor evaluation");
        (void)onnxSessionManager;

        static FakeFactorsOnnxSessionManager fakefactors_onnx_session_manager;

        const std::string &selected_model_ff_QCD = select_model_path_or_throw(
            ff_QCD_variation,
            {
                {"nominal", &model_ff_QCD},
                {"Up", &model_ff_QCD_Up},
                {"Down", &model_ff_QCD_Down},
                {"StatUp", &model_ff_QCD_StatUp},
                {"StatDown", &model_ff_QCD_StatDown},
            },
            "ff_QCD_variation");

        const std::string &selected_model_ff_Wjets = select_model_path_or_throw(
            ff_Wjets_variation,
            {
                {"nominal", &model_ff_Wjets},
                {"Up", &model_ff_Wjets_Up},
                {"Down", &model_ff_Wjets_Down},
                {"StatUp", &model_ff_Wjets_StatUp},
                {"StatDown", &model_ff_Wjets_StatDown},
            },
            "ff_Wjets_variation");

        const std::string &selected_model_ff_ttbar = select_model_path_or_throw(
            ff_ttbar_variation,
            {
                {"nominal", &model_ff_ttbar},
                {"Up", &model_ff_ttbar_Up},
                {"Down", &model_ff_ttbar_Down},
                {"StatUp", &model_ff_ttbar_StatUp},
                {"StatDown", &model_ff_ttbar_StatDown},
            },
            "ff_ttbar_variation");

        const std::string &selected_model_fractions = select_model_path_or_throw(
            ml_fractions_variation,
            {
                {"nominal", &model_fractions},
                {"QCD_Up", &model_fractions_QCD_Up},
                {"QCD_Down", &model_fractions_QCD_Down},
                {"Wjets_Up", &model_fractions_Wjets_Up},
                {"Wjets_Down", &model_fractions_Wjets_Down},
                {"ttbar_Up", &model_fractions_ttbar_Up},
                {"ttbar_Down", &model_fractions_ttbar_Down},
                {"StatUp", &model_fractions_StatUp},
                {"StatDown", &model_fractions_StatDown},
            },
            "ml_fractions_variation");

        const std::string &selected_model_DR_SR_correction_QCD = select_model_path_or_throw(
            QCD_DR_SR_correction_variation,
            {
                {"nominal", &model_DR_SR_correction_QCD},
                {"Up", &model_DR_SR_correction_QCD_Up},
                {"Down", &model_DR_SR_correction_QCD_Down},
                {"StatUp", &model_DR_SR_correction_QCD_StatUp},
                {"StatDown", &model_DR_SR_correction_QCD_StatDown},
            },
            "QCD_DR_SR_correction_variation");

        const std::string &selected_model_DR_SR_correction_Wjets = select_model_path_or_throw(
            Wjets_DR_SR_correction_variation,
            {
                {"nominal", &model_DR_SR_correction_Wjets},
                {"Up", &model_DR_SR_correction_Wjets_Up},
                {"Down", &model_DR_SR_correction_Wjets_Down},
                {"StatUp", &model_DR_SR_correction_Wjets_StatUp},
                {"StatDown", &model_DR_SR_correction_Wjets_StatDown},
            },
            "Wjets_DR_SR_correction_variation");

        OnnxPreparedModelManager::preloadModels(
            fakefactors_onnx_session_manager,
            {
                model_ff_QCD,
                model_ff_QCD_Up,
                model_ff_QCD_Down,
                model_ff_QCD_StatUp,
                model_ff_QCD_StatDown,
                model_ff_Wjets,
                model_ff_Wjets_Up,
                model_ff_Wjets_Down,
                model_ff_Wjets_StatUp,
                model_ff_Wjets_StatDown,
                model_ff_ttbar,
                model_ff_ttbar_Up,
                model_ff_ttbar_Down,
                model_ff_ttbar_StatUp,
                model_ff_ttbar_StatDown,
                model_fractions,
                model_fractions_QCD_Up,
                model_fractions_QCD_Down,
                model_fractions_Wjets_Up,
                model_fractions_Wjets_Down,
                model_fractions_ttbar_Up,
                model_fractions_ttbar_Down,
                model_fractions_StatUp,
                model_fractions_StatDown,
                model_DR_SR_correction_QCD,
                model_DR_SR_correction_QCD_Up,
                model_DR_SR_correction_QCD_Down,
                model_DR_SR_correction_QCD_StatUp,
                model_DR_SR_correction_QCD_StatDown,
                model_DR_SR_correction_Wjets,
                model_DR_SR_correction_Wjets_Up,
                model_DR_SR_correction_Wjets_Down,
                model_DR_SR_correction_Wjets_StatUp,
                model_DR_SR_correction_Wjets_StatDown,
            });

        auto qcd_nc_comp = correctionManager.loadCompoundCorrection(corr_file, "QCD_compound_correction");
        auto wjets_nc_comp = correctionManager.loadCompoundCorrection(corr_file, "Wjets_compound_correction");
        auto ttbar_nc_comp = correctionManager.loadCompoundCorrection(corr_file, "ttbar_compound_correction");

        auto qcd_handler = std::make_shared<fakefactors::sm::NonClosureHandler>("QCD", corr_file, qcd_nc_comp);
        auto wjets_handler = std::make_shared<fakefactors::sm::NonClosureHandler>("Wjets", corr_file, wjets_nc_comp);
        auto ttbar_handler = std::make_shared<fakefactors::sm::NonClosureHandler>("ttbar", corr_file, ttbar_nc_comp);

        auto model_QCD_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_ff_QCD);
        auto model_Wjets_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_ff_Wjets);
        auto model_ttbar_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_ff_ttbar);
        auto model_fractions_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_fractions);
        auto model_DR_QCD_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_DR_SR_correction_QCD);
        auto model_DR_Wjets_prepared = OnnxPreparedModelManager::getPreparedModel(fakefactors_onnx_session_manager, selected_model_DR_SR_correction_Wjets);

        auto _models_evaluator =[
                    model_QCD_prepared, model_Wjets_prepared, model_ttbar_prepared, model_fractions_prepared,
                    model_DR_QCD_prepared, model_DR_Wjets_prepared,
                    qcd_handler, wjets_handler, ttbar_handler,
                    QCD_non_closure_correction, Wjets_non_closure_correction, ttbar_non_closure_correction
                    ](const std::vector<float> &qcd_inputs,
                       const std::vector<float> &wjets_inputs,
                       const std::vector<float> &ttbar_inputs,
                       const std::vector<float> &fractions_inputs,
                       const std::vector<float> &dr_qcd_inputs,
                       const std::vector<float> &dr_wjets_inputs,
                       const std::vector<float> &nc_inputs) -> ModelEvaluationResult {

            ModelEvaluationResult result{};
            result.ttbar_DR_SR_corr = 1.0f;

            static thread_local std::array<float, 1> model_output_scalar{{0.0f}};
            static thread_local std::array<float, 3> model_output_fractions{{0.0f, 0.0f, 0.0f}};

            run_onnx_model(*model_QCD_prepared,
                           qcd_inputs.data(),
                           qcd_inputs.size(),
                           model_output_scalar.data(),
                           model_output_scalar.size());
            result.qcd_ff = model_output_scalar[0];

            run_onnx_model(*model_Wjets_prepared,
                           wjets_inputs.data(),
                           wjets_inputs.size(),
                           model_output_scalar.data(),
                           model_output_scalar.size());
            result.wjets_ff = model_output_scalar[0];

            run_onnx_model(*model_ttbar_prepared,
                           ttbar_inputs.data(),
                           ttbar_inputs.size(),
                           model_output_scalar.data(),
                           model_output_scalar.size());
            result.ttbar_ff = model_output_scalar[0];

            run_onnx_model(*model_fractions_prepared,
                           fractions_inputs.data(),
                           fractions_inputs.size(),
                           model_output_fractions.data(),
                           model_output_fractions.size());
            result.qcd_frac = model_output_fractions[0];
            result.wjets_frac = model_output_fractions[1];
            result.ttbar_frac = model_output_fractions[2];

            run_onnx_model(*model_DR_QCD_prepared,
                           dr_qcd_inputs.data(),
                           dr_qcd_inputs.size(),
                           model_output_scalar.data(),
                           model_output_scalar.size());
            result.qcd_DR_SR_corr = model_output_scalar[0];

            run_onnx_model(*model_DR_Wjets_prepared,
                           dr_wjets_inputs.data(),
                           dr_wjets_inputs.size(),
                           model_output_scalar.data(),
                           model_output_scalar.size());
            result.wjets_DR_SR_corr = model_output_scalar[0];
            result.ttbar_DR_SR_corr = 1.0f;

            std::vector<correction::Variable::Type> nc_args(nc_inputs.begin(), nc_inputs.end());

            result.qcd_nc_corr = qcd_handler->evaluate(QCD_non_closure_correction, nc_args);
            result.wjets_nc_corr = wjets_handler->evaluate(Wjets_non_closure_correction, nc_args);
            result.ttbar_nc_corr = ttbar_handler->evaluate(ttbar_non_closure_correction, nc_args);

            result.qcd_correction = std::max(result.qcd_DR_SR_corr, 0.0f) * std::max(result.qcd_nc_corr, 0.0f);
            result.wjets_correction = std::max(result.wjets_DR_SR_corr, 0.0f) * std::max(result.wjets_nc_corr, 0.0f);
            result.ttbar_correction = std::max(result.ttbar_nc_corr, 0.0f);

            return result;
        };

        if (split_info) {
            auto unroll_prebuilt_evaluator = [_models_evaluator](
                const float &pt_2,
                const std::vector<float> &qcd_inputs,
                const std::vector<float> &wjets_inputs,
                const std::vector<float> &ttbar_inputs,
                const std::vector<float> &fractions_inputs,
                const std::vector<float> &dr_qcd_inputs,
                const std::vector<float> &dr_wjets_inputs,
                const std::vector<float> &nc_inputs) -> std::vector<float> {
                if (pt_2 < 0.0f) {
                    return std::vector<float>{
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f,
                        0.0f
                    };
                }

                const auto evaluated = _models_evaluator(
                    qcd_inputs,
                    wjets_inputs,
                    ttbar_inputs,
                    fractions_inputs,
                    dr_qcd_inputs,
                    dr_wjets_inputs,
                    nc_inputs);

                const float qcd_ff_pos = std::max(evaluated.qcd_ff, 0.0f);
                const float wjets_ff_pos = std::max(evaluated.wjets_ff, 0.0f);
                const float ttbar_ff_pos = std::max(evaluated.ttbar_ff, 0.0f);
                const float qcd_frac_pos = std::max(evaluated.qcd_frac, 0.0f);
                const float wjets_frac_pos = std::max(evaluated.wjets_frac, 0.0f);
                const float ttbar_frac_pos = std::max(evaluated.ttbar_frac, 0.0f);
                const float qcd_DR_SR_corr_pos = std::max(evaluated.qcd_DR_SR_corr, 0.0f);
                const float wjets_DR_SR_corr_pos = std::max(evaluated.wjets_DR_SR_corr, 0.0f);
                const float ttbar_DR_SR_corr_pos = std::max(evaluated.ttbar_DR_SR_corr, 0.0f);
                const float qcd_nc_corr_pos = std::max(evaluated.qcd_nc_corr, 0.0f);
                const float wjets_nc_corr_pos = std::max(evaluated.wjets_nc_corr, 0.0f);
                const float ttbar_nc_corr_pos = std::max(evaluated.ttbar_nc_corr, 0.0f);
                const float qcd_correction_pos = std::max(evaluated.qcd_correction, 0.0f);
                const float wjets_correction_pos = std::max(evaluated.wjets_correction, 0.0f);
                const float ttbar_correction_pos = std::max(evaluated.ttbar_correction, 0.0f);
                const float ff_total =
                    qcd_frac_pos * qcd_ff_pos * qcd_correction_pos +
                    wjets_frac_pos * wjets_ff_pos * wjets_correction_pos +
                    ttbar_frac_pos * ttbar_ff_pos * ttbar_correction_pos;

                return std::vector<float>{
                    ff_total,
                    qcd_ff_pos,
                    wjets_ff_pos,
                    ttbar_ff_pos,
                    qcd_frac_pos,
                    wjets_frac_pos,
                    ttbar_frac_pos,
                    qcd_DR_SR_corr_pos,
                    wjets_DR_SR_corr_pos,
                    ttbar_DR_SR_corr_pos,
                    qcd_nc_corr_pos,
                    wjets_nc_corr_pos,
                    ttbar_nc_corr_pos,
                    qcd_correction_pos,
                    wjets_correction_pos,
                    ttbar_correction_pos,
                    qcd_frac_pos * qcd_ff_pos * qcd_correction_pos,
                    wjets_frac_pos * wjets_ff_pos * wjets_correction_pos,
                    ttbar_frac_pos * ttbar_ff_pos * ttbar_correction_pos
                };
            };

            std::vector<std::string> strings = {
                "fakefactor_ml_lt_split_info",
                outputnames[0],
                ff_QCD_variation,
                ff_Wjets_variation,
                ff_ttbar_variation,
                ml_fractions_variation,
                QCD_DR_SR_correction_variation,
                Wjets_DR_SR_correction_variation,
                QCD_non_closure_correction,
                Wjets_non_closure_correction,
                ttbar_non_closure_correction,
                selected_model_ff_QCD,
                selected_model_ff_Wjets,
                selected_model_ff_ttbar,
                selected_model_fractions,
                selected_model_DR_SR_correction_QCD,
                selected_model_DR_SR_correction_Wjets,
                corr_file
            };
            const std::string shifted_collection_identifier = fakefactors::joinAndReplace(strings, "_");

            auto df1 = df.Define(
                shifted_collection_identifier,
                unroll_prebuilt_evaluator,
                {
                    pt_2_input,
                    model_ff_QCD_input,
                    model_ff_Wjets_input,
                    model_ff_ttbar_input,
                    model_fractions_input,
                    model_ff_QCD_DR_SR_correction_input,
                    model_ff_Wjets_DR_SR_correction_input,
                    model_non_closure_correction_input,
                });
            return event::quantity::Unroll<float>(df1, outputnames, shifted_collection_identifier);
        }

        auto _evaluator = [_models_evaluator](
            const float &pt_2,
            const std::vector<float> &qcd_inputs,
            const std::vector<float> &wjets_inputs,
            const std::vector<float> &ttbar_inputs,
            const std::vector<float> &fractions_inputs,
            const std::vector<float> &dr_qcd_inputs,
            const std::vector<float> &dr_wjets_inputs,
            const std::vector<float> &nc_inputs) -> float {
            if (pt_2 < 0.0f) {
                return 0.0f;
            }

            const auto evaluated = _models_evaluator(
                qcd_inputs,
                wjets_inputs,
                ttbar_inputs,
                fractions_inputs,
                dr_qcd_inputs,
                dr_wjets_inputs,
                nc_inputs);

            return std::max(evaluated.qcd_frac, 0.0f) * std::max(evaluated.qcd_ff, 0.0f) * std::max(evaluated.qcd_correction, 0.0f) +
                   std::max(evaluated.wjets_frac, 0.0f) * std::max(evaluated.wjets_ff, 0.0f) * std::max(evaluated.wjets_correction, 0.0f) +
                   std::max(evaluated.ttbar_frac, 0.0f) * std::max(evaluated.ttbar_ff, 0.0f) * std::max(evaluated.ttbar_correction, 0.0f);
        };

        return df.Define(
            outputnames[0],
            _evaluator,
            {
                pt_2_input,
                model_ff_QCD_input,
                model_ff_Wjets_input,
                model_ff_ttbar_input,
                model_fractions_input,
                model_ff_QCD_DR_SR_correction_input,
                model_ff_Wjets_DR_SR_correction_input,
                model_non_closure_correction_input,
            });
    }

} // namespace ml
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_ML_CXX */
