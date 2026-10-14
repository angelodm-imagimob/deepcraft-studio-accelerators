"""Build SuspiciousSkinLesionClassification from the best two-class project.

The source is SkinLesionClassification_aug_phone.improj. Session files are
hardlinked into Data/<Suspicious|Benign>/<diagnosis>/<session>/ so the folder
name keeps the specific issue while the label stays Suspicious or Benign.
Studio augmentation stays the phone recipe already stored in that project.
This script does not write extra augmented images.
"""

from __future__ import annotations

import csv
import os
import re
import shutil
import uuid
from pathlib import Path

VISION = Path(__file__).resolve().parents[2]
SOURCE_ROOT = VISION / "SkinLesionClassification"
SOURCE_IMPROJ = SOURCE_ROOT / "SkinLesionClassification_aug_phone.improj"
SOURCE_MAPPING = SOURCE_ROOT / "Resources" / "rename_mapping.csv"
DIAG_DATA = VISION / "SkinLesionDiagnosisClassification" / "Data"
DEST_ROOT = VISION / "SuspiciousSkinLesionClassification"
PHONE_IDS = (
    "3656ff5e-7206-4f08-8916-160d73d235f3",
    "f5c12bb7-709a-44fb-934d-0c3bbf344992",
    "5502d71e-47f1-466f-9619-6dabd518ad19",
)

ISSUE_BY_CODE = {
    "MEL": ("Suspicious", "Melanoma"),
    "BCC": ("Suspicious", "Basal_Cell_Carcinoma"),
    "SCC": ("Suspicious", "Squamous_Cell_Carcinoma"),
    "ACK": ("Suspicious", "Actinic_Keratosis"),
    "NEV": ("Benign", "Nevus"),
    "SEK": ("Benign", "Seborrheic_Keratosis"),
}
GROUP_BY_ISSUE = {
    "Melanoma": "Suspicious",
    "Basal_Cell_Carcinoma": "Suspicious",
    "Squamous_Cell_Carcinoma": "Suspicious",
    "Actinic_Keratosis": "Suspicious",
    "Nevus": "Benign",
    "Seborrheic_Keratosis": "Benign",
}
EXTRA_SOURCES = (
    ("fluo", "Melanoma"),
    ("fluo", "Squamous_Cell_Carcinoma"),
    ("hiba", "Melanoma"),
    ("hiba", "Squamous_Cell_Carcinoma"),
    ("hiba", "Basal_Cell_Carcinoma"),
    ("hiba", "Actinic_Keratosis"),
)

SESSION_RE = re.compile(r"      <Session name=\"([^\"]+)\".*?</Session>\n", re.S)
PATH_RE = re.compile(r">(/Data/[^<]+)</")
SESSION_ID_RE = re.compile(r'sessionId="([^"]+)"')

LABELXML = """<?xml version="1.0" encoding="UTF-8"?>
<Annotations>
  <Annotation>
    <Object>
      <Name>{label}</Name>
    </Object>
  </Annotation>
</Annotations>
"""

IMSESSION = """<?xml version="1.0" encoding="UTF-8"?>
<ImagimobStudio version="0.9">
  <Timeline id="{session_id}">
    <Tracks>
      <Track name="image" type="imagejpg">
        <PayloadFile>{name}.jpg</PayloadFile>
        <Shape />
      </Track>
      <Track name="label" type="labelxml">
        <PayloadFile>{name}.labelxml</PayloadFile>
        <Shape />
      </Track>
    </Tracks>
  </Timeline>
</ImagimobStudio>
"""


def load_pad_rows() -> dict[str, dict[str, str]]:
    rows = {}
    with SOURCE_MAPPING.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            name = Path(row["current_name"]).stem
            if name in rows:
                raise SystemExit(f"duplicate mapping for {name}")
            group, issue = ISSUE_BY_CODE[row["diagnostic"]]
            if group != row["label"]:
                raise SystemExit(f"{name} label {row['label']} does not match {row['diagnostic']}")
            row["group"] = group
            row["issue"] = issue
            row["source"] = "pad_ufes"
            rows[name] = row
    return rows


def load_extra_rows(pad_rows: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    rows = {}
    for source, issue in EXTRA_SOURCES:
        folder = DIAG_DATA / source / issue
        if not folder.is_dir():
            raise SystemExit(f"missing {folder}")
        for session_dir in sorted(path for path in folder.iterdir() if path.is_dir()):
            name = session_dir.name
            if name in pad_rows or name in rows:
                raise SystemExit(f"duplicate extra session {name}")
            rows[name] = {
                "group": GROUP_BY_ISSUE[issue],
                "issue": issue,
                "source": source,
                "original_name": name + ".jpg",
                "diagnostic": issue,
                "label": GROUP_BY_ISSUE[issue],
                "split": "train",
                "patient_id": "",
                "md5": "",
            }
    return rows


def link_or_copy(source: Path, dest: Path) -> None:
    if dest.exists():
        raise SystemExit(f"refusing to overwrite {dest}")
    try:
        os.link(source, dest)
    except OSError:
        shutil.copy2(source, dest)


def main() -> None:
    if (DEST_ROOT / "Data").exists() or (DEST_ROOT / "SuspiciousSkinLesionClassification.improj").exists():
        raise SystemExit(f"refusing to overwrite {DEST_ROOT}")
    pad_rows = load_pad_rows()
    extra_rows = load_extra_rows(pad_rows)
    known = {**pad_rows, **extra_rows}
    text = SOURCE_IMPROJ.read_text(encoding="utf-8")
    sessions = list(SESSION_RE.finditer(text))
    if len(sessions) != 2617:
        raise SystemExit(f"expected 2617 sessions, found {len(sessions)}")

    pieces = []
    cursor = 0
    mapping_rows = []
    counts: dict[tuple[str, str, str], int] = {}
    for match in sessions:
        pieces.append(text[cursor:match.start()])
        name = match.group(1)
        block = match.group(0)
        if name not in known:
            raise SystemExit(f"no diagnosis for {name}")
        info = known[name]
        paths = PATH_RE.findall(block)
        if len(paths) != 3:
            raise SystemExit(f"{name} has paths {paths}")
        old_dir = f"/Data/{paths[0].split('/')[2]}/{name}/"
        if not all(path.startswith(old_dir) for path in paths):
            raise SystemExit(f"{name} paths are not in {old_dir}")
        new_dir = f"/Data/{info['group']}/{info['issue']}/{name}/"
        block = block.replace(old_dir, new_dir)
        session_id = SESSION_ID_RE.search(block)
        if session_id is None:
            raise SystemExit(f"{name} has no session id")
        source_jpg = SOURCE_ROOT / paths[0].lstrip("/")
        if not source_jpg.is_file():
            raise SystemExit(f"missing {source_jpg}")
        dest_dir = DEST_ROOT / new_dir.strip("/")
        dest_dir.mkdir(parents=True)
        link_or_copy(source_jpg, dest_dir / f"{name}.jpg")
        (dest_dir / f"{name}.labelxml").write_text(
            LABELXML.format(label=info["label"]),
            encoding="utf-8",
        )
        (dest_dir / f"{name}.imsession").write_text(
            IMSESSION.format(session_id=session_id.group(1), name=name),
            encoding="utf-8",
        )
        pieces.append(block)
        cursor = match.end()
        key = (info["group"], info["issue"], info["split"])
        counts[key] = counts.get(key, 0) + 1
        mapping_rows.append(
            {
                "current_path": f"Data/{info['group']}/{info['issue']}/{name}/{name}.jpg",
                "current_name": f"{name}.jpg",
                "group": info["group"],
                "issue": info["issue"],
                "original_name": info.get("original_name", ""),
                "diagnostic": info.get("diagnostic", info["issue"]),
                "label": info["label"],
                "split": info["split"],
                "patient_id": info.get("patient_id", ""),
                "source": info["source"],
                "md5": info.get("md5", ""),
            }
        )
    pieces.append(text[cursor:])
    rewritten = "".join(pieces)
    if "/Data/extra_suspicious/" in rewritten:
        raise SystemExit("extra_suspicious paths remain")
    if rewritten.count("/Data/Suspicious/pad_ufes_") != 0 or rewritten.count("/Data/Benign/pad_ufes_") != 0:
        raise SystemExit("old session paths remain")
    for old in PHONE_IDS:
        if rewritten.count(old) != 1:
            raise SystemExit(f"{old} count is {rewritten.count(old)}")
        rewritten = rewritten.replace(old, str(uuid.uuid4()), 1)
    if rewritten.count("yolo26n") != 2 or "<Degrees>10</Degrees>" not in rewritten:
        raise SystemExit("phone recipe was not preserved")
    if "<Scale>0.2</Scale>" not in rewritten or "<FlipUpDown>0.5</FlipUpDown>" not in rewritten:
        raise SystemExit("phone augmentation was not preserved")

    improj_path = DEST_ROOT / "SuspiciousSkinLesionClassification.improj"
    improj_path.write_text(rewritten, encoding="utf-8")
    shutil.copytree(SOURCE_ROOT / "Models" / "phone", DEST_ROOT / "Models" / "phone")

    resources = DEST_ROOT / "Resources"
    resources.mkdir()
    fieldnames = list(mapping_rows[0])
    with (resources / "rename_mapping.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mapping_rows)

    print(f"sessions {len(mapping_rows)}")
    for key in sorted(counts):
        print(f"{key[0]}/{key[1]} {key[2]} {counts[key]}")


if __name__ == "__main__":
    main()
