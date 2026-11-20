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


def suspicious_ips(failed_counts, threshold):
    return [(ip, count) for ip, count in failed_counts.most_common() if count >= threshold]
