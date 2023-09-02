from ystream import *


file_subj_v = "../datasets/my_out/out_subj_v.txt"

file_v_subj = "../datasets/my_out/out_v_subj.txt"

file_obj_v = "../datasets/my_out/out_obj_v.txt"

split_key_value = ":"

split_list = ","

encoding = "utf-8"

def load_ngrams(file_subj_v):

    fileLines = yFileLinesStream(encoding)
    fileLines.src(file_subj_v)

    ngrams = yNGramsLinesLoad(split_key_value ,split_list)
    fileLines > ngrams

    ngrams.store()
    return ngrams

subj_v = load_ngrams(file_subj_v)
v_subj = load_ngrams(file_v_subj)
obj_v = load_ngrams(file_obj_v)

print(subj_v.get_nearest("лошадь"))
print(v_subj.get_nearest("ехать"))
print(obj_v.get_nearest("дорога"))





