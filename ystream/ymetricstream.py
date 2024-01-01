from ystream.yabstract import yStream
from ystream import sort_clip_dict, format_output

def common_sum_metric (vector_dict,next_vector_dict):
    common_keys = vector_dict . keys() & next_vector_dict.keys()
    return sum (vector_dict[key] +next_vector_dict[key] for key in common_keys  )

def common_min_metric (vector_dict,next_vector_dict):
    common_keys = vector_dict . keys() & next_vector_dict.keys()
    return sum  (min(vector_dict[key] ,next_vector_dict[key]) for key in common_keys  )


class yItemsSimpleFillWeight(yStream):

    def __init__(self,
                 metric = common_sum_metric,
                 metric_factor = 1 ,
                 trashhold = 30):
        self.metric = metric
        self.trashhold = trashhold
        self.metric_factor = metric_factor


    def __iter__(self):
        metric = self.metric
        trashhold = self.trashhold
        metric_factor = self.metric_factor

        for ngrams in self.source:
            yield from calc_inner_distances(ngrams, metric, metric_factor, trashhold)



def calc_inner_distances(ngrams, metric, metric_factor, trashhold):
                empty_dict = dict()
                keys = list(ngrams.keys())
                for key in keys:
                    vector = ngrams[key]
                    row_distances_dict = dict()
                    for next_key in keys:
                        if next_key != key:
                            next_vector = ngrams[next_key]
                            dist = metric_factor * metric(vector, next_vector)
                            if dist > 0:
                                row_distances_dict[next_key] = dist
                    sorted_row = sort_clip_dict(row_distances_dict, trashhold)
                    line = format_output(key, sorted_row)
                    yield line

