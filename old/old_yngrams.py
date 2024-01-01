"""    from random import sample,choice


    def random(self,key = None, amounts = (4,2,)):
        if key == None:
            key = self.choice(self.bag)
        yield key
        if not amounts:
            return
        yield "("
        amount = amounts[0]
        row = self.ngrams.get(key, dict()).items()
        weightedvalues=  self.sample(row, min(amount, len(row)))
        if amount == 1:
            yield weightedvalues[0][0]
        else :
            child_amount = amounts[1:]
            for value,weight in weightedvalues:
                #print("value" , value)
                yield from self.random(value, child_amount)

        yield ")"
"""


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
