#ifndef GUARDWEIGHTS_CXX
#define GUARDWEIGHTS_CXX

#include "../include/weights.hxx"
#include "ROOT/RDataFrame.hxx"
#include <string>

namespace weights {

ROOT::RDF::RNode Gate(ROOT::RDF::RNode df, const std::string &outputname,
                      const std::string &cond_col, const std::string &value_col) {
    return df.Define(
        outputname,
        [](const bool &cond, const double &value) { return cond ? value : 1.0; },
        {cond_col, value_col});
}

ROOT::RDF::RNode NormalizedGenWeightSign(ROOT::RDF::RNode df,
                                         const std::string &outputname,
                                         const std::string &genweight_col,
                                         const std::string &negative_fraction_col) {
    return df.Define(
        outputname,
        [](const float &genWeight, const double &negative_fraction) {
            double sign = (genWeight < 0) ? -1.0 : 1.0;
            return sign / negative_fraction;
        },
        {genweight_col, negative_fraction_col});
}

} // namespace weights
#endif
