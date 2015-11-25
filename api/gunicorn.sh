#!/bin/sh
gunicorn -b 0.0.0.0:8000 -w 9 'api.app:config_app()' --limit-request-line 0 --timeout 500