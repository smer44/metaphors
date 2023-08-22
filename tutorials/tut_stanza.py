import sys

import stanza

#stanza.download("en")
#stanza.download("ru")

nlp = stanza.Pipeline('ru',download_method=None)


#print(doc)
#print(doc.entities)

def validate_stanza_sentence(sentence):
    #get root:
    for token in sentence.tokens:
        #print("token :" , token)
        for word in token.words:
            #print("word :", word)
            if word.deprel == "root":
                if word.upos != "VERB":
                    print(f"validate_stanza_sentence : root {word.text} is not a verb in the sentence: {sentence.text}", file = sys.stderr)


def validate_stanza_doc(doc):
    for sentence in doc.sentences:
        validate_stanza_sentence(sentence)


doc = nlp("Жил пёс. Пёс был серый.")
validate_stanza_doc(doc)


filename = "../../datasets/facts_gpt.txt"

with open(filename, "r", encoding='utf-8') as file:
    text = file.read()
    doc = nlp(text)
    validate_stanza_doc(doc)