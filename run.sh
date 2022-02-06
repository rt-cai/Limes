
# py=python3
py=python
dir=`pwd`
src=package/src
cd $src
sw=$1
case $sw in
    test | -t)
    echo "> tests"
    echo ""
    $py -m tests
    ;;
    *)
    if [[ $1 = 'add' || $1 = 'blast' ]] && [[ ! -z $2 ]]; then
        case $2 in
            /*)
            # abspath, do nothing 
            ;;
            *)
            args=''
            i=1
            for arg in $@; do
                if [ $i -eq 2 ]; then
                    echo "> run.sh converted relative path to $dir/$arg"
                    args="$args $dir/$arg"
                else
                    args="$args $arg"
                fi
                i=$((i + 1))
            done
            ;;
        esac
    else
        args=$@
    fi
    ;;
esac

echo "> limes"
echo ""
$py -m limes $args

cd $dir