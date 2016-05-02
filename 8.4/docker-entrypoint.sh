#!/bin/bash

set -e

# first check if we're passing flags, if so
# prepend with sentry
if [ "${1:0:1}" = '-' ]; then
	set -- sentry "$@"
fi

case "$1" in
	celery|cleanup|config|createuser|devserver|django|export|help|import|init|plugins|queues|repair|run|shell|start|tsdb|upgrade)
		set -- sentry "$@"
	;;
	generate-secret-key)
		set -- sentry config generate-secret-key
	;;
esac

if [ "$1" = 'sentry' ]; then
	set -- tini -- "$@"
fi

exec "$@"
