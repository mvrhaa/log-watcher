import subprocess
import sys
from pathlib import Path

import pytest

from logwatcher.__main__ import main

ROOT = Path(__file__).parent.parent
ACCESS = str(ROOT / "samples" / "access.log")
AUTH = str(ROOT / "samples" / "auth.log")
CONFIG = str(ROOT / "config.yaml")


def test_full_report_on_samples(capsys):
    code = main(["--access", ACCESS, "--auth", AUTH, "--config", CONFIG])
    output = capsys.readouterr().out

    assert code == 1
    for title in ("Top IPs", "HTTP errors", "Failed logins", "Warnings", "Skipped lines"):
        assert title in output
    assert "203.0.113.45        9" in output
    assert "404                 8" in output
    assert "WARNING: 203.0.113.45 has 7 failed logins (threshold 5)" in output


def test_access_log_only(capsys):
    code = main(["--access", ACCESS, "--config", CONFIG])
    output = capsys.readouterr().out

    assert code == 0
    assert "Top IPs" in output
    assert "Failed logins" not in output


def test_higher_threshold_means_no_warning(tmp_path, capsys):
    config = tmp_path / "config.yaml"
    config.write_text("failed_login_threshold: 10\n")

    code = main(["--auth", AUTH, "--config", str(config)])

    assert code == 0
    assert "WARNING" not in capsys.readouterr().out


def test_no_logs_is_an_error(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--config", CONFIG])

    assert error.value.code == 2
    assert "at least one log" in capsys.readouterr().err


def test_missing_log_file_is_an_error(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--access", "nope.log", "--config", CONFIG])

    assert error.value.code == 2
    assert "log file not found: nope.log" in capsys.readouterr().err


def test_missing_config_is_an_error(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--access", ACCESS, "--config", "nope.yaml"])

    assert error.value.code == 2
    assert "config file not found: nope.yaml" in capsys.readouterr().err


def test_runs_as_module():
    result = subprocess.run(
        [sys.executable, "-m", "logwatcher", "--access", "samples/access.log", "--auth", "samples/auth.log"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "samples/access.log  2" in result.stdout
    assert "samples/auth.log    5" in result.stdout
