from pathlib import Path

import pytest

from logwatcher.config import load_config

ROOT = Path(__file__).parent.parent


def test_loads_project_config():
    assert load_config(ROOT / "config.yaml") == {"failed_login_threshold": 5, "top_n": 5}


def test_missing_key_uses_default(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("failed_login_threshold: 3\n")

    assert load_config(config_file) == {"failed_login_threshold": 3, "top_n": 5}


def test_empty_file_uses_defaults(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("")

    assert load_config(config_file) == {"failed_login_threshold": 5, "top_n": 5}


def test_missing_file_gives_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="config file not found"):
        load_config(tmp_path / "nope.yaml")
