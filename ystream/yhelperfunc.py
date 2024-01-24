def format_output( key, value_pairs):
    if value_pairs:
        #formatted_value = " ,".join(f"{pair[0]}:{pair[1]:.2f}" for pair in value_pairs)
        formatted_value = " ,".join(f"{pair[0]}:{pair[1]}" for pair in value_pairs)
        line = f"{key}:{formatted_value}\n"
        return line
def format_output2( key, value_pairs):
    if value_pairs:
        formatted_value = " ,".join(f"{pair[0]}:{pair[1]}:{pair[2]}" for pair in value_pairs)
        line = f"{key}:{formatted_value}\n"
        return line
def sort_clip_dict(vector,thrashhold):
    vector = sorted(vector.items(), key=lambda pair: -pair[1])
    vector = vector[:thrashhold]
    return vector

def sort_clip_keys(vector,thrashhold):
    vector = sorted(vector.keys(), key=lambda key: -vector[key])
    vector = vector[:thrashhold]
    return vector


def format_list(lst):
    return " ".join(lst)

def sort_dict(vector):
    vector = sorted(vector.items(), key=lambda pair: -pair[1])
    return vector


def normalize_dict(vector):
    all = sum(vector.values())
    for key in vector.keys():
        vector[key] /= vector[key]

def normalize_ngrams(ngrams):
    for vector in ngrams.values():
        normalize_dict(vector)


relation_marker = "@"

def back_relation(relation):
    if relation[-1] == relation_marker:
        return relation [:-1]
    else:
        return relation + relation_marker


#TODO : this should be extracted in analysis class
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



def finalize_relation(ngrams_connected, reverced_ngrams_connected):
    finalize_dict = dict()
    for (subj,verb), object_dict in ngrams_connected.items():
        for obj, object_weight in object_dict.items():
            subj_dict = reverced_ngrams_connected[(obj,verb)]
            subj_weight = subj_dict[subj]
            finalize_obj_dict =finalize_dict.setdefault((subj,verb),dict())
            finalize_obj_dict[obj] = object_weight * subj_weight
    return finalize_dict
