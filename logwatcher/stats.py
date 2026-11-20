"""Aggregate parsed log records into counts."""

from collections import Counter


def top_ips(records, n):
    counts = Counter(record["ip"] for record in records)
    return counts.most_common(n)


def count_status(records, code):
    statuses = Counter(record["status"] for record in records)
    return statuses[code]


def failed_logins_by_ip(records):
    return Counter(record["ip"] for record in records if record["event"] == "failed")
