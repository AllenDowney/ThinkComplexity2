#!/bin/bash

for NOTEBOOK in $@
do
    cp ../soln/$NOTEBOOK .

    python remove_soln.py $NOTEBOOK

    # run tests
    # pip install pytest nbmake
    #pytest --nbmake $NOTEBOOK

    # git add $NOTEBOOK

done
