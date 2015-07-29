#!/bin/bash

TOPDIR=$(dirname $0)/..

if [[ -x /usr/bin/git && -d "$TOPDIR/.git" ]];
    then
        REVISION=$(git rev-parse --short=12 HEAD)
        DIFF_INDEX=$(git diff-index --quiet HEAD)
        if [[ ! $DIFF_INDEX ]];
            then
                REVISION="${REVISION}+"
        fi
    echo "$REVISION"
fi
