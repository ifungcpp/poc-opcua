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
    client) let_run gcc client.c -l open62541 -o client.x ;;
    client-connect) let_run gcc client_connect_loop.c -l open62541 -o client_connect_loop.x ;;
    client-subscribe) let_run gcc client_subscription_loop.c -l open62541 -o client_subscription_loop.x ;;
    esac
}

let_start()
{
    tcpdump -i any -n 'tcp port 4840' -w capture-${1}.pcap &
    case "$1" in
    server)
        let_run ./tutorial_server_firststeps.x
        ;;
    client)
        for i in {1..3}
        do
            echo wait for opc ua server start up ... $i
            sleep 1
        done
        local ipaddr=$(dig +short poc_freeopcua | head -n 1)
        let_run ./client.x "opc.tcp://${ipaddr}:4840"
        ;;
    client-connect)
        for i in {1..3}
        do
            echo wait for opc ua server start up ... $i
            sleep 1
        done
        local ipaddr=$(dig +short poc_open62541 | head -n 1)
        let_run ./client_connect_loop.x "opc.tcp://${ipaddr}:4840"
        ;;
    client-subscribe)
        tcpdump -i any -n 'tcp port 4840' -w capture-open62541-client-subscribe.pcap &
        for i in {1..3}
        do
            echo wait for opc ua server start up ... $i
            sleep 1
        done
        local ipaddr=$(dig +short poc_freeopcua | head -n 1)
        let_run ./client_subscription_loop.x "opc.tcp://${ipaddr}:4840"
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
