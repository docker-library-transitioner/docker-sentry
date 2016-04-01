#!/bin/bash
set -e

current="$(curl -sSL 'https://pypi.python.org/pypi/sentry/json' | awk -F '"' '$2 == "version" { print $4 }')"

set -x
sed -ri 's/^(ENV SENTRY_VERSION) .*/\1 '"$current"'/' 8.3/Dockerfile
