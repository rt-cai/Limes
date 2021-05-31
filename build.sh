#!/bin/bash

# use test pypi for dev
PYPI=testpypi
#PYPI=pypi

TOKEN=`cat credentials/${PYPI}`

for package in common client core; do
    echo "#########################################################"
    echo "building $package"
    echo "#########################################################"
    echo ""
    echo ""
    echo ""
    
    cd limes_$package
    
    python -m build
    python -m twine upload --repository $PYPI dist/* -u __token__ -p $TOKEN

    cd ..
done
