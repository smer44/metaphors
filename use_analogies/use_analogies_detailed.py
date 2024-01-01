from ystream import *


input_bigramms_file = "../../datasets/Rus_word_ngramm/sbj_v.txt"

input_bigramms_file = "../../datasets/out_claues_sv.txt"

#input_bigramms_file = "../../datasets/Rus_word_ngramm/nkrja.txt"

output_bigramms_file = "../../datasets/my_out/out_sbj_v_clipped.txt"

output_bigramms_file = "../../datasets/my_out/out_sbj_v_case_frames.txt"

#output_bigramms_file = "../../datasets/my_out/out_nkrja.txt"

input_file = ySequence(input_bigramms_file)

file_lines = yInputFileLinesStream()

split_symbol = "|"
#split_symbol = None


exclude = {"-",
           "быть",
           "иметь" ,
           "мочь",
           "существовать",
"находиться",
           "делать",
           "человек",
           "часть",
           "жизнь",
           "бог"


}

#for nkrja
split_items = ySplitSimpleStream(split_symbol,
                                 split_len = 11,
                                 selection_to = 3 )

split_items = ySplitSimpleStream(split_symbol,
                                 #split_len = 3,
                                 selection_to = 2 )

items_to_entry = yItemsToKeyValueEntry(inverse = False,
                                       fill_weight = 1,
                                       #weight_to_int = True
                                        )
#exclude = {"-"}
storage = yStorageWithBag(
                         iter_method =  "all",
                         store_before_iter = True,
                         filter_before_iter = 5000,
                         add_backwards = False,
                        exclude = exclude,
                        clip_rows_amount = 50)


distance_lines = yDistancesLinesStream(70,20,tostr = True, is_weighted = False)

#vector_storage = yStorageKeyVector()

#lines_from_storage = ySortedCutVectorsFromStorage()

output_lines = yOutputFileLinesStream()

output_file = ySequence(output_bigramms_file)

# TODO - load it from a file
# then check each combinations in a vector



#input_file > file_lines > split_items > items_to_entry > storage > lines_from_storage > output_lines > output_file
#for item in storage:
#    print(item)



input_file > file_lines > split_items > items_to_entry > storage >distance_lines > output_lines > output_file

#for item in items_to_entry:
#    print(item)


output_lines.save()









