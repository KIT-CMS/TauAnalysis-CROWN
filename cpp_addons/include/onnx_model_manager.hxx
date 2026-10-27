#ifndef GUARD_ONNX_MODEL_MANAGER_H
#define GUARD_ONNX_MODEL_MANAGER_H

#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/utility/OnnxSessionManager.hxx"
#include "fakefactors_ml.hxx"

#include <memory>
#include <mutex>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace fakefactors {
namespace ml {

class OnnxPreparedModelManager {
  public:
    struct PreparedOnnxModel {
        Ort::Session *session;
        Ort::AllocatorWithDefaultOptions allocator;
        std::vector<int64_t> input_node_dims;
        std::vector<int64_t> output_node_dims;
        int num_input_nodes;
        int num_output_nodes;
        size_t input_tensor_size;
        size_t output_tensor_size;
        std::string input_node_name;
        std::string output_node_name;
    };

    static std::shared_ptr<const PreparedOnnxModel>
    getPreparedModel(FakeFactorsOnnxSessionManager &onnxSessionManager,
                     const std::string &model_file_path) {
        std::lock_guard<std::mutex> lock(cache_mutex_);

        auto &manager_cache = cache_[&onnxSessionManager];
        auto it = manager_cache.find(model_file_path);
        if (it != manager_cache.end()) {
            Logger::get("OnnxPreparedModelManager")
                ->info("Using cached prepared model: {}", model_file_path);
            return it->second;
        }

        auto prepared = std::make_shared<PreparedOnnxModel>();
        prepared->session = onnxSessionManager.getSession(model_file_path);
        onnxhelper::prepare_model(prepared->session, prepared->allocator,
                                  prepared->input_node_dims,
                                  prepared->output_node_dims,
                                  prepared->num_input_nodes,
                                  prepared->num_output_nodes);

        prepared->input_tensor_size = tensorSizeOrThrow(prepared->input_node_dims, model_file_path, "input");
        prepared->output_tensor_size = tensorSizeOrThrow(prepared->output_node_dims, model_file_path, "output");

        auto input_name = prepared->session->GetInputNameAllocated(0, prepared->allocator);
        auto output_name = prepared->session->GetOutputNameAllocated(0, prepared->allocator);
        prepared->input_node_name = input_name.get();
        prepared->output_node_name = output_name.get();

        manager_cache[model_file_path] = prepared;
        Logger::get("OnnxPreparedModelManager")
            ->info("Prepared and cached model: {} (in_size={}, out_size={})",
                   model_file_path, prepared->input_tensor_size,
                   prepared->output_tensor_size);
        return prepared;
    }

    static void preloadModels(FakeFactorsOnnxSessionManager &onnxSessionManager,
                              const std::vector<std::string> &model_paths) {
        std::unordered_set<std::string> unique_paths;
        unique_paths.reserve(model_paths.size());

        for (const auto &path : model_paths) {
            if (path.empty()) {
                continue;
            }
            if (!unique_paths.insert(path).second) {
                continue;
            }
            (void)getPreparedModel(onnxSessionManager, path);
        }
    }

  private:
    static size_t tensorSizeOrThrow(const std::vector<int64_t> &dims,
                                    const std::string &model_path,
                                    const std::string &kind) {
        size_t size = 1;
        for (const auto dim : dims) {
            if (dim <= 0) {
                throw std::runtime_error("Unsupported non-static " + kind +
                                         " tensor shape for model " + model_path);
            }
            size *= static_cast<size_t>(dim);
        }
        return size;
    }

    static inline std::mutex cache_mutex_{};
    static inline std::unordered_map<
        FakeFactorsOnnxSessionManager *,
        std::unordered_map<std::string, std::shared_ptr<const PreparedOnnxModel>>>
        cache_{};
};

} // namespace ml
} // namespace fakefactors

#endif /* GUARD_ONNX_MODEL_MANAGER_H */
