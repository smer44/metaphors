from ystream.yabstract import yStream

class yDistancesLinesStream(yStream):

    def __init__(self,
                 input_length_trashhold = None,
                 output_length_trashhold = None,
                 min_dist_trashhold = 3,
                 tostr = False,
                 is_weighted = False,
                 min_distance_clip = 3):
        self.init(input_length_trashhold,output_length_trashhold,min_dist_trashhold,tostr,is_weighted,min_distance_clip)

    def init(self,
             input_length_trashhold= None,
             output_length_trashhold = None,
             min_dist_trashhold = 3,
             tostr = False,
             is_weighted = False,
             min_distance_clip = 3):
        self.input_length_trashhold = input_length_trashhold
        self.output_length_trashhold = output_length_trashhold
        self.min_dist_trashhold = min_dist_trashhold
        self.tostr = tostr
        self.is_weighted = is_weighted
        self.min_distance_clip = min_distance_clip

    def __iter__(self):
        for d in self.source:

            input_length_trashhold = self.input_length_trashhold
            output_length_trashhold = self.output_length_trashhold
            min_dist_trashhold = self.min_dist_trashhold
            tostr = self.tostr
            is_weighted = self.is_weighted
            min_distance_clip = self.min_distance_clip
            metric = self.weight_metric if is_weighted else self.no_weight_metric

            keys = list(d.keys())
            len_keys = len(keys)
            #for i in range(len_keys-1):
            for i in range(len_keys):
                key = keys[i]
                value = d[key]
                if input_length_trashhold:
                    vector = sort_clip_dict(value,input_length_trashhold)
                    value = dict(vector)

                output_vector = []
                #for j in range(i+1,len_keys):
                for j in range(len_keys):
                    if i == j : continue
                    next_key = keys[j]
                    next_value = d[next_key]
                    #common_keys = value.keys() & next_value.keys()
                    #distance = sum(min(value[x], next_value[x]) for x in common_keys)
                    #distance = len(common_keys)
                    distance = metric(value, next_value)
                    if distance > min_distance_clip:
                        output_vector.append((next_key, distance))
                output_vector = sorted(output_vector, key=lambda pair: -pair[1])
                if output_length_trashhold:
                    output_vector = output_vector[:output_length_trashhold]

                if output_vector:
                    if tostr:
                        line = format_output(key, output_vector)
                        #print(line)
                        yield line
                    else:
                        yield key, output_vector

    def no_weight_metric(self, value, next_value):
        common_keys = value.keys() & next_value.keys()
        distance = len(common_keys)
        return distance

    def weight_metric(self, value, next_value):
        common_keys = value.keys() & next_value.keys()
        distance = sum (value[key] + next_value[key]  for key in common_keys)
        return distance












