from ystream import *

input_sv_file = "../../datasets/Rus_word_ngramm/v_obj.txt"

input_as_file = "../../datasets/Rus_word_ngramm/v_obj.txt"

output_sv_file = "../../datasets/my_out/out_Rus_word_ngramm_tfidf_vo.txt"
output_as_file = "../../datasets/my_out/out_Rus_word_ngramm_tfidf_ov.txt"

input_folder_exclude  = "..\..\datasets\pnames"

files_exclude  = yFileNamesWalkStream(input_folder_exclude,ext = "txt")

lines_exclude = yInputFileLinesStream()

ybag_exclude = yBag()


files_exclude > lines_exclude > ybag_exclude

ybag_exclude.store()

print("ybag len  =" , len(ybag_exclude.bag))



input_file = ySequence(input_sv_file)
file_lines = yInputFileLinesStream()
split_symbol = "|"
exclude = {"-"}
exclude.update(ybag_exclude.bag.keys())

print("exclude len  =" , len(exclude))

split_items = ySplitSimpleStream(split_symbol,
                                 #split_len = 11,
                                 selection_to = 3 )

items_to_entry = yItemsToKeyValueEntry(inverse = True,
                                       #fill_weight = 1,
                                       weight_to_int = True
                                        )

storage = yStorageWithBag(
                         iter_method =  "self",
                         store_before_iter = True,
                         filter_before_iter = 5000,
                         add_backwards = False,
                        exclude = exclude,
                        clip_rows_amount = 100#is not used?
)

tfitf_lines = yTFIDFLines()

output_lines = yOutputFileLinesStream()

output_file = ySequence(output_sv_file)





input_file > file_lines > split_items> items_to_entry > storage > tfitf_lines> output_lines > output_file

#storage.store()

#for item in tfitf_lines:
#    print(item)

output_lines.save()


#---- THE SAME FOR  ADJ->N,  inverse = True,


input_file = ySequence(input_as_file)
file_lines = yInputFileLinesStream()

split_items = ySplitSimpleStream(split_symbol,
                                 #split_len = 11,
                                 selection_to = 3 )

items_to_entry = yItemsToKeyValueEntry(inverse = False,
                                       #fill_weight = 1,
                                       weight_to_int = True
                                        )

storage = yStorageWithBag(
                         iter_method =  "self",
                         store_before_iter = True,
                         filter_before_iter = 5000,
                         add_backwards = False,
                        exclude = exclude,
                        clip_rows_amount = 100#is not used?
)

tfitf_lines = yTFIDFLines()

output_lines = yOutputFileLinesStream()

output_file = ySequence(output_as_file)



input_file > file_lines > split_items> items_to_entry > storage > tfitf_lines>output_lines > output_file

output_lines.save()




