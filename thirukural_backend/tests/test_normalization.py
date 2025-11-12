import json
from pathlib import Path
from typing import Any, Dict, List
import importlib
import sys

import pytest

# Point sys.path to allow importing src.api.main
BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def _write_temp_dataset(tmp_path: Path, data: List[Dict[str, Any]]) -> Path:
    data_dir = tmp_path / "src" / "api" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    data_path = data_dir / "thirukural.json"
    with data_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data_path


def _reload_with_dataset(tmp_path: Path, dataset: List[Dict[str, Any]]):
    # Create temp copy of module with overridden _DATA_FILE_PATH
    temp_dir = tmp_path / "src" / "api"
    temp_dir.mkdir(parents=True, exist_ok=True)
    data_path = _write_temp_dataset(tmp_path, dataset)

    # Copy original main.py content into temp module
    original_main_path = BASE_DIR / "src" / "api" / "main.py"
    temp_main_path = temp_dir / "main.py"
    temp_main_path.write_text(original_main_path.read_text(encoding="utf-8"), encoding="utf-8")

    # Create __init__ for package
    (tmp_path / "src" / "api" / "__init__.py").write_text("", encoding="utf-8")
    # Models file copy to support import
    models_src = BASE_DIR / "src" / "api" / "models.py"
    (tmp_path / "src" / "api" / "models.py").write_text(models_src.read_text(encoding="utf-8"), encoding="utf-8")

    # Patch the data file path in the temp main.py
    content = temp_main_path.read_text(encoding="utf-8")
    content = content.replace(
        'os.path.join(os.path.dirname(__file__), "data", "thirukural.json")',
        f'"{str(data_path)}"'
    )
    temp_main_path.write_text(content, encoding="utf-8")

    # Import the temp module
    sys.path.insert(0, str(tmp_path))
    try:
        module = importlib.import_module("src.api.main")
        importlib.reload(module)
        return module
    finally:
        sys.path.pop(0)


def test_normalization_new_schema_minimal(tmp_path: Path):
    dataset = [
        {
            "Number": 1,
            "Line1": "அகர முதல எழுத்தெல்லாம்",
            "Line2": "ஆதி பகவன் முதற்றே உலகு",
            "Translation": "As the letter A is the first of all letters, so is the Eternal God first in the world."
        }
    ]
    mod = _reload_with_dataset(tmp_path, dataset)
    assert isinstance(mod._DATASET, list)
    assert len(mod._DATASET) == 1
    item = mod._DATASET[0]
    assert item["number"] == 1
    assert item["kural"].count("\n") == 1
    assert "அகர முதல" in item["kural"]
    assert "ஆதி பகவன்" in item["kural"]
    assert "Eternal God" in item["translation"]
    assert item.get("section") is None
    assert item.get("chapter") is None


def test_normalization_fallbacks_translation(tmp_path: Path):
    # No Translation; use couplet then explanation
    dataset = [
        {
            "Number": "2",
            "Line1": "கற்றதனால் ஆய பயனென்கொல்",
            "Line2": "வாலறிவன் நற்றாள் தொழாஅர் எனின்",
            "couplet": "What profit have those derived from learning, who worship not the good feet of Him who is pure knowledge?"
        },
        {
            "Number": 3,
            "Line1": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்",
            "Line2": "நிலமிசை நீடுவாழ் வார்",
            "explanation": "They who are united to the glorious feet of Him who occupies eternal space, shall flourish in the highest of worlds."
        }
    ]
    mod = _reload_with_dataset(tmp_path, dataset)
    assert len(mod._DATASET) == 2
    assert mod._DATASET[0]["number"] == 2
    assert "profit" in mod._DATASET[0]["translation"]
    assert mod._DATASET[1]["number"] == 3
    assert "glorious feet" in mod._DATASET[1]["translation"]


def test_normalization_old_schema_passthrough(tmp_path: Path):
    dataset = [
        {
            "number": 10,
            "kural": "தம்மின்தம் மக்கள் தலைப்படுதல் கேடஸ்\nதம்மின்தம் மக்கள் தலைப்பு",
            "translation": "The ruin of a king is the exaltation of his own subjects; the excellence of a king is the exaltation of his own subjects.",
            "section": "பொருட்பால்",
            "chapter": "அரசு"
        }
    ]
    mod = _reload_with_dataset(tmp_path, dataset)
    assert len(mod._DATASET) == 1
    item = mod._DATASET[0]
    assert item["number"] == 10
    assert item["kural"].startswith("தம்மின்தம்")
    assert item["translation"].startswith("The ruin of a king")
    assert item["section"] == "பொருட்பால்"
    assert item["chapter"] == "அரசு"


def test_invalid_entries_are_skipped(tmp_path: Path):
    dataset = [
        {},
        {"Number": "not-number", "Line1": "x", "Line2": "y", "Translation": "t"},
        {"Number": 5, "Line1": "", "Line2": "", "Translation": "t"},
    ]
    with pytest.raises(RuntimeError):
        _reload_with_dataset(tmp_path, dataset)
