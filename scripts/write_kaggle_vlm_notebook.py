#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
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
DEFAULT_MODEL_MATRIX = "configs/vlm_open_weight_model_matrix_v01.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the CURE-OR++ Kaggle GPU VLM notebook and metadata.")
    parser.add_argument("--kaggle-owner", default=DEFAULT_KAGGLE_OWNER)
    parser.add_argument("--kernel-slug", default=DEFAULT_KERNEL_SLUG)
    parser.add_argument("--dataset-slug", default=DEFAULT_DATASET_SLUG)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--run-mode", choices=["smoke", "full"], default="smoke")
    parser.add_argument("--model-matrix", default=DEFAULT_MODEL_MATRIX)
    parser.add_argument("--prompt-pack", default="")
    parser.add_argument("--notebook-path", default=str(NOTEBOOK_PATH.relative_to(ROOT)))
    parser.add_argument("--kaggle-dir", default=str(KAGGLE_DIR.relative_to(ROOT)))
    parser.add_argument("--no-embed-runtime", action="store_true")
    parser.add_argument(
        "--selected-model-slug",
        action="append",
        default=[],
        help="Model slug to run. Repeat for multiple slugs. Empty means enabled_by_default models.",
    )
    args = parser.parse_args()

    model_matrix = json.loads((ROOT / args.model_matrix).read_text(encoding="utf-8"))
    prompt_pack = args.prompt_pack or model_matrix["prompt_pack_path"]

    notebook = {
        "cells": cells(
            run_mode=args.run_mode,
            selected_model_slugs=args.selected_model_slug,
            kaggle_owner=args.kaggle_owner,
            dataset_slug=args.dataset_slug,
            model_matrix=args.model_matrix,
            prompt_pack=prompt_pack,
            embed_runtime=not args.no_embed_runtime,
        ),
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
    notebook_path = resolve_project_path(args.notebook_path)
    kaggle_dir = resolve_project_path(args.kaggle_dir)
    kaggle_notebook_path = kaggle_dir / notebook_path.name
    kaggle_metadata_path = kaggle_dir / "kernel-metadata.json"

    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    kaggle_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(notebook_path, kaggle_notebook_path)
    write_metadata(args, kaggle_metadata_path, notebook_path.name)
    print(notebook_path)
    print(kaggle_notebook_path)
    print(kaggle_metadata_path)
    return 0


def write_metadata(args: argparse.Namespace, metadata_path: Path, code_file: str) -> None:
    existing = {}
    if metadata_path.exists():
        existing = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata = {
        **existing,
        "id": f"{args.kaggle_owner}/{args.kernel_slug}",
        "title": args.title,
        "code_file": code_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "dataset_sources": [
            f"{args.kaggle_owner}/{args.dataset_slug}"
        ],
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


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


def cells(
    *,
    run_mode: str,
    selected_model_slugs: list[str],
    kaggle_owner: str,
    dataset_slug: str,
    model_matrix: str,
    prompt_pack: str,
    embed_runtime: bool,
) -> list[dict]:
    selected_model_slugs_json = json.dumps(selected_model_slugs)
    embedded_runtime_files = {}
    if embed_runtime:
        embedded_runtime_files = {
            model_matrix: (ROOT / model_matrix).read_text(encoding="utf-8"),
            prompt_pack: (ROOT / prompt_pack).read_text(encoding="utf-8"),
            "scripts/run_hf_vlm.py": (ROOT / "scripts/run_hf_vlm.py").read_text(encoding="utf-8"),
            "scripts/evaluate_vlm_response_pack.py": (ROOT / "scripts/evaluate_vlm_response_pack.py").read_text(encoding="utf-8"),
        }
    embedded_runtime_files_json = json.dumps(embedded_runtime_files)
    config_cell = """
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
import pandas as pd

os.environ.setdefault('HF_HOME', '/tmp/cure_or_pp_hf_home')
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# Generated by scripts/write_kaggle_vlm_notebook.py.
RUN_MODE = __RUN_MODE_LITERAL__  # 'smoke' or 'full'
SELECTED_MODEL_SLUGS = __SELECTED_MODEL_SLUGS_LITERAL__  # [] means enabled_by_default models from the matrix.
EMBEDDED_RUNTIME_FILES = __EMBEDDED_RUNTIME_FILES_LITERAL__

PROMPT_PACK_RELATIVE = Path('__PROMPT_PACK_LITERAL__')
MODEL_MATRIX_RELATIVE = Path('__MODEL_MATRIX_LITERAL__')
DATA_RELATIVE = Path('data')
DATASET_CANDIDATES = [
    Path('/kaggle/input/__DATASET_SLUG_LITERAL__'),
    Path('/kaggle/input/datasets/__KAGGLE_OWNER_LITERAL__/__DATASET_SLUG_LITERAL__'),
    Path('/kaggle/input/cure-or-pp-vlm-real-transfer-v02-private'),
    Path('/kaggle/input/cure-or-pp-vlm-real-transfer-v03-private'),
]

def list_input_roots():
    input_root = Path('/kaggle/input')
    if not input_root.exists():
        return []
    return sorted(path for path in input_root.iterdir() if path.is_dir())

def has_data_payload(path):
    return (
        (path / DATA_RELATIVE).exists()
        or (path / 'data.tar').exists()
        or (path / 'data.zip').exists()
    )

def find_data_source_root():
    input_root = Path('/kaggle/input')
    for path in DATASET_CANDIDATES:
        if has_data_payload(path):
            return path
    if input_root.exists():
        payload_candidates = []
        for pattern in ['data', 'data.tar', 'data.zip']:
            payload_candidates.extend(sorted(input_root.rglob(pattern)))
        print('Data payload candidates:', [str(path) for path in payload_candidates[:20]])
        for candidate in payload_candidates:
            root = candidate.parent if candidate.name != 'data' else candidate.parent
            if has_data_payload(root):
                return root
    return None

def materialize_data_root(source_root):
    if (source_root / DATA_RELATIVE).exists():
        return source_root
    unpack_root = Path('/kaggle/working/cure_or_pp_dataset_unpack')
    if unpack_root.exists():
        shutil.rmtree(unpack_root)
    unpack_root.mkdir(parents=True, exist_ok=True)
    data_tar = source_root / 'data.tar'
    data_zip = source_root / 'data.zip'
    if data_tar.exists():
        with tarfile.open(data_tar) as handle:
            handle.extractall(unpack_root)
        return unpack_root
    if data_zip.exists():
        with zipfile.ZipFile(data_zip) as handle:
            handle.extractall(unpack_root)
        return unpack_root
    raise FileNotFoundError(f'No data payload found under {source_root}')

def unpack_runtime_payloads(source_root, runtime_root):
    for name in ['configs', 'reports', 'scripts']:
        source_dir = source_root / name
        target_dir = runtime_root / name
        if source_dir.exists():
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(source_dir, target_dir)
            continue
        source_zip = source_root / f'{name}.zip'
        if source_zip.exists():
            with zipfile.ZipFile(source_zip) as handle:
                handle.extractall(runtime_root)

def write_runtime_overrides(source_root, data_root):
    runtime_root = Path('/kaggle/working/cure_or_pp_runtime_pack')
    runtime_root.mkdir(parents=True, exist_ok=True)
    unpack_runtime_payloads(source_root, runtime_root)
    for relative_path, text in EMBEDDED_RUNTIME_FILES.items():
        target = runtime_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    runtime_data = runtime_root / DATA_RELATIVE
    if runtime_data.exists() or runtime_data.is_symlink():
        if runtime_data.is_symlink() or runtime_data.is_file():
            runtime_data.unlink()
        else:
            shutil.rmtree(runtime_data)
    runtime_data.symlink_to(data_root / DATA_RELATIVE, target_is_directory=True)
    return runtime_root

print('Python:', sys.version)
print('CUDA_VISIBLE_DEVICES:', os.environ.get('CUDA_VISIBLE_DEVICES'))
try:
    subprocess.run(['nvidia-smi'], check=False)
except FileNotFoundError:
    print('nvidia-smi not available')
print('Kaggle input roots:', [path.name for path in list_input_roots()])

DATA_SOURCE_ROOT = find_data_source_root()
if DATA_SOURCE_ROOT is None:
    raise FileNotFoundError(
        'Attach the private CURE-OR++ VLM real-transfer dataset to this notebook. '
        f'Checked explicit candidates: {[str(path) for path in DATASET_CANDIDATES]}; '
        f'available /kaggle/input roots: {[path.name for path in list_input_roots()]}'
    )

DATA_ROOT = materialize_data_root(DATA_SOURCE_ROOT)
RUNTIME_ROOT = write_runtime_overrides(DATA_SOURCE_ROOT, DATA_ROOT)
print('DATA_SOURCE_ROOT:', DATA_SOURCE_ROOT)
print('DATA_ROOT:', DATA_ROOT)
print('RUNTIME_ROOT:', RUNTIME_ROOT)
print('Prompt pack:', RUNTIME_ROOT / PROMPT_PACK_RELATIVE)
print('Model matrix:', RUNTIME_ROOT / MODEL_MATRIX_RELATIVE)
""".replace("__RUN_MODE_LITERAL__", repr(run_mode)).replace(
        "__SELECTED_MODEL_SLUGS_LITERAL__", selected_model_slugs_json
    ).replace(
        "__EMBEDDED_RUNTIME_FILES_LITERAL__", embedded_runtime_files_json
    ).replace(
        "__PROMPT_PACK_LITERAL__", prompt_pack
    ).replace(
        "__MODEL_MATRIX_LITERAL__", model_matrix
    ).replace(
        "__DATASET_SLUG_LITERAL__", dataset_slug
    ).replace(
        "__KAGGLE_OWNER_LITERAL__", kaggle_owner
    )
    return [
        md(
            """
# CURE-OR++ Open-Weight VLM Real-Transfer GPU Matrix

This notebook runs open-weight VLMs over a CURE-OR++ real-transfer prompt pack.
It uses a tiered model matrix so we can smoke-test multiple models before
promoting stable rows to full evaluation.

Default mode: smoke test enabled models from
the configured model matrix.
"""
        ),
        code(config_cell),
        code(
            """
%pip install -q --no-cache-dir --force-reinstall --index-url https://download.pytorch.org/whl/cu121 "torch==2.5.1+cu121" "torchvision==0.20.1+cu121"
%pip install -q --no-cache-dir -U "transformers>=4.57,<5" "accelerate>=1.8,<2" "pillow<12" num2words "qwen-vl-utils>=0.0.8,<0.1"
"""
        ),
        code(
            """
import transformers
import torch

PROMPT_PACK = DATA_ROOT / PROMPT_PACK_RELATIVE
MODEL_MATRIX_PATH = RUNTIME_ROOT / MODEL_MATRIX_RELATIVE
RUNNER = RUNTIME_ROOT / 'scripts/run_hf_vlm.py'
EVALUATOR = RUNTIME_ROOT / 'scripts/evaluate_vlm_response_pack.py'
PROMPT_PACK = RUNTIME_ROOT / PROMPT_PACK_RELATIVE
OUTPUT_ROOT = Path('/kaggle/working/vlm_open_weight_runs') / RUN_MODE
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
CACHE_ROOT = Path('/kaggle/temp/cure_or_pp_vlm_cache') / RUN_MODE
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

for required_path in [PROMPT_PACK, MODEL_MATRIX_PATH, RUNNER, EVALUATOR]:
    if not required_path.exists():
        raise FileNotFoundError(required_path)

matrix = json.loads(MODEL_MATRIX_PATH.read_text())
if RUN_MODE not in {'smoke', 'full'}:
    raise ValueError(f'RUN_MODE must be smoke or full, got {RUN_MODE!r}')

all_models = matrix['models']
if SELECTED_MODEL_SLUGS:
    selected = [model for model in all_models if model['slug'] in set(SELECTED_MODEL_SLUGS)]
    missing = sorted(set(SELECTED_MODEL_SLUGS) - {model['slug'] for model in selected})
    if missing:
        raise ValueError(f'Unknown SELECTED_MODEL_SLUGS: {missing}')
else:
    selected = [model for model in all_models if model.get('enabled_by_default', False)]

print('transformers:', transformers.__version__)
print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('torch cuda arch list:', torch.cuda.get_arch_list())
    print('torch device capability:', torch.cuda.get_device_capability())

pd.DataFrame(selected)[['slug', 'model_id', 'tier', 'status']]
"""
        ),
        code(
            """
def json_arg(value):
    return json.dumps(value or {}, sort_keys=True)

def run_model(model):
    slug = model['slug']
    limit = int(matrix['smoke_limit'] if RUN_MODE == 'smoke' else matrix['full_limit'])
    run_dir = OUTPUT_ROOT / slug
    run_dir.mkdir(parents=True, exist_ok=True)
    responses = run_dir / 'responses.jsonl'
    model_summary = run_dir / 'model_summary.csv'
    recipe_table = run_dir / 'recipe_table.csv'
    label_table = run_dir / 'label_table.csv'
    audit_table = run_dir / 'audit.csv'

    runner_cmd = [
        sys.executable,
        str(RUNNER),
        '--prompt-pack', str(PROMPT_PACK),
        '--provider', model.get('provider', 'huggingface'),
        '--model', model['model_id'],
        '--model-class', model.get('model_class', 'AutoModelForImageTextToText'),
        '--generation-backend', model.get('generation_backend', 'chat_template'),
        '--image-content-key', model.get('image_content_key', 'path'),
        '--output', str(responses),
        '--cache-dir', str(CACHE_ROOT / slug),
        '--force',
        '--max-tokens', str(model.get('max_tokens', 8)),
        '--dtype', model.get('dtype', 'float16'),
        '--processor-kwargs-json', json_arg(model.get('processor_kwargs')),
        '--model-kwargs-json', json_arg(model.get('model_kwargs')),
        '--generate-kwargs-json', json_arg(model.get('generate_kwargs')),
    ]
    if model.get('revision'):
        runner_cmd.extend(['--revision', model['revision']])
    if model.get('trust_remote_code'):
        runner_cmd.append('--trust-remote-code')
    if model.get('device_map'):
        runner_cmd.extend(['--device-map', model['device_map']])
    if model.get('image_max_side'):
        runner_cmd.extend(['--image-max-side', str(int(model['image_max_side']))])
    if model.get('system_prompt') is not None:
        runner_cmd.extend(['--system-prompt', model['system_prompt']])
    smoke_sample_ids = matrix.get('smoke_sample_ids') if RUN_MODE == 'smoke' else None
    if smoke_sample_ids:
        for sample_id in smoke_sample_ids:
            runner_cmd.extend(['--sample-id', sample_id])
    else:
        runner_cmd.extend(['--limit', str(limit)])

    print('\\n=== RUN', slug, model['model_id'], 'limit=', limit, '===')
    print(' '.join(runner_cmd))
    subprocess.run(runner_cmd, check=True, cwd=str(DATA_ROOT))

    eval_cmd = [
        sys.executable,
        str(EVALUATOR),
        '--prompt-pack', str(PROMPT_PACK),
        '--responses', str(responses),
        '--model-summary', str(model_summary),
        '--recipe-table', str(recipe_table),
        '--label-table', str(label_table),
        '--audit-table', str(audit_table),
    ]
    print(' '.join(eval_cmd))
    subprocess.run(eval_cmd, check=True, cwd=str(DATA_ROOT))

    summary = pd.read_csv(model_summary)
    recipe = pd.read_csv(recipe_table)
    label = pd.read_csv(label_table)
    summary.insert(0, 'slug', slug)
    recipe.insert(0, 'slug', slug)
    label.insert(0, 'slug', slug)
    return {'summary': summary, 'recipe': recipe, 'label': label, 'run_dir': run_dir}

results = []
for model in selected:
    try:
        results.append(run_model(model))
    except Exception as exc:
        print(f'FAILED {model["slug"]}: {exc}')
        if RUN_MODE == 'full':
            raise

if not results:
    raise RuntimeError('No successful model runs.')
"""
        ),
        code(
            """
summary_df = pd.concat([item['summary'] for item in results], ignore_index=True)
recipe_df = pd.concat([item['recipe'] for item in results], ignore_index=True)
label_df = pd.concat([item['label'] for item in results], ignore_index=True)

summary_out = OUTPUT_ROOT / 'combined_model_summary.csv'
recipe_out = OUTPUT_ROOT / 'combined_recipe_table.csv'
label_out = OUTPUT_ROOT / 'combined_label_table.csv'
summary_df.to_csv(summary_out, index=False)
recipe_df.to_csv(recipe_out, index=False)
label_df.to_csv(label_out, index=False)

manifest = pd.DataFrame([
    {'slug': item['summary']['slug'].iloc[0], 'run_dir': str(item['run_dir'])}
    for item in results
])
manifest_out = OUTPUT_ROOT / 'run_manifest.csv'
manifest.to_csv(manifest_out, index=False)

print('Combined summary:', summary_out)
print('Combined recipe:', recipe_out)
print('Combined labels:', label_out)
print('Manifest:', manifest_out)
summary_df.sort_values(['real_accuracy', 'clean_accuracy'], ascending=False)
"""
        ),
        code(
            """
recipe_df.sort_values(['slug', 'recipe'])
"""
        ),
        code(
            """
label_df.sort_values(['slug', 'real_accuracy', 'label']).groupby('slug').head(10)
"""
        ),
    ]


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
