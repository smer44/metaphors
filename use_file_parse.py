from  ystream import *
from yngrams import yNgramsDict

file_name = toystream("../datasets/my_gpt/facts_gpt.txt")
file_lines = yInputFileLinesStream()

parse = yClausesSpacy(yClausesSpacy.ru)

output_file = toystream("../datasets/my_out/out_facts_gpt.txt")

output = yOutputFileLinesStream()



file_name > file_lines > parse  >output > output_file

output.save()