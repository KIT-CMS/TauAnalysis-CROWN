#ifndef GUARDNORMALIZATION_H
#define GUARDNORMALIZATION_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "ROOT/RDataFrame.hxx"
#include <string>

namespace normalization {

// Defines three per-file constant columns -- crossSectionPerEventWeight
// (xsec), numberGeneratedEventsWeight (1/nevents) and
// negative_events_fraction (generator_weight) -- by looking up this file's
// sample nick in a nick -> {xsec, nevents, generator_weight} JSON table.
// Names/semantics match the legacy Python xsec/build_friend_tree.py friend
// this replaces, for drop-in compatibility with existing downstream readers
// (TauFakeFactors' gen_weight(), TauKITFlow's process_selection.py).
// The table is generated at code-gen time from
// sample_database/nanoAOD_vXX/datasets.json, filtered to the (sample_type,
// era) this friend build is for -- see normalization.py/weights_friends.py.
// The nick itself is parsed from the input file's path at runtime via
// ROOT::RDF::RSampleInfo (path convention: .../{era}/{nick}/{scope}/
// {nick}_{N}.root, same as KingMaker's CROWNRun output layout), so one
// compiled executable correctly normalizes every nick of its sample_type.
// An unknown nick throws rather than silently defaulting.
ROOT::RDF::RNode
SampleNormalization(ROOT::RDF::RNode df,
                     correctionManager::CorrectionManager &correctionManager,
                     const std::string &xsec_output,
                     const std::string &ngen_weight_output,
                     const std::string &genweight_output,
                     const std::string &norm_table_path);

} // namespace normalization
#endif
