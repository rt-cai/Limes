#!/bin/bash
./build.sh

for package in common core client; do
    pip install limes_$package/dist
done