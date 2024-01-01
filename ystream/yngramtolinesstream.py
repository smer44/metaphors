from yabstract import yStream

class yNgramToLinesStream(yStream):


    def __iter__(self):
        for key, vector in self.source:
            if vector:
                formatted_vecor = ",".join(f"{item}" for item in vector)
                line = f"{key}:{formatted_vecor}\n"
                yield line
