#!/usr/bin/env python3
"""Detect objects in the first three images of a folder and print the results.

Usage:
    python3 detect_first_three.py -path ~/path/to/images
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from rfdetr_plus import RFDETR2XLarge

REPO_ROOT = Path(__file__).resolve().parent


def load_env(repo_root: Path = REPO_ROOT) -> None:
    """Load RF_HOME from the .env file in the repo root.

    An already-exported RF_HOME wins. Relative values are resolved against the
    repo root, so the checked-in .env works from any working directory.
    """
    if os.environ.get("RF_HOME"):
        return
    env_file = repo_root / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() != "RF_HOME":
            continue
        path = Path(value.strip().strip('"').strip("'")).expanduser()
        os.environ["RF_HOME"] = str(path if path.is_absolute() else repo_root / path)
        return


DEFAULT_PATH = Path().cwd()
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}


def first_three_images(image_dir: Path) -> list[Path]:
    if not image_dir.is_dir():
        raise SystemExit(f"Image directory not found: {image_dir}")
    images = sorted(p for p in image_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        raise SystemExit(f"No images found in {image_dir}")
    return images[:3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect objects in the first three images of a folder.")
    parser.add_argument("-path", type=Path, default=DEFAULT_PATH, help="Path to the images folder")
    parser.add_argument("--threshold", type=float, default=0.5, help="Minimum confidence (default: 0.5)")
    parser.add_argument(
        "-w", "-weights", "--weights",
        type=Path,
        default=None,
        help="Model weights (.pth). Defaults to rf-detr-xxlarge.pth under RF_HOME.",
    )
    args = parser.parse_args()

    images = first_three_images(args.path.expanduser())

    print("Loading RFDETR2XLarge ...")
    load_env()
    model_kwargs = {}
    if args.weights is not None:
        model_kwargs["pretrain_weights"] = str(args.weights.expanduser())
        print(f"Weights: {model_kwargs['pretrain_weights']}")
    else:
        print(f"Weights: {os.environ.get('RF_HOME', '~/.roboflow/models')}/rf-detr-xxlarge.pth")
    model = RFDETR2XLarge(**model_kwargs)

    paths = [str(p) for p in images]
    print(f"Running inference on {len(paths)} image(s) (threshold={args.threshold}) ...\n")
    results = model.predict(paths, threshold=args.threshold, include_source_image=False)
    if not isinstance(results, list):
        results = [results]

    total = 0
    for path, detections in zip(paths, results):
        print(f"== {Path(path).name} ==")
        if len(detections) == 0:
            print("  (no objects detected)\n")
            continue

        names = detections.data.get("class_name")
        for i, (box, score, class_id) in enumerate(
            zip(detections.xyxy, detections.confidence, detections.class_id), start=1
        ):
            name = str(names[i - 1]) if names is not None else str(class_id)
            x1, y1, x2, y2 = (int(round(v)) for v in box)
            print(f"  {i}. {name:<20}")
            total += 1
        print()

    print(f"Total detections: {total}")


if __name__ == "__main__":
    main()
