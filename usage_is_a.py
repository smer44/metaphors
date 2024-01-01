from  ystream import *


file_name = ySequence("../datasets/my_gpt/is_a.txt")

file_lines = yInputFileLinesStream()

lines_to_items =  ySplitSimpleStream("- это")

strip_items = yMapStream(fn = lambda items: (items[0], (items[1][:-1], "является"), 1))

ngrams_dict = yStorageWithBag(iter_method ="kv", store_before_iter = True)

file_name > file_lines >lines_to_items >strip_items > ngrams_dict


for item in ngrams_dict:
    print(item)

#ngrams_to_lines = yNgramToLinesStream()


file_output = yOutputFileLinesStream()

file_output_name = ySequence("../datasets/my_gpt/out_is_a.txt")

#ngrams_dict > ngrams_to_lines > file_output  > file_output_name

#file_output.save()


