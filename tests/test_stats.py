from pathlib import Path

from logwatcher.parsers import parse_auth_line, parse_nginx_line, read_log
from logwatcher.stats import count_status, failed_logins_by_ip, top_ips

SAMPLES = Path(__file__).parent.parent / "samples"
ACCESS, _ = read_log(SAMPLES / "access.log", parse_nginx_line)
AUTH, _ = read_log(SAMPLES / "auth.log", parse_auth_line)


def test_top_ips():
    assert top_ips(ACCESS, 5) == [
        ("203.0.113.45", 9),
        ("198.51.100.23", 6),
        ("192.0.2.10", 5),
        ("10.0.0.5", 4),
        ("198.51.100.77", 2),
    ]


def test_top_ips_respects_n():
    assert top_ips(ACCESS, 1) == [("203.0.113.45", 9)]


def test_count_status():
    assert count_status(ACCESS, 404) == 8
    assert count_status(ACCESS, 500) == 3
    assert count_status(ACCESS, 200) == 15


def test_count_status_missing_code_is_zero():
    assert count_status(ACCESS, 418) == 0


def test_failed_logins_by_ip_ignores_accepted():
    assert failed_logins_by_ip(AUTH) == {
        "203.0.113.45": 7,
        "198.51.100.150": 4,
        "10.0.0.20": 1,
    }
