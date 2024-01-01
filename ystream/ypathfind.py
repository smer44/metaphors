from ystream.yabstract import yStream


class yPathTripletsInSimpleStorage(yStream):

    def __init__(self,start_word,end_word,):
        self.init(start_word, end_word)

    def init(self,start_word,end_word,):
        self.start_word = start_word
        self.end_word = end_word


    def __iter__(self):
        start_word = self.start_word
        end_word = self.end_word

        for storage in self.source:
            ngrams = storage.ngrams
            #print("- items - " , ngrams[start_word].items())
            if end_word not in ngrams:
                for (next_word, next_relation), weight_forward in ngrams[start_word].items():
                    print(" -->>" , start_word, next_relation, next_word)
                    if next_word == end_word:
                        yield "-- start ->  end --"
                        yield start_word," -> ",  next_relation, " ->", next_word
                        yield "-- end --"
                    if next_word in ngrams:
                        for (next_word_2, next_relation_2), weight_forward_2 in ngrams[next_word].items():
                            if next_word_2 == end_word:
                                yield "-- start -> next -> end --"
                                yield start_word," -> ",next_relation," -> ",next_word
                                yield next_word, " -> ",next_relation_2, " -> ",next_word_2
                                yield "-- end --"
                            if next_word_2 in ngrams:
                                for (next_word_3, next_relation_3), weight_forward_3 in ngrams[next_word_2].items():
                                    if next_word_3 == end_word:
                                        yield "-- start -> next -> next_word_2 -> end --"
                                        yield start_word, " -> ",next_relation, " -> ",next_word
                                        yield next_word," -> ", next_relation_2, " -> ",next_word_2
                                        yield next_word_2, " -> ",next_relation_2, " -> ",next_word_3
                                        yield "-- end --"
            else:
                for (next_word, next_relation) , weight_forward in ngrams[start_word].items():
                    #yield "->", start_word, next_relation, next_word, end_word
                    print(" -- start_word, next_relation, next_word ",start_word, next_relation, next_word)
                    if next_word == end_word:
                        yield "-- start ->  end --"
                        yield start_word, " -> ",next_relation, " -> ",next_word
                        yield "-- end --"
                        continue
                    for (prev_word, prev_relation), weight_backward in ngrams[end_word].items():
                        print(" -- end_word, prev_relation, prev_word ", end_word, prev_relation, prev_word)
                        if prev_word == start_word:
                            yield "-- start <-  end --"
                            yield end_word, prev_relation, start_word
                            yield "-- end --"
                            continue
                        if next_word not in ngrams:
                            continue
                        for (next_word_2, next_relation_2), weight_forward_2 in ngrams[next_word].items():
                            #print(" -- -- next_word, next_relation_2, next_word_2 ", next_word, next_relation_2, next_word_2)
                            # possible start_word -> next_word -> (next_word_2 =prev_word) -> end_word
                            if  next_word_2 == prev_word:
                                yield f"-- start:{start_word} -> next:{next_word} -> (next_2:{next_word_2} = prev:{prev_word} ) <- end:{end_word} --"
                                yield start_word, next_relation, next_word
                                yield next_word, next_relation_2, prev_word
                                yield end_word, prev_relation, prev_word
                                yield "-- end --"
                                continue

                            #possible start_word -> next_word -> next_word_2 =end_word
                            if next_word_2 == end_word:
                                yield "-- start -> next -> end --"
                                yield start_word,next_relation,next_word
                                yield next_word, next_relation_2, next_word_2
                                yield "-- end --"
                                continue
                        if prev_word not in ngrams:
                            #print("prev_word not in ngrams : " , prev_word)

                            #print("prev_word not in ngrams продукт питания ?: ", "продукт питание" in ngrams)
                            continue
                        for (prev_word_2, prev_relation_2), weight_backward_2 in ngrams[prev_word].items():
                            # possible start_word -> (next_word =prev_word_2)  <- prev_word <- end_word
                            if prev_word_2 == start_word:
                                yield "-- start -> (next = prev) <- end "
                                yield prev_word_2, prev_relation_2, prev_word
                                yield prev_word, prev_relation, end_word
                                yield "-- end --"
                                continue
                            #print(" -- -- prev_word_2, prev_relation_2, prev_word ", prev_word_2, prev_relation_2, prev_word)
                            if prev_word_2 == next_word:
                                yield f"-- start:{start_word} -> (next:{next_word} = prev2:{prev_word_2}) <- prev:{prev_word} <- end:{end_word} 2"
                                yield start_word, next_relation, next_word
                                yield prev_word, prev_relation_2, next_word
                                yield end_word, prev_relation, prev_word
                                yield "-- end --"
                                continue







class yPathInSimpleStorage(yStream):

    def __init__(self,start_word,end_word,max_items = 100):
        self.init(start_word,end_word,max_items )

    def init(self,start_word,end_word,max_items = 100):
        self.start_word = start_word
        self.end_word = end_word
        self.max_items = max_items

    def __iter__(self):
        start_word = self.start_word
        end_word = self.end_word
        max_items = self.max_items
        structure = dict()
        depth_for_words= dict()
        depth_for_words[start_word] = 0
        for storage in self.source:
            ngrams = storage.ngrams
            stack = [start_word]
            stack_set = set()
            while stack:
                max_items-=1
                if max_items <=0: break
                word = stack[0]
                depth = depth_for_words[word]





                next_depth = depth +1
                stack = stack[1:]
                row = ngrams[word]
                for (next_word, relation) , weight in row.items():
                    if next_word not in structure and word not in structure:
                        structure.setdefault(next_word,[]).append(word)

                    #if next_word == end_word:
                        #while next_word in structure:
                            #prev_word, relation = structure[next_word]
                            #yield prev_word,relation, next_word
                            #next_word = prev_word
                        #return
                    yield  word, depth, relation, next_word,depth_for_words.get(next_word, -1)
                    if next_word == end_word:
                            while depth > 0:
                                print(f"check if {word} is in structure : ", word in structure)
                                if word not in structure:
                                    return
                                for prev_word in structure.get(word, []):
                                    if depth_for_words[prev_word] == depth - 1:
                                        yield "->", prev_word, word
                                        word = prev_word
                                        break
                                depth = depth - 1
                            stack = []

                    if next_word in ngrams and next_word not in stack_set:
                        stack.append(next_word)
                        stack_set.add(next_word)
                        depth_for_words[next_word] = next_depth








class yGetAssociationsFromMultiStorage(yStream):

    def __init__(self,start_word, end_word,max_items = 100):

        self.start_word = start_word
        self.end_word = end_word
        self.max_items = max_items

    def __iter__(self):
        end_word = self.end_word

        for storage in self.source:
            multi_ngrams = storage.multi_ngrams
            verb_subjects = storage.verb_subjects
            nouns = storage.nouns
            verbs = storage.verbs
            stack = [self.start_word]
            stack_set = set(stack)
            count = self.max_items
            while stack :

                #print("stack :" , stack )
                word = stack[0]
                stack = stack [1:]
                if word in nouns:
                    ngrams = multi_ngrams[word]
                    for verb, items in ngrams.items():
                        #if verb not in stack_set:
                        #    stack.append(verb)
                        #    stack_set.add(verb)

                        for item in items:
                            yield word, verb, item
                            if item  == end_word:
                                return

                            if item not in stack_set:
                                stack.append(item)
                                stack_set.add(item)

                #if word in verbs:
                #    nouns = verb_subjects[word]
                #    stack.extend(nouns)
                #    for item in nouns:
                        #yield item,word
                #        if item not in stack_set:
                #            stack.append(item)
                #            stack_set.add(item)

                count -= 1
                if count == 0: break



