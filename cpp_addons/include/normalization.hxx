#ifndef GUARD_NORMALIZATION_H
#define GUARD_NORMALIZATION_H

#include "ROOT/RDataFrame.hxx"
#include <cstdint>
#include <string>

namespace event::normalization {

/**
 * @brief This function creates a flag column that splits a dataset into two
 * subsets of a given size. The quantity (e.g. the event number) is mapped to
 * a uniform number in [0, 1) by the splitmix64 hash, and the flag is `true`
 * if that number is below `fraction`. Unlike `EvenOddFlag`, the subsets are
 * unrelated to the parity of the quantity. The same mapping is implemented in
 * python by the sample database's `samplemanager/scripts/split_fractions.py`,
 * which measures the generator-weight fraction of each subset.
 *
 * @tparam T type of the quantity (e.g. `ULong64_t`)
 * @param df input dataframe
 * @param outputname name of the new flag column
 * @param quantity name of the column containing the quantity to hash
 * @param fraction expected fraction of the dataset flagged as `true`
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode
FractionSplitFlag(ROOT::RDF::RNode df, const std::string &outputname,
                  const std::string &quantity, const double &fraction) {
    return df.Define(outputname,
                     [fraction](const T &quantity) {
                         uint64_t z = static_cast<uint64_t>(quantity) +
                                      0x9e3779b97f4a7c15ULL;
                         z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
                         z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
                         z ^= z >> 31;
                         return (z >> 11) * 0x1.0p-53 < fraction;
                     },
                     {quantity});
}

ROOT::RDF::RNode SampleNormalization(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &xsec_output, const std::string &ngen_weight_output,
    const std::string &genweight_output, const std::string &split_weight_output,
    const std::string &norm_table_path,
    const double &default_split_fraction = 1.0);
}
#endif /* GUARD_NORMALIZATION_H */
