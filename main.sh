#!/bin/bash

python3 src/main.py ./

var1=$?
if [ $var1 -eq 0 ];
then
cd docs && python3 -m http.server 8888
else
echo "python script failed with code " $var1
fi

