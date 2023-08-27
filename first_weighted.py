from yngrams import yNgrams

subject_verb_filename = "../datasets/Rus_word_ngramm/sbj_v.txt"
verb_object_filename = "../datasets/Rus_word_ngramm/v_obj.txt"

opts = {"item_per_line" : True,
        "max_lines " : -100000,
        "ngrams_forward": True,
        "split_len_expected": 3,
        "split_symbol" : "|",
        "continue_after_error" : True,
        "distance_method" : "1w"}

utils = yNgrams(opts)
utils.load_file_lines(subject_verb_filename)

utils.sort_value_vector_thrashold(utils.forward, 100)
distances_generator = utils.yield_distances(utils.forward, 15)
#pp.pprint(distances)

out_file = "class_out.txt"
utils.save(out_file,distances_generator, True)