"""Entry point: python -m logwatcher"""

import argparse
import sys


def build_parser():
    # argparse generates the --help text from this description
    parser = argparse.ArgumentParser(
        prog="logwatcher",
        description="Read nginx access logs and SSH auth logs and report suspicious activity.",
    )
    return parser


def main(argv=None):
    # argv=None means "read sys.argv"; tests can pass their own list instead
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    # the return value of main() becomes the process exit code
    sys.exit(main())
