#!/bin/sh

start() {
    /etc/while.sh &
}

stop() {
    kill `ps | grep while | awk 'NR==1{print $1}'`
}

case "$1" in
    start)
        start
        ;;

    stop)
        stop
        ;;

    restart)
        stop
        sleep 1
        start
        ;;

    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1

esac
