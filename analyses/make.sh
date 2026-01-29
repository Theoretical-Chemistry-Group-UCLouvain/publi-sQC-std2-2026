#/bin/bash

python ./plot_1PA_dset.py ../data/CT.csv -o ../Figure1.pdf
python ./plot_2PA_dset.py ../data/CT.csv -o ../Figure2.pdf --gmax 0.3

python ./plot_1PA_dset.py ../data/QUEST_1PA.csv -o ../FigureS1.pdf
python ./plot_2PA_dset.py ../data/QUEST_2PA.csv -o ../FigureS2.pdf
