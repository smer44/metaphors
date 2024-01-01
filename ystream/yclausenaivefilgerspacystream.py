from ystream.yabstract import yStream

import operator as op

class ySimpleFilterSpacyStream(yStream):

    def __init__(self):
        pass

    def __iter__(self):
        for token in self.source:
            if token.pos_ == "PROPN":
                yield token.lemma_ #f"{token.lemma_} : {token.pos_}"



class yClauseNaiveFilterSpacyStream(yStream):
    def __init__(self):
        self.get_children_variants = {#"voa" : self.get_svo_attr,
                                      "oa" : self.check_object_attr,
                                      "svoa2": self.get_svo2_attr}
        self.count_objs = []

    def __iter__(self):
        for token in self.source:
            #features = self.check_token_children_features(token)
            #print(token, "::", ", ".join(f"{x}:{x.dep_}:{x.pos_}" for x in token.children), ",features", features)
            #yield from self.get_svo2_attr(token)
            yield from self.try_get_sv(token)

    #TODO - check that token has correct symbols
    def check_object_attr(self,token):
        objects = []
        attrs = []
        for child in token.children:
            if child.dep_ in {"obj","obl","nsubj"}:
                if child.pos_ == "NOUN":
                    object = child.lemma_
                elif child.pos_ == "PRON" or child.pos_ == "PROPN":
                    object = "<obj_ref>"
                else:
                    object = None
                    #print("strange noun", child.pos_)
                if object:
                    objects.append(object)
            if child.dep_ == "amod":
                attrs.append(child.lemma_)
        if token.pos_ == "VERB":
            for object_str in objects:
                    line = f"VO|{token.lemma_}|{object_str}"
                    # assert op.countOf(line, "|") == 2 , f"yClauseNaiveFilterSpacyStream : wrong line: " + line + " token: " + token.lemma_ + ", object: " + object_str
                    if op.countOf(line, "|") == 2:
                        yield line

        for attr_str in attrs:
            line = f"OA|{token.lemma_}|{attr_str}"
            if op.countOf(line, "|") == 2:
                yield line


    def check_token_children_features(self,token):
        features = dict()
        for child in token.children:
            if child.dep_ == "nsubj":
                features.setdefault("subject",[]).append(child)
                child_features = self.check_token_children_features(child)
                features.setdefault("subject", []).extend(child_features.get("additive",[]))
                continue
            if child.dep_ in {"amod","advmod","xcomp"}:#
                features.setdefault("attribute",[]).append(child)
                continue
            if child.dep_ in {"obj","obl","nmod"}:#
                features.setdefault("object",[]).append(child)
                child_features = self.check_token_children_features(child)
                features.setdefault("object", []).extend(child_features.get("additive", []))
                continue
            if child.dep_ in {"conj"}:
                features.setdefault("additive",[]).append(child)
                continue

            if  child.pos_ ==  "ADP" and child.dep_  == "case":
                features.setdefault("prep", []).append(child)
                continue
        #print( token, "::", ", ".join(f"{x}:{x.dep_}:{x.pos_}"  for x in token.children), ",features", features)
        return features



    def try_get_sv(self, token):
        if token.pos_ == "VERB":
            for child in token.children:
                if child.dep_ == "nsubj" and child.pos_ in {"NOUN"}:
                    mo =  str(token.morph)
                    try:
                        voice_str = mo[mo.rindex("|Voice=")+7:]
                    except ValueError:
                        voice_str ="unknown"
                    yield f"{child.lemma_}|{token.lemma_}|{voice_str}"





    def yield_subject_object_attriutes_for_verb(self, token):
        subject = None
        objects = []
        attributes = []
        noun_attributes = []
        #print(token)


        for child in token.children:
            if child.dep_ == "nsubj" and child.pos_ in {"NOUN", "PRON", "PROPN"}:
                subject = child
                for subject_child in subject.children:#woman and
                    if subject_child.dep_ in {"amod", "advmod","nmod"}:
                        noun_attributes.append(subject_child)

            elif child.pos_ == "NOUN" and child.dep_ in {"obj","obl"}:
                objects.append(child.lemma_)
            elif child.dep_ in {"amod","advmod"}:#"xcomp" - ?
                attributes.append(child)
            elif child.pos_ == "VERB":
                #print("entering ii")
                for inner_verb in child.children:
                    if inner_verb.lemma_ == "и":
                        yield from self.yield_subject_object_attriutes_for_verb(inner_verb)

        if subject:
            if objects:
                self.count_objs.append(len(objects))
            for  object_name in objects:
                    yield f"SVO|{token.lemma_}|{subject.lemma_}|{object_name}"
            for attr_name in attributes:
                    yield f"SVAv|{token.lemma_}|{subject.lemma_}|{attr_name}"
            for noun_attr_name in noun_attributes:
                    for object_name in objects:
                        yield f"ASO|{noun_attr_name}|{subject.lemma_}|{object_name}"



    def get_svo2_attr(self,token):
        subject = None
        objects = []
        attributes = []
        noun_attributes = []
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            yield from self.yield_subject_object_attriutes_for_verb(token)




    def statistics(self):
        print(sum(self.count_objs)/len(self.count_objs))



    def check_if(self, token):
        advcl_found = False
        if_found = False

        for child in token.children:
            if child.dep_ == "adcvl":
                for inner_child in child.children:
                    if inner_child.lemma_ == "если":
                        return True

    def check_in_case(self, token):
        pass
        #adcvl -> В - mark ? ->


