#!/bin/bash

echo 'test - .pqp'
python ../parseMetaboAssayLibToSkylineTransitionList.py \
-in ./assaylibrary_t3_decoy_test.pqp \
-out ./skyline_transitions_list_from_pqp_test.tsv \
-rtw 0.6

echo '-----------------------------'

echo 'test - .TraML'
python ../parseMetaboAssayLibToSkylineTransitionList.py \
-in ./assaylibrary_t3_decoy_test.TraML \
-out ./skyline_transitions_list_from_TraML_test.tsv \
-rtw 0.6

echo '-----------------------------'

echo 'test - .tsv'
python ../parseMetaboAssayLibToSkylineTransitionList.py \
-in ./assaylibrary_t3_decoy_test.tsv \
-out ./skyline_transitions_list_from_tsv_test.tsv \
-rtw 0.6
