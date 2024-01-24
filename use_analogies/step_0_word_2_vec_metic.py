from ystream import *

input_w2v_file =  "../../datasets/ruscorpora_upos_skipgram_300_5_2018.vec"


output_w2v_file =  "../../datasets/my_out/word2vec_metric.txt"

input_file = ySequence(input_w2v_file)

file_lines = yInputFileLinesStream(skip_first_lines = 1)

split_to_key_vector = ySplitSimpleStream(split_symbol = " ")

split_to_entry  = yItemstoW2VEntry()



storage = yStorageW2V()

distance_lines = yDistancesW2V()

output_lines = yOutputFileLinesStream()

output_file = ySequence(output_w2v_file)



input_file > file_lines > split_to_key_vector > split_to_entry > storage

storage.store()

storage > distance_lines > output_lines > output_file

output_lines.save()