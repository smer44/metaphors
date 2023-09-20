from  ystream import *
from yngrams import yNgramsDict

encoding=  'utf-8'


input_file = toystream("../datasets/Rus_word_ngramm/sbj_v.txt")

input_file_2 = toystream("../datasets/Rus_word_ngramm/v_obj.txt")

fileLines = yInputFileLinesStream(encoding, -1)

ngramsLoad = yNGramsRawLoad("|")

ngramsDict = yNgramsDict(forwards = False, backwards = True)

input_file > fileLines > ngramsLoad > ngramsDict



ngramsDict.store()

ngramsDict.init(forwards = True, backwards = False)

ngramsDict.store()


ngramsDict.cut(30)

#for line in ngramsDict:
#    print(line)

distancesLines = yDistancesLinesStream(ngramsDict.ngrams, 30 )

output_file = toystream("../datasets/my_out/out_v_subj_obj.txt")

output = yOutputFileLinesStream(encoding)

distancesLines >output > output_file

output.save()



