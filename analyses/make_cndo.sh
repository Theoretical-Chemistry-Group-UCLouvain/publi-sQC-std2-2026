#!/bin/bash

. ./venv/bin/activate

for m in {LiH,H2O,C2H4}; do
  for b in {sto-3g,cc-pvdz,cc-pvtz}; do
       python ./pyscf_cndo.py -m ${m} -b ${b} -o ../data/CNDO/${m}_${b}.csv 
    done
  done
