"""Entry point: python -m logwatcher"""

import argparse
import os
import sys

from logwatcher.config import load_config
from logwatcher.parsers import parse_auth_line, parse_nginx_line, read_log
from logwatcher.report import format_section, format_warnings
from logwatcher.stats import count_status, failed_logins_by_ip, suspicious_ips, top_ips


def build_parser():
    parser = argparse.ArgumentParser(
        prog="logwatcher",
        description="Read nginx access logs and SSH auth logs and report suspicious activity.",
    )
    parser.add_argument("--access", help="path to an nginx access log")
    parser.add_argument("--auth", help="path to an SSH auth log")
    parser.add_argument("--config", default="config.yaml", help="path to the config file (default: config.yaml)")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.access and not args.auth:
        parser.error("give at least one log: --access and/or --auth")
    for path in (args.access, args.auth):
        if path and not os.path.isfile(path):
            parser.error(f"log file not found: {path}")

    try:
        config = load_config(args.config)
    except FileNotFoundError as error:
        parser.error(str(error))

    sections = []
    skipped = []
    warnings = []

    if args.access:
        records, skipped_lines = read_log(args.access, parse_nginx_line)
        skipped.append((args.access, skipped_lines))
        errors = [(code, count_status(records, code)) for code in (404, 500)]
        sections.append(format_section("Top IPs", top_ips(records, config["top_n"])))
        sections.append(format_section("HTTP errors", errors))

    if args.auth:
        records, skipped_lines = read_log(args.auth, parse_auth_line)
        skipped.append((args.auth, skipped_lines))
        failed = failed_logins_by_ip(records)
        threshold = config["failed_login_threshold"]
        warnings = suspicious_ips(failed, threshold)
        sections.append(format_section("Failed logins", failed.most_common()))
        sections.append(format_warnings(warnings, threshold))

    sections.append(format_section("Skipped lines", skipped))
    print("\n\n".join(sections))

    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
