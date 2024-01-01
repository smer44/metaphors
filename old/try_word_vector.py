from ystream import *
import numpy as np
filename = "../datasets/ruscorpora_upos_skipgram_300_5_2018.vec"

input_files = ySequence(filename)

file_vector = yInputFileVector()

input_files >  file_vector

for line in file_vector:
    print(line)


#TODO - make vector distance stream



"""

dictionary_size = None
names, vectors = [] , []
with open(filename, 'r', encoding='utf-8') as file:
    first_line = file.readline().strip()
    dictionary_size, vector_size = first_line.split()
    dictionary_size, vector_size = int(dictionary_size), int(vector_size)
    print("num " , dictionary_size, vector_size)
    for n in range(dictionary_size):
        line = file.readline().strip()
        if line :
            name, *vector = line.split()
            assert len(vector) == vector_size, f" wrong vector size for word {name}"
            vector = [float(x) for x in vector]
            names.append(name)
            vectors.append(vector)
print(f"file {filename} read")

output_filename = f"out_{filename}"
vectors = np.array(vectors)
thrashhold = 10
last_word = "2-й_ADJ"
with open(output_filename, 'w', encoding='utf-8') as out_file:
    for i in range(dictionary_size-1):
        name, vector = names[i] , vectors[i]
        distances = []
        for j in range(i+1,dictionary_size):
            next_name = names[j]
            next_vector = vectors[j]
            distance  = np.sum(np.abs(vector - next_vector))
            distances.append(distance)
        np_distances = np.array(distances)
        arg_pos = np.argsort(np_distances)[:thrashhold]
        values = ", ".join( f"{names[i+1+arg]}:{distances[arg]}" for arg in arg_pos)
        out_line = f"{name}:{values}\n\n"
        out_file.writelines(out_line)
        print(out_line)
"""








