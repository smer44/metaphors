from  ystream import *


file_name = ySequence("../datasets/my_gpt/facts_gpt.txt")

input_folder ="E:\data\Научная фантастика"
input_folder_files = yFileNamesWalkStream(input_folder, ".rtf")

file_lines = yInputFileLinesStream()

input_file_full = yInputFileFull(encoding=encoding_ru,to_rtf= True)

parser = ySpacyTokenStream()

clause_filter = yClauseNaiveFilterSpacyStream()# yClauseFilterSpacyStream()

output_stream = yOutputFileLinesStream()

output_file = ySequence("../datasets/my_out/out_parced_clauses.txt")


input_folder_files> input_file_full >  parser > clause_filter>output_stream > output_file

output_stream.save()

#for tuple in clause_filter:
#    print(tuple )



