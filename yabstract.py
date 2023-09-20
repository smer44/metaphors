class yStream:

    def __call__(self,other):
        if isinstance(other,str):
            other = [other]
        self.source = other
        return self

    def __gt__(self, other):
        other.source = self
        return other

    def __iter__(self):
        return self.iter_items

    def __next__(self):
        return next(self.iter_items)

