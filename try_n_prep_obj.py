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

dictionary2 = dict()
for key, value in dictionary.items():
    summ_set = None
    for item in value:
        next_set = backwards_dictionary.get(item, set())
        if next_set:
            if summ_set is None:
                next_set.remove(key)
                summ_set = next_set
            else:
                summ_set = summ_set.intersection(next_set)
    dictionary2[key] = summ_set

dictionary3 = dict()
for key, value in dictionary2.items():
    summ_set = None
    for item in value:
        next_set = dictionary.get(item, set())
        if next_set:
            summ_set = next_set
        else:
            summ_set = summ_set.intersection(next_set)
    dictionary3[key] = summ_set




output3 = f"next_step_dict_n_prep_obj.txt"
store_dict(output3,dictionary3)