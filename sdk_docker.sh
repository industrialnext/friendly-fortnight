#!/usr/bin/env bash

#
# Get config file from env, or use default
#
CONFIG_FILE=${CONFIG_FILE:="$(pwd)/config.toml.example"}

#
# Build using Industrial Next-provided python index
#
BUILD_CMD="time docker build --build-arg INDUSTRIALNEXT_PY_INDEX=%s -t presdk:latest ."

#
# Default `docker run` command. Enables imager usage
#
RUN_CMD="time docker run -it --rm --runtime nvidia
    -v /tmp/argus_socket:/tmp/argus_socket 
    -v %s:/app/config.toml
    presdk:latest -c /app/config.toml"


print_usage () {
    SUBCMD_HELP_FMT="%8s: %s\n"
    echo "Helper script for running docker commands associated with SDK Alpha"
    echo "Usage: $0 <build,run,print> [-c config_file]"
    printf "%16s\n" "Default config file is $DEFAULT_CONFIG_FILE"
    printf "$SUBCMD_HELP_FMT" "build" "Build the presdk container"
    printf "$SUBCMD_HELP_FMT" "run" "Run the presdk container with the given config file"
    printf "$SUBCMD_HELP_FMT" "print" "Just print the template commands and exit"
}

do_build() {
    [ -z "$INDUSTRIALNEXT_PY_INDEX" ] && echo "INDUSTRIALNEXT_PY_INDEX not set. See help or README.md" && exit
    CMD=$(printf "$BUILD_CMD" "$INDUSTRIALNEXT_PY_INDEX")
    echo "building with:"
    echo $CMD
    sleep 1
    eval $CMD
}

do_run() {
    CMD=$(printf "$RUN_CMD" "$CONFIG_FILE")
    echo "running with:"
    echo "$CMD"
    sleep 1
    eval $CMD
}

[ $# -lt 1 ] && print_usage && exit 1;

case $1 in
    "build")
        do_build 
        ;;
    "run")
        do_run
        ;;
    "buildrun")
        do_build && do_run
        ;;
    "print")
        echo "Command to build container:"
        printf "$BUILD_CMD\n" "\$INDUSTRIALNEXT_PY_INDEX"
        echo 
        echo "Command to run container:"
        printf "$RUN_CMD\n" "CHANGE_THIS_PATH/config.toml"
        echo
        ;;
    *)
        echo "Unrecognized command."
        print_usage
        ;;
    esac
