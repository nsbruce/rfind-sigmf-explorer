from argparse import ArgumentParser, Namespace
from pathlib import Path

from rfind_sigmf_explorer.sigmf_loader import load_sigmf_dask, load_sigmf_full
from rfind_sigmf_explorer.waterfall_plotter import plot_interactive_waterfall


def make_interactive_waterfall(args: Namespace) -> None:
    sigmf_path = Path(args.sigmf_meta)

    # samples = load_sigmf_full(sigmf_path)
    samples = load_sigmf_dask(sigmf_path)

    plot_interactive_waterfall(samples)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('sigmf_meta', type=str, help="path to sigmf-meta file")
    args = parser.parse_args()
    make_interactive_waterfall(args)


if __name__ == '__main__':
    main()
