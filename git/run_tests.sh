#!/bin/bash
set -e

docker run --rm \
    -e SENTRY_SKIP_BACKEND_VALIDATION=1 \
    -e SENTRY_SECRET_KEY=abc \
    -e SENTRY_REDIS_HOST=localhost \
    "$1" config get system.secret-key
