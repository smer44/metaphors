from ystream import *
#TODO - lemmatization
file_names = "..\datasets\my_gpt\is_a_3.txt" #, "..\datasets\my_gpt\is_used.txt"

output_name = "..\datasets\my_gpt\is_a_3_out.txt"

file_name_input = ySequence(file_names)

file_lines = yInputFileLinesStream()

lines_split_by_defis = ySplitSimpleStream(split_symbol ="-", split_len = 2)

stamming_words = yStammingSpacyStream()

format_out_lines =  yFormatItemsToString(" - ")

out_lines_file =  yOutputFileLinesStream()

out_file_name = ySequence(output_name)

file_name_input > file_lines > lines_split_by_defis >stamming_words > format_out_lines > out_lines_file > out_file_name

out_lines_file.save()

#for items in format_out:
#    print(items)

#for items in ydict:
#    d = items.verb_subjects
#    for key, value in d.items():
#        print(key, value )