from ystream.yabstract import yStream


class yAnalogsTripletCombinations(yStream):

    def __init__(self,subject_analogs, object_analogs, triplet_storage):
        self.subject_analogs_storage = subject_analogs

        self.object_analogs_storage = object_analogs
        self.triplet_storage = triplet_storage

    def variants(self,subject,verb,object):
        #unrestricted analogues:
        subject_analogs =self.subject_analogs_storage.analogs(subject)
        object_analogs = self.object_analogs_storage.analogs(object)
        for subj in subject_analogs:
            for obj in object_analogs:
                if self.triplet_storage.contains(subj,verb,obj):
                    yield subj,verb,obj


def analogs_by_context(key,context_key,key_analog_storage, context_pair_storage):
        key_analogs = key_analog_storage.analogs(key)
        context_suitable_keys=context_pair_storage.analogs(context_key)

        return key_analogs.intersect(context_suitable_keys)

class yAnalogsTripletCombinationsRestricted(yStream):
    def __init__(self,subject_analogs, object_analogs, verb_subject_rows, verb_object_rows, triplet_storage):
        self.subject_analogs_storage = subject_analogs
        self.object_analogs_storage = object_analogs
        self.verb_subject_rows = verb_subject_rows
        self.verb_object_rows = verb_object_rows
        self.triplet_storage = triplet_storage








    def variants(self,subject,verb,object):
        #unrestricted analogues:
        subject_analogs =analogs_by_context(subject,verb,self.subject_analogs_storage,self.verb_subject_rows)
        object_analogs = analogs_by_context(object, verb, self.object_analogs_storage, self.verb_object_rows)

        for subj in subject_analogs:
            for obj in object_analogs:
                if self.triplet_storage.contains(subj,verb,obj):
                    yield subj,verb,obj



