

# use test pypi for dev
# PYPI=testpypi
PYPI=pypi

TOKEN=`cat credentials/${PYPI}`
# allPackages=(inventory)
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
    cd limes_$package

    if $upload ; then
        echo "#########################################################"
        echo "uploading $package"
        python -m twine upload --repository $PYPI dist/* -u __token__ -p $TOKEN
    else
        echo "#########################################################"
        echo "building $package"
        echo "#########################################################"
        echo ""
        echo ""
        echo ""
        python -m build
    fi
    cd $wdir
done
