FROM python:3.8-alpine AS builder

WORKDIR /build

RUN pip install pipenv==2020.8.13

COPY Pipfile /build/
COPY Pipfile.lock /build/

ARG PIPENV_NOSPIN=true
ARG PIPENV_VENV_IN_PROJECT=true
RUN pipenv install --deploy --ignore-pipfile

FROM python:3.8-alpine

RUN set -x \
    && apk add --no-cache bash=5.0.17-r0 \
    && addgroup -g 1000 bot \
    && adduser -G bot -u 1000 -s /bin/bash -D -H bot

WORKDIR /app

USER bot

COPY --from=builder /build/.venv/lib /usr/local/lib

COPY bot /app/

CMD python bot.py
