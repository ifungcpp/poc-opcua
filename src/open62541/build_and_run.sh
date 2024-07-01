#!/bin/bash

set -e

let_run()
{
    echo
    echo $*
    echo
    time $*
}

let_make()
{
    case "$1" in
    server) let_run gcc tutorial_server_firststeps.c -l open62541 -o tutorial_server_firststeps.x ;;
    client) let_run gcc client_connect_loop.c -l open62541 -o client_connect_loop.x ;;
    esac
}

let_start()
{
    case "$1" in
    server)
        tcpdump -i any -n 'tcp port 4840' -w capture.pcap &
        let_run ./tutorial_server_firststeps.x
        ;;
    client)
        for i in {1..3}
        do
            echo wait for opc ua server start up ... $i
            sleep 1
        done
        local ipaddr=$(dig +short poc_open62541 | head -n 1)
        let_run ./client_connect_loop.x "opc.tcp://${ipaddr}:4840"
        ;;
    esac
}

main_func()
{
    local cur_dir=$(realpath $(dirname $0))
    pushd $cur_dir >/dev/null
    let_make $1
    let_start $1
    popd >/dev/null
}

main_func $*
