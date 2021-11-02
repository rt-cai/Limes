#!/bin/bash

# python -m pip install --upgrade build
# python -m pip install --upgrade twine

chmod 700 ./run.sh
chmod 700 ./build.sh
# chmod 700 ./package/src/server/certificate/gencert.sh

vsSetup=.vscode/settings.json
if test -f "$vsSetup"; then
    echo ""
    echo ""
    echo "======================================="
    echo "*** existing vs code settings found ***"
    echo "======================================="
    echo 'please manually add ./package/src to python paths.'
    echo 'for vs code, add:'
    echo '"python.analysis.extraPaths": ["${workspaceFolder}/package/src"],'
    echo 'to settings.json'
else
    mkdir .vscode
    touch $vsSetup
    $(echo '{"python.analysis.extraPaths": ["${workspaceFolder}/package/src"],}' > $vsSetup)
    chmod 755 $vsSetup
fi