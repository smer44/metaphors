from  ystream import *


file_name = ySequence("../datasets/my_gpt/facts_gpt.txt")
file_lines = yInputFileLinesStream()

parse = ySpacyTokenStream()

to_str = (f"{x.lemma_}:{x.pos_}:{x.dep_}" for x in parse)

output_file = ySequence("../datasets/my_out/out_facts_gpt.txt")

output = yOutputFileLinesStream()



file_name > file_lines > parse  >output > output_file

output.save()