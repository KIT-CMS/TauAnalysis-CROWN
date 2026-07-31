#ifndef GUARD_SELECTION_H
#define GUARD_SELECTION_H

#include "ROOT/RDataFrame.hxx"
#include "../../../../include/utility/Logger.hxx"

#include <algorithm>
#include <string>
#include <vector>

/**
 * @file selection.hxx
 *
 * @brief Header-only helpers to express analysis event selections as boolean
 * flag columns.
 *
 * These functions complement the generic flag helpers already available in
 * `event::quantity` (`MinFlag` = `>=`, `MaxFlag` = `<`, `EqualFlag` = `==`,
 * `AbsMaxFlag` = `abs(x) <`). Together they cover every cut expression that
 * appears in the analysis selection configuration
 * (`TauKITFlow/config/cuts.yaml` and the `TauFakeFactors` region configs), so
 * that each cut can be materialised as a single `bool` column and the region
 * masks can be built with `event::CombineFlags(..., "all_of")`.
 *
 * Conventions:
 * - All functions take the *column names* as strings, never `Quantity`
 *   objects. This makes them usable for columns that are leaves of a
 *   `QuantityGroup` (e.g. `id_tau_vsJet_Medium_2`, `trg_single_mu24`), which
 *   cannot be referenced as plain input quantities from the python side.
 * - The template parameter `T` must match the *stored* type of the column.
 *   In this analysis: `float` for `pt_*`/`iso_*`/`mt_1`, `int` for `nbtag` and
 *   the `id_tau_vs*` flags, `UChar_t` for `tau_decaymode_*`, `int`/`Short_t`
 *   for `q_1`/`q_2` and `bool` for trigger and veto flags.
 * - `PassFlag`/`FailFlag` implement the `> 0.5` / `< 0.5` idiom used in the
 *   yaml cut strings for integer-valued ID and trigger flags; they cast to
 *   `double` internally so they work for `bool`, `int` and `UChar_t` alike.
 */

namespace selection {

/**
 * @brief Flag that is `true` if the value of a column passes the `> 0.5`
 * convention used for ID/trigger/veto flags.
 *
 * @tparam T stored type of the column (e.g. `bool`, `int`, `UChar_t`)
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode PassFlag(ROOT::RDF::RNode df,
                                 const std::string &outputname,
                                 const std::string &quantity) {
    return df.Define(
        outputname,
        [](const T &value) { return static_cast<double>(value) > 0.5; },
        {quantity});
}

/**
 * @brief Flag that is `true` if the value of a column fails the `> 0.5`
 * convention, i.e. `< 0.5`. Used for the veto columns (`extraelec_veto`,
 * `jet_vetomap`, ...) and for anti-isolated tau ID requirements.
 *
 * @tparam T stored type of the column (e.g. `bool`, `int`, `UChar_t`)
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode FailFlag(ROOT::RDF::RNode df,
                                 const std::string &outputname,
                                 const std::string &quantity) {
    return df.Define(
        outputname,
        [](const T &value) { return static_cast<double>(value) < 0.5; },
        {quantity});
}

/**
 * @brief Flag for a strict lower bound, `value > threshold`.
 *
 * @tparam T stored type of the column and of the threshold
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 * @param threshold exclusive lower bound
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode GreaterFlag(ROOT::RDF::RNode df,
                                    const std::string &outputname,
                                    const std::string &quantity,
                                    const T &threshold) {
    return df.Define(
        outputname, [threshold](const T &value) { return value > threshold; },
        {quantity});
}

/**
 * @brief Flag for an inclusive upper bound, `value <= threshold`.
 *
 * Complements `event::quantity::MaxFlag`, which implements the exclusive
 * `value < threshold`.
 *
 * @tparam T stored type of the column and of the threshold
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 * @param threshold inclusive upper bound
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode MaxOrEqualFlag(ROOT::RDF::RNode df,
                                       const std::string &outputname,
                                       const std::string &quantity,
                                       const T &threshold) {
    return df.Define(
        outputname, [threshold](const T &value) { return value <= threshold; },
        {quantity});
}

/**
 * @brief Flag for a closed interval, `lower <= value <= upper`.
 *
 * This is the literal translation of the `((iso_1 >= x) && (iso_1 <= y))`
 * isolation windows used in the fake factor region definitions.
 *
 * @tparam T stored type of the column and of the interval boundaries
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 * @param lower inclusive lower boundary
 * @param upper inclusive upper boundary
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode InRangeFlag(ROOT::RDF::RNode df,
                                    const std::string &outputname,
                                    const std::string &quantity,
                                    const T &lower, const T &upper) {
    return df.Define(outputname,
                     [lower, upper](const T &value) {
                         return (value >= lower) && (value <= upper);
                     },
                     {quantity});
}

/**
 * @brief Flag for the complement of a closed interval,
 * `!(lower <= value <= upper)`.
 *
 * This is the literal translation of the inverted isolation windows used in
 * the QCD determination-region to signal-region corrections.
 *
 * @tparam T stored type of the column and of the interval boundaries
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 * @param lower inclusive lower boundary of the excluded interval
 * @param upper inclusive upper boundary of the excluded interval
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode OutOfRangeFlag(ROOT::RDF::RNode df,
                                       const std::string &outputname,
                                       const std::string &quantity,
                                       const T &lower, const T &upper) {
    return df.Define(outputname,
                     [lower, upper](const T &value) {
                         return !((value >= lower) && (value <= upper));
                     },
                     {quantity});
}

/**
 * @brief Flag that is `true` if the two charge columns have the same sign,
 * `(charge_1 * charge_2) > 0`.
 *
 * The two template parameters are independent because the charge columns can
 * have different stored types depending on the scope (e.g. `int` for the
 * light lepton and `Short_t` for the hadronic tau).
 *
 * @tparam T1 stored type of the first charge column
 * @tparam T2 stored type of the second charge column
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param charge_1 name of the first charge column
 * @param charge_2 name of the second charge column
 *
 * @return a dataframe with the new flag column
 */
template <typename T1, typename T2>
inline ROOT::RDF::RNode SameSignFlag(ROOT::RDF::RNode df,
                                     const std::string &outputname,
                                     const std::string &charge_1,
                                     const std::string &charge_2) {
    return df.Define(outputname,
                     [](const T1 &q1, const T2 &q2) {
                         return (static_cast<double>(q1) *
                                 static_cast<double>(q2)) > 0.0;
                     },
                     {charge_1, charge_2});
}

/**
 * @brief Flag that is `true` if the two charge columns have opposite sign,
 * `(charge_1 * charge_2) < 0`.
 *
 * @tparam T1 stored type of the first charge column
 * @tparam T2 stored type of the second charge column
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param charge_1 name of the first charge column
 * @param charge_2 name of the second charge column
 *
 * @return a dataframe with the new flag column
 */
template <typename T1, typename T2>
inline ROOT::RDF::RNode OppositeSignFlag(ROOT::RDF::RNode df,
                                         const std::string &outputname,
                                         const std::string &charge_1,
                                         const std::string &charge_2) {
    return df.Define(outputname,
                     [](const T1 &q1, const T2 &q2) {
                         return (static_cast<double>(q1) *
                                 static_cast<double>(q2)) < 0.0;
                     },
                     {charge_1, charge_2});
}

/**
 * @brief Flag that is `true` if the value of a column is contained in a list
 * of allowed values, e.g. the accepted hadronic tau decay modes
 * `{0, 1, 10, 11}`.
 *
 * @tparam T stored type of the column and of the list entries
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param quantity name of the column to be evaluated
 * @param values list of accepted values
 *
 * @return a dataframe with the new flag column
 */
template <typename T>
inline ROOT::RDF::RNode InListFlag(ROOT::RDF::RNode df,
                                   const std::string &outputname,
                                   const std::string &quantity,
                                   const std::vector<T> &values) {
    if (values.empty()) {
        Logger::get("selection::InListFlag")
            ->error("Empty list of accepted values for column {}!", quantity);
        throw std::runtime_error("selection::InListFlag: empty value list");
    }
    return df.Define(outputname,
                     [values](const T &value) {
                         return std::find(values.begin(), values.end(),
                                          value) != values.end();
                     },
                     {quantity});
}

/**
 * @brief Flag that is the logical negation of an existing `bool` flag column.
 *
 * Used to build the inverted lepton veto (`!(extramuon_veto < 0.5 &&
 * extraelec_veto < 0.5 && dilepton_veto < 0.5)`) of the ttbar signal- and
 * application-like regions from the combined veto flag.
 *
 * @param df input dataframe
 * @param outputname name of the new `bool` column
 * @param flagname name of the existing `bool` column to be inverted
 *
 * @return a dataframe with the new flag column
 */
inline ROOT::RDF::RNode InvertFlag(ROOT::RDF::RNode df,
                                   const std::string &outputname,
                                   const std::string &flagname) {
    return df.Define(outputname, [](const bool flag) { return !flag; },
                     {flagname});
}

} // end namespace selection

#endif /* GUARD_SELECTION_H */
