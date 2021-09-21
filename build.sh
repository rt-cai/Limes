#!/bin/bash

# use test pypi for dev
# PYPI=testpypi
PYPI=pypi

ver="0.4.1.dev1"
TOKEN=`cat credentials/${PYPI}`
configs=(LICENSE pyproject.toml README.md setup.cfg)

allPackages=(inventory server)
packages=(inventory)

install=false
build=true

for arg in "$@"; do
    case $arg in
    --react | -r)
        echo "building React client"
        wdir=`pwd`
        cd package/src/website
        npm run build
        cd $wdir
        exit 0
        ;;
    --clean | -c)
        echo "cleaning previous builds..."
        wdir=`pwd`
        cd package

        rm -rf build
        rm -rf dist
        for file in "${configs[@]}"; do
            rm $file
        done

        cd src
        for dir in */; do
            if [[ $dir == *.egg-info/ ]]; then
                rm -rf $dir
            fi
        done

        cd $wdir
        exit 0
        ;;
    --all | -a)
        echo "building all"
        packages=("${allPackages[@]}")
        ;;
    --upload | -u)
        python -m twine upload --repository $PYPI package/dist/* -u __token__ -p $TOKEN
        exit 0
        ;;
    --install | -i)
        install=true
        build=false
        ;;
    --build-install | -bi)
        install=true
        ;;
    test)
        echo "***build script test branch ***"
        versionLine=`grep 'version' config.common/setup.cfg`
        echo $versionLine
        sed -i "s/$versionLine/$ver/" config.common/setup.cfg
        exit 0
        ;;
    *)
        echo "ignoring unknown option [$arg]"
        ;;
    esac
done

wdir=`pwd`
cd package
doneOnce=false
for package in "${packages[@]}"; do
    if $build ; then
        echo ""
        echo "#########################################################"
        echo "building $package"
        echo ""

        # update version
        versionLine=`grep 'version' ../config.$package/setup.cfg`
        sed -i "s/$versionLine/version = $ver/" ../config.$package/setup.cfg
        if ! $doneOnce ; then
            versionLine=$(grep 'limes version' ./src/limes/res/strings.py)
            sed -i "s/$versionLine/'limes version $ver'/" ./src/limes/res/strings.py
            doneOnce=true
        fi

        # copy over config files
        for file in "${configs[@]}"; do
            yes | cp -rf ../config.$package/$file ./
        done

        python -m build
    fi
    
    if $install ; then
        echo ""
        echo "#########################################################"
        echo "installing $package"
        echo ""
        pip uninstall -y limes-$package
        pip install ./dist/limes-$package-$ver.tar.gz
    fi
done