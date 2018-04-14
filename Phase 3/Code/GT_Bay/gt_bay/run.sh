#!/usr/bin/env bash
NUM_WORKERS=3
TIMEOUT=120
PIDFILE="gunicorn.pid"

if [ -d "/home/ubuntu/Applications/python_envs" ]; then
    source /home/ubuntu/Applications/python_envs/bin/activate
fi

exec gunicorn gt_bay_app:app \
--workers $NUM_WORKERS \
--worker-class gevent \
--timeout $TIMEOUT \
--log-level=debug \
--bind=0.0.0.0:9000 \
--pid=$PIDFILE
