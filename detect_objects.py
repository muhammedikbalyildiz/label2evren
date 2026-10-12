#!/usr/bin/env python3
"""Yerel RF-DETR modeliyle resimlerde nesne tespiti yapar.

Bulunan nesneler labeled.csv dosyasına, hiçbir nesne bulunamayan resimler
unlabeled.csv dosyasına yazılır. Ardından yalnızca labeled.csv'de adı geçen
resimler, bu CSV'deki koordinatlara göre üretilen XML dosyalarıyla birlikte
Evren platformuna uygun ZIP arşivine (JPEGImages/ + Annotations/, txt yok)
paketlenir.
"""

from __future__ import annotations

import argparse
import csv
import os
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from rfdetr_plus import RFDETR2XLarge

REPO_ROOT = Path(__file__).resolve().parent


def load_env(repo_root: Path = REPO_ROOT) -> None:
    """Repo kökündeki .env dosyasından RF_HOME'u okur.

    Değişken zaten ortamda tanımlıysa dokunmaz (üst etkileşim geçerlidir).
    Göreli bir yol verilirse repo köküne göre çözümlenir.
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

THRESHOLD = 0.5
DEFAULT_ZIP = "veri.zip"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}
JPEG_DIR = "JPEGImages"
ANN_DIR = "Annotations"
LABELED_CSV = "labeled.csv"
UNLABELED_CSV = "unlabeled.csv"
LABELED_FIELDS = ("filename", "label", "xmin", "ymin", "xmax", "ymax")

DESCRIPTION = """\
Yerel model (RF-DETR) ile resimlerin bulunduğu dizinde nesne tespiti yapar.

Çıktı dosyaları (ZIP dosyasının yazıldığı klasöre kaydedilir):
  labeled.csv    En az 1 nesne bulunan resimler: dosya adı, etiket ve koordinatlar
  unlabeled.csv  Hiç nesne bulunamayan resimlerin dosya adları
  <zip>          Yalnızca labeled.csv'de adı geçen resimler ve bu CSV'deki
                 koordinatlara göre oluşturulan XML dosyaları
                 (JPEGImages/ + Annotations/, ara txt dosyası yok)

Örnekler:
  detect-objects.py -obj airplane
  detect-objects.py -obj airplane,drone -path ./images -zip veri.zip
  detect-objects.py -obj all -label airplane:drone
  detect-objects.py -help
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="detect-objects.py",
        add_help=False,
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-h", "-help", "--help",
        action="help",
        help="Yardım metnini gösterir ve çıkar.",
    )
    parser.add_argument(
        "-p", "-path", "--path",
        dest="path",
        type=Path,
        default=Path().cwd(),
        metavar="DIZIN",
        help="Resimlerin bulunduğu dizin (varsayılan: güncel dizin).",
    )
    parser.add_argument(
        "-o", "-obj", "--obj",
        dest="objects",
        nargs="+",
        metavar="NESNE",
        help="Tespit edilecek nesne adları (boşluk/virgülle ayrılabilir); "
             "tüm nesneler için 'all' yazın. Zorunludur.",
    )
    parser.add_argument(
        "-z", "-zip", "--zip",
        dest="zip",
        type=Path,
        default=Path(DEFAULT_ZIP),
        metavar="DOSYA",
        help=f"Oluşturulacak ZIP dosyasının adı (varsayılan: {DEFAULT_ZIP}).",
    )
    parser.add_argument(
        "-w", "-weights", "--weights",
        dest="weights",
        type=Path,
        default=None,
        metavar="DOSYA",
        help="Kullanılacak model ağırlıkları (.pth). Verilmezse RF_HOME dizinindeki "
             "rf-detr-xxlarge.pth kullanılır.",
    )
    parser.add_argument(
        "-l", "-label", "--label",
        dest="label",
        nargs="+",
        default=[],
        metavar="ESKI:YENI",
        help="Etiket yeniden adlandırma, ESKİ:YENİ biçiminde; boşluk ve virgülle "
             "ayrılabilir (örn. -label airplane:drone car:automobile).",
    )
    return parser


def collect_images(image_dir: Path) -> list[Path]:
    if not image_dir.is_dir():
        raise SystemExit(f"Hata: Dizin bulunamadı: {image_dir}")
    images = sorted(p for p in image_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        raise SystemExit(f"Hata: Düzende resim bulunamadı: {image_dir}")
    return images


def parse_names(values: list[str]) -> list[str]:
    return [part.strip().lower() for value in values for part in value.split(",") if part.strip()]


def parse_label_map(values: list[str]) -> dict[str, str]:
    """-label ESKİ:YENİ girdilerini {eski_kucuk: yeni} sözlüğüne çevirir."""
    mapping: dict[str, str] = {}
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if not item:
                continue
            if ":" not in item:
                raise SystemExit(f"Hata: Geçersiz -label değeri (biçim ESKİ:YENİ): {item}")
            old, new = (part.strip() for part in item.split(":", 1))
            if not old or not new:
                raise SystemExit(f"Hata: Geçersiz -label değeri (biçim ESKİ:YENİ): {item}")
            mapping[old.lower()] = new
    if not mapping:
        raise SystemExit("Hata: -label sonrasında değer verilmedi.")
    return mapping


def resolve_wanted(
    wanted: list[str], known: set[str], label_map: dict[str, str]
) -> tuple[set[str], list[str]]:
    """İstenen adları gerçek model sınıflarına bağlar.

    Ad hem orijinal sınıf (airplane) hem de yeniden adlandırılmış hedef
    (-label airplane:drone için 'drone') olarak verilebilir.
    """
    by_target: dict[str, set[str]] = {}
    for old, new in label_map.items():
        by_target.setdefault(new.lower(), set()).add(old)

    model_names: set[str] = set()
    missing: list[str] = []
    for name in wanted:
        if name in known:
            model_names.add(name)
            continue
        sources = {s for s in by_target.get(name, set()) if s in known}
        if sources:
            model_names.update(sources)
            continue
        missing.append(name)
    return model_names, missing


def image_size(image_path: Path) -> tuple[int, int]:
    from PIL import Image

    with Image.open(image_path) as image:
        return image.size


def clamp_box(
    x1: int, y1: int, x2: int, y2: int, width: int, height: int
) -> tuple[int, int, int, int]:
    """Kutuyu resim sınırları içinde ve sıralı (x1 <= x2, y1 <= y2) tutar."""
    x1 = min(max(x1, 0), width - 1)
    x2 = min(max(x2, 0), width - 1)
    y1 = min(max(y1, 0), height - 1)
    y2 = min(max(y2, 0), height - 1)
    return x1, y1, max(x1, x2), max(y1, y2)


def voc_xml(image_path: Path, rows: list[tuple[str, int, int, int, int]]) -> str:
    """CSV satırlarından Pascal VOC XML üretir (nesnesiz XML = boş görsel)."""
    from PIL import Image

    with Image.open(image_path) as image:
        width, height = image.size
        depth = len(image.getbands())

    objects = []
    for label, x1, y1, x2, y2 in rows:
        x1, y1, x2, y2 = clamp_box(x1, y1, x2, y2, width, height)
        objects.append(
            "  <object>\n"
            f"    <name>{escape(label)}</name>\n"
            "    <pose>Unspecified</pose>\n"
            "    <truncated>0</truncated>\n"
            "    <difficult>0</difficult>\n"
            "    <bndbox>\n"
            f"      <xmin>{x1}</xmin>\n"
            f"      <ymin>{y1}</ymin>\n"
            f"      <xmax>{x2}</xmax>\n"
            f"      <ymax>{y2}</ymax>\n"
            "    </bndbox>\n"
            "  </object>\n"
        )
    return (
        "<annotation>\n"
        f"  <folder>{JPEG_DIR}</folder>\n"
        f"  <filename>{escape(image_path.name)}</filename>\n"
        f"  <path>{escape(str(image_path.resolve()))}</path>\n"
        "  <source>\n"
        "    <database>Unknown</database>\n"
        "  </source>\n"
        "  <size>\n"
        f"    <width>{width}</width>\n"
        f"    <height>{height}</height>\n"
        f"    <depth>{depth}</depth>\n"
        "  </size>\n"
        "  <segmented>0</segmented>\n"
        + "".join(objects)
        + "</annotation>\n"
    )


def write_csv(path: Path, fields: tuple[str, ...], rows: list[tuple]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(fields)
        writer.writerows(rows)


def read_labeled_csv(path: Path) -> dict[str, list[tuple[str, int, int, int, int]]]:
    """labeled.csv'yi {dosya adı: [(etiket, x1, y1, x2, y2), ...]} olarak okur."""
    labeled: dict[str, list[tuple[str, int, int, int, int]]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            labeled.setdefault(row["filename"], []).append(
                (
                    row["label"],
                    int(row["xmin"]),
                    int(row["ymin"]),
                    int(row["xmax"]),
                    int(row["ymax"]),
                )
            )
    return labeled


def build_zip(
    zip_path: Path,
    labeled: dict[str, list[tuple[str, int, int, int, int]]],
    images_by_name: dict[str, Path],
) -> tuple[int, int]:
    """Yalnızca labeled.csv'deki resimleri XML'leriyle birlikte ZIP'e yazar."""
    zip_path = zip_path.expanduser()
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    written_images = 0
    written_xml = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for filename, rows in labeled.items():
            image_path = images_by_name.get(filename.lower())
            if image_path is None:
                continue
            archive.write(image_path, f"{JPEG_DIR}/{image_path.name}")
            archive.writestr(f"{ANN_DIR}/{image_path.stem}.xml", voc_xml(image_path, rows))
            written_images += 1
            written_xml += 1
    return written_images, written_xml


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    wanted = parse_names(args.objects or [])
    if not wanted:
        raise SystemExit(
            "Hata: -obj / -o / --obj parametresi zorunludur "
            "(tüm nesneler için 'all' yazın)."
        )

    label_map = parse_label_map(args.label) if args.label else {}
    images = collect_images(args.path.expanduser())

    zip_path = args.zip.expanduser()
    out_dir = zip_path.parent if str(zip_path.parent) else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Yerel model yükleniyor (RFDETR2XLarge) ...", flush=True)
    load_env()
    model_kwargs = {}
    if args.weights is not None:
        model_kwargs["pretrain_weights"] = str(args.weights.expanduser())
        print(f"Model ağırlıkları: {model_kwargs['pretrain_weights']}", flush=True)
    else:
        print(f"Model ağırlıkları: {os.environ.get('RF_HOME', '~/.roboflow/models')}/rf-detr-xxlarge.pth", flush=True)
    model = RFDETR2XLarge(**model_kwargs)
    known = {str(n).lower() for n in model.class_names}

    model_names: set[str] | None = None
    if "all" not in wanted:
        model_names, missing = resolve_wanted(wanted, known, label_map)
        if missing:
            raise SystemExit(
                "Bilinmeyen nesne adı: " + ", ".join(missing) + "\n"
                "Kullanılabilir adlar: " + ", ".join(sorted(known))
            )

    if label_map:
        print(
            "Etiket yeniden adlandırma: "
            + ", ".join(f"{old} -> {new}" for old, new in sorted(label_map.items())),
            flush=True,
        )
    hedef = "tüm nesneler" if model_names is None else ", ".join(sorted(model_names))
    print(f"{len(images)} resimde {hedef} aranıyor (eşik={THRESHOLD}) ...\n", flush=True)

    labeled_rows: list[tuple] = []
    unlabeled_rows: list[tuple] = []
    for idx, image in enumerate(images, start=1):
        detections = model.predict(str(image), threshold=THRESHOLD, include_source_image=False)
        names = detections.data.get("class_name")

        hits: list[tuple[str, int, int, int, int]] = []
        for i, (box, _score, class_id) in enumerate(
            zip(detections.xyxy, detections.confidence, detections.class_id)
        ):
            raw = str(names[i]) if names is not None else str(class_id)
            if model_names is not None and raw.lower() not in model_names:
                continue
            label = label_map.get(raw.lower(), raw)
            x1, y1, x2, y2 = (int(round(v)) for v in box)
            hits.append((label, x1, y1, x2, y2))

        print(f"[{idx}/{len(images)}] {image.name}: {len(hits)} nesne", flush=True)
        if hits:
            width, height = image_size(image)
            for label, x1, y1, x2, y2 in hits:
                x1, y1, x2, y2 = clamp_box(x1, y1, x2, y2, width, height)
                print(f"    {label:<24} ({x1}, {y1}) - ({x2}, {y2})")
                labeled_rows.append((image.name, label, x1, y1, x2, y2))
        else:
            print("    nesne bulunamadı -> unlabeled.csv")
            unlabeled_rows.append((image.name,))

    labeled_csv = out_dir / LABELED_CSV
    unlabeled_csv = out_dir / UNLABELED_CSV
    write_csv(labeled_csv, LABELED_FIELDS, labeled_rows)
    write_csv(unlabeled_csv, ("filename",), unlabeled_rows)

    labeled = read_labeled_csv(labeled_csv)
    images_by_name = {image.name.lower(): image for image in images}
    zip_images, zip_xml = build_zip(zip_path, labeled, images_by_name)

    labeled_files = len(labeled)
    unlabeled_files = len(unlabeled_rows)
    print(f"\n{labeled_csv.resolve()}: {labeled_files} resim, {len(labeled_rows)} kutu")
    print(f"{unlabeled_csv.resolve()}: {unlabeled_files} resim")
    print(f"{zip_path.resolve()}: {zip_images} resim, {zip_xml} XML ({JPEG_DIR}/ + {ANN_DIR}/)")
    print(f"\nToplam nesne: {len(labeled_rows)}")


if __name__ == "__main__":
    main()
