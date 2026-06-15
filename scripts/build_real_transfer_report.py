#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import random
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SAMPLES = 5000
BOOTSTRAP_SEED = 20260616

MODEL_SPECS = [
    {
        "model_slug": "clip_vit_b16",
        "model_name": "CLIP ViT-B/16",
        "predictions": "results/clip_vit_b16_real_transfer_v02_predictions.csv",
    },
    {
        "model_slug": "clip_vit_b32",
        "model_name": "CLIP ViT-B/32",
        "predictions": "results/clip_vit_b32_real_transfer_v02_predictions.csv",
    },
    {
        "model_slug": "openclip_vit_b32_laion2b",
        "model_name": "OpenCLIP ViT-B/32 LAION-2B",
        "predictions": "results/openclip_vit_b32_laion2b_real_transfer_v02_predictions.csv",
    },
    {
        "model_slug": "openclip_vit_b16_datacomp_xl",
        "model_name": "OpenCLIP ViT-B/16 DataComp-XL",
        "predictions": "results/openclip_vit_b16_datacomp_xl_real_transfer_v02_predictions.csv",
    },
]

PIPELINE_DISPLAY = {
    "messenger_upload_download": "Messenger upload/download",
    "phone_screenshot_resave": "Phone screenshot/resave",
    "video_call_frame_capture": "Video-call frame capture",
}

PIPELINE_ORDER = [
    "messenger_upload_download",
    "phone_screenshot_resave",
    "video_call_frame_capture",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build source-matched real-transfer v0.2 report tables.")
    parser.add_argument("--manifest", default="data/real_transfer/v02/manifest.csv")
    parser.add_argument("--model-table", default="reports/real_transfer_v02_model_pipeline_table.csv")
    parser.add_argument("--pipeline-table", default="reports/real_transfer_v02_pipeline_consensus_table.csv")
    parser.add_argument("--label-table", default="reports/real_transfer_v02_label_failure_table.csv")
    parser.add_argument("--markdown", default="reports/real_transfer_v02_results.md")
    args = parser.parse_args()

    manifest_rows = load_csv(resolve_project_path(args.manifest))
    source_paths = sorted({row["source_path"] for row in manifest_rows})
    labels = sorted({row["label"] for row in manifest_rows})

    model_rows = []
    label_rows = []
    for spec in MODEL_SPECS:
        predictions_path = resolve_project_path(spec["predictions"])
        predictions = load_csv(predictions_path)
        model_rows.extend(build_model_rows(spec, predictions, source_paths))
        label_rows.extend(build_label_rows(spec, predictions, source_paths))

    pipeline_rows = build_pipeline_rows(model_rows)

    write_csv(resolve_project_path(args.model_table), model_rows, MODEL_TABLE_FIELDS)
    write_csv(resolve_project_path(args.pipeline_table), pipeline_rows, PIPELINE_TABLE_FIELDS)
    write_csv(resolve_project_path(args.label_table), label_rows, LABEL_TABLE_FIELDS)
    write_markdown(
        resolve_project_path(args.markdown),
        manifest_rows,
        source_paths,
        labels,
        model_rows,
        pipeline_rows,
        label_rows,
    )

    print(f"Manifest rows: {len(manifest_rows)}")
    print(f"Source images: {len(source_paths)}")
    print(f"Labels: {len(labels)}")
    print(f"Model-pipeline rows: {len(model_rows)}")
    print(f"Pipeline consensus rows: {len(pipeline_rows)}")
    print(f"Label rows: {len(label_rows)}")
    print(f"Wrote {resolve_project_path(args.markdown)}")
    return 0


MODEL_TABLE_FIELDS = [
    "model_name",
    "model_slug",
    "pipeline",
    "pipeline_name",
    "matched_clean_n",
    "matched_clean_accuracy",
    "matched_clean_accuracy_ci_low",
    "matched_clean_accuracy_ci_high",
    "matched_clean_mean_confidence",
    "real_n",
    "real_accuracy",
    "real_accuracy_ci_low",
    "real_accuracy_ci_high",
    "real_mean_confidence",
    "accuracy_drop_vs_matched_clean",
    "accuracy_drop_ci_low",
    "accuracy_drop_ci_high",
    "confidence_shift_vs_matched_clean",
    "source_pipeline_pair_count",
    "both_repeats_correct_rate",
    "any_repeat_correct_rate",
    "repeat_prediction_agreement_rate",
]

PIPELINE_TABLE_FIELDS = [
    "pipeline",
    "pipeline_name",
    "model_count",
    "mean_real_accuracy",
    "mean_accuracy_drop_vs_matched_clean",
    "min_real_accuracy",
    "max_accuracy_drop_vs_matched_clean",
    "worst_model",
]

LABEL_TABLE_FIELDS = [
    "model_name",
    "model_slug",
    "label",
    "matched_clean_n",
    "matched_clean_accuracy",
    "real_n",
    "real_accuracy",
    "accuracy_drop_vs_matched_clean",
]


def build_model_rows(spec: dict[str, str], predictions: list[dict[str, str]], source_paths: list[str]) -> list[dict]:
    source_set = set(map(normalize_path, source_paths))
    clean_rows = [
        row
        for row in predictions
        if row["family"] == "clean" and normalize_path(row["image_path"]) in source_set
    ]
    clean_accuracy = accuracy(clean_rows)
    clean_confidence = mean_float(clean_rows, "confidence")

    output = []
    for pipeline in PIPELINE_ORDER:
        real_rows = [row for row in predictions if row["family"] == "real_transfer" and row["recipe"] == pipeline]
        real_accuracy = accuracy(real_rows)
        real_confidence = mean_float(real_rows, "confidence")
        repeat_stats = summarize_repeats(real_rows)
        bootstrap = bootstrap_source_matched(
            clean_rows=clean_rows,
            real_rows=real_rows,
            source_paths=source_paths,
            seed=f"{BOOTSTRAP_SEED}:{spec['model_slug']}:{pipeline}",
        )
        output.append(
            {
                "model_name": spec["model_name"],
                "model_slug": spec["model_slug"],
                "pipeline": pipeline,
                "pipeline_name": PIPELINE_DISPLAY[pipeline],
                "matched_clean_n": len(clean_rows),
                "matched_clean_accuracy": clean_accuracy,
                "matched_clean_accuracy_ci_low": bootstrap["clean_accuracy_ci_low"],
                "matched_clean_accuracy_ci_high": bootstrap["clean_accuracy_ci_high"],
                "matched_clean_mean_confidence": clean_confidence,
                "real_n": len(real_rows),
                "real_accuracy": real_accuracy,
                "real_accuracy_ci_low": bootstrap["real_accuracy_ci_low"],
                "real_accuracy_ci_high": bootstrap["real_accuracy_ci_high"],
                "real_mean_confidence": real_confidence,
                "accuracy_drop_vs_matched_clean": clean_accuracy - real_accuracy,
                "accuracy_drop_ci_low": bootstrap["accuracy_drop_ci_low"],
                "accuracy_drop_ci_high": bootstrap["accuracy_drop_ci_high"],
                "confidence_shift_vs_matched_clean": real_confidence - clean_confidence,
                **repeat_stats,
            }
        )
    return output


def build_label_rows(spec: dict[str, str], predictions: list[dict[str, str]], source_paths: list[str]) -> list[dict]:
    source_set = set(map(normalize_path, source_paths))
    labels = sorted({row["label"] for row in predictions if row["family"] == "real_transfer"})
    output = []
    for label in labels:
        clean_rows = [
            row
            for row in predictions
            if row["family"] == "clean" and normalize_path(row["image_path"]) in source_set and row["label"] == label
        ]
        real_rows = [row for row in predictions if row["family"] == "real_transfer" and row["label"] == label]
        clean_accuracy = accuracy(clean_rows)
        real_accuracy = accuracy(real_rows)
        output.append(
            {
                "model_name": spec["model_name"],
                "model_slug": spec["model_slug"],
                "label": label,
                "matched_clean_n": len(clean_rows),
                "matched_clean_accuracy": clean_accuracy,
                "real_n": len(real_rows),
                "real_accuracy": real_accuracy,
                "accuracy_drop_vs_matched_clean": clean_accuracy - real_accuracy,
            }
        )
    return sorted(output, key=lambda row: (float(row["real_accuracy"]), -float(row["accuracy_drop_vs_matched_clean"])))


def build_pipeline_rows(model_rows: list[dict]) -> list[dict]:
    output = []
    for pipeline in PIPELINE_ORDER:
        rows = [row for row in model_rows if row["pipeline"] == pipeline]
        worst = max(rows, key=lambda row: float(row["accuracy_drop_vs_matched_clean"]))
        output.append(
            {
                "pipeline": pipeline,
                "pipeline_name": PIPELINE_DISPLAY[pipeline],
                "model_count": len(rows),
                "mean_real_accuracy": mean([float(row["real_accuracy"]) for row in rows]),
                "mean_accuracy_drop_vs_matched_clean": mean(
                    [float(row["accuracy_drop_vs_matched_clean"]) for row in rows]
                ),
                "min_real_accuracy": min(float(row["real_accuracy"]) for row in rows),
                "max_accuracy_drop_vs_matched_clean": max(
                    float(row["accuracy_drop_vs_matched_clean"]) for row in rows
                ),
                "worst_model": worst["model_name"],
            }
        )
    return sorted(output, key=lambda row: float(row["mean_accuracy_drop_vs_matched_clean"]), reverse=True)


def summarize_repeats(rows: list[dict[str, str]]) -> dict[str, float | int]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["source_path"], row["recipe"])].append(row)

    both_correct = 0
    any_correct = 0
    agreed = 0
    for pair_rows in grouped.values():
        correct_values = [int(row["correct"]) for row in pair_rows]
        predictions = {row["predicted_label"] for row in pair_rows}
        if correct_values and all(correct_values):
            both_correct += 1
        if any(correct_values):
            any_correct += 1
        if len(predictions) == 1:
            agreed += 1

    denom = len(grouped)
    return {
        "source_pipeline_pair_count": denom,
        "both_repeats_correct_rate": both_correct / denom if denom else math.nan,
        "any_repeat_correct_rate": any_correct / denom if denom else math.nan,
        "repeat_prediction_agreement_rate": agreed / denom if denom else math.nan,
    }


def bootstrap_source_matched(
    *,
    clean_rows: list[dict[str, str]],
    real_rows: list[dict[str, str]],
    source_paths: list[str],
    seed: str,
) -> dict[str, float]:
    clean_by_source = {normalize_path(row["image_path"]): int(row["correct"]) for row in clean_rows}
    real_by_source: dict[str, list[int]] = defaultdict(list)
    for row in real_rows:
        real_by_source[normalize_path(row["source_path"])].append(int(row["correct"]))

    clean_values = []
    real_values = []
    drop_values = []
    rng = random.Random(seed)
    normalized_sources = [normalize_path(path) for path in source_paths]
    sample_size = len(normalized_sources)

    for _ in range(BOOTSTRAP_SAMPLES):
        sampled_sources = [normalized_sources[rng.randrange(sample_size)] for _ in range(sample_size)]
        sampled_clean = [clean_by_source[source] for source in sampled_sources if source in clean_by_source]
        sampled_real = [
            ok
            for source in sampled_sources
            for ok in real_by_source.get(source, [])
        ]
        clean_acc = mean(sampled_clean)
        real_acc = mean(sampled_real)
        clean_values.append(clean_acc)
        real_values.append(real_acc)
        drop_values.append(clean_acc - real_acc)

    return {
        "clean_accuracy_ci_low": quantile(clean_values, 0.025),
        "clean_accuracy_ci_high": quantile(clean_values, 0.975),
        "real_accuracy_ci_low": quantile(real_values, 0.025),
        "real_accuracy_ci_high": quantile(real_values, 0.975),
        "accuracy_drop_ci_low": quantile(drop_values, 0.025),
        "accuracy_drop_ci_high": quantile(drop_values, 0.975),
    }


def write_markdown(
    path: Path,
    manifest_rows: list[dict[str, str]],
    source_paths: list[str],
    labels: list[str],
    model_rows: list[dict],
    pipeline_rows: list[dict],
    label_rows: list[dict],
) -> None:
    metadata = summarize_capture_metadata(manifest_rows)
    lines = [
        "# Real-Transfer v0.2 Results",
        "",
        "This report uses the source-matched real-transfer comparison: each model's real-transfer accuracy is compared against its clean accuracy on the 30 source images used to create the transferred outputs.",
        "",
        "## Protocol Status",
        "",
        markdown_table(
            ["Item", "Value"],
            [
                ["Transferred outputs", str(len(manifest_rows))],
                ["Source images", str(len(source_paths))],
                ["Labels", str(len(labels))],
                ["Pipelines", str(len(PIPELINE_ORDER))],
                ["Repeats per source/pipeline", "2"],
                ["Capture device", metadata["capture_device"]],
                ["Messenger pipeline", metadata["pipeline_variants"].get("messenger_upload_download", "")],
                ["Screenshot pipeline", metadata["pipeline_variants"].get("phone_screenshot_resave", "")],
                ["Video-call pipeline", metadata["pipeline_variants"].get("video_call_frame_capture", "")],
            ],
        ),
        "",
        "## Figures",
        "",
        "![Source-matched accuracy drops with bootstrap confidence intervals](../results/real_transfer_v02_source_matched_drops.png)",
        "",
        "![Real-transfer accuracy heatmap](../results/real_transfer_v02_accuracy_heatmap.png)",
        "",
        "## Model x Pipeline Results",
        "",
        markdown_table(
            [
                "Model",
                "Pipeline",
                "Clean src.",
                "Real acc. (95% CI)",
                "Drop (95% CI)",
                "Both repeats",
                "Any repeat",
                "Repeat agree",
            ],
            [
                [
                    row["model_name"],
                    row["pipeline_name"],
                    fmt_pct(row["matched_clean_accuracy"]),
                    fmt_interval(
                        row["real_accuracy"],
                        row["real_accuracy_ci_low"],
                        row["real_accuracy_ci_high"],
                    ),
                    fmt_interval(
                        row["accuracy_drop_vs_matched_clean"],
                        row["accuracy_drop_ci_low"],
                        row["accuracy_drop_ci_high"],
                    ),
                    fmt_pct(row["both_repeats_correct_rate"]),
                    fmt_pct(row["any_repeat_correct_rate"]),
                    fmt_pct(row["repeat_prediction_agreement_rate"]),
                ]
                for row in model_rows
            ],
        ),
        "",
        "## Pipeline Consensus",
        "",
        markdown_table(
            ["Pipeline", "Mean real acc.", "Mean drop", "Min acc.", "Max drop", "Worst model"],
            [
                [
                    row["pipeline_name"],
                    fmt_pct(row["mean_real_accuracy"]),
                    fmt_pct(row["mean_accuracy_drop_vs_matched_clean"]),
                    fmt_pct(row["min_real_accuracy"]),
                    fmt_pct(row["max_accuracy_drop_vs_matched_clean"]),
                    row["worst_model"],
                ]
                for row in pipeline_rows
            ],
        ),
        "",
        "## Weakest Label Rows",
        "",
        markdown_table(
            ["Model", "Label", "Clean src.", "Real acc.", "Drop"],
            [
                [
                    row["model_name"],
                    row["label"],
                    fmt_pct(row["matched_clean_accuracy"]),
                    fmt_pct(row["real_accuracy"]),
                    fmt_pct(row["accuracy_drop_vs_matched_clean"]),
                ]
                for row in sorted(
                    label_rows,
                    key=lambda row: (float(row["real_accuracy"]), -float(row["accuracy_drop_vs_matched_clean"])),
                )[:16]
            ],
        ),
        "",
        "## Interpretation",
        "",
        "- Real app/device transfer is now evaluated, not only scaffolded.",
        "- Collector-supplied metadata identifies the capture device as iPhone 15 Pro, the messenger pipeline as WhatsApp, and the video-call/video-transmission pipeline as FaceTime.",
        "- The observed drops are moderate rather than catastrophic, which is useful: the block acts as a realism guardrail for the larger simulated and native CURE-OR benchmark.",
        "- Source-level bootstrap intervals are wide because the real-transfer block intentionally uses 30 source images; this supports cautious interpretation rather than overclaiming small pipeline differences.",
        "- The strongest claim is model- and pipeline-dependent sensitivity, not a universal collapse under every real transfer pipeline.",
        "- Per-file capture dates are not manually asserted here; they can be extracted from image metadata where present if needed for the final release.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_capture_metadata(rows: list[dict[str, str]]) -> dict:
    devices = sorted({row.get("capture_device", "").strip() for row in rows if row.get("capture_device", "").strip()})
    variants: dict[str, str] = {}
    for recipe in PIPELINE_ORDER:
        recipe_variants = sorted(
            {row.get("pipeline_variant", "").strip() for row in rows if row.get("recipe") == recipe and row.get("pipeline_variant", "").strip()}
        )
        variants[recipe] = "; ".join(recipe_variants)
    return {
        "capture_device": "; ".join(devices),
        "pipeline_variants": variants,
    }


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def accuracy(rows: list[dict[str, str]]) -> float:
    if not rows:
        return math.nan
    return sum(int(row["correct"]) for row in rows) / len(rows)


def mean_float(rows: list[dict[str, str]], key: str) -> float:
    if not rows:
        return math.nan
    return mean([float(row[key]) for row in rows])


def mean(values: list[float]) -> float:
    values = [value for value in values if not math.isnan(value)]
    return sum(values) / len(values) if values else math.nan


def quantile(values: list[float], q: float) -> float:
    if not values:
        return math.nan
    sorted_values = sorted(values)
    position = (len(sorted_values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[int(position)]
    lower_value = sorted_values[lower]
    upper_value = sorted_values[upper]
    return lower_value + (upper_value - lower_value) * (position - lower)


def fmt_pct(value: object) -> str:
    number = float(value)
    if math.isnan(number):
        return ""
    return f"{number * 100:.1f}%"


def fmt_interval(value: object, low: object, high: object) -> str:
    return f"{fmt_pct(value)} [{fmt_pct(low)}, {fmt_pct(high)}]"


def normalize_path(path: str) -> str:
    return str(Path(path))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
