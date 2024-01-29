#!/usr/bin/env bash

print_usage () {
    echo "$0: helper script for running docker commands associated with SDK Alpha"
}

[ $# -lt 1 ] && print_usage && exit 1;

case $1 in

    "build")
        echo "building"
        ;;
    "run")
        echo "running"
        ;;
    *)
        echo "Unrecognized command"
        ;;
    esac
