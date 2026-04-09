import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATASET_PATH = "cleaned_flood_dataset.csv"


def get_top_feature_correlations(corr_with_target: pd.Series, top_n: int = 8) -> pd.Series:
    """Return top features by absolute correlation with the target."""
    return corr_with_target.reindex(corr_with_target.abs().sort_values(ascending=False).index).head(top_n)


def format_corr_table(series: pd.Series) -> str:
    lines = ["| Feature | Correlation with Flood |", "|---|---:|"]
    for feature, value in series.items():
        lines.append(f"| {feature} | {value:.4f} |")
    return "\n".join(lines)


def main() -> None:
    sns.set_style("whitegrid")

    df = pd.read_csv(DATASET_PATH)
    numeric_df = df.select_dtypes(include=[np.number]).copy()

    if "Flood" not in numeric_df.columns:
        raise ValueError("Expected 'Flood' column in numeric dataset for target comparison.")

    # 1) Full numeric correlation heatmap
    corr = numeric_df.corr(method="pearson")
    plt.figure(figsize=(16, 12))
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, linewidths=0.2)
    plt.title("Parameter Correlation Heatmap (Pearson)", fontsize=14, pad=12)
    plt.tight_layout()
    plt.savefig("parameter_correlation_heatmap.png", dpi=300)
    plt.close()

    # 2) Top feature correlations with Flood target
    corr_with_flood = corr["Flood"].drop("Flood").sort_values(ascending=False)
    top_positive = corr_with_flood.head(6)
    top_negative = corr_with_flood.tail(6)
    top_abs = get_top_feature_correlations(corr_with_flood, top_n=8)

    plt.figure(figsize=(10, 6))
    plot_df = pd.DataFrame(
        {
            "Parameter": top_abs.index,
            "Correlation": top_abs.values,
            "Direction": ["Positive" if x >= 0 else "Negative" for x in top_abs.values],
        }
    )
    sns.barplot(
        data=plot_df,
        x="Correlation",
        y="Parameter",
        hue="Direction",
        dodge=False,
        palette={"Positive": "#1f77b4", "Negative": "#d62728"},
        legend=False,
    )
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Top Parameters Related to Flood (Absolute Correlation)", fontsize=13)
    plt.xlabel("Pearson Correlation with Flood")
    plt.ylabel("Parameters")
    plt.tight_layout()
    plt.savefig("flood_top_parameter_relations.png", dpi=300)
    plt.close()

    # 3) Multivariate pair comparison for strongest related parameters
    selected_for_pairplot = list(top_abs.index[:5]) + ["Flood"]
    pair_df = df[selected_for_pairplot].copy()
    pair_df["Flood"] = pair_df["Flood"].map({0: "Non-Flood", 1: "Flood"})
    pair_plot = sns.pairplot(
        pair_df,
        hue="Flood",
        diag_kind="kde",
        corner=True,
        plot_kws={"alpha": 0.6, "s": 30},
    )
    pair_plot.fig.suptitle("Multivariate Comparison of Top Flood-Related Parameters", y=1.02)
    pair_plot.savefig("multivariate_pairplot_top_parameters.png", dpi=250)
    plt.close("all")

    # 4) Class-wise distribution comparison for top 6 absolute related features
    top_6 = list(top_abs.index[:6])
    melted = df[["Flood"] + top_6].melt(id_vars="Flood", var_name="Parameter", value_name="Value")
    melted["Flood"] = melted["Flood"].map({0: "Non-Flood", 1: "Flood"})

    plt.figure(figsize=(14, 8))
    sns.boxplot(data=melted, x="Parameter", y="Value", hue="Flood")
    plt.title("Parameter Distribution by Flood vs Non-Flood", fontsize=13)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig("flood_vs_nonflood_multivariate_boxplot.png", dpi=300)
    plt.close()

    # 5) Inter-feature high-correlation pairs (possible multicollinearity)
    corr_no_target = corr.drop(index="Flood", columns="Flood")
    upper_mask = np.triu(np.ones(corr_no_target.shape), k=1).astype(bool)
    upper_corr = corr_no_target.where(upper_mask)

    high_pairs = []
    for col in upper_corr.columns:
        for idx in upper_corr.index:
            value = upper_corr.loc[idx, col]
            if pd.notna(value) and abs(value) >= 0.70:
                high_pairs.append((idx, col, value))

    high_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    # 6) Create a concise report for forwarding
    report_lines = [
        "# Multivariate Parameter Relationship Analysis",
        "",
        "Dataset: `cleaned_flood_dataset.csv`",
        "",
        "## What Was Compared",
        "- Pairwise correlations between all numeric parameters",
        "- Direct relation of each parameter with Flood label",
        "- Multivariate comparison (pairplot) of top flood-related parameters",
        "- Flood vs Non-Flood distributions for strongest parameters",
        "",
        "## Top Positive Correlations with Flood",
        format_corr_table(top_positive),
        "",
        "## Top Negative Correlations with Flood",
        format_corr_table(top_negative),
        "",
        "## Strong Inter-Parameter Correlations (|r| >= 0.70)",
    ]

    if high_pairs:
        report_lines.append("| Parameter A | Parameter B | Correlation |")
        report_lines.append("|---|---|---:|")
        for a, b, c in high_pairs[:20]:
            report_lines.append(f"| {a} | {b} | {c:.4f} |")
    else:
        report_lines.append("No very strong pairwise inter-parameter correlations found at threshold |r| >= 0.70.")

    report_lines.extend(
        [
            "",
            "## Generated Visual Files",
            "- `parameter_correlation_heatmap.png`",
            "- `flood_top_parameter_relations.png`",
            "- `multivariate_pairplot_top_parameters.png`",
            "- `flood_vs_nonflood_multivariate_boxplot.png`",
            "",
            "## Interpretation Note",
            "Correlation indicates statistical association, not guaranteed causation."
            " Parameters should be interpreted with domain context (rainfall systems, seasonal cycles, pressure systems).",
        ]
    )

    with open("parameter_relations_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("Multivariate analysis complete.")
    print("Generated files:")
    print(" - parameter_correlation_heatmap.png")
    print(" - flood_top_parameter_relations.png")
    print(" - multivariate_pairplot_top_parameters.png")
    print(" - flood_vs_nonflood_multivariate_boxplot.png")
    print(" - parameter_relations_report.md")


if __name__ == "__main__":
    main()
