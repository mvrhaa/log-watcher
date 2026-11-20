from logwatcher.parsers import parse_nginx_line


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
