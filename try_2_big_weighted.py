from  ystream import *

#subject_verb_filename = "../datasets/Rus_word_ngramm/sbj_v.txt"

input_file_name = "../datasets/out_claues.txt"
encoding=  'utf-8'

input_file = ySequence(input_file_name)

file_lines = yInputFileLinesStream()

#linegen = yFileLinesStream(files, encoding, -1)

lines_split = ySplitSimpleStream("|")


#split_to_entry = yItemsFilterByFirstItem(first_item = "svo")

split_to_entry = yMapStream(fn = lambda items : (items[1], (items[3], items[2]),1))



klause_storage = yStorageWithBag(iter_method ="kv", store_before_iter = True)

items_to_line = yFormatKeyDictDuoToString()


#use some ngram storage here
#ngrams.store()

output_file = ySequence("out_claues_stored.txt")


output = yOutputFileLinesStream(append=False)

#output.save()

input_file > file_lines > lines_split > split_to_entry > klause_storage > items_to_line > output > output_file

output.save()

#for items in items_to_line:
#    print(items)






