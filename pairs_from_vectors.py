import numpy as np
filename = "../datasets/ruscorpora_upos_skipgram_300_5_2018.vec"

dictionary_size = None
names, vectors = [] , []
dictionary_size, vector_size = None, None
print(f"reading file :{filename}")
with open(filename, 'r', encoding='utf-8') as file:
    first_line = file.readline().strip()
    dictionary_size, vector_size = first_line.split()
    dictionary_size, vector_size = int(dictionary_size), int(vector_size)

    for n in range(dictionary_size):
        line = file.readline().strip()
        if line :
            name, *vector = line.split()
            assert len(vector) == vector_size, f" wrong vector size for word {name}"
            vector = [float(x) for x in vector]
            names.append(name)
            vectors.append(vector)
print(f"done : read file:{filename}")
print("num " , dictionary_size, vector_size)

print(f"splitting dict on POS")
vectors = np.array(vectors)
dict_categories = dict()
for n in range(len(names)):
    fullname = names[n]
    name, part_of_speech = fullname.split("_")
    this_names, this_vectors = dict_categories.setdefault(part_of_speech , (list(),list()))
    this_names.append(name)
    this_vectors.append(vectors[n])

print(f"done : split dict on POS")

print("categories : ", dict_categories.keys())

verb_names, verb_vectors = dict_categories["VERB"]
noun_names, noun_vectors  = dict_categories["NOUN"]

assert len(verb_names) == len(verb_vectors)
assert len(noun_names) == len(noun_vectors)

distances = np.zeros(len(noun_names))
print(f"amount of verbs: {len(verb_names)} , amount of nouns: {len(noun_names)}")
threshold = 10

output_filename = (f"out2_ruscorpora_upos_skipgram_300_5_2018.txt")
with open(output_filename, 'w', encoding='utf-8') as out_file:
    for i in range(len(verb_names)):
        verb_name = verb_names[i]
        verb_vector = verb_vectors[i]

        for j in range(len(noun_names)):
            noun_name = noun_names[j]
            noun_vector = noun_vectors[j]
            distance = np.sum(np.abs(verb_vector - noun_vector))
            distances[j] = distance
        arg_pos = np.argsort(distances)[:threshold]
        values = ", ".join(f"{noun_names[arg]}:{distances[arg]}" for arg in arg_pos)
        out_line  = f"{verb_name}: {values}\n\n"
        out_file.writelines(out_line)
        print(out_line)


