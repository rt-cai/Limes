
# py=python3
py=python
wdir=`pwd`

test=false
limes=true
scratch=false

src=package
cd $src
sw=$1
case $sw in
    --scratch | -s)
    scratch=true
    limes=false
    ;;
    --test | -t)
    test=true
    limes=false
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

if $scratch ; then
    cd $wdir/scratch
    echo "> scratch"
    echo ""
    python scratch.py
fi


if $test ; then
    cd $wdir
    echo "> tests"
    echo ""
    $py -m tests
fi

if $limes ; then
    echo "> limes"
    echo ""
    $py -m limes $args
fi

cd $wdir