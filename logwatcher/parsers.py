"""Turn single nginx and SSH auth log lines into dicts."""

import re

NGINX_LINE = re.compile(
    r'(?P<ip>\S+) - \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) HTTP/[\d.]+" '
    r'(?P<status>\d{3}) (?P<size>\d+|-) '
    r'"[^"]*" "[^"]*"'
)


def parse_nginx_line(line):
    match = NGINX_LINE.fullmatch(line.strip())
    if match is None:
        return None

    record = match.groupdict()
    record["status"] = int(record["status"])
    record["size"] = 0 if record["size"] == "-" else int(record["size"])
    return record
