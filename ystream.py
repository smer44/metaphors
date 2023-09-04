import os
from yngrams import to_sorted_lists

class yStream:

    def __call__(self,other):
        if isinstance(other,str):
            other = [other]
        self.source = other
        return self

    def __gt__(self, other):
        other.source = self
        return other

    def __iter__(self):
        return self.iter_items

    def __next__(self):
        return next(self.iter_items)
def toystream(*items):
    obj = yStream()
    obj.iter_items = iter(items)
    return obj

class yOutputFileLinesStream(yStream):

    def __init__(self, encoding,append=False, printout=False):
        self.opts( encoding, append , printout)

    def opts(self, encoding, append=False, printout=False):
        self.encoding = encoding
        self.printout = printout
        self.mode  = 'a' if append else 'w'

    def save(self):
        self.before()
        for line in self.source:
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
        self.filename = next(other)


class yFileNamesStream(yStream):

    def __init__(self,rootdir):
        self.init(rootdir)

    def init(self,rootdir):
        self.rootdir = rootdir

    def __iter__(self):
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                yield filepath




class yInputFileLinesStream(yStream):

    def __init__(self, encoding, max_lines = -1):
        self.opts(  encoding, max_lines)

    def opts(self,  encoding, max_lines = -1):
        self.encoding = encoding
        self.max_lines = max_lines

    def __iter__(self):
        for token in self.source:
            with (open(token, 'r', encoding=self.encoding) as file):
                print("yFileLinesLoader : loading file" , token)
                max_lines = self.max_lines
                for line in file.readlines():
                    line = line.strip()
                    if line:
                        if max_lines == 0:
                            break
                        max_lines -=1
                        yield line




class yFilterLastLineItemStream(yStream):

    def __init__(self,  split_symbol):
        self.opts(split_symbol)

    def opts(self, split_symbol):
        self.split_symbol = split_symbol

    def __iter(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            yield items[-1]

class yUniqueStream(yStream):

    def __init__(self):
        self.last_hash = 0

    def __iter__(self):
        for item in self.source:
            this_hash = hash(item)
            if this_hash != self.last_hash:
                self.last_hash = this_hash
                yield item

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




class yNGramsRawLoad(yStream):

    def __init__(self,  split_symbol, backwards):
        self.init(split_symbol, backwards)

    def init(self, split_symbol, backwards):
        self.split_symbol = split_symbol
        self.backwards = backwards

    def store2(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            subject, verb, *objects = items
            key = subject
            yield key, None,None
            for object in objects:
                item = verb,object
                yield None, item, 1

    def __iter__(self):
        backwards = self.backwards
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            if len(items) != 3 :
                continue

            if backwards:
                 item, key, weight = items
            else:
                key, item,  weight = items


            weight = int(weight)
            yield key, item,  weight




class yDistancesLinesStream(yStream):

    def __init__(self,dictionary,trashhold):
        self.init(dictionary,trashhold)

    def init(self,dictionary,trashhold):
        self.dictionary = dictionary
        self.trashhold = trashhold

    def __iter__(self):
        d = self.dictionary
        trashhold = self.trashhold
        keys = list(d.keys())
        len_keys = len(keys)
        for i in range(len_keys-1):
            key = keys[i]
            value = d[key]
            output_vector = []
            for j in range(i+1,len_keys):
                next_key = keys[j]
                next_value = d[next_key]
                common_keys = value.keys() & next_value.keys()
                #distance = sum(min(value[x], next_value[x]) for x in common_keys)
                distance = len(common_keys)
                if distance > 0:
                    output_vector.append((next_key, distance))
            output_vector = sorted(output_vector, key=lambda pair: -pair[1])
            output_vector = output_vector[:trashhold]
            line = self.format_output(key, output_vector)
            if line:
                yield line

    def format_output(self, key, value_pairs):
        if value_pairs:
            formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in value_pairs)
            line = f"{key}:{formatted_value}\n"
            return line








class yClausesSpacy(yStream):

    def __init__(self,source,spacy_lib,lang_name):
        self.init(source,spacy_lib,lang_name)

    def init(self, source,spacy_lib, lang_name):
        self.source = source
        self.spacy_lib = spacy_lib
        self.lang_name = lang_name
        self.spacy_lib.prefer_gpu()
        self.nlp = self.spacy_lib.load(self.lang_name)

    def action(self, text):
        doc = self.nlp(text)
        for n, sentence in enumerate(doc.sents):
            for token in sentence:
                if token.dep_ == "ROOT":
                    yield from self.yield_clauses(token)
    def yield_clauses(self, root_token):
        stack = [(root_token,0)]
        while stack:
            token,depth = stack.pop()
            children = list(token.children)
            #remove unclassifyed dependencies:
            skip = False
            objects = []
            verb = None
            subject = None
            if  token.pos_ == "VERB":
                verb =  token.lemma_
            for child in children:
                if (child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and child.dep_ == "nsubj":
                    subject =child.lemma_
                if ((child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and (child.dep_ == "obj" or child.dep_ == "obl")) or  \
                    (child.pos_ == "VERB" and child.dep_ == "xcomp" ):
                    objects.append(child.lemma_)

            if subject and verb and objects:
                yield "|".join( (subject , verb, *objects))
            children.reverse()
            depth+=1
            for child in children:
                stack.append((child,depth ))



