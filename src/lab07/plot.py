import matplotlib.pyplot as plt
from adjustText import adjust_text


def show_bench_plot(recs: list[dict]):
    """
    Show plot for benchmark results.
    """

    fig, ax = plt.subplots()
    texts = []
    for rec in recs:
        xpoints, ypoints = [], []

        keys = list(rec.keys())[2:]
        for key in keys:
            if rec[key] == '-':
                continue
            xpoints.append(key)
            if rec[key][0] == '>':
                ypoints.append(float(rec[key][1:]))
            else:
                ypoints.append(float(rec[key]))

        ax.plot(xpoints, ypoints, label=rec["Algorithm"], marker="o")
        texts.append(ax.text(xpoints[-1], ypoints[-1], rec["Algorithm"]))



    ax.semilogy()
    ax.grid()
    ax.grid(which="minor", color="0.9")
    ax.margins(0.40)

    # ax.legend(loc='upper left')

    # ax.xlabel("Input size")
    ax.set_xlabel("Input size")
    # ax.ylabel("Time, s")
    ax.set_ylabel("Time, s")

    adjust_text(
        texts,
        only_move={
            "text": "y",
            "static": "y",
            "explode": "y",
            "pull": "y",
        },
        force_text=(1, 1),
        arrowprops=dict(
            arrowstyle="-"
        )
    ) 

    plt.show()


def main():
    """Plot example"""
    import csv
    from pathlib import Path

    path = Path("data/lab07/bench.csv")
    with path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        recs = list(r)

    show_bench_plot(recs)


if __name__ == "__main__":
    main()