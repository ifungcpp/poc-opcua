#!/bin/bash

set -e

let_run()
{
    echo
    echo $*
    echo
    time $*
}

let_tcpdump()
{
    (let_run tcpdump -i any -n 'tcp port 4840' -w capture.pcap) &
}

let_make()
{
    let_run make clean
    let_run make
}

let_subscribe()
{
    echo
    echo SET_SUBSCRIBE_TIMEOUT=yes ./subscribe.x i=2258
    echo
    SET_SUBSCRIBE_TIMEOUT=yes ./subscribe.x i=2258
}

main_func()
{
    local cur_dir=$(realpath $(dirname $0))
    pushd $cur_dir >/dev/null
    let_tcpdump
    let_make
    for i in {1..9}
    do
        echo wait for opc ua server start up ... $i
        sleep 1
    done
    echo
    let_subscribe
    popd >/dev/null
}

main_func $*
