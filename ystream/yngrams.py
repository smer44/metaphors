from ystream.yabstract import yStream
from ystream.yhelperfunc import sort_clip_dict



#TODO - write yStorageTriplet load test -
# TODO also this has replaced some class, so check a source where  it was

class yStorageTriplet(yStream):

    iter_method_all = "all"
    iter_method_kv = "kv"

    def __init__(self,iter_method = "all",store_before_iter = False):
        self.vso_ngrams = dict()
        self.svo_ngrams = dict()
        self.ovs_ngrams = dict()
        self.subjects_bag = dict()
        self.verbs_bag  = dict()
        self.objects_bag = dict()
        self.init(iter_method,store_before_iter)

    def init(self,iter_method = "all",store_before_iter = False):
        self.iter_method = iter_method
        self.store_before_iter = store_before_iter

    def __put_triplet__(self,ngrams, first,second,third,weight):
        row = ngrams.setdefault(first, dict())
        old_weight = row.setdefault((second,third), 0)
        row[(second,third)] = old_weight + weight

    def __put_bag__(self,bag,item,weight):
        old_weight = bag.setdefault(item, 0)
        bag[item] = old_weight + weight

    def __put_all__(self,  first,second,third,weight):
        self.__put_triplet__(self.vso_ngrams ,first,second,third,weight )
        self.__put_triplet__(self.svo_ngrams,  second,first, third, weight)
        self.__put_triplet__(self.ovs_ngrams, third, first, second, weight)
        self.__put_bag__(self.subjects_bag,first, weight)
        self.__put_bag__(self.subjects_bag, second, weight)
        self.__put_bag__(self.objects_bag, third, weight)


    def contains(self, subject,verb,object, order ="vso"):
        if order == "vso":
            known = self.vso_ngrams.get(verb,None)
            if known:
                known = known.get((subject,object), None)
            return known
        if order == "svo":
            known = self.svo_ngrams.get(subject, dict())
            if known:
                known = known.get((verb, object), None)
            return known

    def store(self):
        multi = self.multi_ngrams
        verb_subjects = self.verb_subjects
        for verb, subject ,object ,weight in self.source:
            self.__put_all__(verb,subject,object,weight)




    def __iter__(self):
        if self.store_before_iter:
            self.store()

        if self.iter_method == "dict":
            yield self
        elif self.iter_method == "svo":
            for subject, row in self.svo_ngrams.items():
                for (verb,object), weight in row.items():
                    yield subject, verb,object, weight

        elif self.iter_method == "vso":
            for verb, row in self.vso_ngrams.items():
                for (subject,object), weight in row.items():
                    yield subject, verb,object, weight


class yStorageWithBag(yStream):

    def __init__(self,
                 iter_method = "kv",
                 store_before_iter = False,
                 filter_before_iter = False,
                 add_backwards = False,
                 exclude = None,
                 clip_rows_amount = False,
                ):
        self.ngrams = dict()
        self.bag_keys = dict()
        self.bag_values = dict()
        self.iter_method = iter_method
        self.store_before_iter = store_before_iter
        self.filter_before_iter = filter_before_iter
        self.add_backwards = add_backwards
        self.exclude = exclude
        self.clip_rows_amount = clip_rows_amount

    def store(self):
        if self.store_before_iter:
            raise RuntimeError("yStorageSimple.store: store called while it should hapen automatically: store_before_iter is set to True")

        self.__store__()

    def __store__(self):
        d = self.ngrams
        exclude = self.exclude
        if self.add_backwards:
            for key,  value, weight in self.source:
                if exclude:
                    if key  in exclude or value  in exclude:
                        continue
                self.store_item_simple(d,key,value,weight)
                self.store_item_simple(d, value, key, weight)
                self.add_to_bag(self.bag_keys,key,weight)
                self.add_to_bag(self.bag_values, value, weight)

        else:
            for key,  value, weight in self.source:
                if exclude:
                    if key in exclude or value in exclude:
                        continue

                self.store_item_simple(d,key,value,weight)
                self.add_to_bag(self.bag_keys,key,weight)
                self.add_to_bag(self.bag_values, value, weight)

    def trim_bag(self,bag,min_items, max_items):
        filtered_bag = [*bag.items()]
        filtered_bag.sort(key = lambda kw: - kw[1])
        filtered_bag = filtered_bag[min_items:max_items]
        return filtered_bag

    def filter_bags(self,max_items):
        filtered_key_bag = self.trim_bag(self.bag_keys,0,max_items)
        filtered_key_bag = set(f[0] for f in filtered_key_bag)

        filtered_values_bag = self.trim_bag(self.bag_values,0,max_items)
        filtered_values_bag = set(f[0] for f in filtered_values_bag)

        #print("filtered_bag : " , filtered_bag)
        keys = list(self.ngrams.keys())
        for key in keys:
            if key not in filtered_key_bag:
                del self.ngrams[key]
                continue
            row = self.ngrams[key]
            inner_keys = list(row.keys())
            for inner_key in inner_keys:
                if inner_key not in filtered_values_bag:
                    del row[inner_key]

    def add_to_bag(self,bag, key, weight):
        bag[key] = bag.get(key,0)+ weight
    def store_item_simple(self,d, key, value,weight):
        row = d.setdefault(key, dict())
        old_weight = row.setdefault(value, 0)
        row[value] = old_weight + weight


    def clip_rows(self, trashhold):
        ngrams = self.ngrams
        keys = list(ngrams.keys())
        for key in keys:
            row = ngrams[key]
            sorted_row = sort_clip_dict(row,trashhold)
            sorted_row_to_dict = {key: value for key, value in sorted_row}
            ngrams[key] = sorted_row_to_dict

    def items(self):
        if self.store_before_iter:
            self.store()

        for key, items in self.ngrams.items():
            yield key, items


    def analogs(self, key):
        return self.ngrams.get(key, set())


    def analogs_with_verb(self, key, verb):
        pass



    def __iter__(self):
        if self.store_before_iter:
            self.__store__()

        if self.clip_rows_amount:
            self.clip_rows(self.clip_rows_amount)

        if  self.filter_before_iter is not None and self.filter_before_iter is not False:
            self.filter_bags(self.filter_before_iter)
            #print("freq bag_values :",sorted(self.bag_values.items(), key = lambda kw: -kw[1]))
        if self.iter_method == "kv":
            for key, items in self.ngrams.items():
                yield key, items
        elif self.iter_method == "bag":
            for item in self.bag:
                yield item

        elif self.iter_method == "dict":
            yield self.ngrams
        elif self.iter_method == "self":
            yield self
        else:
            raise ValueError(f"yStorageSimple.__iter__: wrong iter_method set : {self.iter_method}")


    def printall(self):
        for key, value in self.ngrams.items():
            print(key,value)






class yNgramsTagDict(yStream):

    def __init__(self):
        self.tag_dicts = dict()
        self.tag_pairs = dict()

    def store_tags(self):
        tag_dicts = self.tag_dicts
        for key, key_tags,value,value_tags in self.source:
            key_tag_str = " ".join(key_tags)
            value_tag_str = " ".join(value_tags)
            self.tag_pairs.setdefault(key_tag_str,set()).add(key)
            #self.tag_pairs.add(key_tag_str + " " + value_tag_str)
            self.store_item(key, key_tag_str,value,value_tag_str)
            #self.store_item( value, value_tag_str,key, key_tag_str,)




    def store_item(self,key, key_tag_str,value,value_tag_str):
        tag_dicts = self.tag_dicts
        key_dict = tag_dicts.setdefault(key_tag_str, dict())
        value_tag_dict = key_dict.setdefault(key, dict())
        value_row = value_tag_dict.setdefault(value_tag_str, dict())
        old_weight = value_row.setdefault(value, 0)
        value_row[value] = old_weight + 1
        #store value_tag -> value -> empty just in case:
        key_dict = tag_dicts.setdefault(value_tag_str, dict())
        value_tag_dict = key_dict.setdefault(value, dict())



    def __iter__(self):
        for key_tag_str,key_dict in self.tag_dicts.items():
            for key, value_tag_dict in key_dict.items():
                for value_tag_str, value_row in value_tag_dict.items():
                    for value, weight in value_row.items():
                        yield key, key_tag_str,value,value_tag_str

    from random import sample,choice
    #TODO - check this random method
    def random(self,key_tag = 'VERB ROOT',key = None, amounts = (4,2)):
        key_dict = self.tag_dicts[key_tag]
        if key == None:
            all_keys = list(key_dict.keys())
            #print("all_keys : " , all_keys )
            key = self.choice(all_keys)
            #print("key : " , key )
        yield f"{key}:{key_tag}"#key #
        if not amounts :
            return
        yield "("
        amount = amounts[0]
        value_tag_dict_kw = key_dict[key].items()
        choised_value_tags = self.sample(value_tag_dict_kw, min( len(value_tag_dict_kw),amount))
        child_amount = amounts[1:]
        for value_tag, value_row in choised_value_tags:
            #value_tag, value_row = self.choice(value_tag_dict.items(), 1)
            value,weight = self.choice(list(value_row.items()))
            #print("enter value, weight: " , value_tag, value, weight)
            yield from self.random(value_tag, value, child_amount)
        yield ")"



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


class yStorageBackwardsSimple(yStream):

    def __init__(self, iter_method = "kv",store_before_iter = False):
        self.ngrams = dict()
        self.ngrams_backwards = dict()
        self.bag = set()
        self.iter_method = iter_method
        self.store_before_iter = store_before_iter

    def store(self):
        d = self.ngrams
        back_d = self.ngrams_backwards
        for key, item,relation, weight in self.source:
            value = (item,relation)
            self.store_item_simple(d,key,value,weight)
            value = (key,relation)
            self.store_item_simple(back_d, item, value, weight)
            self.bag.add(key)
            self.bag.add(value)

    def store_item_simple(self,d, key, value,weight):
        row = d.setdefault(key, dict())
        old_weight = row.setdefault(value, 0)
        row[value] = old_weight + weight

    def __iter__(self):
        if self.store_before_iter:
            self.store()
        if self.iter_method == "kv":
            for key, items in self.ngrams.items():
                yield key, items
            for key, items in self.ngrams_backwards.items():
                yield key, items
        elif self.iter_method == "bag":
            for item in self.bag:
                yield item
        else:
            yield self