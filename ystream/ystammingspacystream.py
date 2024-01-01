from ystream.yabstract import yStream

class yStammingSpacyStream(yStream):

    en = "en_core_web_sm"
    ru = 'ru_core_news_sm'

    def __init__(self,lang_name = ru, spacy_lib = None, is_list = True):
        self.init(lang_name,spacy_lib,is_list)

    def init(self, lang_name = ru, spacy_lib= None, is_list = True):
        if spacy_lib is None:
            import spacy
            spacy_lib = spacy
        self.spacy_lib = spacy_lib
        self.lang_name = lang_name
        self.is_list = is_list
        self.spacy_lib.prefer_gpu()
        self.nlp = self.spacy_lib.load(self.lang_name)
        self.nlp.max_length = 1500000


    def __iter__(self):
        if self.is_list:
            for items in self.source:
                lemmas = []
                for item in items:
                    doc = self.nlp(item)
                    words = []
                    for sentence in doc.sents:
                        for token in sentence:
                            words.append(token.lemma_)
                    lemmas.append ( " ".join(word for word in words))
                yield lemmas


