class yNGramsLinesLoad:

    def __init__(self, split_key_value, split_list):
        self.conf(split_key_value,split_list)

    def conf(self, split_key_value, split_list):
        self.split_key_value = split_key_value
        self.split_list =split_list


    def __iter__(self):

        for line in self.source:
            line = line.strip()
            if line:
                key, vector = line.split(self.split_key_value, maxsplit = 1)
                key, vector = key.strip(), vector.strip()

                yield key, None, None
                for item_pair in vector.split(self.split_list):
                    item_pair = item_pair.strip()
                    item , weight = item_pair.split(self.split_key_value)
                    item, weight = item.strip(), weight.strip()
                    weight = int(weight)
                    yield None, item, weight