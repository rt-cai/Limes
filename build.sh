#!/bin/bash

# use test pypi for dev
PYPI=testpypi
#PYPI=pypi

TOKEN=`cat credentials/${PYPI}`
packages=(common server inventory)

# prebuild
for arg in "$@"; do
    case $arg in
    -clean)
        echo "cleaning previous builds..."
        wdir=`pwd`
        for package in "${packages[@]}"; do
            cd limes_$package
            rm -rf build
            rm -rf dist
            cd src
            for dir in */; do
                if [[ $dir == *.egg-info/ ]]; then
                    rm -rf $dir
                fi
            done
            cd $wdir
        done
        ;;
    *)
        echo "ignoring unknown option [$arg]"
        ;;
    esac
done

wdir=`pwd`
for package in "${packages[@]}"; do
    echo "#########################################################"
    echo "building $package"
    echo "#########################################################"
    echo ""
    echo ""
    echo ""
    
    cd limes_$package
    
    python -m build

    cd $wdir
done

# post build
for arg in "$@"; do
    case $arg in
    -upload)
        echo "uploading ..."
        wdir=`pwd`
        for package in "${packages[@]}"; do
            cd limes_$package
            python -m twine upload --repository $PYPI dist/* -u __token__ -p $TOKEN
            cd $wdir
        done
        ;;
    *)
        echo "ignoring unknown option [$arg]"
        ;;
    esac
done
