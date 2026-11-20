# Log Watcher

![CI](https://github.com/mvrhaa/log-watcher/actions/workflows/ci.yml/badge.svg)

A small Python CLI that reads nginx access logs and SSH auth logs and reports:

- the most active IPs
- how many 404 and 500 responses there were
- failed SSH logins per IP
- a `WARNING` line for every IP whose failed logins reach the threshold in `config.yaml`

Malformed lines never crash the tool: they are skipped and counted. The exit code is `1` when a warning was printed, so the tool can fail a CI job or trigger an alert from cron.

## Example output

```
$ python -m logwatcher --access samples/access.log --auth samples/auth.log
Top IPs
  203.0.113.45        9
  198.51.100.23       6
  192.0.2.10          5
  10.0.0.5            4
  198.51.100.77       2

HTTP errors
  404                 8
  500                 3

Failed logins
  203.0.113.45        7
  198.51.100.150      4
  10.0.0.20           1

Warnings
  WARNING: 203.0.113.45 has 7 failed logins (threshold 5)

Skipped lines
  samples/access.log  2
  samples/auth.log    5
```

The sample logs are fake. Their IPs come from the ranges reserved for documentation (RFC 5737).

## Run locally

Needs Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m logwatcher --access samples/access.log --auth samples/auth.log
```

Both logs are optional, but at least one is required. `--config` defaults to `config.yaml` in the current directory.

## Run with Docker

```bash
docker build -t log-watcher .
docker run --rm -v "$PWD/samples:/logs" log-watcher --access /logs/access.log --auth /logs/auth.log
```

The image is based on `python:3.12-slim` and runs as a non-root user. Logs are passed in through a volume.

## Configuration

```yaml
failed_login_threshold: 5
top_n: 5
```

A missing key falls back to the default shown above.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | report printed, no warnings |
| 1 | report printed with at least one warning |
| 2 | bad arguments, or a log or config file was not found |

## Tests

```bash
ruff check .
pytest
```

GitHub Actions runs on every push and pull request. The `test` job runs ruff and pytest. The `docker` job builds the image and runs it on `samples/` as a smoke test. Exit code `1` is expected there because the samples contain a warning.

## Project structure

```
log-watcher/
├── logwatcher/
│   ├── __init__.py
│   ├── __main__.py      # entry point: python -m logwatcher
│   ├── parsers.py       # parse_nginx_line(), parse_auth_line(), read_log()
│   ├── stats.py         # top_ips(), count_status(), failed_logins_by_ip(), suspicious_ips()
│   ├── config.py        # load_config()
│   └── report.py        # text report formatting
├── tests/
├── samples/             # fake access.log and auth.log
├── config.yaml
├── pyproject.toml
├── Dockerfile
├── .dockerignore
└── .github/workflows/ci.yml
```

## What I learned

- TODO
- TODO
- TODO

## License

MIT, see [LICENSE](LICENSE).
