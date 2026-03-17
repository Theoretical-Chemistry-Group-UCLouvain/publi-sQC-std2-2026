#/bin/bash

python ./plot_1PA_dset.py ../data/CT.csv -o ../Figure3.pdf
python ./plot_OR.py ../data/OR_XCFs.csv ../data/OR_simplified_XCFs.csv -o ../Figure11.pdf
python ./plot_2PA_dset.py ../data/CT.csv -o ../Figure13.pdf --gmax 0.3

python ./plot_cndo.py ../data/CNDO/LiH_{sto-3g,cc-pvdz,cc-pvtz}.csv -n "STO-3G" "cc-pVDZ" "cc-pVTZ" --req 1.619022000 -l "Li-H" -o ../FigureS1.pdf
python ./plot_cndo.py ../data/CNDO/H2O_{sto-3g,cc-pvdz,cc-pvtz}.csv -n "STO-3G" "cc-pVDZ" "cc-pVTZ" --req 0.946222800 -l "O-H" -o ../FigureS2.pdf
python ./plot_cndo.py ../data/CNDO/C2H4_{sto-3g,cc-pvdz,cc-pvtz}.csv -n "STO-3G" "cc-pVDZ" "cc-pVTZ" --req 1.320891000 -l "C=C" -o ../FigureS3.pdf

python ./plot_1PA_dset.py ../data/QUEST_1PA.csv -o ../FigureS4.pdf
python ./plot_2PA_dset.py ../data/QUEST_2PA.csv -o ../FigureS5.pdf
