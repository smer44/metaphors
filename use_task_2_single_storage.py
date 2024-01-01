from ystream import *

file_name_is_located = "..\datasets\my_gpt\is_a_3_out.txt"

file_name_input = ySequence(file_name_is_located)

file_lines = yInputFileLinesStream()

lines_split_by_defis = ySplitSimpleStream(split_symbol ="-", split_len = 2)

items_to_entry = yItemsSimpleToEntry(inverse = True)

ystorage= yStorageWithBag(iter_method ="bag", store_before_iter = True)

file_name_input > file_lines > lines_split_by_defis > items_to_entry>  ystorage


for item in ystorage:
    print(item)