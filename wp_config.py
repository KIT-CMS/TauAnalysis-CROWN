"""
Single source of truth for the tau-vsJet / tau-vsEle WPs shared by
selection_friends.py and weights_friends.py -- the same physical quantities,
imported by both instead of duplicated as separate literals, so a WP change (or a
Run2/Run3 default change) can't silently drift the SF applied out of sync with the
selection it's meant to match (see project memory: this drifted once already,
in TauKITFlow's own config/weights.yaml vs process_selection.py).

selection_friends.py uses these under the names ff_tau_iso_vsjet_wp/presel_vsele_wp
(the WP that defines the signal region / preselection); weights_friends.py uses them
under vs_jet_wp/vs_ele_wp (the WP the SF is evaluated at) -- deliberately the same
values, since the SF must be evaluated at whatever WP defines "selected" for the
event to be meaningful.
"""
from code_generation.modifiers import EraModifier

from .tau_triggersetup import RUN2_ERAS

# tau-vsJet WP: Run 2's combined tau ID has no Medium/VVVLoose split the way Run 3's
# does, so Run 2 uses Tight/VLoose instead -- matches selection_friends.py's existing
# ff_tau_iso_vsjet_wp/ff_tau_antiiso_vsjet_wp EraModifiers.
VSJET_WP = EraModifier({era: "Tight" for era in RUN2_ERAS}, default="Medium")
VSJET_ANTIISO_WP = EraModifier({era: "VLoose" for era in RUN2_ERAS}, default="VVVLoose")

# tau-vsEle WP per channel: et needs the tighter cut against electron fakes (the
# dominant fake background there), mt/tt use the looser default. Matches
# selection_friends.py's existing per-channel presel_vsele_wp values and
# TauKITFlow's config.analysis.vs_ele_wp_for().
VSELE_WP = {"et": "Tight", "mt": "VVLoose", "tt": "VVLoose"}
