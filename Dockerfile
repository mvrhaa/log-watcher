FROM python:3.12-slim

RUN useradd --create-home appuser

WORKDIR /app
COPY pyproject.toml ./
COPY logwatcher ./logwatcher
RUN pip install --no-cache-dir .

COPY config.yaml ./

USER appuser
ENTRYPOINT ["python", "-m", "logwatcher"]
