from ystream import *
#TODO - lemmatization
file_name_is_located = "..\datasets\my_gpt\is_in_out.txt"

#file_name_is_used = "..\datasets\my_gpt\is_used.txt"

file_name_is_a_3 = "..\datasets\my_gpt\is_a_3_out.txt"

file_name_input = ySequence(file_name_is_located, file_name_is_a_3)

file_lines = yInputFileLinesStream()

lines_split_by_defis = ySplitSimpleStream(split_symbol ="-")

#stamming_words = yStammingSpacyStream()


#triplets_to_entry  = yItemsFilterToMultiEntry(invert_marker = "@anti")

triplets_to_entry  = yItemsToSimpleEntryDoubleValue(True, False , fill_relation = "является",enclause = False)

#ydict = yStorageMulti()
ontology_simple = yStorageBackwardsSimple(iter_method = None,store_before_iter = True)

#associations = yGetAssociationsFromMultiStorage('комната',"велосипед", 1000)

#path_finder = yPathInSimpleStorage("комната", "велосипед",1000)
#path_finder = yPathInSimpleStorage("дом", "книга",1000)
path_finder = yPathTripletsInSimpleStorage("компьютер", "машина")
#file_name_input > file_lines > lines_split_by_defis >  triplets_to_entry > ydict > associations
file_name_input > file_lines > lines_split_by_defis > triplets_to_entry > ontology_simple > path_finder


for items in path_finder:
    print(items)

#for items in ydict:
#    d = items.verb_subjects
#    for key, value in d.items():
#        print(key, value )