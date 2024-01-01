from ystream.yabstract import yStream,yMasterSlaveStream
from ystream.yhelperfunc import sort_clip_keys,format_list

class yAnalogsCombinations(yStream):


    def __init__(self, subject,object, amount):
        self.init(subject,object, amount)

    def init(self,subject,object, amount):
        self.subject = subject
        self.object = object
        self.amount = amount

    def __iter__(self):
        for ystorage in self.source:
            subject_analogs = ystorage.ngrams.get(self.subject, dict())
            object_analogs = ystorage.ngrams.get(self.object, dict())
            subject_analogs = sort_clip_keys(subject_analogs,self.amount)
            object_analogs = sort_clip_keys(object_analogs, self.amount)
            yield subject_analogs , object_analogs
            #yield f" subject : {format_list(subject_analogs)} : {format_list(object_analogs)}"





