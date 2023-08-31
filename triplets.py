from  ystream import *

input_file = "../datasets/Rus_word_ngramm/v_obj.txt"
encoding=  'utf-8'

files = [input_file]

linegen = yFileLinesLoader(files, encoding,-1)

ngrams = yNGramsStorage(linegen , "|")

ngrams.store()

output_file = "out_v_obj.txt"

output = yFileLinesSaver(ngrams.yield_first_method(),  output_file, encoding)

output.save()