cd package/src/

sw=$1
set -- "${@:2}" #removed the 1st parameter
case $sw in
    server | -s)
    ori=`pwd`
    cd package/src
    gunicorn limes_server.wsgi
    cd $ori
    ;;
    *)
    python -m limes $args
    ;;
esac