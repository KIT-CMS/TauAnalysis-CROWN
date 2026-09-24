from ..quantities import output as q
from code_generation.producer import Producer

# {norm_table_path} is a per-(sample_type, era) config parameter set by
# weights_friends.py's build_config() -- the relative path (under CROWN's
# data/, shipped by cmake's `install(DIRECTORY data/ ...)`) to the JSON
# table normalization.build_norm_table() generates at code-gen time. Not
# wired for data/embedding scopes' samples (see weights_friends.py) -- there
# is no per-nick normalization to look up there.
SampleNormalization = Producer(
    call='''normalization::SampleNormalization({df}, correctionManager, {output}, "{norm_table_path}")''',
    # no per-event input columns -- DefinePerSample reads the file's own
    # RSampleInfo, not any branch
    input=[],
    # order must match cpp_addons SampleNormalization's positional string
    # args: (xsec, 1/nevents, generator_weight)
    output=[
        q.crossSectionPerEventWeight,
        q.numberGeneratedEventsWeight,
        q.negative_events_fraction,
    ],
    scopes=["et", "mt", "tt", "em"],
)
