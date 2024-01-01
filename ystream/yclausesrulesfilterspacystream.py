from ystream.yabstract import yStream



class yClausesRulesFilterSpacyStream(yStream):

    def __init__(self):

       self.rules = {("VERB", "ROOT") :[[("NOUN", "nsubj") ,("NOUN", "obj") ],[("PRON", "nsubj") ,("NOUN", "obj")  ],[("NOUN", "nsubj") ,("NOUN", "obl") ], ] }

    def __iter__(self):
        for token in self.source:
            rules_row = self.rules.get((token.pos_, token.dep_), None)
            if not rules_row: continue
            children_dict = {(child.pos_, child.dep_): child for  child in token.children}
            if rules_row:
                for rule_variant in rules_row:
                    found = True
                    found_children = []
                    for pos_, dep_ in rule_variant:
                        child_candidate = children_dict.get((pos_, dep_), None)
                        if child_candidate:
                            found_children.append(child_candidate.lemma_)
                        else:
                            found = False
                            break
                    if found:
                        yield token,found_children
