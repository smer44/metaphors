import pprint as pp
import sys



class yNgramsDeprecated:

    def __init__(self, opts):
        self.opts = dict()


        self.line_handling_variants = {"load" : self.load_line,
                                       "inspect" : self.inspect_line}
        self.item_handling_variants = {"weighted_pair" : self.handle_weighted_pair,
                                       "items10" : self.hangle_10_items}
        self.configure(opts)

    def configure(self, opts):
        for key, value in opts.items():
            self.opts[key.strip()] = value

        line_handling = self.opts.get("line_handling", None)
        if not line_handling:
            raise ValueError("NGrams.configure : no line_handling option given")
        self.line_handling_method = self.line_handling_variants.get(line_handling, None)
        if not self.line_handling_method:
            raise ValueError("NGrams.configure : wrong line_handling option given")
        if line_handling == "load":
            items_handling = self.opts.get("items_handling", None)
            if not items_handling:
                raise ValueError("NGrams.configure : no items_handling option given")
            self.item_handling_method = self.item_handling_variants.get(items_handling, None)
            if not self.item_handling_method:
                raise ValueError("NGrams.configure : wrong item_handling option given")





    def load(self, filename, encoding='utf-8'):
        line_handling_method = self.line_handling_method
        for n, line in enumerate(self.yield_lines(filename,encoding)):
            line_handling_method(line)

    def yield_lines(self,filename, encoding):
        self.word_set = set()  if self.opts.get("use_word_set",False) else None
        self.forward = dict() if self.opts.get("ngrams_forward", False) else None
        self.backward = dict() if self.opts.get("ngrams_backward", False) else None
        max_lines = self.opts.get("max_lines" , -1)

        with (open(filename, 'r', encoding=encoding) as file):
            for line in file.readlines():
                line = line.strip()
                if line:
                    if max_lines == 0:
                        break
                    max_lines -= 1
                    yield line

    def load_line(self,line):
        split_symbol = self.opts.get("split_symbol", None)
        items = line.split(split_symbol)
        self.check_line_split(items)
        items = [item.strip() for item in items]
        if self.word_set:
            self.word_set.update(items)
        #this must be customized:
        self.item_handling_method(items)

    def inspect_line(self, line):
        split_symbol = self.opts.get("split_symbol", None)
        items = line.split(split_symbol)
        len_items = len(items)
        #print(len(items) , " : " ,  items)
        self.length_histo.setdefault(len_items,0)
        self.length_histo[len_items] +=1






    def handle_weighted_pair(self, items):
        weight = float(items[-1])
        value = items[-2]
        key = " ".join(items[:-2])
        if self.forward is not None:
            key_dict = self.forward.setdefault(key, dict())
            old_weight = key_dict.setdefault(value, 0)
            key_dict[value] = old_weight + weight
        if self.backward is not None:
            key_dict = self.back.setdefault(value, dict())
            old_weight = key_dict.setdefault(key, 0)
            key_dict[key] = old_weight + weight

    def hangle_10_items(self, items):
        print(len(items) , items)
        #id,verb,subject,genitive,dative,accusative,instrumentative, prepositive,no_case,sentence = items
        #print(subject, verb, genitive,dative,accusative,instrumentative, prepositive,no_case)


    def yield_distances(self,d,thrashhold_absolute):
        distance_method = self.opts.get("distance_method", None)
        if  distance_method == "1w":
            dist_fn = self.__set_dict_weighted_distance__
        elif distance_method == "1":
            dist_fn = self.__set_dict_len_and_distance__
        else:
            raise ValueError("TextUtils.yield_distances: distance_method option is not set")

        keys = list(d.keys())
        len_keys = len(keys)
        for i in range(0,len_keys-1):
            key = keys[i]
            value = d[key]
            output_vector = []
            for j in range(i+1,len_keys):
                next_key = keys[j]
                next_value = d[next_key]
                distance = dist_fn(value,next_value)
                if distance > 0:
                    output_vector.append((next_key,distance))
            output_vector = sorted(output_vector, key = lambda pair : -pair[1] )
            output_vector = output_vector[:thrashhold_absolute]
            yield key, output_vector


    def __dict_len_and_distance__(self, d, next_d):
        return len(d.keys() & next_d.keys())

    def __set_dict_weighted_distance__(self,d,next_d):
        common_keys = d.keys() & next_d.keys()
        s = sum( min(d[key] , next_d[key] ) for key in common_keys)
        return s


    def print_err_msg(self,err_msg):
        if self.opts.get("continue_after_error", False):
            print(err_msg, file=sys.stderr)
        else:
            assert False, err_msg

    def check_line_split(self,spl):
        len_spl = len(spl)
        split_len_expected = self.opts.get("split_len_expected", None)
        if split_len_expected is not None and len_spl != split_len_expected:
            err_msg = f"load_ngrams_lines:expected exact length:{spl}, wrong split:{spl}"
            self.print_err_msg(err_msg)

        split_len_max = self.opts.get("split_len_max", None)
        if split_len_max is not None and len_spl > split_len_max:
            err_msg = f"load_ngrams_lines:expected max length:{spl}, wrong split:{spl}"
            self.print_err_msg(err_msg)

    def reverce_ngrams(self, ngrams):
        ngrams_reverced = dict()
        for key, key_dict in ngrams.items():
            key_dict_len = len(key_dict)
            for word,word_weight in key_dict.items():
                reverced_key_dict = ngrams_reverced.setdefault(word, dict())
                old_weight = reverced_key_dict.get(key, 0)
                reverced_key_dict[key] = old_weight + word_weight
        return ngrams_reverced

    def save(self,out_file,items , printout = False):
        if isinstance(items, dict):
            items = items.items()

        with open(out_file, 'w', encoding='utf-8') as file:
            for key, value in items:
                #formatted_key = str(key)
                #formatted_value = ",".join(f"{pair[0]}:{pair[1]*10000:.6f}" for pair in value)
                formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in value)
                line = f"{key}:{formatted_value}\n"
                file.writelines (line)
                if printout:
                    print(line)



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



def sort_value_vector_thrashold( d, thrashhold):
    """
    Sorts dictionary-value by inner item-value descending
    and stores it as
    :param d: dict of key: dict
    :param thrashhold:
    :return: None, changes d
    """
    for key, vector in d.items():
        vector = sorted(vector.items(), key = lambda pair: -pair[1] )
        d[key] = {key: value for key, value in vector[:thrashhold]}


def finalize_relation(ngrams_connected, reverced_ngrams_connected):
    finalize_dict = dict()
    for (subj,verb), object_dict in ngrams_connected.items():
        for obj, object_weight in object_dict.items():
            subj_dict = reverced_ngrams_connected[(obj,verb)]
            subj_weight = subj_dict[subj]
            finalize_obj_dict =finalize_dict.setdefault((subj,verb),dict())
            finalize_obj_dict[obj] = object_weight * subj_weight
    return finalize_dict






class yNgramsDict:

    def __init__(self):
        self.ngrams = dict()

    def store(self):
        ngrams = self.ngrams
        key, row = None, None
        for new_key, item,weight in self.source:
            if new_key is not None:
                key = new_key
                row = self.ngrams.setdefault(key, dict())
            if item is not None:
                old_weight = row.setdefault(item, 0)
                row[item] = old_weight + weight
                backward_row = self.ngrams.setdefault(item, dict())
                old_backwards_weight = backward_row.setdefault(key, 0)
                backward_row[key] = old_backwards_weight + weight


    def cut(self , trashhold):
        ngrams = self.ngrams
        for key, vector in ngrams.items():
            vector = sorted(vector.items(), key=lambda kw: -kw[1])
            vector = vector[:trashhold]
            vector = {key: value for key, value in vector}
            ngrams[key] = vector


def to_sorted_lists( ngrams, trashhold= None):
    ngrams_obj = yNgramsList()
    ngrams_list = ngrams_obj.ngrams
    for key, vector in ngrams.items():
        vector = sorted(vector.items(), key = lambda kw: -kw[1] )
        if trashhold:
            ngrams_list[key] = vector[:trashhold]
        else:
            ngrams_list[key] =vector


    return ngrams_obj



class yNgramsList:

    def __init__(self):
        self.ngrams = dict()

    def start_store(self):
        self.backward_dict = dict()


    def new_row(self, key):
        self.last_key = key
        self.last_row = self.ngrams.setdefault(key, list())

    def store_item(self,item,weight):
        ngrams = self.ngrams
        key = self.last_key
        self.last_row.append((item,weight))
        if item not in ngrams:
            backward_vector_store = self.backward_dict.setdefault(item, dict())
            assert key not in backward_vector_store
            backward_vector_store[key] = weight

    def finalize(self):
        backward_dict = self.backward_dict
        ngrams = self.ngrams
        for backward_key, backward_vector_store in backward_dict.items():
            sorted_vector = sorted(backward_vector_store.items(), key=lambda item_weight_pair: -item_weight_pair[1])
            assert backward_key not in ngrams, f" backward_key {backward_key} is already in dictionary"
            ngrams[backward_key] = sorted_vector

    def get_nearest(self,key,range):
        return ", ".join(kw[0] for kw in  self.ngrams[key][:range])