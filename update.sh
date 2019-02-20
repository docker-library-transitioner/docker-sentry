#!/bin/bash

set -e

current="$(
    curl -sSL 'https://pypi.python.org/pypi/sentry/json' | \
    python -m json.tool | \
    awk -F '"' '$2 == "version" { print $4 }'
)"

set -x
sed -ri 's/^(ENV SENTRY_VERSION) .*/\1 '"$current"'/' 9.0/Dockerfile
