#ifndef GUARDWEIGHTS_H
#define GUARDWEIGHTS_H

#include "ROOT/RDataFrame.hxx"
#include <string>

namespace weights {

// value_col if cond_col else 1.0 (SF gating). Fixed to double.
ROOT::RDF::RNode Gate(ROOT::RDF::RNode df, const std::string &outputname,
                      const std::string &cond_col, const std::string &value_col);

// sign(genWeight) / negative_events_fraction.
ROOT::RDF::RNode NormalizedGenWeightSign(ROOT::RDF::RNode df,
                                         const std::string &outputname,
                                         const std::string &genweight_col,
                                         const std::string &negative_fraction_col);

// true_col if cond_col else false_col. Fixed to double.
ROOT::RDF::RNode Select(ROOT::RDF::RNode df, const std::string &outputname,
                        const std::string &cond_col, const std::string &true_col,
                        const std::string &false_col);

} // namespace weights
#endif
