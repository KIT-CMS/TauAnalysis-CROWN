from os import path, makedirs
import importlib
from code_generation.code_generation import CodeGenerator


def run(args):
    analysis_name = "tau"

    # available_samples = [
    #     "ggh_htautau",
    #     "ggh_hbb",
    #     "vbf_htautau",
    #     "vbf_hbb",
    #     "rem_htautau",
    #     "rem_hbb",
    #     "embedding",
    #     "embedding_mc",
    #     "singletop",
    #     "ttbar",
    #     "diboson",
    #     "dyjets",
    #     "wjets",
    #     "data",
    #     "electroweak_boson",
    #     "nmssm_Ybb",
    #     "nmssm_Ytautau",
    # ]

    available_samples = [
        "data",
        "hh2b2tau",
        "dyjets",
        "wjets",
        "electroweak_boson",
        "singletop",
        "ggh_htautau",
        "vbf_htautau",
        "ttbar",
        "ttH",
        "diboson",
        "triboson",
        "rem_htautau",
        "rem_hbb",
        "rem_ttbar",
        "embedding",
        "embedding_mc",
        "vbf_hbb",
        "ggh_hbb"
    ]

    
    available_eras = ["2016preVFP", "2016postVFP", "2017", "2018"]
    available_scopes = ["et", "mt", "tt", "mm"]

    ## setup variables
    shifts = set([shift.lower() for shift in args.shifts])
    sample_group = args.sample
    era = args.era
    scopes = list(set([scope.lower() for scope in args.scopes]))

    ## load config
    configname = args.config
    config = importlib.import_module(
        f"analysis_configurations.{analysis_name}.{configname}"
    )
    ## Setting up executable
    executable = f"{configname}_{sample_group}_{era}.cxx"
    args.logger.info(f"Generating code for {sample_group}...")
    args.logger.info(f"Configuration used: {config}")
    args.logger.info(f"Era: {era}")
    args.logger.info(f"Shifts: {shifts}")
    config = config.build_config(
        era,
        sample_group,
        scopes,
        shifts,
        available_samples,
        available_eras,
        available_scopes,
    )
    # create a CodeGenerator object
    generator = CodeGenerator(
        main_template_path=args.template,
        sub_template_path=args.subset_template,
        configuration=config,
        executable_name=f"{configname}_{sample_group}_{era}",
        analysis_name=analysis_name,
        config_name=configname,
        output_folder=args.output,
        threads=args.threads,
    )
    if args.debug == "true":
        generator.debug = True
    # generate the code
    generator.generate_code()

    executable = generator.get_cmake_path()

    # append the executable name to the files.txt file
    # if the file does not exist, create it
    if not path.exists(path.join(args.output, "files.txt")):
        with open(path.join(args.output, "files.txt"), "w") as f:
            f.write(f"{executable}\n")
    else:
        with open(path.join(args.output, "files.txt"), "r+") as f:
            for line in f:
                if executable in line:
                    break
            else:
                f.write(f"{executable}\n")
