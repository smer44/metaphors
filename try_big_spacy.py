import spacy
from  yngrams import yNgrams

lang_name = "en_core_web_sm"
#lang_name = 'ru_core_news_sm'
spacy.prefer_gpu()
print("what is dep token :" , spacy.explain("dep"))
print("what is pcomp token :" , spacy.explain("pcomp"))
print("what is xcomp token :" , spacy.explain("xcomp"))

#print(spacy.info()["pipelines"])

nlp = spacy.load(lang_name)
#print("Pipeline:", nlp.pipe_names)
text = "Apple is looking at buying U.K. startup for $1 billion"


#filename = "../datasets/dummy_text.txt"
filename =  "E:\data\dictionaries\case_frames_0.fr.txt"

encoding=  'cp1251'
encoding=  'utf-8'

#with open(filename, 'r', encoding=encoding) as file:     text = file.read()


#variants
#девочка аня
#девочка, которую звали
# девочка, чьё имя было Аня
#В небольшой деревне жила  девочка по национальности русская
#В небольшой деревне жила русская девочка
#В небольшой унылой русской деревне жила <нерусская> девочка


# продвинутый уровень - подъежая к станции у меня слетела шляпа

doc = nlp(text)
#iteration possibilities:
#for token in doc
#sentences : doc.sents

#doc.sents is a list of type <class 'spacy.tokens.span.Span'>

"""
obl: oblique nominal
The obl relation is used for a nominal (noun, pronoun, noun phrase) 
functioning as a non-core (oblique) 
argument or adjunct. This means that 
it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.

idea: replace obl on advmod
"""





def yield_clauses(root_token):
    stack = [(root_token,0)]
    while stack:
        token,depth = stack.pop()
        prefix = "\t-"*depth
        #print("\t-"*depth, token ,  ":" , token.dep_)
        children = list(token.children)
        #remove unclassifyed dependencies:

        objects = []
        verb = None
        subject = None
        if  token.pos_ == "VERB":
            verb =  token.lemma_
        for child in children:
            if (child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and child.dep_ == "nsubj":
                subject =child.lemma_
            if ((child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and (child.dep_ == "obj" or child.dep_ == "obl"or child.dep_ == "dep")) or  \
                (child.pos_ == "VERB" and (child.dep_ == "xcomp" or child.dep_ == "pcomp") ):
                objects.append(child.lemma_)

        if subject and verb and objects:
            yield " ".join( (subject , verb, *objects))

        #children_lemmas=[f"{token.lemma_}:{token.dep_}:{token.pos_}" ] + [f"{child.lemma_}:{child.dep_}:{child.pos_}"for child in children]
        #clause = "|".join(children_lemmas)
        #line = f"{prefix}{token} : {clause}"
        children.reverse()
        depth+=1
        for child in children:
            stack.append((child,depth ))


def yield_clauses_dfs(root_token):
    stack = [(root_token,0)]
    while stack:
        token,depth = stack.pop()
        prefix = "\t-"*depth
        #print("\t-"*depth, token ,  ":" , token.dep_)
        children = list(token.children)
        if children:
            skip = False
            for child in children:
                if child.dep_ == "dep":
                    skip = True

            skip = skip or token.dep_ == "punct"
            #if skip: continue
            children_lemmas=[f"{token.lemma_}:{token.dep_}" ] + [f"{child.lemma_}:{child.dep_}"for child in children]
            clause = "|".join(children_lemmas)
            yield clause
            #line = f"{prefix}{token} : {clause}"
            #print(line)

            children.reverse()
            depth+=1
            for child in children:
                stack.append((child,depth ))

def print_sentence(sentence):
    return " ".join(f"{token.lemma_}:{token.dep_}:{token.pos_}" for token in sentence)

def print_shallow_token(token):
    return " ".join(f"{child.lemma_}:{child.dep_}:{child.pos_}" for child in list(token.children))

def save_clauses(doc):
    for n, sentence in enumerate(doc.sents):
        #print("type:" , type ( sentence))
        #print("sentence: ", sentence)
        #print("tokens  : ", print_sentence(sentence))
        for token in sentence:
            if token.dep_ == "ROOT":
                print("ROOT : " , print_shallow_token(token))#consumes children generator
                #print(yield_brackets_recursive(token))
                for clause in yield_clauses(token):
                    print("  -  clause: " , clause)
                #for clause in yield_clauses_dfs(token):
                    #print(clause)


save_clauses(doc)


