from ystream import *

input_name = "../datasets/my_out/out_trigrams_skazki.txt"

input_name ="../datasets/out_claues.txt"

input_file = ySequence(input_name)

file_lines = yInputFileLinesStream()

split_items = yClausesRulesFilterSpacyStream()

markers = "SVO" , "ASO", "SVAv"
storage = yMultipletStorage(*markers)

lines_from_storage = ySortedCutVectorsFromStorage()

output_lines = yOutputFileLinesStream()

input_file > file_lines > split_items > storage > lines_from_storage

#for line in storage:
#    print(line)

output_file = ySequence("../datasets/my_out/out_klauses_big_dataset.txt")


input_file > file_lines > split_items > storage > lines_from_storage > output_lines > output_file


output_lines.save()



