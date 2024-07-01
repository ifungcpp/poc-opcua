#!/bin/bash

set -e

set_var()
{
    export S2OPC_VERSION=1.5.1
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
    if docker images | grep poc.s2opc | grep ${S2OPC_VERSION} >/dev/null
    then
        echo docker image exist ... poc.s2opc:${S2OPC_VERSION}
    else
        if ! test -d $CUR_DIR/lib/S2OPC
        then
            mkdir -p $CUR_DIR/lib
            pushd $CUR_DIR/lib
            let_run git clone https://gitlab.com/systerel/S2OPC.git 
            popd >/dev/null
        fi
        pushd $CUR_DIR/lib/S2OPC >/dev/null
        let_run git checkout S2OPC_Toolkit_${S2OPC_VERSION}
        popd >/dev/null

        pushd $CUR_DIR >/dev/null
        let_run docker build -f docker/Dockerfile.s2opc -t poc.s2opc:${S2OPC_VERSION} lib/S2OPC
        popd >/dev/null
    fi
}

docker_build_freeopcua()
{
    if docker images | grep poc.freeopcua >/dev/null
    then
        echo docker image exist ... poc.freeopcua:latest
    else
        pushd $CUR_DIR/docker >/dev/null
        let_run docker build -f Dockerfile.freeopcua -t poc.freeopcua .
        popd >/dev/null
    fi
}

docker_compose_up()
{
    pushd $CUR_DIR >/dev/null
    let_run docker compose up
    popd >/dev/null
}

main_func()
{
    set_var
    docker_build_s2opc
    docker_build_freeopcua
    docker_compose_up
}

main_func $*
