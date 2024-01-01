from  ystream import *
from yngrams import yNgramsDict

input_file = ySequence("../datasets/Rus_word_ngramm/adj_n.txt")
encoding=  'utf-8'

#files = [input_file]

fileLines = yInputFileLinesStream(encoding, -1)
#TODO - move backwards to ngram dict and not in ngrams raw load
ngramsLoad = yNGramsRawLoad( "|")

ngramsDict = yNgramsDict()

input_file > fileLines > ngramsLoad > ngramsDict
ngramsDict.store()

ngramsDict.cut(30)

#TODO: currently no vector cliping
distancesLines = yDistancesLinesStream(ngramsDict.ngrams, 30 )


output_file = ySequence("../datasets/my_out/out_adj_n.txt")

output = yOutputFileLinesStream(encoding)

distancesLines >output > output_file

output.save()