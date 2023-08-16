filename = "sbj_v.txt"
filename = "Bigram_wiki_v.txt"

def load_ngramm_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        dictionary = dict()
        for line in file.readlines():

            #spl = line.split("|",maxsplit=3)
            spl = line.split( maxsplit=3)

            first,second, *rest = spl
            first = first.strip()
            second = second.strip()
            #dictionary.setdefault(first,list()).append(second)
            dictionary.setdefault(second, set()).add(first)
        return dictionary


dictionary = load_ngramm_file(filename)
print(f"file {filename} is read into a dictionary of size {len(dictionary)}")

output = f"out_{filename}"





#calculate similarity for items, naive
distances = dict()
keys = list(dictionary.keys())
with open(output, 'w', encoding='utf-8') as out_file:
    for i in range(len(keys)):
        key = keys[i]
        words = dictionary[key]

        #current_dict = dict()
        #distances[key] = current_dict
        current_list = list()
        for j in range(i+1,len(keys)):
            next_key = keys[j]
            next_words = dictionary[next_key]
            common_words = words.intersection(next_words)
            common_weight = len(common_words)
            current_list.append((next_key, common_weight))
        current_list.sort(key = lambda pair: -pair[1])

        current_list = current_list[:5]
        #distances[key] = current_list
        print(f"processed word: {key} : {current_list}")
        formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in current_list)
        line = f"{key}:{formatted_value}\n\n"
        out_file.writelines(line)

print(f"dictionary stored in output file : {output}")

#--
def save_dict(out_file):
    with open(output, 'w', encoding='utf-8') as out_file:
        for key, value in distances.items():
            #formatted_key = str(key)
            formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in value)
            line = f"{key}:{formatted_value}\n\n"
            out_file.writelines (line)


