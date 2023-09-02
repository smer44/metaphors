from  ystream import *

#subject_verb_filename = "../datasets/Rus_word_ngramm/sbj_v.txt"

input_file = "../datasets/out_claues.txt"
encoding=  'utf-8'

files = [input_file]

linegen = yFileLinesStream(files, encoding, -1)

ngrams = yNGramsStorage(linegen , "|")


ngrams.store()

output_file = "out_.txt"
encoding=  'utf-8'

output = yFileLinesSaver(ngrams.yield_first_method(),  output_file, encoding)

output.save()






