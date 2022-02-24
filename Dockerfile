FROM python:3.10-slim-bullseye AS dev
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends git\
    && pip install --upgrade pip\
    && pip install --upgrade build\
    && pip install\
    pytest==7.0.1\
    coverage==6.3.2\
    mkdocs-material==8.2.1\
    mkdocstrings==0.18.0\
    black==22.1.0\
    flake8==4.0.1\
    mypy==0.931\
    ipython==8.0.1