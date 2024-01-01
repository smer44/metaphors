from ystream.yabstract import yStream
from striprtf.striprtf import rtf_to_text


encoding_std = "utf-8"
encoding_ru =  'cp1251'



class yInputFileFull(yStream):

    def __init__(self, encoding=encoding_std,to_rtf=False):
        self.init(encoding,to_rtf)

    def init(self,  encoding=encoding_std ,to_rtf=False):
        self.encoding = encoding
        self.to_rtf= to_rtf

    def __iter__(self):
        for file_name in self.source:
            with (open(file_name, 'r', encoding=self.encoding) as file):
                print("yFileLinesLoader : loading file", file_name)
                text = file.read()
                if self.to_rtf:
                    text = rtf_to_text(text)
                yield text















class yOutputFileLinesStream(yStream):

    def __init__(self, encoding = encoding_std,append=False, printout=False):
        self.opts( encoding, append , printout)

    def opts(self, encoding, append=False, printout=False):
        self.encoding = encoding
        self.printout = printout
        self.mode  = 'a' if append else 'w'

    def save(self):
        self.before()
        for line in self.source:
            if line:
                line = line.strip()
                self.action(line)
        self.after()

    def before(self):
        self.file = open(self.filename,self.mode, encoding=self.encoding)
        print("yFileLinesSaver: saving file: " , self.filename, f", mode : {self.mode}")

    def after(self):
        self.file.close()

    def action(self,line):
        self.file.write(line)
        self.file.write('\n')
        if self.printout :
            print(line)

    def __gt__(self, other):
        assert not isinstance(other,str), f"yOutputFileLinesStream: set string as source, what will cause iteration over chars"
        self.filenames = iter(other)
        self.next_out()


    def next_out(self):
        self.filename = next(self.filenames)



class yInputFileLinesStream(yStream):
    """
    Class what represents an input file stream of lines of this file,
    splitted by file.readlines(), stripped with line.strip() and
    empty strings are skipped
    init variables:
    - encoding
    - max_lines - amount of lines, read from the file. put negative value for all lines from a file
    """

    def __init__(self, encoding=encoding_std, max_lines = -1):
        self.init(  encoding, max_lines)

    def init(self,  encoding, max_lines = -1):
        self.encoding = encoding
        self.max_lines = max_lines

    def __iter__(self):
        for token in self.source:
            print("yInputFileLinesStream loading file:", token)
            with (open(token, 'r', encoding=self.encoding) as file):
                #print("yFileLinesLoader : loading file" , token)
                max_lines = self.max_lines
                for line in file.readlines():
                    line = line.strip()
                    if line:
                        if max_lines == 0:
                            break
                        max_lines -=1
                        yield line
