
dir=`pwd`
cd package/src/

sw=$1
case $sw in
    server | -s)
    set -- "${@:2}" #removed the 1st parameter
    gunicorn -c limes_server/gunicorn.conf.py limes_server.wsgi
    ;;
    *)
    python -m limes $@
    ;;
esac

cd $dir