import pprint as pp

filename = "../datasets/n_prep_obj.txt"

def load_nprep_obj_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        dictionary = dict()
        backwards_dictionary = dict()
        limit = -100000
        for line in file.readlines():
            limit -=1
            if limit == 0: break
            line = line.strip()
            if line:
                spl = line.split("|")
                assert len(spl) == 4, f"!! wrong line {line}"
                noun1, prep, noun2, times = spl
                noun1 = noun1.strip().lower()
                prep = prep.strip().lower()
                key = noun1 # f"{noun1} {prep}"
                noun2 = noun2.strip().lower()
                dictionary.setdefault(key, set()).add(noun2)
                backwards_dictionary.setdefault(noun2, set()).add(key)
        return dictionary,backwards_dictionary

def set_uniform_weights(dictionary):
    ret_dictionary = dict()
    for key,value in dictionary.items():
        uniform_weight = 1/len(value)
        weighted_value = {(item, uniform_weight) for item in value}
        ret_dictionary[key] = weighted_value
    return ret_dictionary

def key_key_weighted(dictionary, backwards_dictionary):
    key_key_dict = dict()
    for key, value in dictionary.items():
        key_key_weights = dict()
        for item, item_weight in value:
            backward_vector = backwards_dictionary.get(item,[])
            for other_key, other_key_weight in backward_vector:
                if other_key != key:
                    key_weight_sum = key_key_weights.setdefault(other_key,0) +other_key_weight
                    key_key_weights[other_key] = key_weight_sum
        #need to normalize key_key_weights:
        norma = sum(value for value in key_key_weights.values())
        for key in key_key_weights:
            key_key_weights[key] /= norma

        sorted_list = [(key, value) for key, value in key_key_weights.items()]
        sorted_list.sort(key = lambda tuple : -tuple[1])
        sorted_list = sorted_list[:50]
        key_key_dict[key] = sorted_list
    return key_key_dict

def store_dict(file_name,dictionary, itemformat = lambda item : item):
    with open(file_name, 'w', encoding='utf-8') as out_file:
        for key, value in dictionary.items():
            if value:
                formatted_value = ",".join(f"{itemformat(item)}" for item in value)
                line = f"{key}:{formatted_value}\n"
                out_file.writelines(line)

#use methods :

dictionary,backwards_dictionary = load_nprep_obj_file(filename)

dictionary = set_uniform_weights(dictionary)
backwards_dictionary = set_uniform_weights(backwards_dictionary)

key_key_dict = key_key_weighted(dictionary, backwards_dictionary)
key_key_dict = key_key_weighted(key_key_dict, key_key_dict)
#key_key_dict = key_key_weighted(key_key_dict, key_key_dict)
#key_key_dict = key_key_weighted(key_key_dict, key_key_dict)
#pp.pprint(key_key_dict)

output = f"weighted_dict_n_prep_obj.txt"

store_dict(output, key_key_dict,itemformat = lambda item : item[0])




