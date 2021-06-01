
for package in core client; do
    python -m pip install --index-url https://test.pypi.org/simple/ --no-deps limes-$package-Tony-xy-Liu
done