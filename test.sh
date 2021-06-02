                        
source build.sh
# source build.sh -com-only


ver="0.1.dev1"
# for package in common server inventory; do
for package in "${packages[@]}"; do
    echo "#########################################################"
    echo "installing $package"
    echo ""
    echo ""

    pip install --ignore-installed limes_$package/dist/limes-$package-$ver.tar.gz
    echo $package
done