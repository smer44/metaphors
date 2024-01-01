from ystream import *

#words_folder = "..\..\datasets\pnames"

words_unsorted = "..\..\datasets\pnames\\unsorted.txt"

words_known = "..\..\datasets\pnames\english_names.txt",
"..\..\datasets\pnames\\female_names_rus.txt",
"..\..\datasets\pnames\\male_names_rus.txt",
"..\..\datasets\pnames\\male_surnames_ru.txt",
"..\..\datasets\pnames\\names_all.txt",


files_known = ySequence(*words_known)

files_unsorted = ySequence(words_unsorted)


#files_known = yFileNamesWalkStream(words_folder,ext = "txt")

lines = yInputFileLinesStream()

ybag = yBag()

files_unsorted > lines > ybag

ybag.store()
print("ybag len  =" , len(ybag.bag))

files_known > lines > ybag

ybag.exclude()

print("names in words_folder: ", len(ybag.bag))

output_lines = yOutputFileLinesStream()

output_file = ySequence("..\..\datasets\pnames\\unsorted_cleared.txt")


ybag > output_lines > output_file

output_lines.save()




#for item in ybag.bag:
#    print(item)

#lets find pnames in rus_words :


sv_file = "../../datasets/Rus_word_ngramm/sbj_v.txt"

sa_file = "../../datasets/Rus_word_ngramm/adj_n.txt"


input_files = ySequence(sv_file, sa_file)

input_file_full = yInputFileLinesStream()#   yInputFileFull()

line_split_stream = ySplitStream(skip = " \t\r\n|")

parce_tokens = ySpacyTokenStream()

filter_pname_lemmas = ySimpleFilterSpacyStream()




#input_files > input_file_full > line_split_stream> parce_tokens > filter_pname_lemmas > output_lines > output_file


#output_lines.save()

#for item in filter_pname_lemmas:
#    print(item)





