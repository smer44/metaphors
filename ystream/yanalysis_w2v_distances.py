from ystream.yabstract import yStream
from ystream.yhelperfunc import format_output
import numpy as np

class yDistancesW2V(yStream):

    def __init__(self):
        self.thrashhold = 30



    def __iter__(self):

        for storage in self.source:
            matrix = np.array(storage.matrix)
            words = storage.words
            mlen = len(matrix)
            thrashhold = self.thrashhold

            for x in range(0,mlen):
                row1 = matrix[x]
                word1 = words[x]
                vector = []
                dejavu = set()
                for y in range(0,mlen):
                    if x == y : continue
                    row2 = matrix[y]
                    word2 = words[y]
                    if word2 in dejavu : continue
                    dejavu.add(word2)
                    diff = row1-row2
                    dist = np.sum(np.abs(diff))
                    vector.append((word2, dist))
                vector = sorted(vector, key=lambda key: key[1])
                vector = vector[:thrashhold]
                line = format_output(word1,vector)
                yield line








