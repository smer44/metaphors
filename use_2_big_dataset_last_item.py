from  ystream import *


#TODO - correct mistakes:
# -|
#амммммммяммммммм
# глагол нет
#одинаковой-- ( два тире в конце)
#точка тире
# но может быть и корректно человек --
#может ли быть имя фу?
#тысячелетие|комментировать?
#пассивный залог делает активным
#И тем не менее тысячелетия исполины человеческой мысли снова и снова комментировали Писание, раскрывая все более глубокие его слои .

#last file = E:\data\dictionaries\case_frames_21.fr.txt

file_name = "E:\data\dictionaries\case_frames_0.fr.txt"

output_file_name = "../datasets/out_claues_sv.txt"

encoding=  'cp1251'
folder_name = "E:\data\dictionaries"


skip_until = "E:\data\dictionaries\case_frames_26.fr.txt"
file_names = yFileNamesWalkStream(folder_name,skip_until = skip_until)
file_to_lines = yInputFileLinesStream( encoding, -1)

sentences = ySplitSimpleStream("\t", selection=-1)

uniques = yUniqueStream()

parce_tokens = ySpacyTokenStream()

clauses =yClauseNaiveFilterSpacyStream()

output_encoding=  'utf-8'

lines_to_output_file = yOutputFileLinesStream(output_encoding, True)

output_file_name = ySequence(output_file_name)

file_names > file_to_lines > sentences > uniques >parce_tokens > clauses > lines_to_output_file > output_file_name


lines_to_output_file.save()
#for item in file_names:
#    print(item)

