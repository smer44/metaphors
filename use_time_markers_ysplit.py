from  ystream import *
"""
было [1209, 2975, 3084, 3464, 3578, 4803, 6630, 6676, 6794, 8020, 8131, 8174, 8618, 8792, 9966, 10144, 10600, 10860, 11442, 12484, 12833, 13279, 14405, 15583, 16790, 24168, 24638, 27587, 29941, 30275, 30309, 32249, 32667, 32779, 35333, 35365, 35489, 36763, 36806, 37028, 37732, 38181, 38255, 39171, 40701, 42044, 42817, 44070, 44163, 45931, 46077, 46353, 47579, 48405, 49238, 49377, 49428, 50461, 54723, 59508, 59520, 60076, 60119, 61901, 62688, 63857, 65908, 67794, 69030, 71301, 71889, 71900, 72178, 72952, 78463, 82027, 82068, 82087, 84963]
исчезло [1211, 11640, 12812, 75346]
прошедшие [1195, 9713]
вчерашнее [1208, 69472]
"""

input_file = "E:\data\Научная фантастика\Русская\Александр Абашели\Абашели - Женщина в зеркале.rtf"

input_folder ="E:\data\Научная фантастика"


input_file_name = yFileNamesWalkStream(input_folder, ".rtf")

#input_file_name = ySequence(input_file)

input_file_full = yInputFileFull(encoding=encoding_ru,to_rtf= True)

split = ySplitStream()

marker = yPseudoTimeMarker()


#input_file_name > input_file_full > split > marker

input_file_name > input_file_full > split > marker

marker.store()

#marker.nearest_words()

#marker.random_nearest()
marker.nearest_all_list_cut()

output = yOutputFileLinesStream()

output_file = ySequence("../datasets/my_out/out_time_markers.txt")

def value_format(v):
    return ", ".join(f"{value[0][0]}:{value[0][1]}:{value[1]}"  for value in v )

output.source = (f"{k} ~ {value_format(v)}" for k,v in marker.words_nearest_lists.items())

output > output_file

output.save()

