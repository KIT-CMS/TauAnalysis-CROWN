"""The selection masks as a friend tree of an existing CROWN ntuple.

This is the second of the two ways to get the mask branches of
`producers/selection.py`; both are supported:

  * `config.py` writes them into the main ntuple as it is produced. Use this
    when the ntuples are produced (or re-produced) anyway.
  * this config writes exactly the same branches into a friend tree next to an
    existing ntuple. Use this to add the masks to ntuples that are already on
    disk, or to change a region definition without re-running the full ntuple
    production.

Nothing about the selection is written down again here. The regions, the atomic
cuts, the thresholds, the working points and the output branches all come from
`add_selection()` of `selection_config.py`, the very function `config.py` calls,
invoked with `friend=True`. That switch does exactly two things (see there): it
swaps the flag producers that read a tau ID or trigger column out of an
`ExtendedVectorProducer.output_group` for their input-less twins -- in a friend
job the group producer does not run, and the column is read from the input
ntuple, which is why declaring the group as an input would fail the friend input
validation -- and it skips the producer rules, which would append their
replacement at the end of the producer list, whereas a friend production runs
the producers in exactly the order the configuration lists them.

The friend tree is produced per scope (`et`, `mt`, `tt`, `em`), one executable
each, as the friend machinery requires. Nominal only: the mask branches that
downstream consumes per shift (`presel_mask`, `sel_os`, `sel_ss`) are the ones
the main production already keeps shifted copies of, and a shifted mask cannot
be built here anyway, because the shifted input columns of the ID and trigger
flags are addressed by name and are not part of the friend input map.

Usage (one build, one executable per scope):

    cmake .. -DANALYSIS=tau -DCONFIG=selection_friends -DSAMPLES=<sample> \
             -DERAS=<era> -DSCOPES=et,mt,tt,em -DSHIFTS=none \
             -DQUANTITIESMAP=<ntuple or quantities map>
    ./selection_friends_<sample>_<era>_<scope> friend.root ntuple.root
"""

from typing import List, Union

from code_generation.friend_trees import FriendTreeConfiguration

from .config import TAU_DECAY_MODES
from .selection_config import add_selection


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
) -> FriendTreeConfiguration:
    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    # the masks are only defined on nominal. Refuse anything else instead of
    # silently writing a shifted mask that was built from nominal columns.
    requested = {
        shift
        for scope in configuration.selected_scopes
        for shift in configuration.requested_shifts[scope]
    }
    if requested - {"nominal"}:
        raise ValueError(
            "The selection masks are produced for the nominal shift only, but "
            f"{sorted(requested - {'nominal'})} were requested. Build with "
            "-DSHIFTS=none."
        )

    #########################
    # Parameters the masks need from outside `add_selection`
    #########################

    # the accepted hadronic tau decay modes. In the main production this comes
    # with the tau object definition of `config.py`, which a friend production
    # does not run; the value itself is imported from there, so the decay mode
    # cut of `presel_mask` is the same list on both paths.
    configuration.add_config_parameters(
        ["et", "mt", "tt"],
        {
            "tau_dms": TAU_DECAY_MODES,
        },
    )

    #########################
    # The selection masks, exactly as the main production defines them
    #########################

    configuration = add_selection(
        configuration,
        scopes,
        era,
        sample,
        # a friend tree has to have one entry per entry of the ntuple it is a
        # friend of, so the optional hard filter on the preselection is not
        # available here -- the whole point of `presel_mask` is that filtering
        # is left to the consumer
        apply_preselection_filter=False,
        friend=True,
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
