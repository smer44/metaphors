from ystream.yabstract import yStream


def format_vector(key, vector):
    formatted_value = "|".join(f"{pair[0]}:{pair[1]}" for pair in vector)
    line = f"{key}~{formatted_value}\n"
    return line

class ySortedCutVectorsFromStorage(yStream):

    def __init__(self, thrashhold = 30, format_output = True):
        self.init(thrashhold, format_output)

    def init(self, thrashhold = 30, output_lines = True ):
        self.thrashhold = 30
        self.output_lines = True

    def __iter__(self):
        """
        Sorts dictionary-value by inner item-value descending
        and stores it as
        :param d: dict of key:  each value of this dict is a dict with item - weight items
        :param thrashhold:
        :return: None, changes d
        """
        thrashhold = self.thrashhold
        output_lines = self.output_lines

        if thrashhold:
            for d in self.source:
                for key, vector in d.items():
                    vector = sorted(vector.items(), key = lambda pair: -pair[1] )
                    vector = vector[:thrashhold]
                    if output_lines :
                        line = format_vector(key, vector)
                        yield line
                    else:
                        yield key, vector
        else:
            for d in self.source:
                for key, vector in d.items():
                    vector = sorted(vector.items(), key = lambda pair: -pair[1] )
                    #vector = vector[:thrashhold]
                    if output_lines :
                        line = format_vector(key, vector)
                        yield line
                    else:
                        yield key, vector



                #d[key] = {key: value for key, value in vector[:thrashhold]}
