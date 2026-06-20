#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb"
KAGGLE_DIR = ROOT / "kaggle/vlm_kernel"
KAGGLE_NOTEBOOK_PATH = KAGGLE_DIR / "cure_or_pp_vlm_open_weight_kaggle_v01.ipynb"
KAGGLE_METADATA_PATH = KAGGLE_DIR / "kernel-metadata.json"
DEFAULT_KAGGLE_OWNER = "yaroslavkholmirzayev"
DEFAULT_KERNEL_SLUG = "cure-or-open-weight-vlm-real-transfer-gpu-pilot"
DEFAULT_DATASET_SLUG = "cure-or-pp-vlm-real-transfer-v02-private"
DEFAULT_TITLE = "CURE-OR++ Open-Weight VLM Real-Transfer GPU Pilot"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the CURE-OR++ Kaggle GPU VLM notebook and metadata.")
    parser.add_argument("--kaggle-owner", default=DEFAULT_KAGGLE_OWNER)
    parser.add_argument("--kernel-slug", default=DEFAULT_KERNEL_SLUG)
    parser.add_argument("--dataset-slug", default=DEFAULT_DATASET_SLUG)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    args = parser.parse_args()

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
    write_metadata(args)
    print(NOTEBOOK_PATH)
    print(KAGGLE_NOTEBOOK_PATH)
    print(KAGGLE_METADATA_PATH)
    return 0


def write_metadata(args: argparse.Namespace) -> None:
    metadata = {
        "id": f"{args.kaggle_owner}/{args.kernel_slug}",
        "title": args.title,
        "code_file": "cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "dataset_sources": [
            f"{args.kaggle_owner}/{args.dataset_slug}"
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

os.environ.setdefault('HF_HOME', '/tmp/cure_or_pp_hf_home')
PROMPT_PACK_RELATIVE = Path('reports/vlm_api_track_v01_prompt_pack.jsonl')
DATASET_CANDIDATES = [
    Path('/kaggle/input/cure-or-pp-vlm-real-transfer-v02-private'),
    Path('/kaggle/input/cure-or-plus-plus-vlm-real-transfer-v02-private'),
    Path('/kaggle/input/datasets/yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v02-private'),
]

def list_input_roots():
    input_root = Path('/kaggle/input')
    if not input_root.exists():
        return []
    return sorted(path for path in input_root.iterdir() if path.is_dir())

def find_data_root():
    input_root = Path('/kaggle/input')
    for path in DATASET_CANDIDATES:
        if (path / PROMPT_PACK_RELATIVE).exists():
            return path
    if input_root.exists():
        prompt_pack_candidates = sorted(input_root.rglob(str(PROMPT_PACK_RELATIVE)))
        print('Prompt pack candidates:', [str(path) for path in prompt_pack_candidates[:20]])
        if prompt_pack_candidates:
            return prompt_pack_candidates[0].parent.parent
    return None

print('Python:', sys.version)
print('CUDA_VISIBLE_DEVICES:', os.environ.get('CUDA_VISIBLE_DEVICES'))
try:
    subprocess.run(['nvidia-smi'], check=False)
except FileNotFoundError:
    print('nvidia-smi not available')
print('Kaggle input roots:', [path.name for path in list_input_roots()])

DATA_ROOT = find_data_root()
if DATA_ROOT is None:
    raise FileNotFoundError(
        'Attach the private CURE-OR++ VLM real-transfer dataset to this notebook. '
        f'Checked explicit candidates: {[str(path) for path in DATASET_CANDIDATES]}; '
        f'available /kaggle/input roots: {[path.name for path in list_input_roots()]}'
    )

print('DATA_ROOT:', DATA_ROOT)
print('Prompt pack:', DATA_ROOT / 'reports/vlm_api_track_v01_prompt_pack.jsonl')
"""
        ),
        code(
            """
%pip install -q --no-cache-dir --force-reinstall --index-url https://download.pytorch.org/whl/cu121 "torch==2.5.1+cu121" "torchvision==0.20.1+cu121"
%pip install -q --no-cache-dir -U "transformers>=4.57,<5" "accelerate>=1.8,<2" "pillow<12" num2words
"""
        ),
        code(
            """
import transformers
import torch

PROMPT_PACK = DATA_ROOT / 'reports/vlm_api_track_v01_prompt_pack.jsonl'
RUNNER = DATA_ROOT / 'scripts/run_hf_vlm.py'
EVALUATOR = DATA_ROOT / 'scripts/evaluate_vlm_response_pack.py'

for required_path in [PROMPT_PACK, RUNNER, EVALUATOR]:
    if not required_path.exists():
        raise FileNotFoundError(required_path)

print('transformers:', transformers.__version__)
print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('torch cuda arch list:', torch.cuda.get_arch_list())
    print('torch device capability:', torch.cuda.get_device_capability())

MODEL_ID = 'HuggingFaceTB/SmolVLM2-500M-Video-Instruct'
RUN_LIMIT = 210
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
    '--dtype', 'float16',
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
