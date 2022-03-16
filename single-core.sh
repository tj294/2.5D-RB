#!/bin/bash
rm -rf __pycache__

python3 rb_convect.py -o $1

rm -rf __pycache__

python3 merge.py $1/analysis --cleanup
python3 merge.py $1/snapshots --cleanup
