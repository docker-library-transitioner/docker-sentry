#!/bin/bash

set -e

if [ "$1" = 'sentry' ]; then
	defaultConf='/home/user/.sentry/sentry.conf.py'
	linksConf='/home/user/docker-links.conf.py'
	
	if [ ! -s "$defaultConf" ]; then
		sentry init "$defaultConf"
	fi
	
	line="execfile('$linksConf')"
	if ! grep -q "$line" "$defaultConf"; then
		echo "$line" >> "$defaultConf"
	fi
	
	[ -d /docker-entrypoint-init.d ] && for f in /docker-entrypoint-init.d/*; do
		case "$f" in
			*.sh)  echo "$0: running $f"; . "$f" ;;
			*)     echo "$0: ignoring $f" ;;
		esac
		echo
	done

	# TODO sentry upgrade?
	# it requires stdin to answer questions and dies on 'unexpected EOF'
	# but does not ask again when run a second time
fi

exec "$@"
