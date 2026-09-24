from ..quantities import output as q
from code_generation.helpers import defaults
from code_generation.producer import Producer

# {norm_table_path} is a per-(sample_type, era) config parameter set by
# weights_friends.py's build_config() -- the relative path (under CROWN's
# data/, shipped by cmake's `install(DIRECTORY data/ ...)`) to the JSON
# table normalization.build_norm_table() generates at code-gen time.
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

# data/embedding: no per-nick normalization applies (no xsec, no genWeight), but the
# friend still has to carry these three columns with the same names/types as the MC
# path -- a friend with a different schema per sample_type (or, worse, no friend at
# all) breaks downstream code that attaches this friend uniformly and multiplies by
# these columns. Constant 1.0 is a no-op weight, same defensive pattern
# TauFakeFactors/preselection.py already uses for MC-only branches missing on data.
with defaults(
    scopes=["et", "mt", "tt", "em"],
    call='''event::quantity::Define<float>({df}, {output}, 1.0f)''',
    input=[],
):
    ConstantCrossSectionPerEventWeight = Producer(output=[q.crossSectionPerEventWeight])
    ConstantNumberGeneratedEventsWeight = Producer(output=[q.numberGeneratedEventsWeight])
    ConstantNegativeEventsFraction = Producer(output=[q.negative_events_fraction])
