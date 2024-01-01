from ystream import *

input_folder ="E:\data\Научная фантастика"


skip_until = "E:\data\Научная фантастика\Русская\Альберт Валентинов\Валентинов - Казнь.rtf"

input_file_name = yFileNamesWalkStream(input_folder, ".rtf", skip_until=None)

file_name = "E:\data\skazki.txt"

file_name = "E:\data\small_tale.txt"

input_file_name =ySequence(file_name)

input_file_full = yInputFileFull(encoding=encoding_ru,to_rtf= True)

input_file_full = yInputFileFull()


parse_tokens = ySpacyTokenStream()

clauses = yClauseNaiveFilterSpacyStream()


output = yOutputFileLinesStream(append=False)
output_file = ySequence("../datasets/my_out/out_trigrams_skazki.txt")


input_file_name > input_file_full > parse_tokens > clauses > output > output_file


output.save()
clauses.statistics()

