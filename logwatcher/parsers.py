"""Turn single nginx and SSH auth log lines into dicts."""

import re

NGINX_LINE = re.compile(
    r'(?P<ip>\S+) - \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) HTTP/[\d.]+" '
    r'(?P<status>\d{3}) (?P<size>\d+|-) '
    r'"[^"]*" "[^"]*"'
)

AUTH_LINE = re.compile(
    r'(?P<event>Failed|Accepted) password for (?:invalid user )?'
    r'(?P<user>\S+) from (?P<ip>\S+) port \d+ ssh2$'
)


def parse_nginx_line(line):
    match = NGINX_LINE.fullmatch(line.strip())
    if match is None:
        return None

    record = match.groupdict()
    record["status"] = int(record["status"])
    record["size"] = 0 if record["size"] == "-" else int(record["size"])
    return record


def parse_auth_line(line):
    match = AUTH_LINE.search(line.strip())
    if match is None:
        return None

    return {
        "ip": match["ip"],
        "user": match["user"],
        "event": match["event"].lower(),
    }


def read_log(path, parse_line):
    records = []
    skipped = 0
    with open(path, encoding="utf-8", errors="replace") as file:
        for line in file:
            record = parse_line(line)
            if record is None:
                skipped += 1
            else:
                records.append(record)
    return records, skipped
