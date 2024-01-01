from ystream import *
#from ystream.ydistanceslinesstream import format_output2

input_bigramms_file = "../../datasets/my_out/out_Rus_word_ngramm_distances_tfidf_sv_as.txt"
output_file = "../../datasets/my_out/out_groups_sbj_v_weighted.txt"

input_file = ySequence(input_bigramms_file)

file_lines = yInputFileLinesStream()

split_to_entry = ySplitKeyVector(weightConvertFn = float)


input_file > file_lines > split_to_entry

ngrams = dict()

for key,vector in split_to_entry:
    assert key not in ngrams
    ngrams[key] = vector

#print(ngrams)



def calc_inner_distances(ngrams):
    #keys = list(ngrams.keys())
    #key_size = len(keys)
    #dmatrix = [[0 for _ in range(key_size)] for _ in range(key_size)]
    result = dict()
    empty_dict = dict()
    for key, vector in ngrams.items():
        inner_keys = list(vector.keys())
        inner_key_size = len(inner_keys)

        vector_all_dists = []
        for key_index in range(inner_key_size - 1):
            inner_key = inner_keys[key_index]
            for next_key_index in range(key_index+1,inner_key_size):
                next_inner_key = inner_keys[next_key_index]
                dist = ngrams.get(inner_key,empty_dict) .get(next_inner_key,0)
                if dist > 3:
                    vector_all_dists.append((inner_key,next_inner_key,dist))
        sorted_vector = sorted(vector_all_dists, key=lambda pair: -pair[2])
        sorted_vector = sorted_vector[:30]
        #result[key] = sorted_vector
        #line = format_output2(key, sorted_vector)
        #print(line)
        yield key, sorted_vector

#example жизнь:работа:29,люди:человек:29,город:дом:28,город:школа:28,язык:школа:27,
# жизнь:характер:26,люди:дом:26,человек:дом:26,жизнь:человек:25,жизнь:время:25,
# жизнь:сила:25,день:человек:25,день:программа:25,люди:часть:25,люди:работа:25,
# люди:время:25,форма:работа:25,человек:работа:25,жизнь:люди:24,жизнь:вид:24,
# жизнь:проблема:24,день:работа:24,люди:язык:24,люди:сила:24,человек:город:24,
# человек:образ:24,человек:время:24,человек:мир:24,человек:сила:24,язык:город:24

test_items = [("жизнь","работа",29), ("люди","человек",29),("город","дом",28) , ("город","школа",28) , ("язык","школа",27),
         ("жизнь","характер",26), ("люди","дом",26),("человек","дом",26), ("жизнь","человек",25) ]

def glue_list(items,limit = 4):
    known_sets= dict()
    for key, next_key, value in items:
        if key in known_sets:
            known_set = known_sets[key]
            if next_key not in known_set:
                if next_key in known_sets:
                    glued_set = known_sets[next_key]
                    if len(known_set) + len(glued_set) <= limit:
                        known_set.update(glued_set)
                        for item_in_set in known_set:
                            known_sets[item_in_set] = known_set
                else:
                    if len(known_set) +1 <= limit:
                        known_set.add(next_key)
                        known_sets[next_key] = known_set
        elif next_key in known_sets:
            known_set = known_sets[next_key]
            known_set.add(key)
            known_sets[key] = known_set
        else:
            new_set = {key, next_key}
            known_sets[key] = new_set
            known_sets[next_key] = new_set


    return {  "(" + ",".join(v) + ") " for v in known_sets.values()}



#known = glue_list(test_items)
#print(known)





encoding=  'utf-8'
with open(output_file, 'w', encoding=encoding) as file:
    for key, vector in calc_inner_distances(ngrams):
        glued_sets = glue_list(vector)
        line = f'{key} : {", ".join(glued_sets)}\n'
        file.write(line)


#calc_inner_distances(ngrams)


