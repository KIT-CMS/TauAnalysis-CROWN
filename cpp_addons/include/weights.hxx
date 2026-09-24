#ifndef GUARDWEIGHTS_H
#define GUARDWEIGHTS_H

#include "ROOT/RDataFrame.hxx"
#include <string>

namespace weights {

// Returns value_col if cond_col is true, else 1.0 -- the "SF only applies to a genuine
// object, no-op otherwise" pattern used throughout the tau vsJet/vsEle/vsMu SFs (e.g.
// (gen_match_2==5)*SF + (gen_match_2!=5)*1 in TauKITFlow's process_selection.py /
// TauFakeFactors' preselection configs). All concrete uses in this analysis produce
// double-typed SFs (verified against the correctionlib evaluate() passthrough in
// src/taus.cxx, src/muons.cxx, src/electrons.cxx), so value_col's type is fixed to
// double rather than templated -- widen if a float-typed gated value shows up.
ROOT::RDF::RNode Gate(ROOT::RDF::RNode df, const std::string &outputname,
                      const std::string &cond_col, const std::string &value_col);

// sign(genWeight) / negative_events_fraction -- the generator-weight sign/normalization
// term used by both TauFakeFactors' gen_weight() and TauKITFlow's
// MC_base_process_selection. genweight_col is expected float (NanoAOD's genWeight is
// always Float_t); negative_fraction_col is expected double (matches
// normalization::SampleNormalization's negative_events_fraction output).
ROOT::RDF::RNode NormalizedGenWeightSign(ROOT::RDF::RNode df,
                                         const std::string &outputname,
                                         const std::string &genweight_col,
                                         const std::string &negative_fraction_col);

} // namespace weights
#endif
