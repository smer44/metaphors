
from yabstract import yStream


class yPseudoTimeMarker(yStream):
    """
    marks given text with pseudo time.

    """

    default_special_words= {"," : 5 , "!" : 10, "." : 10, "?" : 10, "-" : 3}

    def __init__(self, special_units=default_special_words):
        self.init(special_units)
        self.timestamp =0
        self.words = dict()
        self.objects_per_time = []

    def init(self,  special_units=default_special_words):
        self.special_units = special_units

    def store(self):
        special_units = self.special_units
        words = self.words
        objects_per_time =self.objects_per_time

        for word in self.source:
            #if word in special_units:
            #    self.timestamp+=special_units[word]
            #else:
            #    time_vector = words.setdefault(word,[])
            #    time_vector.append(self.timestamp)
            #    self.timestamp+=1
            self.objects_per_time.append(word)
            time_vector = words.setdefault(word, [])
            time_vector.append(self.timestamp)
            self.timestamp +=1




    def __iter__(self):
        for word,vector in self.words.items():
            yield word,vector


    def nearest_words_list(self, word, near = 1):
        assert word in self.words
        time_vector = self.words[word]
        near_words = dict()
        for time_stamp in time_vector:
            for near_time in range (max(0,time_stamp-near), time_stamp):
                near_word = self.objects_per_time[near_time]
                count = near_words.setdefault((near_word, "before"),0)
                near_words[(near_word, "before")] = count+1
                #near_words.append((self.objects_per_time[near_time], "before"))
            for near_time in range(time_stamp + 1 , min(len(self.objects_per_time), time_stamp + near+1)):
                near_word = self.objects_per_time[near_time]
                count = near_words.setdefault((near_word, "after"),0)
                near_words[(near_word, "after")] = count+1

                #near_words.append((self.objects_per_time[near_time], "after"))
        return near_words

    def nearest_all_list_cut(self, trim = 30):
        self.words_nearest_lists = dict()
        for word in self.words.keys():
            near_words_dict = self.nearest_words_list(word)
            near_words_list = sorted(near_words_dict.items(), key= lambda kw: -kw[1])[:trim]
            self.words_nearest_lists[word] = near_words_list




    from random import choice
    def random_nearest(self, range = 1):
        word = self.choice(self.objects_per_time)
        print("choosed word : " , word )
        print( self.nearest_words_list(word,range))




    def nearest_words_vector_distance(self):
        self.nearest = dict()
        keys = list(self.words)
        len_keys = len(keys)
        for i in range(len_keys-1):
            vector = self.words[keys[i]]
            min_dist = 1000000
            min_index = -1
            for j in range(i+1,len_keys):
                next_vector = self.words[keys[j]]
                this_dist = self.vector_min_distance(vector,next_vector)
                if this_dist < min_dist:
                    min_dist = this_dist
                    min_index = j
            self.nearest[keys[i]] = (min_dist, keys[min_index])

    def iter_nearest(self):
        for key, value in self.nearest.items():
            yield key, value





    def vector_min_distance(self,vector,next_vector):
        index = 0
        next_index = 0
        len_vector = len(vector)
        len_next_vector = len(next_vector)
        dist = 1000000
        while index < len_vector and next_index < len_next_vector:
            this_dist = vector[index] - next_vector[next_index]
            if this_dist < 0:
                index+=1
            else:
                next_index+=1
            abs_dist = abs(this_dist)
            if abs_dist < dist:
                dist = abs_dist
        return dist

