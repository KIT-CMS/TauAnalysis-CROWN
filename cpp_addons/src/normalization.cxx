#ifndef GUARDNORMALIZATION_CXX
#define GUARDNORMALIZATION_CXX

#include "../include/normalization.hxx"
#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <string>
#include <vector>

namespace normalization {

namespace {

// sample_id is RSampleInfo::AsString(), "<filename>/<treename>" for a
// TTree/TChain source. Path convention: .../{era}/{nick}/{scope}/
// {nick}_{N}.root -- the nick is the third-from-last path segment.
std::string ParseNickFromPath(const std::string &sample_id) {
    auto tree_sep = sample_id.rfind('/');
    std::string filename =
        (tree_sep == std::string::npos) ? sample_id : sample_id.substr(0, tree_sep);
    std::vector<std::string> parts;
    size_t pos = 0;
    size_t next;
    while ((next = filename.find('/', pos)) != std::string::npos) {
        parts.push_back(filename.substr(pos, next - pos));
        pos = next + 1;
    }
    parts.push_back(filename.substr(pos));
    if (parts.size() < 3) {
        throw std::runtime_error(
            "normalization::ParseNickFromPath: path '" + filename +
            "' has too few segments to contain a nick (expected "
            ".../era/nick/scope/nick_N.root)");
    }
    return parts[parts.size() - 3];
}

double LookupField(const nlohmann::json &norm_table, const std::string &nick,
                    const std::string &field) {
    if (!norm_table.contains(nick)) {
        Logger::get("normalization::SampleNormalization")
            ->error("nick '{}' not found in the normalization table -- "
                    "sample_database is missing an entry for this "
                    "(sample_type, era), or the input file path doesn't "
                    "match the expected .../era/nick/scope/nick_N.root "
                    "layout",
                    nick);
        throw std::runtime_error(
            "normalization::SampleNormalization: unknown nick " + nick);
    }
    return norm_table.at(nick).at(field).get<double>();
}

} // namespace

ROOT::RDF::RNode
SampleNormalization(ROOT::RDF::RNode df,
                     correctionManager::CorrectionManager &correctionManager,
                     const std::string &xsec_output,
                     const std::string &ngen_weight_output,
                     const std::string &genweight_output,
                     const std::string &norm_table_path) {
    nlohmann::json norm_table = *correctionManager.loadjson(norm_table_path);

    // crossSectionPerEventWeight -- the raw xsec (pb), unit and semantics
    // matching the legacy xsec/build_friend_tree.py friend it replaces.
    auto df1 = df.DefinePerSample(
        xsec_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return LookupField(norm_table, ParseNickFromPath(id.AsString()),
                                "xsec");
        });
    // numberGeneratedEventsWeight -- 1/nevents, computed here (not left to a
    // downstream Redefine) so there is exactly one place that can get the
    // reciprocal wrong.
    auto df2 = df1.DefinePerSample(
        ngen_weight_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return 1.0 / LookupField(norm_table, ParseNickFromPath(id.AsString()),
                                      "nevents");
        });
    // negative_events_fraction -- same field/semantics as the legacy friend.
    auto df3 = df2.DefinePerSample(
        genweight_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return LookupField(norm_table, ParseNickFromPath(id.AsString()),
                                "generator_weight");
        });
    return df3;
}

} // namespace normalization
#endif
