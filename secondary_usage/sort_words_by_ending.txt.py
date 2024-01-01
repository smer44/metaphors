from ystream import *
import pprint as pp
input_bigramms_file = "../../datasets/russian_nouns.txt"

input_file = ySequence(input_bigramms_file)

file_lines = yInputFileLinesStream()

#invert_word = yMapStream(fn = lambda txt: txt[::-1])

input_file > file_lines

suffixes = "тель","чик","щик","ник","ниц","к","иц","юх","ёнок","ушк","ышк","ость" ,
"як", "ун","ач", "ущ","кос","кас","ив", "чив", "лив", "ист", "ск", "ов", "ев", "евит", "ин"


short_word_stams = "воз", "ход" , "лёт", "езд", "плав", "вяз", "ново"

suffixes =  short_word_stams
#d = {word[:3]:word[::-1] for word in file_lines}
d = dict()
for word in file_lines:
    #key = word[-3:]
    #d.setdefault(key,[]).append(word)
    for s in suffixes:
        if s in word:
            d.setdefault(s,[]).append(word)
encoding=  'utf-8'
for key, items in d.items():
    #print()
    #print (f" - {key} - ")
    #print()
    if items:
        with open("out_suffix_" + key + ".txt", "w",encoding = encoding) as file:
            for word in items:
                file.write(word + "\n")

        #print(word)


