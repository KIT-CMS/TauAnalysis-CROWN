#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/defaults.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace physicsobject {

namespace jet {

namespace quantities {

/**
 * @brief Patch for wrong Jet ID values in Run3 NanoAOD v12 samples.
 * 
 * The implementation follows the recipe by the [JME POG](https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV#nanoAOD_Flags).
 * 
 * @param df the input dataframe
 * @param outputname the name of the produced column
 * @param jet_pt name of the column with jet pt values
 * @param jet_eta name of the column with jet eta values
 * @param jet_id name of the column with (broken) jet ID values 
 * @param jet_ne_hef name of the column with neutral hadron energy fraction
 * @param jet_ne_em_ef name of the column with neutral EM energy fraction
 * @param jet_mu_ef name of the column with muon energy fraction
 * @param jet_ch_em_ef name of the column with charged EM energy fraction
 * 
 * @return a dataframe with the new column
 */
ROOT::RDF::RNode CorrectJetIDRun3NanoV12(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_id,
    const std::string &jet_ne_hef,
    const std::string &jet_ne_em_ef,
    const std::string &jet_mu_ef,
    const std::string &jet_ch_em_ef
) {

    // we do not need to ensure the correct casting for NanoAOD v9 samples here as this fix applies to NanoAOD v12 samples only

    auto correction = [] (
        const ROOT::RVec<float> &jet_pt,
        const ROOT::RVec<float> &jet_eta,
        const ROOT::RVec<UChar_t> &jet_id_v12,
        const ROOT::RVec<float> &jet_ne_hef,
        const ROOT::RVec<float> &jet_ne_em_ef,
        const ROOT::RVec<float> &jet_mu_ef,
        const ROOT::RVec<float> &jet_ch_em_ef
    ) {
        // cast jet_id to integer
        auto jet_id = static_cast<ROOT::RVec<int>>(jet_id_v12);

        // apply the JME POG recipe
        auto jet_id_corrected = ROOT::RVec<int>(jet_id.size(), 0);
        for (int i = 0; i < jet_pt.size(); ++i) {
            // evaluate if the jet passes the tight WP
            bool pass_tight = false;
            if (abs(jet_eta.at(i)) <= 2.7) {
                pass_tight = jet_id.at(i) & (1 << 1);
            } else if (abs(jet_eta.at(i)) > 2.7 && abs(jet_eta.at(i)) <= 3.0) {
                pass_tight = (jet_id.at(i) & (1 << 1)) && (jet_ne_hef.at(i) < 0.99);
            } else if (abs(jet_eta.at(i)) > 3.0) {
                pass_tight = (jet_id.at(i) & (1 << 1)) && (jet_ne_em_ef.at(i) < 0.4);
            }

            // evaluate if the jet passes the tight WP and fulfills the lepton veto
            bool pass_tight_lep_veto = false;
            if (abs(jet_eta.at(i)) <= 2.7) {
                pass_tight_lep_veto = pass_tight && (jet_mu_ef.at(i) < 0.8) && (jet_ch_em_ef.at(i) < 0.8);
            } else {
                pass_tight_lep_veto = pass_tight;
            }

            // return value of the working point that is passed
            // - 0 == fail
            // - 2 == pass tight & fail tightlepveto
            // - 6 == pass tight & pass tightlepveto
            if (pass_tight && !pass_tight_lep_veto) {
                jet_id_corrected[i] = 2;
            } else if (pass_tight && pass_tight_lep_veto) {
                jet_id_corrected[i] = 6;
            } else {
                jet_id_corrected[i] = 0;
            }
        }

        // convert the data type to default in NanoAOD v12 (UChar_t)
        auto jet_id_corrected_v12 = static_cast<ROOT::RVec<int>>(jet_id_corrected);

        return jet_id_corrected_v12;
    };

    // redefine the data type of the Jet ID mask
    return df.Define(
        outputname,
        correction,
        {
            jet_pt,
            jet_eta,
            jet_id,
            jet_ne_hef,
            jet_ne_em_ef,
            jet_mu_ef,
            jet_ch_em_ef
        }
    );
}

} // end quantities

// namespace vetoes 
namespace vetoes {

    /**
        * @brief Create a veto flag for events with jets in regions, which are known to produce wrong measurements.
        * The function checks for jets which pass the base selection criteria if they are in a eta-phi region with
        * "hot" and/or "cold" towers. Events with any jet in such a region are vetoed in data and simulation.
        * If the event is vetoed, a value of `true` is stored in the new column, otherwise `false`.
        * The locations are provided by a `correctionlib` file and depend on the data-taking era. This procedure
        * follows the official [JME POG recommendations](https://cms-jerc.web.cern.ch/Recommendations/#jet-veto-maps).
        *  
        * The documentation of the `correctionlib` files for the respective eras can be found here:
        * - [2022preEE](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22_jetvetomaps.html)
        * - [2022postEE](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22EE_jetvetomaps.html)
        * - [2023preBPix](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23_jetvetomaps.html)
        * - [2023postBPix](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23BPix_jetvetomaps.html)
        * 
        * @param df The input data frame.
        * @param correctionManager The CorrectionManager object
        * @param output_mask The output mask column.
        * @param jet_pt The tranverse momentum column of the jets.
        * @param jet_eta The pseudorapidity column of the jets.
        * @param jet_phi The azimuthal angle column of the jets.
        * @param jet_id The jet identification bitmask column of the jets.
        * @param jet_ch_em_ef The charged electromagnetic energy fraction column of the jets.
        * @param jet_n_em_ef The neutral electromagnetic energy fraction column of the jets.
        * @param jet_vetomap_file The file path to the correctionlib jet veto map.
        * @param jet_vetomap_name The name of the correction to access jet veto map.
        * @param jet_vetomap_type The jet veto map type; for analyses, this name should be `"jetvetomap"`.
        * @param min_pt The minimum transverse momentum for selected jets.
        * @param id_wp The working point for the jet identification.
        * @param max_em_frac The maximum charged and neutral electromagnetic energy fraction for selected jets.
        * @param min_delta_r_jet_muon The minimum deltaR separation between jets and particle-flow muons.
        * 
        * @return A new data frame with the selection mask column.
        * 
        * @note The veto map selection is mandatory for Run 3 analyses and can also be applied to Run 2 analyses.
        */
    ROOT::RDF::RNode jet_vetomap(
        ROOT::RDF::RNode df,
        correctionManager::CorrectionManager &correctionManager,
        const std::string &output_mask,
        const std::string &jet_pt,
        const std::string &jet_eta,
        const std::string &jet_phi,
        const std::string &jet_id,
        const std::string &jet_ch_em_ef,
        const std::string &jet_n_em_ef,
        const std::string &jet_vetomap_file,
        const std::string &jet_vetomap_name,
        const std::string &jet_vetomap_type,
        const float &min_pt,
        const int &id_wp,
        const float &max_em_frac
    ) {
        // load the veto map evaluator
        auto evaluator = correctionManager.loadCorrection(jet_vetomap_file, jet_vetomap_name);

        auto select = [
            evaluator, min_pt, id_wp, max_em_frac, jet_vetomap_type
        ] (
            const ROOT::RVec<float> &jet_pt,
            const ROOT::RVec<float> &jet_eta,
            const ROOT::RVec<float> &jet_phi,
            const ROOT::RVec<int> &jet_id,
            const ROOT::RVec<float> &jet_ch_em_ef,
            const ROOT::RVec<float> &jet_n_em_ef
        ) {
            // debug output for selection criteria and jet observables
            Logger::get("xyh::vetoes::jet_vetomap")->debug("Create selection masks for jets");
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    min_pt {}, id_wp {}, max_em_fraction {}", min_pt, id_wp, max_em_frac);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    pt {}", jet_pt);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    eta {}", jet_eta);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    phi {}", jet_phi);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    id {}", jet_id);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    ch_em_ef {}", jet_ch_em_ef);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    n_em_ef {}", jet_n_em_ef);

            // create the index of selected jets
            auto jet_index = ROOT::VecOps::Nonzero(
                (jet_pt > min_pt)
                && (jet_id >= id_wp)
                && ((jet_ch_em_ef + jet_n_em_ef) < max_em_frac)
            );

            // create container with indices for vetoed jets
            auto jet_index_vetoed = ROOT::RVec<int>(0);

            for (const auto &i : jet_index) {
                // evaluate the jet veto map value
                auto jet_vetoed = evaluator->evaluate({
                    jet_vetomap_type,
                    jet_eta.at(i),
                    jet_phi.at(i)
                });

                // if the jet is vetoed, add it to the vetoed jet index
                if (jet_vetoed) {
                    jet_index_vetoed.push_back(i);
                };
            }

            // check if any jet has been vetoed
            bool event_veto = false;
            if (!jet_index_vetoed.empty()) {
                event_veto = true;
            }

            // debug output for vetoes
            Logger::get("xyh::vetoes::jet_vetomap")->debug("Vetoes");
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    jet_index_vetoed {}", jet_index_vetoed);
            Logger::get("xyh::vetoes::jet_vetomap")->debug("    event_veto {}", event_veto);

            return event_veto;
        };

        return df.Define(
            output_mask,
            select,
            {
                jet_pt,
                jet_eta,
                jet_phi,
                jet_id,
                jet_ch_em_ef,
                jet_n_em_ef,
            }
        );
    }

} // end namespace vetoes 

} // end jet

} // end physicsobject


#endif