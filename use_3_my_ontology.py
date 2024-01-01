from ystream import *

file_names = "..\datasets\my_gpt\is_a_artifical.txt"

file_name_input = ySequence(file_names)

file_lines = yInputFileLinesStream()

lines_to_storage = yLinesToSimpleOntology()

ontology_simple = yStorageWithBag(iter_method = None, store_before_iter = True)

path_finder = yPathInSimpleStorage("кровать", "автомобиль",10000)

path_3_finder = yPathTripletsInSimpleStorage("спальня", "еда")
#path_finder = yPathInSimpleStorage("книга", "дом")

#file_name_input > file_lines > lines_to_storage > ontology_simple >path_finder
file_name_input > file_lines > lines_to_storage > ontology_simple >path_3_finder

for items in path_3_finder:
    print(items)
