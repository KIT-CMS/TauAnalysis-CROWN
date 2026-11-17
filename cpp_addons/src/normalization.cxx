#ifndef GUARD_NORMALIZATION_H
#define GUARD_NORMALIZATION_H

#include "../include/utility/CorrectionManager.hxx"
#include "../include/utility/Logger.hxx"
#include "../include/utility/utility.hxx"
#include "ROOT/RDataFrame.hxx"
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <string>
#include <vector>

namespace event::normalization {

namespace {

std::string SampleNormalizationParseNickFromPath(const std::string &sample_id) {
    auto tree_sep = sample_id.rfind('/');
    std::string filename = (tree_sep == std::string::npos)
                               ? sample_id
                               : sample_id.substr(0, tree_sep);
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
            "event::normalization::SampleNormalization: path '" + filename +
            "' has too few segments to contain a nick (expected "
            ".../era/nick/scope/nick_N.root)");
    }
    return parts[parts.size() - 3];
}

double SampleNormalizationLookupField(const nlohmann::json &norm_table,
                                      const std::string &nick,
                                      const std::string &field) {
    if (!norm_table.contains(nick)) {
        Logger::get("event::normalization::SampleNormalization")
            ->error("nick '{}' not found in the normalization table, "
                    "sample_database is missing an entry for this ",
                    nick);
        throw std::runtime_error(
            "event::normalization::SampleNormalization: unknown nick " + nick);
    }
    return norm_table.at(nick).at(field).get<double>();
}

} // namespace

/**
 * @brief This function defines a column `outputname` containing 1 / the
 * fraction of the sample kept by an era split (e.g. `FractionSplitFlag`), by
 * looking up the sample nick in a flat `nick -> fraction` JSON table. Nicks
 * not in the table fall back to `default_split_fraction`.
 *
 * The nick is read from the `nick` column (set from `CROWN_SAMPLE_INFO`), so
 * this also works on NanoAOD input.
 *
 * @param df input dataframe
 * @param correctionManager correction manager responsible for loading the
 * JSON table
 * @param outputname name of the new column containing 1 / fraction
 * @param nick name of the column containing the sample nick
 * @param split_fractions_path path to the `nick -> fraction` JSON table
 * @param default_split_fraction fraction of the sample kept by the era split
 * for nicks not in the table
 *
 * @return a dataframe with the new column
 */
ROOT::RDF::RNode
FractionSplitWeight(ROOT::RDF::RNode df,
                    correctionManager::CorrectionManager &correctionManager,
                    const std::string &outputname, const std::string &nick,
                    const std::string &split_fractions_path,
                    const double &default_split_fraction) {
    nlohmann::json split_fractions =
        *correctionManager.loadjson(split_fractions_path);

    // 1/split_fraction, 1/default_split_fraction if the nick is not measured
    return df.Define(
        outputname,
        [split_fractions, default_split_fraction](const std::string &nick) {
            return static_cast<float>(
                1.0 / split_fractions.value(nick, default_split_fraction));
        },
        {nick});
}

/**
 * @brief This function defines three per-file constant columns --
 * `xsec_output` (cross section), `ngen_weight_output` (1 / number of
 * generated events) and `genweight_output` (effective normalization factor
 * accounting for negative generator weights) -- by looking up this file's
 * sample nick in a `nick -> {xsec, nevents, generator_weight}` JSON table.
 *
 * The sample nick is parsed from the input file's path at runtime via
 * `ROOT::RDF::RSampleInfo` (path convention: `.../{era}/{nick}/{scope}/
 * {nick}_{N}.root`), so one compiled executable correctly normalizes every
 * nick contained in its input sample. An unknown nick throws rather than
 * silently defaulting.
 *
 * @param df input dataframe
 * @param correctionManager correction manager responsible for loading the
 * normalization JSON table
 * @param xsec_output name of the new column containing the cross section
 * @param ngen_weight_output name of the new column containing 1/nevents
 * @param genweight_output name of the new column containing the effective
 * generator-weight normalization factor
 * @param norm_table_path path to the `nick -> {xsec, nevents,
 * generator_weight}` JSON lookup table
 *
 * @return a dataframe with the three new columns
 */
ROOT::RDF::RNode
SampleNormalization(ROOT::RDF::RNode df,
                    correctionManager::CorrectionManager &correctionManager,
                    const std::string &xsec_output,
                    const std::string &ngen_weight_output,
                    const std::string &genweight_output,
                    const std::string &norm_table_path) {
    nlohmann::json norm_table = *correctionManager.loadjson(norm_table_path);

    // crossSectionPerEventWeight -- the raw xsec (pb)
    auto df1 = df.DefinePerSample(
        xsec_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return SampleNormalizationLookupField(
                norm_table, SampleNormalizationParseNickFromPath(id.AsString()),
                "xsec");
        });
    // numberGeneratedEventsWeight -- 1/nevents
    auto df2 = df1.DefinePerSample(
        ngen_weight_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return 1.0 /
                   SampleNormalizationLookupField(
                       norm_table,
                       SampleNormalizationParseNickFromPath(id.AsString()),
                       "nevents");
        });
    // negative_events_fraction -- effective normalization factor
    return df2.DefinePerSample(
        genweight_output,
        [norm_table](unsigned int /*slot*/, const ROOT::RDF::RSampleInfo &id) {
            return SampleNormalizationLookupField(
                norm_table, SampleNormalizationParseNickFromPath(id.AsString()),
                "generator_weight");
        });
}

} // end namespace event::normalization
#endif /* GUARD_NORMALIZATION_H */
