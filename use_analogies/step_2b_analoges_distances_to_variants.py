from ystream import *

input_file =  "../../datasets/my_out/out_Rus_word_ngramm_distances_tfidf_sv_as.txt"


input_file = ySequence(input_file)
file_lines = yInputFileLinesStream()
split_to_entry = ySplitKeyVector(weightConvertFn = float)
key_vector_to_storage_input = yKeyVectorToKeyValueWeightStream()

storage = yStorageWithBag(
                         iter_method = "self",
                         store_before_iter = True,
                         filter_before_iter = 10000,
                         add_backwards = True,
                         #exclude = exclude
                        )


subject = "рука"
object = "мяч"

combis = yAnalogsCombinations(subject, object, 10)

input_file > file_lines > split_to_entry > key_vector_to_storage_input > storage > combis


for subjects, objects in combis:
    print(f"{subject} : {' '.join(subjects)} \n{object} :  {' '.join(objects)}")








