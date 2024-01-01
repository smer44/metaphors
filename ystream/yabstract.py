class yStream:

    def __gt__(self, other):
        other.__set_first_type_source__(self)
        return other

    def __rshift__(self, other):
        other.__set_second_type_source__(self)
        return other

    def __ge__(self,other):
        other.__set_third_type_source__(self)
        return other


    def __set_first_type_source__(self, source):
        self.source = source

    def __set_second_type_source__(self, source):
        raise RuntimeError(f"yStream : >> operator called but not implemented for class {type(self)}")

    def __set_third_type_source__(self, source):
        raise RuntimeError(f"yStream : >= operator called but not implemented for class {type(self)}")

    def __iter__(self):
        #return self.iter_items
        raise RuntimeError(f"yStream.__iter__ : subclass: {self.__class__.__name__} should implement __iter__")

    def __add__(self, other):
        concat = yConcatStream(self,other)
        return concat

    def __mul__(self, other):
        masterslave = yMasterSlaveStream(self,other)
        return masterslave


   # def __next__(self):
   #    return next(self.iter_items)

class ySequence(yStream):

    def __init__(self,*items):
        self.source = items
        #print("ySequence: set items:" , self.source)

    def __iter__(self):
        return iter(self.source)


class yMapStream(yStream):
    def __init__(self,fn):
        self.fn = fn

    def __iter__(self):
        fn = self.fn
        for item in self.source:
            yield fn(item)




class yConcatStream(yStream):

    def __init__(self,*parts):
        self.parts = list(parts)

    def __iter__(self):
        parts = self.parts
        for stream_part in self.parts:
            for item in stream_part:
                yield item

    def __set_first_type_source__(self, source):
        for part in self.parts:
            source > part


    def __set_second_type_source__(self, source):
        self.parts.append(source)

    def __add__(self, other):
        self.parts.append(other)
        return self





class yMasterSlaveStream(yStream):

    def __init__(self,masterstream,slavestream):
        self.source= masterstream
        self.slave = slavestream

    def check_sources(self):
        assert hasattr(self,"source") and  isinstance(self.source, yStream), f"{self.__class__.__name__} : source not set"
        assert hasattr(self,"slave") and isinstance(self.slave, yStream), f"{self.__class__.__name__} : slave not set"



    def __set_second_type_source__(self, slavestream):
        self.slave= slavestream

    def __set_third_type_source__(self, source):
        if isinstance(source, yMasterSlaveStream):
            self.source = source.source
            self.slave  = source.slave
        else:
            raise RuntimeError("yMasterSlaveStream : wrong operator >= , used not from the yMasterSlaveStream source")


    def __mul__(self, other):
        raise RuntimeError("yMasterSlaveStream : wrong operator * , multiple slaves are currently not suported")


class yMap2Stream(yMasterSlaveStream):
    def __init__(self,fn):
        self.fn = fn

    def __iter__(self):
        self.check_sources()
        iter_master = iter(self.source)
        iter_slave = iter(self.slave)
        fn = self.fn
        try:
            while True:
                master_item = next(iter_master)
                slave_item = next(iter_slave)
                yield fn(master_item,slave_item)
        except StopIteration:
            pass

