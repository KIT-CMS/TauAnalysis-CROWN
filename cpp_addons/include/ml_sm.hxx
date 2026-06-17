#ifndef GUARDML_SM_H
#define GUARDML_SM_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/OnnxSessionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/ml.hxx"
#include "../../../../include/utility/utility.hxx"
#include <cstddef>

namespace ml_sm {
    template <std::size_t nParameters>
    inline ROOT::RDF::RNode Extracted_NN_Output(
        ROOT::RDF::RNode df, OnnxSessionManager &onnxSessionManager,
        const std::string &outputname_vector, const std::string &outputname_class,
        const std::string &outputname_max_value,
        const std::string &model_file_path,
        const std::vector<std::string> &input_vec) {

        auto df1 = ml::GenericOnnxEvaluator<nParameters>(
            df,
            onnxSessionManager,
            outputname_vector,
            model_file_path,
            input_vec);

        Logger::get("Extracted_NN_Output")
            ->debug("Successfully created evaluation function of the ONNX model: {}", model_file_path);

        auto df2 = df1.Define(
            outputname_class,
            [](const std::vector<float> &prediction) {
                int max_idx = std::distance(
                    prediction.begin(),
                    std::max_element(prediction.begin(), prediction.end()));
                Logger::get("Extracted_NN_Output")
                    ->debug("Max idx: {}", max_idx);
                return max_idx;
            },
            {outputname_vector});
        
        Logger::get("Extracted_NN_Output")
            ->debug("Successfully created extraction function of the predicted class.");

        auto df3 = df2.Define(
            outputname_max_value,
            [](const std::vector<float> &prediction, const int &max_idx) {
                float max_value = prediction[max_idx];
                Logger::get("Extracted_NN_Output")
                    ->debug("Max value: {}", max_value);
                return max_value;
            },
            {outputname_vector, outputname_class});
        
        Logger::get("Extracted_NN_Output")
            ->debug("Successfully created extraction function of the maximum predicted value.");

        return df3;
    };

    inline ROOT::RDF::RNode
    EventParity(
        ROOT::RDF::RNode df,
        const std::string &outputname,
        const std::string &inputname) {

        auto col_names = df.GetColumnNames();  // Skip if column already exists
        if (std::find(col_names.begin(), col_names.end(), outputname) != col_names.end()) {
            return df;
        }

        return df.Define(
            outputname,
                [](unsigned long long event) {
                    auto result = static_cast<float>(event % 2);
                    Logger::get("EventParity")
                        ->debug("Casting {} to {}", event, result);
                    return result;
                },
            {inputname});
    }
}
#endif /* GUARDML_SM_H */
