FROM python:3.10-slim-bullseye AS dev
COPY .requirements /tmp
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends git\
    && pip install --upgrade pip\
    && pip install --upgrade build\
    && pip install \
    -r /tmp/test.txt\
    -r /tmp/lint.txt\
    -r /tmp/docs.txt\
    -r /tmp/ipython.txt