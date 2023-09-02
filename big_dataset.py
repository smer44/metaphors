from  ystream import *



file_name = "E:\data\dictionaries\case_frames_0.fr.txt"
encoding=  'cp1251'
folder_name = "E:\data\dictionaries"

files = yFileNamesStream(folder_name)

linegen = yFileLinesStream(files, encoding, -100000)

sentences = yLastItemStream(linegen, "\t")

uniques = yUniqueStream(sentences)

import spacy
lang_name = 'ru_core_news_sm'
clauses =yClausesSpacy(uniques,spacy,lang_name)

output_encoding=  'utf-8'
output_file_name = "../datasets/out_claues.txt"

saver = yFileLinesSaver(clauses, output_file_name, output_encoding, True)

saver.save()

