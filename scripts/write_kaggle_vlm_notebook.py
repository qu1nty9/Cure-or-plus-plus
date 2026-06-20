#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb"
KAGGLE_DIR = ROOT / "kaggle/vlm_kernel"
KAGGLE_NOTEBOOK_PATH = KAGGLE_DIR / "cure_or_pp_vlm_open_weight_kaggle_v01.ipynb"
KAGGLE_METADATA_PATH = KAGGLE_DIR / "kernel-metadata.json"


def main() -> int:
    notebook = {
        "cells": cells(),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    KAGGLE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NOTEBOOK_PATH, KAGGLE_NOTEBOOK_PATH)
    write_metadata()
    print(NOTEBOOK_PATH)
    print(KAGGLE_NOTEBOOK_PATH)
    print(KAGGLE_METADATA_PATH)
    return 0


def write_metadata() -> None:
    metadata = {
        "id": "YOUR_KAGGLE_USERNAME/cure-or-pp-vlm-open-weight-gpu-v01",
        "title": "CURE-OR++ Open-Weight VLM Real-Transfer GPU Pilot",
        "code_file": "cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "dataset_sources": [
            "YOUR_KAGGLE_USERNAME/cure-or-pp-vlm-real-transfer-v02-private"
        ],
    }
    KAGGLE_METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")],
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")],
    }


def cells() -> list[dict]:
    return [
        md(
            """
# CURE-OR++ Open-Weight VLM Real-Transfer GPU Pilot

This notebook runs an open-weight VLM over the CURE-OR++ real-transfer v0.2
prompt pack. It is intended to produce a reproducible VLM baseline without
paid frontier API calls.

Default model: `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`.
"""
        ),
        code(
            """
from pathlib import Path
import os
import subprocess
import sys
import pandas as pd

os.environ.setdefault('HF_HOME', '/kaggle/working/hf_home')

DATASET_CANDIDATES = [
    Path('/kaggle/input/cure-or-pp-vlm-real-transfer-v02-private'),
    Path('/kaggle/input/cure-or-plus-plus-vlm-real-transfer-v02-private'),
]
DATA_ROOT = next((path for path in DATASET_CANDIDATES if (path / 'reports/vlm_api_track_v01_prompt_pack.jsonl').exists()), None)
if DATA_ROOT is None:
    raise FileNotFoundError('Attach the private CURE-OR++ VLM real-transfer dataset to this notebook.')

DATA_ROOT
"""
        ),
        code(
            """
%pip install -q num2words
"""
        ),
        code(
            """
PROMPT_PACK = DATA_ROOT / 'reports/vlm_api_track_v01_prompt_pack.jsonl'
RUNNER = DATA_ROOT / 'scripts/run_hf_vlm.py'
EVALUATOR = DATA_ROOT / 'scripts/evaluate_vlm_response_pack.py'

MODEL_ID = 'HuggingFaceTB/SmolVLM2-500M-Video-Instruct'
RUN_LIMIT = 210  # set to 5 for smoke testing
RESPONSES = Path('/kaggle/working/vlm_responses_smolvlm2_500m.jsonl')

cmd = [
    sys.executable,
    str(RUNNER),
    '--prompt-pack', str(PROMPT_PACK),
    '--model', MODEL_ID,
    '--output', str(RESPONSES),
    '--cache-dir', '/kaggle/working/vlm_response_cache',
    '--limit', str(RUN_LIMIT),
    '--force',
    '--max-tokens', '8',
]
print(' '.join(cmd))
subprocess.run(cmd, check=True, cwd=str(DATA_ROOT))
"""
        ),
        code(
            """
MODEL_SUMMARY = Path('/kaggle/working/vlm_smolvlm2_model_summary.csv')
RECIPE_TABLE = Path('/kaggle/working/vlm_smolvlm2_recipe_table.csv')
LABEL_TABLE = Path('/kaggle/working/vlm_smolvlm2_label_table.csv')
AUDIT_TABLE = Path('/kaggle/working/vlm_smolvlm2_audit.csv')

cmd = [
    sys.executable,
    str(EVALUATOR),
    '--prompt-pack', str(PROMPT_PACK),
    '--responses', str(RESPONSES),
    '--model-summary', str(MODEL_SUMMARY),
    '--recipe-table', str(RECIPE_TABLE),
    '--label-table', str(LABEL_TABLE),
    '--audit-table', str(AUDIT_TABLE),
]
print(' '.join(cmd))
subprocess.run(cmd, check=True, cwd=str(DATA_ROOT))
"""
        ),
        code(
            """
pd.read_csv(MODEL_SUMMARY)
"""
        ),
        code(
            """
pd.read_csv(RECIPE_TABLE)
"""
        ),
        code(
            """
pd.read_csv(LABEL_TABLE).sort_values(['real_accuracy', 'label']).head(20)
"""
        ),
    ]


if __name__ == "__main__":
    raise SystemExit(main())
