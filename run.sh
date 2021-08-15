
dir=`pwd`
src=package/src
cd $src
sw=$1
case $sw in
    server | -s)
    set -- "${@:2}" #removed the 1st parameter
    gunicorn -c limes_server/gunicorn.conf.py limes_server.wsgi
    ;;
    fosdb | -f)
    echo "> fosDB"
    echo ""
    python -m fosDB
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
    echo "> limes"
    echo ""
    python -m limes $args
    ;;
esac

cd $dir