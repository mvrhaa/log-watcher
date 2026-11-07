"""Entry point: python -m logwatcher"""

import argparse
import os
import sys


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

    return 0


if __name__ == "__main__":
    sys.exit(main())
