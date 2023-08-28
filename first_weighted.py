from yngrams import yNgrams

subject_verb_filename = "../datasets/Rus_word_ngramm/sbj_v.txt"
#verb_object_filename = "../datasets/Rus_word_ngramm/v_obj.txt"

dictionary_predicate_file = "E:\data\dictionaries_predicate\sketches.fr.dir_mt"



opts = {"item_per_line" : True,
        "line_handling" : "load",
        "max_lines " : 100000000,
        "ngrams_forward": True,
        "split_len_expected": 3,
        "split_symbol" : "|",
        "split_symbol" : "\t",
        "continue_after_error" : True,
        "distance_method" : "1w"}

utils = yNgrams(opts)
utils.load(dictionary_predicate_file)

utils.sort_value_vector_thrashold(utils.forward, 100)
distances_generator = utils.yield_distances(utils.forward, 15)
#pp.pprint(distances)

out_file = "big_out.txt"
utils.save(out_file,distances_generator, True)