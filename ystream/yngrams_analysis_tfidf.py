from ystream.yabstract import yStream
from ystream.yhelperfunc import format_output,sort_dict
import math
class yTFIDFLines(yStream):

    def __init__(self):

        pass


    def __iter__(self):
        for storage in self.source:
            #calculate idf-ns for each word:
            idf_dict = dict()
            for key, row in storage.ngrams.items():
                for value,_ in row.items():
                    old_weight = idf_dict.get(value,0)
                    idf_dict[value] = old_weight+1
            #aply idf formula to all values:
            n = len(storage.ngrams)
            for value in list(idf_dict.keys()):
                idf_dict[value] =math.log( idf_dict[value]/n)

            #tfidf = dict()
            for key, row in storage.ngrams.items():
                result_row = dict()
                #tfidf[key] = result_row
                total_weight = sum(row.values())
                for value,weight in row.items():
                    tf = weight/total_weight
                    tfidf = tf * idf_dict[value]
                    result_row[value] = tfidf
                vector  = sort_dict(result_row)
                line = format_output(key, vector)
                yield (line)



            #for value, weight in idf_dict.items():
            #    yield f"{value} : {weight}"



