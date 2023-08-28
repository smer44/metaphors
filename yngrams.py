import pprint as pp
import sys



class yNgrams:

    def __init__(self, opts):
        self.opts = dict()
        self.configure(opts)

    def configure(self, opts):
        for key, value in opts.items():
            self.opts[key.strip()] = value

    def load(self, filename, encoding='utf-8'):
        line_handling = self.opts.get("line_handling",None)
        if line_handling == "load":
            line_handling = self.load_line
        elif line_handling == "inspect":
            line_handling = self.inspect_line
            self.length_histo = dict()
        else :
            raise ValueError("NGrams.load_file_lines : wrong line_handling option")

            line_handling = self.load_line

        for n, line in enumerate(self.yield_lines(filename,encoding)):

            line_handling(line)

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
        self.load_line_items(items)

    def inspect_line(self, line):
        split_symbol = self.opts.get("split_symbol", None)
        items = line.split(split_symbol)
        len_items = len(items)
        #print(len(items) , " : " ,  items)
        self.length_histo.setdefault(len_items,0)
        self.length_histo[len_items] +=1






    def load_line_items(self, items):
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

    def load_10_items(self, items):
        id,verb,subject,genitive,dative,accusative,instrumentative, prepositive,no_case,sentence = items


    def sort_value_vector_thrashold(self, d, thrashhold_absolute):
        for key, vector in d.items():
            vector = sorted(vector.items(), key = lambda pair: -pair[1] )
            d[key] = {key: value for key, value in vector[:thrashhold_absolute]}

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








