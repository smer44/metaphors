from ystream.yabstract import yStream

encoding_std = "utf-8"
encoding_utf_8_sig ="utf-8-sig"
encoding_ru =  'cp1251'
encoding_ru_koi8r = "koi8-r"

class yInputFileVector(yStream):

    def __init__(self, encoding=encoding_std):
        self.init(encoding)

    def init(self,  encoding=encoding_std):
        self.encoding = encoding


    def __iter__(self):
        for file_name in self.source:
            with (open(file_name, 'r', encoding=self.encoding) as file):

                first_line = file.readline().strip()
                dictionary_size, vector_size = first_line.split()
                dictionary_size, vector_size = int(dictionary_size), int(vector_size)
                print("yInputFileVector : loading vector file : ", file_name , "dictionary size :" , dictionary_size, "vector size :" , vector_size)
                for n in range(dictionary_size):
                    line = file.readline().strip()
                    if line:
                        name, *vector = line.split()
                        assert len(vector) == vector_size, f" wrong vector size for word {name}"
                        vector = [float(x) for x in vector]
                        yield name, vector
