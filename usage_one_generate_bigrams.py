from  ystream import *
from yngrams import yNgramsDict

input_file = toystream("../datasets/Rus_word_ngramm/v_obj.txt")
encoding=  'utf-8'

#files = [input_file]

fileLines = yInputFileLinesStream(encoding, -1)
ngramsLoad = yNGramsRawLoad( "|", True)

ngramsDict = yNgramsDict()

input_file > fileLines > ngramsLoad > ngramsDict
ngramsDict.store()

ngramsDict.cut(30)

#TODO: currently no vector cliping
distancesLines = yDistancesLinesStream(ngramsDict.ngrams, 30 )


output_file = toystream("../datasets/my_out/out_obj_v_2.txt")

output = yOutputFileLinesStream(encoding)

distancesLines >output > output_file

output.save()