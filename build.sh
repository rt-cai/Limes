#!/bin/bash

# use test pypi for dev
# PYPI=testpypi
PYPI=pypi

ver=`cat version`
TOKEN=`cat credentials/${PYPI}`

package=inventory

install=false
build=true
upload=false
clean=false
version=false

for arg in "$@"; do
    case $arg in
    --version | -v)
        version=true
        build=false
        ;;
    --clean | -c)
        clean=true
        build=false
        ;;
    --upload | -u)
        upload=true
        ;;
    --install | -i)
        install=true
        ;;
    --only-i | -oi)
        install=true
        build=false
        ;;
    test)
        echo "***build script test branch ***"
        versionLine=`cat version`
        echo $versionLine
        exit 0
        ;;
    *)
        echo "ignoring unknown option [$arg]"
        ;;
    esac
done

wdir=`pwd`
cd package
if $version ; then
    echo ""
    echo "#########################################################"
    echo "update version strings"

    # update version
    versionLine=`grep 'version' setup.cfg`
    sed -i "s/$versionLine/version = $ver/" setup.cfg

    versionLine=$(grep 'limes version' ./src/limes/res/strings.py)
    sed -i "s/$versionLine/'limes version $ver'/" ./src/limes/res/strings.py
fi

if $build ; then
    echo ""
    echo "#########################################################"
    echo "building limes-$package"
    echo ""

    python -m build
fi

if $install ; then
    echo ""
    echo "#########################################################"
    echo "installing limes-$package"
    echo ""
    pip uninstall -y limes-$package
    pip install ./dist/limes-$package-$ver.tar.gz
fi

cd $wdir
if $upload ; then
    python -m twine upload --repository $PYPI package/dist/* -u __token__ -p $TOKEN
fi

if $clean ; then
    echo ""
    echo "#########################################################"
    echo "cleaning up builds..."
    echo ""
    wdir=`pwd`
    cd package

    rm -rf build
    rm -rf dist

    cd src
    for dir in */; do
        if [[ $dir == *.egg-info/ ]]; then
            rm -rf $dir
        fi
    done

    cd $wdir

    pip uninstall -y limes-$package
    echo "done!"
fi