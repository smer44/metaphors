from ystream import *
#from ystream import format_output2


#TODO - extract it to classes

#input_bigramms_file = "../../datasets/my_out/out_sbj_v_clipped.txt"
#input_bigramms_file = "../../datasets/my_out/out_wiki_sbj_v.txt"
#input_bigramms_file = "../../datasets/my_out/out_n.txt"

#input_sv_file =  "../../datasets/my_out/out_Rus_word_ngramm_tfidf_sv.txt"
input_file =  "../../datasets/my_out/out_Rus_word_ngramm_distances_tfidf_sv_as.txt"

#input_bigramms_file = "../../datasets/my_out/out_sbj_v_case_frames.txt"

#input_bigramms_file = "../../datasets/my_out/out_nkrja.txt"

#output_file = "../../datasets/my_out/out_split_v2.txt"
#output_file = "../../datasets/my_out/out_split_wiki.txt"
#output_file = "../../datasets/my_out/out_split_case_frames.txt"
output_file = "../../datasets/my_out/out_kmeans_Rus_word_ngramm_distances_tfidf.txt"
#output_file = "../../datasets/my_out/out_split_nkrja.txt"

input_file = ySequence(input_file)

file_lines = yInputFileLinesStream()

split_to_entry = ySplitKeyVector(weightConvertFn = float)

input_file > file_lines > split_to_entry

vector_size = 20
word_distances = dict()

for key,vector in split_to_entry:
    assert key not in word_distances
    word_distances[key] = vector

for key,vector in list(word_distances.items()):
    for next_key, weight in vector.items():
        word_distances.setdefault(next_key,dict()).setdefault(key,weight)
    word_distances[key][key] = vector_size

normalize_ngrams(word_distances)

words = {*word_distances.keys()}

for item in word_distances.items():
    #print(item)
    words.update(vector.keys())
words = list(words)
print("LENGTH OF WORDS : ", len(words))

def init_centroid_distances(items,item_distances,choise_step):
    centroid_distances = {f"{items[n]}":{**item_distances[items[n]]} for n in range(0,len(items),choise_step)}
    return centroid_distances

centroid_distances = init_centroid_distances(words,word_distances,5)
print("length of centroid_distances = ", len(centroid_distances))
def pd(comment,d):
    print(comment)
    for key, value in d.items():
        print(key , " : " , value)

#pd("initial centroid_distances : " , centroid_distances)

def cluster_points_step(items_list,item_distances_dict, centroid_distances):
    #print("started cluster_points_step:")
    centroid_shift = float("inf")
    centroid_selections = dict()




    for item in items_list:
        selected_centroid_name = None
        min_dist = float("inf")
        for centroid, centroid_distances_for_item in centroid_distances.items():
            dist = -centroid_distances_for_item.get(item,0)
            #print(f"no entry found for key { item} for centroid {centroid}")
            if dist < min_dist:
                selected_centroid_name = centroid
                min_dist = dist
        #if selected_centroid_name is None:
            #print(f"no centroid selected for item {item} , with distances {item_distances_dict[item]}")
        centroid_selections.setdefault(selected_centroid_name, []).append(item)
    #print("length of centroid_selections : " , len(centroid_selections))
    for centroid_name, items_for_centroid in centroid_selections.items():

        items_len = len(items_for_centroid)
        for item in items_list:
            avg_dist = sum(item_distances_dict[item].get(item_for_centroid,0) for item_for_centroid in items_for_centroid) / items_len
            centroid_distances[centroid_name][item] = avg_dist
        #print(f"centroid_distances for : centroid_distances[{centroid_name}] = {centroid_distances[centroid_name]}")

    #print("ended cluster_points_step:")
    return centroid_distances, centroid_selections

def cluster_points(point_distances, points, centroid_distances, steps):

    for n in range(steps):
        centroid_distances,centroid_selections = cluster_points_step(points,point_distances,  centroid_distances)
    return centroid_selections

#centroid_distances, centroid_selections = cluster_points_step(words,word_distances, centroid_distances)

centroid_selections = cluster_points(word_distances, words, centroid_distances, 20)

#pd("FINAL centroid_selections : " , centroid_selections)

#make additional split for large groups:
split_limit = 7
encoding=  'utf-8'
with open(output_file, 'w', encoding=encoding) as file:
    for group_name,word_list in centroid_selections.items():
        if len(word_list) >70:
            group_items = set(word_list)
            group_word_distances = dict()
            for key in word_list:
                row = dict()
                group_word_distances[key] = row
                for inner_key in word_list:
                    dist = word_distances[key].get(inner_key,0)
                    if dist > 0 :
                        row[inner_key] = dist
            #pd(f"word_distances for group : {group_name}", group_word_distances)
            group_centroid_distances = init_centroid_distances(word_list, group_word_distances, len(word_list)//3)
            result = cluster_points(group_word_distances, word_list, group_centroid_distances, 20)
            #pd(f" - - SPLITTED GROUP : {group_name}", centroid_selections)
            #file.write(f" - - SPLITTED GROUP : {group_name}\n")
            for key, value in result.items():
                #file.write(f"{key} : {value}\n")
                line = " ".join(value)
                file.write(f"{line}\n")
        else:
            #file.write(f" - GROUP : {group_name} : {word_list}\n")
            line = " ".join(word_list)
            file.write(f"{line}\n")














