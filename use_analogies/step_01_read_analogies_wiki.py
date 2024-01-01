from ystream import *


input_bigramms_file = "../../datasets/wiki/Bigram_wiki_verb_subj.txt"

output_bigramms_file = "../../datasets/my_out/out_wiki_20_sbj_v.txt"

exclude = {"время",
           "человек",
           "раз" ,
           "сила" ,
           "слово" ,
           "дело",
           "люди",
           "случай",
           "день",
           "жизнь",
           "мир",
           "год",
           "мужчина",
           "женщина"}

exclude = {"-"}

input_file = ySequence(input_bigramms_file)

file_lines = yInputFileLinesStream(encoding=encoding_utf_8_sig )

split_items = ySplitSimpleStream(None,split_len = 3)

items_to_entry = yItemsToKeyValueEntry(inverse = True,
                                       fill_weight = False,

                                       )

storage = yStorageWithBag(
                         iter_method = "all",
                         store_before_iter = True,
                         filter_before_iter = 10000,
                         add_backwards = False,
                         exclude = exclude
                        )


distance_lines = yDistancesLinesStream(20,
                                       20,
                                       tostr = True,
                                       is_weighted = False)


#for item in distance_lines:
#    print(item)

output_lines = yOutputFileLinesStream()

output_file = ySequence(output_bigramms_file)

input_file > file_lines > split_items > items_to_entry> storage>distance_lines> output_lines > output_file


output_lines.save()
