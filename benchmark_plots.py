import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


def plotit(stats, python_versions, label):
    labels = ["avro", "fastavro"]
    avro_ops = stats["avro"]
    fastavro_ops = stats["fastavro"]

    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 12))

    bars1 = ax.bar(x - width / 2, avro_ops, width, label="avro", color="orangered")
    bars2 = ax.bar(
        x + width / 2, fastavro_ops, width, label="fastavro", color="dodgerblue"
    )

    ax.set_ylabel("ops/s")
    ax.set_xticks(x)
    ax.set_xticklabels(python_versions)
    ax.set_title("{} benchmark".format(label), color="black", fontweight="bold")
    ax.legend()

    autolabel(ax, bars1)
    autolabel(ax, bars2)

    fig.tight_layout()

    plt.show()


def autolabel(ax, bars):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            "{0:.2f}".format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )


def read_ops_stats(group, python_versions):
    stats = defaultdict(list)
    for python_version in python_versions:
        with open("reports/benchmark-{}.json".format(python_version), "r") as f:
            data = json.loads(f.read())
            for benchmark in data["benchmarks"]:
                if benchmark["group"] == group:
                    if "fastavro" in benchmark["name"]:
                        stats["fastavro"].append(benchmark["stats"]["ops"])
                    else:
                        stats["avro"].append(benchmark["stats"]["ops"])
    return stats


if __name__ == "__main__":
    benchmark_groups = ["Encoders", "Decoders"]
    python_versions = ["python3.7", "python3.8"]

    for bg in benchmark_groups:
        plotit(
            stats=read_ops_stats(bg, python_versions),
            python_versions=python_versions,
            label=bg,
        )
