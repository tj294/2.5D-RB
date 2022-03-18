#!/bin/bash
rm -rf __pycache__

mpiexec -n $1 python3 rb_convect.py -o $2

rm -rf __pycache__

python3 merge.py $2
