import argparse
import gzip
import json
import os
from itertools import combinations, count, product
from typing import Any, Dict, Generator, List, Tuple, Union

import correctionlib
import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np

matplotlib.use("Agg")
hep.style.use("CMS")

parser = argparse.ArgumentParser(description="Script for visually comparing two correctionlibs by their individual corrections")
parser.add_argument("--input-a", type=str, help="path to a json.gz correctionlib file")
parser.add_argument("--input-b", type=str, help="path to a json.gz correctionlib file that is used for comparison")
parser.add_argument("--tag-a", type=str, help="Name that will be plotted in the legend in form of '$sf_{<tag-a>}$'", default="A")
parser.add_argument("--tag-b", type=str, help="Name that will be plotted in the legend in form of '$sf_{<tag-b>}$'", default="B")
parser.add_argument(
    "--correction-name",
    type=str,
    help="Name of a correction that will only be plotted. Other corrections are skipped when specified",
    default="",
)
parser.add_argument("--output", type=str, help="Output directory", default="comparison_plots")
args = parser.parse_args()


def windowed(
    iterable: Union[List[Any], Tuple[Any], np.ndarray],
    n: int,
) -> Generator[Tuple[Any, ...], None, None]:
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


def plot_corrections(
    corrections_a: dict,
    corrections_b: dict,
    correction_tag_a: str,
    correction_tag_b: str,
    output_directory: str,
    specific_correction: Union[str, None] = None,
    unroll_axis: int = 0,
) -> None:
    correction_count = count()

    for correction_key_a, correction_key_b in combinations([*corrections_a.keys(), *corrections_b.keys()], 2):
        if correction_key_a != correction_key_b or (specific_correction and correction_key_a != specific_correction):
            continue
        else:
            nth_correction = next(correction_count)
            correction_a, correction_b = corrections_a[correction_key_a], corrections_b[correction_key_b]
            name = correction_key_a
            processes = correction_a.types

        adjusted_binning = False
        if not is_equal_binning(correction_a, correction_b):
            print("Not equal binning detected, expanding to common binning")
            correction_a.adjust_binning_with(correction_b)
            adjusted_binning = True

        correction_a.unroll(unroll_axis)
        correction_b.unroll(unroll_axis)
        unrolled_keys = correction_a.unrolled[processes[0]].keys()

        for nth_window, window in enumerate(unrolled_keys):
            fig, axes = plt.subplots(
                2,
                len(correction_a.types),
                gridspec_kw=dict(height_ratios=[0.7, 0.3]),
                figsize=(10 * len(correction_a.types), 12),
                sharex=True,
            )

            plt.subplots_adjust(hspace=0.1)
            fig.suptitle(name)

            for correction_type, ax in zip(
                processes,
                [axes[:, 0], axes[:, 1]] if len(processes) > 1 else [axes],
            ):
                ax[0].set_title(
                    f"{correction_type}{': ' if correction_type else ''}{KeyTo.latex(window)}",
                    loc="left",
                    fontsize=16,
                )
                for correction, tag_name in zip(
                    [correction_a, correction_b],
                    [correction_tag_a, correction_tag_b],
                ):
                    hep.histplot(
                        correction.unrolled[correction_type][window],
                        correction.edges,
                        label=tag_name,
                        ax=ax[0],
                        histtype="errorbar",
                        yerr=False,
                        xerr=True,
                        markerfacecolor="none",
                    )

                hep.histplot(
                    correction_a.unrolled[correction_type][window] / correction_b.unrolled[correction_type][window],
                    correction_a.edges,
                    label=f"${correction_a.ylabel}_{{{correction_tag_a}}}$ / ${correction_b.ylabel}_{{{correction_tag_b}}}$",
                    ax=ax[1],
                    histtype="errorbar",
                    yerr=False,
                    xerr=True,
                    markerfacecolor="none",
                )

                _max_y_value: float = np.max([np.max(correction.unrolled[correction_type][window]) for correction in [correction_a, correction_b]])

                ax[0].set(
                    xscale="log",
                    ylim=(None, _max_y_value + 0.1),
                    ylabel=correction_a.ylabel,
                )
                ax[1].set(
                    xscale="log",
                    xlabel=correction_a.xlabel,
                    ylabel="ratio",
                )

                hep.cms.label("Own Work", ax=ax[0], loc=2, data=not correction_type == "mc")
                [_ax.legend() for _ax in ax]

            if not os.path.exists(output_directory):
                os.makedirs(name="comparison_plots", exist_ok=True)

            os.makedirs(name=os.path.join(output_directory, name), exist_ok=True)
            for ext in ["pdf", "png"]:
                plt.savefig(
                    os.path.join(
                        output_directory,
                        name,
                        f"comparison_{name}_{correction_tag_a}_{correction_tag_b}_{KeyTo.path(window)}.{ext}",
                    ),
                )
            plt.close("all")

            print(
                " | ".join(
                    [
                        f"Correction {nth_correction + 1}/{len(corrections_a)}: {name}",
                        f"Window {nth_window + 1}/{len(unrolled_keys)}: {KeyTo.prompt(window)}",
                    ]
                    + (["binning adjusted"] if adjusted_binning else [])
                )
            )


if __name__ == "__main__":
    plot_corrections(
        corrections_a=get_corrections(args.input_a),
        corrections_b=get_corrections(args.input_b),
        correction_tag_a=args.tag_a,
        correction_tag_b=args.tag_b,
        output_directory=args.output,
        specific_correction=args.correction_name if args.correction_name else None,
    )
    print("Done")
