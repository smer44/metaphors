import pprint as pp

import numpy as np

filename = "../n_prep_obj.txt"


def load_nprep_obj_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        dictionary = dict()
        backwards_dictionary = dict()
        #limit = 10000000
        for line in file.readlines():
            #limit -=1
            #if limit == 0: break
            line = line.strip()
            if line:
                #print(line)
                spl = line.split("|")
                assert len(spl) == 4, f"!! wrong line {line}"
                noun1, prep, noun2, times = spl
                noun1 = noun1.strip().lower()
                prep = prep.strip().lower()
                key = noun1
                #key = f"{noun1} {prep}"
                noun2 = noun2.strip().lower()
                dictionary.setdefault(key, set()).add(noun2)


                backwards_dictionary.setdefault(noun2, set()).add(key)
        return dictionary,backwards_dictionary

dictionary,backwards_dictionary = load_nprep_obj_file(filename)


#pp.pprint(dictionary)
#pp.pprint(backwards_dictionary)

def store_dict(file_name,dictionary_to_print):
    with open(file_name, 'w', encoding='utf-8') as out_file:
        for key, value in dictionary_to_print.items():
            #print("key, value : ", key , value)
            if value:
                formatted_value = ",".join(item for item in value)
                line = f"{key}:{formatted_value}\n"
                out_file.writelines(line)

def distance_set_values(output_file_object,dictionary):
    print(f"distance_set_values : storing at {output_file_object.name}")
    all_keys = list(dictionary.keys())
    all_len = len(all_keys)
    dist_for_key = np.zeros(all_len,dtype=np.int32)
    trashold = 30
    for i in range(all_len-1):
        key = all_keys[i]
        value = dictionary.get(key,None)
        if not value : continue
        dist_for_key[0:i + 1] = 0
        for j in range(i+1,all_len):
            next_name = all_keys[j]
            #print("pair:", key, next_name)
            next_value = dictionary[all_keys[j]]
            common_items = value.intersection(next_value)
            common_items_amount = len(common_items)
            dist_for_key[j] = -common_items_amount
        #trim = min(trashold,all_len-i-1)
        arg_pos = np.argsort(dist_for_key)[:trashold]
        #build an output string:
        formatted_value = ",".join(f"{all_keys[pos]}:{-dist_for_key[pos]}" for pos in arg_pos)
        line = f"{key}:{formatted_value}\n"
        #print("line:",line, arg_pos)
        output_file_object.writelines(line)


def intersect_set_values(dictionary, reference_dict):

    dictionary2 = dict()
    for key, value in dictionary.items():
        summ_set = None
        if not value: continue
        for item in value:
            next_set = reference_dict.get(item, set())
            if next_set:
                if summ_set is None:
                    if key in next_set:
                        next_set.remove(key)
                    summ_set = next_set
                else:
                    summ_set = summ_set.intersection(next_set)
        dictionary2[key] = summ_set
    return dictionary2
#do i remove something from dictionary here ?
#dictionary2 = intersect_set_values(dictionary, backwards_dictionary )
#backwards_dictionary2 = intersect_set_values(backwards_dictionary, dictionary )

#TODO : this destroys dictionary somehow:
#dictionary3 = intersect_set_values(dictionary2, dictionary )

#backwards_dictionary3 = intersect_set_values(backwards_dictionary2, backwards_dictionary )

#dictionary4 = intersect_set_values(dictionary3, backwards_dictionary3 )
#backwards_dictionary4 = intersect_set_values(backwards_dictionary3, dictionary3 )

#dictionary_final = intersect_set_values(dictionary4, dictionary2 )
#dictionary_final =  dictionary3

output = f"forward_dict_n_prep_obj.txt"
output_backward = f"backward_dict_n_prep_obj.txt"

#store_dict(output,dictionary)
#store_dict(output_backward,backwards_dictionary)

output_final = f"dist_n_prep_obj.txt"
with open(output_final, 'w', encoding='utf-8') as out_file: distance_set_values(out_file,dictionary)