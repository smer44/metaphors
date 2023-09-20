from ystream import *
from yngrams import yNgramsDict

file_subj_v = "../datasets/my_out/out_sbj_v_noweight.txt"

file_v_subj = "../datasets/my_out/out_v_sbj_noweight.txt"

file_obj_v = "../datasets/my_out/out_obj_v_noweight.txt"

file_v_obj = "../datasets/my_out/out_v_obj_noweight.txt"

split_key_value = ":"

split_list = ","

encoding = "utf-8"

def load_ngrams2(file_v_subj,  file_v_obj):

    fileLines = yInputFileLinesStream(encoding)
    ngramsloader = yNGramsLinesLoad(split_key_value, split_list)
    ngramsDict = yNgramsDict()

    fileLines(file_v_subj)> ngramsloader > ngramsDict
    ngramsDict.store()

    fileLines(file_v_obj)> ngramsloader > ngramsDict

    ngramsDict.store()

    return ngramsDict.to_sorted_lists()

def load_ngrams(file_name):

    fileLines = yFileLinesStream(encoding)
    ngramsloader = yNGramsLinesLoad(split_key_value, split_list)
    ngramsDict = yNgramsDict()

    fileLines(file_name)> ngramsloader > ngramsDict

    ngramsDict.store()

    return ngramsDict.to_sorted_lists()


subj_v = load_ngrams(file_subj_v)
v_subj = load_ngrams(file_v_obj)
obj_v = load_ngrams(file_obj_v)

rng = 5
print(subj_v.get_nearest("лошадь",rng))
print(v_subj.get_nearest("ехать",rng))
print(obj_v.get_nearest("дорога",rng))





