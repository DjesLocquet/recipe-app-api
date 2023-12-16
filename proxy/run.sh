#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status.

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf  # Replace environment variables in NGINX config file, e.g. ${NGINX_PORT} with 9000
nginx -g 'daemon off;'  # Start NGINX server as main process, daemon off means run in foreground