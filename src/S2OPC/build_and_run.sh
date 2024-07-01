#!/bin/bash

set -e

let_make()
{
    make clean
    make
}

let_subscribe()
{
    SET_SUBSCRIBE_TIMEOUT=yes ./subscribe.x i=2258
}

main_func()
{
    local cur_dir=$(realpath $(dirname $0))
    pushd $cur_dir >/dev/null
    let_make
    for i in {1..19}
    do
        echo wait for opc ua server start up ... $i
        sleep 1
    done
    echo
    let_subscribe
    popd >/dev/null
}

main_func $*
