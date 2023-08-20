import pprint as pp

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
                spl = line.split("|")
                assert len(spl) == 4, f"!! wrong line {line}"
                noun1, prep, noun2, times = spl
                noun1 = noun1.strip().lower()
                prep = prep.strip().lower()
                key = f"{noun1} {prep}"
                noun2 = noun2.strip().lower()
                dictionary.setdefault(key, set()).add(noun2)
                backwards_dictionary.setdefault(noun2, set()).add(key)
        return dictionary,backwards_dictionary

dictionary,backwards_dictionary = load_nprep_obj_file(filename)


#pp.pprint(dictionary)
output = f"backward_dict_n_prep_obj.txt"
def store_dict(file_name,dictionary):
    with open(file_name, 'w', encoding='utf-8') as out_file:
        for key, value in dictionary.items():
            if value:
                formatted_value = ",".join(item for item in value)
                line = f"{key}:{formatted_value}\n"
                out_file.writelines(line)


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

dictionary2 = intersect_set_values(dictionary, backwards_dictionary )
backwards_dictionary2 = intersect_set_values(backwards_dictionary, dictionary )

dictionary3 = intersect_set_values(dictionary2, dictionary )
backwards_dictionary3 = intersect_set_values(backwards_dictionary2, backwards_dictionary )

dictionary4 = intersect_set_values(dictionary3, backwards_dictionary3 )
backwards_dictionary4 = intersect_set_values(backwards_dictionary3, dictionary3 )

dictionary_final = intersect_set_values(dictionary4, dictionary2 )


output3 = f"next2_step_dict_n_prep_obj.txt"
store_dict(output3,dictionary_final)