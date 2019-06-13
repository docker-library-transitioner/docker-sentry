#!/bin/bash
set -e

current="$(curl -sSL 'https://pypi.python.org/pypi/sentry/json' | awk 'BEGIN { RS=",|:{\n"; FS="\""; } $2 == "version" { print $4 }')"

set -x
sed -ri 's/^(ENV SENTRY_VERSION) .*/\1 '"$current"'/' 9.1/Dockerfile
