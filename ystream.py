import os


class yAbstractStream:

    def __iter__(self):
        for token in self.source:
            yield self.action(token)


    def action(self,token):
        return token

class yAbstractFilterStream:

    def __iter__(self):
        for token in self.source:
            result = self.action(token)
            if result is not None:
                yield result


    def action(self,token):
        return token

class yAbstractGenStream:

    def __iter__(self):
        for token in self.source:
            yield from self.action(token)

    def action(self,token):
        yield token


class yAbstractStreamSaver:

    def before(self):
        pass

    def after(self):
        pass

    def save(self):
        self.before()
        for token in self.source:
            self.action(token)
        self.after()

    def action(self,token):
        print("saved:" , token)

class yFileLinesSaver(yAbstractStreamSaver):

    def __init__(self,source,filename , encoding,append=False, printout=False):
        self.opts(source, filename , encoding, append , printout)

    def opts(self, source, filename , encoding, append=False, printout=False):
        self.source = source
        self.filename = filename
        self.encoding = encoding
        self.printout = printout
        self.mode  = 'a' if append else 'w'

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


class yFileNamesStream:

    def __init__(self,rootdir):
        self.init(rootdir)

    def init(self,rootdir):
        self.rootdir = rootdir

    def __iter__(self):
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                yield filepath




class yFileLinesStream(yAbstractGenStream):

    def __init__(self, encoding, max_lines = -1):
        self.opts(  encoding, max_lines)

    def opts(self,  encoding, max_lines = -1):
        self.encoding = encoding
        self.max_lines = max_lines

    def action(self, token):
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

    def src(self,other):
        if isinstance(other,str):
            other = [other]
        self.source = other

    def __gt__(self, other):
        other.source = self


class yLastItemStream(yAbstractStream):

    def __init__(self, source, split_symbol):
        self.opts(source, split_symbol)

    def opts(self, source, split_symbol):
        self.source = source
        self.split_symbol = split_symbol

    def action(self,line):
        items = line.split(self.split_symbol)
        return items[-1]

class yUniqueStream(yAbstractFilterStream):

    def __init__(self,source):
        self.source = source
        self.last_hash = 0

    def action(self,item):
        this_hash = hash(item)
        if this_hash != self.last_hash:
            self.last_hash = this_hash
            return item

class yNGramsLinesLoad():

    def __init__(self, split_key_value, split_list):
        self.conf(split_key_value,split_list)
        self.ngrams = dict()

    def conf(self, split_key_value, split_list):
        self.split_key_value = split_key_value
        self.split_list =split_list


    def store(self):
        for line in self.source:
            line = line.strip()
            ngrams = self.ngrams
            backward_dict = dict()
            if line:
                #vector = line.split(self.split_key_value, maxsplit = 2)
                #print(vector)
                key, vector = line.split(self.split_key_value, maxsplit = 1)
                key, vector = key.strip(), vector.strip()
                assert key not in ngrams , f" key {key} is already in dictionary :\n - line {line}\n vector : {vector}"
                vector_store = ngrams.setdefault(key, list())
                for item_pair in vector.split(self.split_list):
                    item_pair = item_pair.strip()
                    item , weight = item_pair.split(self.split_key_value)
                    item, weight = item.strip(), weight.strip()
                    weight = int(weight)
                    vector_store.append((item,weight))
                    if item not in ngrams:
                        backward_vector_store = backward_dict.setdefault(item, dict())
                        assert key not in backward_vector_store
                        backward_vector_store[key] = weight

        for backward_key,  backward_vector_store in backward_dict.items():
            sorted_vector = sorted( backward_vector_store.items() , key = lambda item_weight_pair : -item_weight_pair[1] )
            assert backward_key not in  ngrams , f" backward_key {backward_key} is already in dictionary"
            ngrams[backward_key] = sorted_vector


    def __gt__(self, other):
        other.source = self

    def get_nearest(self, key):
        return self.ngrams[key][0]






class yNGramsStorage():

    def __init__(self, source, split_symbol):
        self.init(source, split_symbol)

    def init(self, source, split_symbol):
        self.source = source
        self.split_symbol = split_symbol
        self.ngrams= dict()

    def store2(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            #subject, verb, *objects = items
            subject, verb, *objects = items
            #objects = [verb]
            vector_dict = self.ngrams.setdefault(subject, dict())
            for object in objects:
                key_inside_vector = verb, object
                old_count = vector_dict.setdefault(key_inside_vector, 0)
                vector_dict[key_inside_vector] = old_count + 1

    def store(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            if len(items) != 3 :
                continue
            subject, verb, weight = items
            weight = int(weight)
            vector_dict = self.ngrams.setdefault(subject, dict())

            key_inside_vector = verb
            old_count = vector_dict.setdefault(key_inside_vector, 0)
            vector_dict[key_inside_vector] = old_count + weight





    def clear_ngrams(self):
        thrashhold_absolute = 30
        d = self.ngrams
        for key, vector in d.items():
            vector = sorted(vector.items(), key=lambda pair: -pair[1])
            d[key] = {key: value for key, value in vector[:thrashhold_absolute]}



    def yield_first_method(self):
        d = self.ngrams
        thrashhold_absolute = 20
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
                distance = sum(min(value[x], next_value[x]) for x in common_keys)
                if distance > 0:
                    output_vector.append((next_key, distance))
            output_vector = sorted(output_vector, key=lambda pair: -pair[1])
            output_vector = output_vector[:thrashhold_absolute]
            line = self.format_output(key, output_vector)
            if line:
                yield line

    def format_output(self, key, value_pairs):
        if value_pairs:
            formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in value_pairs)
            line = f"{key}:{formatted_value}\n"
            return line








class yClausesSpacy(yAbstractGenStream):

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























