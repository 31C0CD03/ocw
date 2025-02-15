#!/bin/sh

ARIA2_ARGS="-q -x16 -s16"

if ! command -v aria2c 2>&1 >/dev/null
then
    echo "aria2c not found, please make sure it is in PATH"
    exit 1
fi

if [ ! -f $1 ];
then
    echo "file not found"
    exit 1
fi

aria2c $ARIA2_ARGS --input-file=$1 --dir=${1%%.*}
