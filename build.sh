#!/bin/bash

# use test pypi for dev
# PYPI=testpypi
PYPI=pypi

TOKEN=`cat credentials/${PYPI}`
allPackages=(common inventory)
# allPackages=(common inventory server)
packages=("${allPackages[@]}")

upload=false

for arg in "$@"; do
    case $arg in
    -clean)
        echo "cleaning previous builds..."
        wdir=`pwd`
        for package in "${allPackages[@]}"; do
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
        exit 0
        ;;
    -com-only)
        echo "only building common"
        packages=(common)
        ;;
    -upload)
        upload=true
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

    if $upload ; then
        echo "uploading ..."
        python -m twine upload --repository $PYPI dist/* -u __token__ -p $TOKEN
    fi
    cd $wdir
done
