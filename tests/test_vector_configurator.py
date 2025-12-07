import json
from pathlib import Path

import pytest

from src.vector_configurator import VectorConfiguration


def test_update_component(tmp_path: Path) -> None:
    config = VectorConfiguration(name="demo", components=[0.0, 0.0, 0.0])
    config_path = tmp_path / "config.json"
    config.to_file(config_path)

    config.update_component(1, 5.5)
    config.to_file(config_path)

    reloaded = VectorConfiguration.from_file(config_path)
    assert reloaded.components == [0.0, 5.5, 0.0]


def test_normalization_creates_unit_vector(tmp_path: Path) -> None:
    config = VectorConfiguration(name="demo", components=[3.0, 4.0])
    normalized = config.normalize()

    assert pytest.approx(1.0) == normalized.magnitude()
    assert normalized.name == "demo-normalized"


def test_from_dict_rejects_invalid_components() -> None:
    with pytest.raises(ValueError):
        VectorConfiguration.from_dict({"name": "bad", "components": "not-a-list"})


def test_from_file_round_trip(tmp_path: Path) -> None:
    payload = {"name": "sample", "components": [1, 2, 3]}
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(payload))

    config = VectorConfiguration.from_file(path)
    assert config.name == "sample"
    assert config.components == [1.0, 2.0, 3.0]
