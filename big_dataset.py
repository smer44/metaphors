from  yngrams import yNgrams

file_name = "E:\data\dictionaries\case_frames_0.fr.txt"



opts = {"item_per_line" : True,
        #"line_handling" : "inspect",
        "line_handling" : "load",
        "max_lines " : 10000000,
        "ngrams_forward": True,
        "split_len_expected": 10,
        "split_symbol" : "\t",
        "continue_after_error" : True,
        "distance_method" : "1w"}

#encoding='utf-8' # basic encoding
#encoding='windows-1253'#no
#encoding= 'iso-8859-7'#no
encoding=  'cp1251'#alt russian encoding

yng = yNgrams(opts)

yng.load(file_name, encoding=encoding)

print(yng.length_histo)