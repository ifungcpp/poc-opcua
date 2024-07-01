#!/bin/bash

set -e

set_var()
{
    S2OPC_VERSION=1.5.1
    OPEN62541_VERSION=1.4.1
    CUR_DIR=$(realpath $(dirname $0))
    echo "CUR_DIR: $CUR_DIR"
}

let_run()
{
    echo
    echo "PWD: $(pwd)"
    echo "CMD: $*"
    echo
    time $*
}

docker_build_s2opc()
{
    if ! test -d $CUR_DIR/lib/S2OPC
    then
        let_run git clone https://gitlab.com/systerel/S2OPC.git 
    fi
    pushd $CUR_DIR/lib/S2OPC >/dev/null
    let_run git checkout S2OPC_Toolkit_${S2OPC_VERSION}
    popd >/dev/null

    pushd $CUR_DIR >/dev/null
    let_run docker build -f docker/Dockerfile.s2opc -t poc.s2opc:${S2OPC_VERSION} lib/S2OPC
    popd >/dev/null
}

docker_run_s2opc_subscribe()
{
    pushd $CUR_DIR/src/S2OPC >/dev/null
    let_run docker run -it -v $(pwd):/src -w /src poc.s2opc:${S2OPC_VERSION} bash build_and_run.sh
    popd >/dev/null
}

run_s2opc_subscribe()
{
    pushd $CUR_DIR/src/S2OPC >/dev/null
    export SET_SUBSCRIBE_TIMEOUT=yes 
    let_run ./subscribe.x i=2258
    popd >/dev/null
}

docker_build_freeopcua()
{
    pushd $CUR_DIR/docker >/dev/null
    let_run docker build -f Dockerfile.freeopcua -t poc.freeopcua .
    popd >/dev/null
}

docker_build_open62541()
{   
    if ! test -d $CUR_DIR/lib/open62541
    then
        let_run git clone https://github.com/open62541/open62541.git
    fi
    pushd $CUR_DIR/lib/open62541 >/dev/null
    let_run git checkout v${OPEN62541_VERSION}
    popd >/dev/null

    pushd $CUR_DIR >/dev/null
    let_run docker build -f docker/Dockerfile.open62541 -t poc.open62541:${OPEN62541_VERSION} lib/open62541
    popd >/dev/null
}

docker_run_freeopcua_client()
{
    pushd $CUR_DIR/src >/dev/null
    let_run docker run -it -v $(pwd):/src -w /src poc.freeopcua python /src/freeopcua/sync/client-minimal.py
    popd >/dev/null
}

docker_run_freeopcua_server()
{
    pushd $CUR_DIR/src >/dev/null
    let_run docker run -it -v $(pwd):/src -w /src -p 4840:4840 poc.freeopcua python /src/freeopcua/sync/server-minimal.py
    popd >/dev/null
}

docker_run_open62541_server()
{
    pushd $CUR_DIR/src/open62541 >/dev/null
    let_run docker run -it -v $(pwd):/app -w /app poc.open62541:${OPEN62541_VERSION} gcc tutorial_server_firststeps.c -l open62541 -o tutorial_server_firststeps.x
    let_run ./tutorial_server_firststeps.x
    popd >/dev/null
}

docker_run_open62541_client()
{
    pushd $CUR_DIR/src/open62541 >/dev/null
    let_run docker run -it -v $(pwd):/app -w /app poc.open62541:${OPEN62541_VERSION} gcc client_connect_loop.c -l open62541 -o client_connect_loop.x
    let_run ./client_connect_loop.x
    popd >/dev/null
}

docker_copy_s2opc_build_bin()
{
    mkdir -p $CUR_DIR/src/S2OPC/build
    let_run docker cp poc.s2opc:${S2OPC_VERSION}:/opt/S2OPC/build/bin $CUR_DIR/src/S2OPC/build
}

docker_exec_s2opc()
{
    pushd $CUR_DIR >/dev/null
    let_run docker run -it -v $(pwd):/poc -w /poc poc.s2opc:${S2OPC_VERSION} bash 
    popd >/dev/null
}

print_usage()
{
    echo "Usage: bash $0
    dbfree ) docker_build_freeopcua      ;;
    dbopen ) docker_build_open62541      ;;
    dbs2   ) docker_build_s2opc          ;;
    drs2   ) docker_run_s2opc_subscribe  ;;
    runs2  ) run_s2opc_subscribe         ;;
    dr     ) docker_run                  ;;
    drfc   ) docker_run_freeopcua_client ;;
    drfs   ) docker_run_freeopcua_server ;;
    dr6c   ) docker_run_open62541_client ;;
    dr6s   ) docker_run_open62541_server ;;
    dcp    ) docker_copy_s2opc_build_bin ;;
    dex    ) docker_exec_s2opc ;;
    "
}

main_func()
{
    set_var
    case "$1" in
    dbfree ) docker_build_freeopcua      ;;
    dbopen ) docker_build_open62541      ;;
    dbs2   ) docker_build_s2opc          ;;
    drs2   ) docker_run_s2opc_subscribe  ;;
    runs2  ) run_s2opc_subscribe         ;;
    dr     ) docker_run                  ;;
    drfc   ) docker_run_freeopcua_client ;;
    drfs   ) docker_run_freeopcua_server ;;
    dr6c   ) docker_run_open62541_client ;;
    dr6s   ) docker_run_open62541_server ;;
    dcp    ) docker_copy_s2opc_build_bin ;;
    dex    ) docker_exec_s2opc ;;
    *) print_usage;;
    esac
}

main_func $*