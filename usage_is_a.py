from  ystream import *
from yngrams import yNgramsDict


file_name = toystream("../datasets/my_gpt/is_a.txt")

file_lines = yInputFileLinesStream()

lines_to_ngrams = yNGramsRawLoad("- это" , False , noweight = True)


ngrams_dict = yNgramsDict()

file_name > file_lines >lines_to_ngrams >ngrams_dict

ngrams_dict.store()

print(len(ngrams_dict.ngrams))

ngrams_to_lines = yNgramToLinesStream()


file_output = yOutputFileLinesStream()

file_output_name = toystream("../datasets/my_gpt/out_is_a.txt")

ngrams_dict > ngrams_to_lines > file_output  > file_output_name

#file_output.save()


