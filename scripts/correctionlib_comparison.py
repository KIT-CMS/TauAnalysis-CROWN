import argparse
import gzip
import json
import os
from itertools import combinations, count, product, cycle, zip_longest
from multiprocessing import Pool
from typing import Any, Dict, Generator, List, Tuple, Union

import correctionlib
import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np

matplotlib.use("Agg")
hep.style.use("CMS")

parser = argparse.ArgumentParser(description="Script for visually comparing two correctionlibs by their individual corrections")

parser.add_argument("--input-a", type=str, help="path to a reference json.gz correctionlib file for the comparison")
parser.add_argument("--tag-a", type=str, help="Name that will be plotted in the legend in form of '$sf_{<tag-a>}$'", default="A")

parser.add_argument(
    "--input-b",
    metavar="str",
    nargs="+",
    help="path(s) to a json.gz correctionlib file(s) that are compared to the reference (separation by white space)",
    default="",
)
parser.add_argument(
    "--tag-b",
    metavar="str",
    nargs="+",
    help="Name(s) that will be plotted in the legend in form of '$sf_{<tag-b>}$' (separation by white space)",
    default="",
)

parser.add_argument(
    "--correction-name",
    metavar="str",
    nargs="+",
    help="Name of a correction that will only be plotted. Other corrections are skipped when specified",
    default="",
)
parser.add_argument(
    "--output",
    type=str,
    help="Output directory",
    default="comparison_plots",
)
parser.add_argument(
    "--parallel",
    default=False,
    required=False,
    action="store_true",
    help="Create correction comparisons in parallel using 10 processes (default)",
)
parser.add_argument(
    "-np",
    type=int,
    help="Number of maximal used parallel processes if --parallel is set",
    default=10,
    required=False,
)
parser.add_argument(
    "--processes",
    metavar="str",
    nargs="+",
    help="Processes that will be plotted. If not specified, all processes are plotted",
    default=None,
)
args = parser.parse_args()

assert len(args.input_b) == len(args.tag_b), f"Number of input-b files ({len(args.input_b)}) and tag-b items ({len(args.tab_b)}) must be equal"


def windowed(iterable: Union[List[Any], Tuple[Any], np.ndarray], n: int) -> Generator[Tuple[Any, ...], None, None]:
    assert n > 0
    for i in range(0, len(iterable) - n + 1):
        yield tuple(iterable[i: i + n])


def to_latex(string: str) -> str:
    conversion = {
        "pt_1": r"$p_{T_1}$",
        "pt_2": r"$p_{T_2}$",
        "abs(eta_1)": r"$|\eta_1|$",
        "abs(eta_2)": r"$|\eta_2|$",
        "abs(eta)": r"$|\eta|$",
        "pt": r"$p_T$",
    }
    return conversion[string] if string in conversion else string


class KeyTo:
    @staticmethod
    def latex(key: Tuple) -> str:
        return ", ".join([f"{to_latex(name)}$\\in$[{interval[0]}, {interval[1]}]{'' if 'eta' in name else ' GeV'}" for name, interval in key])

    @staticmethod
    def path(key: Tuple) -> str:
        return "_".join([f"_{name}_{interval[0]}_{interval[1]}" for name, interval in key])

    @staticmethod
    def prompt(key: Tuple) -> str:
        return ", ".join([f"{name}=[{interval[0]}, {interval[1]}]" for name, interval in key])


def is_equal_binning(first_obj: "CorrectionHelper", second_obj: "CorrectionHelper") -> bool:
    if isinstance(first_obj, CorrectionHelper) and isinstance(second_obj, CorrectionHelper):
        assert first_obj._inputs == second_obj._inputs
        for item in first_obj._inputs:
            if not np.all(first_obj.histogram_edges[item] == second_obj.histogram_edges[item]):
                return False
        return True
    else:
        raise TypeError


class CorrectionHelper(object):
    def __init__(self, correction: correctionlib.Correction, raw_correction_data: dict) -> None:
        self._correction = correction
        self._raw_correction_data = raw_correction_data["data"]
        self._histogram_edges: Union[dict, None] = None

        self._inputs = [it["name"] for it in raw_correction_data["inputs"] if it["name"] != "type"]
        self.types = [""] if "type" not in {it["name"] for it in raw_correction_data["inputs"]} else ["mc", "emb"]
        self.ylabel = to_latex(raw_correction_data["output"]["name"])

    def __getattribute__(self, name: str, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().__getattribute__(name, *args, **kwargs)
        except AttributeError:
            return self._correction.__getattribute__(name, *args, **kwargs)

    @property
    def histogram_edges(self) -> Dict[str, np.ndarray]:
        if self._histogram_edges is None:
            self._histogram_edges = {}
            _tmp = self._raw_correction_data
            for item in self._inputs:
                if "abs" in item:
                    self._histogram_edges[item] = np.unique(np.append([0.0], np.abs(_tmp["edges"])))
                else:
                    self._histogram_edges[item] = np.array(_tmp["edges"])
                _tmp = _tmp["content"][0]
        return self._histogram_edges

    @property
    def windowed_histogram_edges(self) -> Dict[str, np.ndarray]:
        return {k: np.array(list(windowed(v, 2))) for k, v in self.histogram_edges.items()}

    def adjust_binning_with(self, other: "CorrectionHelper") -> None:
        if isinstance(other, CorrectionHelper):
            assert self._inputs == other._inputs
            for item in self._inputs:
                merged_binning = np.unique(np.concatenate([self.histogram_edges[item], other.histogram_edges[item]]))
                self.histogram_edges[item] = merged_binning
                other.histogram_edges[item] = merged_binning
        else:
            raise TypeError

    def unroll(self, axis: int = 0) -> None:
        self.edges = self.histogram_edges[self._inputs[axis]]
        self.xlabel = f"{to_latex(self._inputs[axis])}{' (GeV)' if 'eta' not in self._inputs[axis] else ''}"
        self.unrolled: Dict[str, Dict[tuple, np.ndarray]] = {key: {} for key in self.types}

        walking_inputs = [item for idx, item in enumerate(self._inputs) if idx != axis]
        for key in self.types:
            for windows in product(*[self.windowed_histogram_edges[item] for item in walking_inputs]):
                args = [self.edges[:-1] + np.diff(self.edges) / 2, *tuple(map(np.mean, windows))]
                if key:
                    args.append(key)
                self.unrolled[key][tuple(zip(walking_inputs, map(tuple, windows)))] = self.evaluate(*args)


def get_corrections(filename: str) -> Dict[str, CorrectionHelper]:
    if isinstance(filename, str):
        if not filename:
            return {}
        if not filename.endswith(".json.gz"):
            raise TypeError(f"File {filename} is not a json.gz file")
        with gzip.open(filename, "rb") as f:
            raw_corrections = json.load(f)["corrections"]
        corrections = correctionlib.CorrectionSet.from_file(filename)
        return {
            item["name"]: CorrectionHelper(
                corrections[item["name"]],
                item,
            )
            for item in raw_corrections
        }
    elif isinstance(filename, (list, tuple)):
        return [get_corrections(it) for it in filename]
    else:
        raise TypeError


def _plot_single_correction(args):
    plot_single_correction(*args)


def plot_single_correction(
    name: str,
    processes: List[str],
    window: Tuple[Tuple[str, Tuple[float, float]], ...],
    nth_window: int,
    correction_a_bins: Tuple[dict[str, np.ndarray]],
    correction_edges: Tuple[np.ndarray],
    correction_a_tag: str,
    ylabel: str,
    xlabel: str,
    output_directory: str,
    #
    nth_correction: int,
    len_corrections_a: int,
    len_unrolled_keys: int,
    adjusted_binning: bool,
    correction_b_bins: Union[Tuple[dict[str, np.ndarray]], Tuple[Tuple[dict[str, np.ndarray]]], None] = None,
    correction_b_tag: Union[Tuple[str], None] = None,
):

    add_ratio = len(correction_b_bins) > 0
    add_process = len(processes) > 1

    fig, axes = plt.subplots(
        2 if add_ratio else 1,
        len(processes),
        gridspec_kw=dict(height_ratios=[0.7, 0.3]) if add_ratio else None,
        figsize=(10 * len(processes), 12),
        sharex=add_ratio,
        sharey=add_process,
    )
    axes = np.atleast_2d(axes)

    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    fig.suptitle(name)
    shared_ratio_ylim = 0
    for idx, (correction_type, ax) in enumerate(
        zip(
            processes,
            [axes[:, 0], axes[:, 1]] if len(processes) > 1 else axes,
        )
    ):
        ax[0].set_title(
            f"{correction_type}{': ' if correction_type else ''}{KeyTo.latex(window)}",
            loc="left",
            fontsize=16,
        )
        for correction, tag_name, color, marker in zip(
            [correction_a_bins, *correction_b_bins],
            [correction_a_tag, *correction_b_tag],
            cycle(plt.rcParams['axes.prop_cycle'].by_key()['color']),
            cycle(["o", "v", "^", "s", "D"]),
        ):
            hep.histplot(
                correction[idx],
                correction_edges[idx],
                label=f"${tag_name}$",
                ax=ax[0],
                histtype="errorbar",
                yerr=False,
                xerr=True,
                markerfacecolor="none",
                color=color,
                marker=marker,
            )

        for _correction_b_bins, _correction_b_tag, _color, _marker in zip(
            correction_b_bins,
            correction_b_tag,
            cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'][1:]),
            cycle(["v", "^", "s", "D"]),
        ):
            with np.errstate(divide="ignore", invalid="ignore"):
                hep.histplot(
                    correction_a_bins[idx] / _correction_b_bins[idx],
                    correction_edges[idx],
                    label=f"${_correction_b_tag}$",
                    ax=ax[1],
                    histtype="errorbar",
                    yerr=False,
                    xerr=True,
                    markerfacecolor="none",
                    color=_color,
                    marker=_marker,
                )

        ax[0].set(
            xscale="log",
            xlim=(correction_edges[idx][0], correction_edges[idx][-1]),
            ylabel=ylabel if idx == 0 else None,
        )

        hep.cms.label("Own Work", ax=ax[0], loc=2, data=not correction_type == "mc")
        ax[0].legend(loc="upper right")

        if add_ratio:
            for correction_type, ax in zip(
                processes,
                [axes[:, 0], axes[:, 1]] if len(processes) > 1 else axes,
            ):
                ax[1].set(
                    xscale="log",
                    xlabel=xlabel,
                    ylabel=f"Ratio w.r.t. {correction_a_tag}",
                    xlim=(correction_edges[idx][0], correction_edges[idx][-1]),
                )

    # not nice but it works
    if len(processes) > 1:
        ymin = min(map(lambda it: it.get_ylim()[0], axes[:, 0]))
        ymax = max(map(lambda it: it.get_ylim()[1], axes[:, 0]))
        if add_ratio:
            _distance = max(0, max(map(lambda it: max(map(lambda subit: abs(subit - 1), it.get_ylim())), axes[:, 1]))) * 1.25
            ymin_ratio, ymax_ratio = 1 - _distance, 1 + _distance
    else:
        ymin, ymax = axes[0, 0].get_ylim()
        if add_ratio:
            _distance = max(0, max(map(lambda it: abs(it - 1), axes[0, 1].get_ylim()))) * 1.25
            ymin_ratio, ymax_ratio = 1 - _distance, 1 + _distance
    for _ax in axes[:, 0]:
        _ax.set(ylim=(None, (ymax - ymin) * 1.25 + ymin))
    if add_ratio:
        for _ax in axes[:, 1]:
            _ax.set(ylim=(ymin_ratio, ymax_ratio))

    if not os.path.exists(output_directory):
        os.makedirs(name="comparison_plots", exist_ok=True)

    os.makedirs(name=os.path.join(output_directory, name), exist_ok=True)
    for ext in ["pdf", "png"]:
        plt.savefig(
            os.path.join(
                output_directory,
                name,
                f"comparison_{name}_{correction_a_tag}_{'_'.join(correction_b_tag)}_{KeyTo.path(window)}.{ext}",
            ),
        )
    plt.close()
    print(
        " | ".join(
            [
                f"Correction {nth_correction + 1}/{len_corrections_a}: {name}",
                f"Window {nth_window + 1}/{len_unrolled_keys}: {KeyTo.prompt(window)}",
            ]
            + (["binning adjusted"] if adjusted_binning else [])
        )
    )


def plot_corrections(
    corrections_a: dict,
    corrections_b: List[dict],
    correction_tag_a: str,
    correction_tag_b: List[str],
    output_directory: str,
    specific_correction: Union[str, None] = None,
    unroll_axis: int = 0,
    processes: Union[None, str, Tuple[str]] = None,
) -> None:
    correction_count, seen_corrections = count(), set()
    for name_a, name_b in combinations(
        [
            *corrections_a.keys(),
            *list({key for correction in corrections_b for key in correction.keys()}),
        ],
        2,
    ):
        # not one of the selected corrections if specific_correction is set
        if specific_correction and (name_a not in specific_correction):
            continue

        # if corrections to compare with are set and the names are not the same
        if corrections_b and (name_a != name_b):
            continue

        # if corrections_bto compare with are not set and name_a was not plotted yet
        if not corrections_b and name_a in seen_corrections:
            continue
        if not corrections_b and name_a not in seen_corrections:
            seen_corrections.add(name_a)

        nth_correction = next(correction_count)
        correction_a, correction_b = corrections_a[name_a], [it[name_b] for it in corrections_b]
        name = name_a
        if processes is None:
            processes = correction_a.types

        adjust_binning = not all(is_equal_binning(correction_a, it) for it in correction_b)
        if adjust_binning:
            print("Not equal binning detected, expanding to most granular common binning")
            combined_corrections = list([correction_a, *correction_b])
            for it in combined_corrections:
                for subit in combined_corrections:
                    if it != subit:
                        it.adjust_binning_with(subit)
        assert all(is_equal_binning(correction_a, it) for it in correction_b), "Something went wrong with the binning adjustment"

        correction_a.unroll(unroll_axis)
        for it in correction_b:
            it.unroll(unroll_axis)
        unrolled_keys = correction_a.unrolled[processes[0]].keys()

        plot_single_correction_args = [
            (
                name,  # name
                processes,  # processes
                window,  # window
                nth_window,  # nth_window
                tuple(correction_a.unrolled[it][window] for it in processes),  # correction_a_bins
                tuple(correction_a.edges for it in processes),  # correction_edges
                correction_tag_a,  # correction_a_tag
                correction_a.ylabel,  # ylabel
                correction_a.xlabel,  # xlabel
                output_directory,  # output_directory
                nth_correction,  # nth_correction
                len(corrections_a),  # len_corrections_a
                len(unrolled_keys),  # len_unrolled_keys
                adjust_binning,  # adjusted_binning
                tuple(tuple(it.unrolled[subit][window] for subit in processes) for it in correction_b),  # correction_b_bins
                tuple(correction_tag_b),  # correction_b_tag
            )
            for nth_window, window in enumerate(unrolled_keys)
        ]

        if args.parallel:
            used_processes = len(plot_single_correction_args)
            if len(plot_single_correction_args) > args.np:
                used_processes = args.np
            with Pool(processes=used_processes) as pool:
                pool.map(_plot_single_correction, plot_single_correction_args)
        else:
            for arg in plot_single_correction_args:
                plot_single_correction(*arg)


if __name__ == "__main__":
    plot_corrections(
        corrections_a=get_corrections(args.input_a),
        corrections_b=get_corrections(args.input_b),
        correction_tag_a=args.tag_a,
        correction_tag_b=args.tag_b,
        output_directory=args.output,
        specific_correction=args.correction_name if args.correction_name else None,
        processes=args.processes,
    )
    print("Done")
