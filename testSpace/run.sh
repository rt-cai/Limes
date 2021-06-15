
dir=`pwd`
src=../package/src
cd $src

sw=$1
case $sw in
    server | -s)
    set -- "${@:2}" #removed the 1st parameter
    gunicorn -c limes_server/gunicorn.conf.py limes_server.wsgi
    ;;
    *)
    if [ $1 = 'add' ] && [ ! -z $2 ]; then
        case $2 in
            /*)
            # abspath, do nothing 
            ;;
            *)
            args=''
            i=0
            for arg in $@; do
                if [ $i -eq 2 ]; then
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
    python -m limes $args
    ;;
esac

cd $dir