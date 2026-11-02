#ifndef GUARD_NORMALIZATION_H
#define GUARD_NORMALIZATION_H

namespace event::normalization {

ROOT::RDF::RNode SampleNormalization(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &xsec_output, const std::string &ngen_weight_output,
    const std::string &genweight_output, const std::string &split_weight_output,
    const std::string &norm_table_path,
    const double &default_split_fraction = 1.0);
}
#endif /* GUARD_NORMALIZATION_H */
