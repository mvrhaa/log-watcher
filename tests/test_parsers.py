from pathlib import Path

from logwatcher.parsers import parse_auth_line, parse_nginx_line, read_log

SAMPLES = Path(__file__).parent.parent / "samples"


def test_valid_line():
    line = (
        '198.51.100.23 - - [06/Nov/2026:10:16:20 +0000] "POST /checkout HTTP/1.1" 500 186 '
        '"https://shop.example.com/cart" "Mozilla/5.0"\n'
    )

    assert parse_nginx_line(line) == {
        "ip": "198.51.100.23",
        "time": "06/Nov/2026:10:16:20 +0000",
        "method": "POST",
        "path": "/checkout",
        "status": 500,
        "size": 186,
    }


def test_dash_size_becomes_zero():
    line = (
        '192.0.2.10 - - [06/Nov/2026:10:16:31 +0000] "GET /static/logo.png HTTP/1.1" 304 - '
        '"-" "Mozilla/5.0"'
    )

    record = parse_nginx_line(line)

    assert record["status"] == 304
    assert record["size"] == 0


def test_malformed_line_returns_none():
    line = '198.51.100.23 - - [06/Nov/2026:10:16:52 +0000] "POST /checkout HTTP/1.1" 5'

    assert parse_nginx_line(line) is None


def test_empty_line_returns_none():
    assert parse_nginx_line("") is None


def test_failed_password_for_existing_user():
    line = "Nov  6 10:20:01 web01 sshd[2150]: Failed password for root from 203.0.113.45 port 52344 ssh2\n"

    assert parse_auth_line(line) == {"ip": "203.0.113.45", "user": "root", "event": "failed"}


def test_failed_password_for_invalid_user():
    line = "Nov  6 10:20:24 web01 sshd[2155]: Failed password for invalid user bob from 203.0.113.45 port 52366 ssh2"

    assert parse_auth_line(line) == {"ip": "203.0.113.45", "user": "bob", "event": "failed"}


def test_accepted_password():
    line = "Nov  6 10:40:02 web01 sshd[2245]: Accepted password for ops from 10.0.0.21 port 50410 ssh2"

    assert parse_auth_line(line) == {"ip": "10.0.0.21", "user": "ops", "event": "accepted"}


def test_non_matching_auth_line_returns_none():
    line = "Nov  6 10:20:15 web01 sshd[2153]: Invalid user admin from 203.0.113.45 port 52360"

    assert parse_auth_line(line) is None


def test_read_log_counts_skipped_nginx_lines():
    records, skipped = read_log(SAMPLES / "access.log", parse_nginx_line)

    assert len(records) == 28
    assert skipped == 2


def test_read_log_counts_skipped_auth_lines():
    records, skipped = read_log(SAMPLES / "auth.log", parse_auth_line)

    assert len(records) == 15
    assert skipped == 5


def test_read_log_survives_invalid_bytes(tmp_path):
    log = tmp_path / "access.log"
    log.write_bytes(b"\xff\xfe broken bytes\n")

    records, skipped = read_log(log, parse_nginx_line)

    assert records == []
    assert skipped == 1
