
# py=python3
py=python
dir=`pwd`
src=package/src
cd $src
sw=$1
case $sw in
    react | -r)
    cd website
    npm run start
    ;;
    server-rebuild-react | -sr)
    cd $dir
    ./build.sh -r
    cd $src
    gunicorn -c server/gunicorn.conf.py server.wsgi
    ;;
    server | -s)
    gunicorn -c server/gunicorn.conf.py server.wsgi
    # python -m server
    ;;
    fosdb | -f)
    echo "> fosDB"
    echo ""
    $py -m fosDB
    ;;
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
    echo "> limes"
    echo ""
    $py -m limes $args
    ;;
esac

cd $dir