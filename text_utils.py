import pprint as pp

subject_verb_filename = "../datasets/Rus_word_ngramm/sbj_v.txt"
verb_object_filename = "../datasets/Rus_word_ngramm/v_obj.txt"

def load_ngrams_lines(filename, words, split_symbol = "|",lineLen=3, max_lines=400000 ):
    with (open(filename, 'r', encoding='utf-8') as file):
        ngrams = dict()
        reverced_ngrams = dict()
        for line in file.readlines():
            line = line.strip()
            if line:
                max_lines  -=1
                if max_lines == 0:
                    break

                #spl = line.split("|",maxsplit=3)
                spl = line.split(split_symbol)
                assert len(spl) > 1 and len(spl) == lineLen ,\
                    f"load_ngrams_lines : wrong split {spl}"

                weight = float(spl[-1].strip())
                value = spl[-2].strip()
                rest = [item.strip() for item in spl[:-2]]
                words.add(value)
                words.update(rest)
                key = " ".join(rest)
                key_dict = ngrams.setdefault(key, dict())
                old_weight = key_dict.setdefault(value,0)
                key_dict[value]  = old_weight + weight
                #put in test reverced ngrams:
                #TODO must be deleted later
                #key_dict = reverced_ngrams.setdefault(value, dict())
                #old_weight = key_dict.setdefault(key, 0)
                #key_dict[key] = old_weight + weight



        return ngrams, reverced_ngrams

def reverce_ngrams(ngrams):
    ngrams_reverced = dict()
    for key, key_dict in ngrams.items():
        key_dict_len = len(key_dict)
        for word,word_weight in key_dict.items():
            reverced_key_dict = ngrams_reverced.setdefault(word, dict())
            old_weight = reverced_key_dict.get(key, 0)
            reverced_key_dict[key] = old_weight + word_weight
    return ngrams_reverced





def normalize_ngrams(ngrams):
    for key, key_dict in ngrams.items():
        norm = sum(key_dict.values())
        for word in key_dict:
            key_dict[word] /=norm


def connect_ngrams(ngrams , ngrams2):
    ngrams_connected = dict()
    for word, word_dict in ngrams.items():
        for word2, word2_weight in word_dict.items():
            word_2_dict = ngrams2.get(word2,None)
            if word_2_dict:
                for word3, word3_weight in word_2_dict.items():
                    pair_dict = ngrams_connected.setdefault((word, word2) , dict())
                    old_weight = pair_dict.get(word3,0)
                    pair_dict[word3] = old_weight + word2_weight*word3_weight
    return ngrams_connected








words = set()



# for bigram wiki
#ngrams = load_ngrams_lines(filename,words, split_symbol =None)
ngrams, reverced_ngrams = load_ngrams_lines(subject_verb_filename,words, split_symbol ="|")
ngrams2, reverced_ngrams2 = load_ngrams_lines(verb_object_filename,words, split_symbol ="|")

normalize_ngrams(ngrams)
#normalize_ngrams(reverced_ngrams)
normalize_ngrams(ngrams2)
#normalize_ngrams(reverced_ngrams2)



#ngrams_reverced = reverce_ngrams(ngrams)
#normalize_ngrams(ngrams_reverced)
#pp.pprint(ngrams_reverced)
#pp.pprint(reverced_ngrams_test)

#ngrams2 = load_ngrams_lines(filename2,words, split_symbol ="|")
#normalize_ngrams(ngrams2)
#pp.pprint(ngrams2)

ngrams_connected = connect_ngrams(ngrams,ngrams2)#has subj_v -> obj connection
reverced_ngrams_connected = connect_ngrams(reverced_ngrams2,reverced_ngrams) #has obj, verb -> subj connection
#also need subj, obj -> verb, will do it later.

def finalize_relation(ngrams_connected, reverced_ngrams_connected):
    finalize_dict = dict()
    for (subj,verb), object_dict in ngrams_connected.items():
        for obj, object_weight in object_dict.items():
            subj_dict = reverced_ngrams_connected[(obj,verb)]
            subj_weight = subj_dict[subj]
            finalize_obj_dict =finalize_dict.setdefault((subj,verb),dict())
            finalize_obj_dict[obj] = object_weight * subj_weight
    return finalize_dict


def sort_inner_dicts(d, limit= None):
    sorted_dict = dict()
    for key, inner_dict in d.items():
        sorted_row = sorted(inner_dict.items(),key = lambda key_value: -key_value[1])
        if limit:
            sorted_row =  sorted_row[:limit]
        sorted_dict[key] = sorted_row
    return sorted_dict



normalize_ngrams(ngrams_connected)
#pp.pprint(ngrams_connected)
#normalize_ngrams(reverced_ngrams_connected)
#pp.pprint(reverced_ngrams_connected)
final_ngrams =ngrams_connected # finalize_relation(ngrams_connected,reverced_ngrams_connected)

sorted_dict = sort_inner_dicts(final_ngrams,30)

#pp.pprint(sorted_dict)


#saving it


def save_dict_of_iterables(out_file,dictionary ):
    with open(out_file, 'w', encoding='utf-8') as file:
        for key, value in dictionary.items():
            #formatted_key = str(key)
            #formatted_value = ",".join(f"{pair[0]}:{pair[1]*10000:.6f}" for pair in value)
            formatted_value = ",".join(f"{pair[0]}" for pair in value)
            line = f"{key}:{formatted_value}\n"
            file.writelines (line)
            print(line)


out_file = "connect_out.txt"

save_dict_of_iterables(out_file,sorted_dict)
