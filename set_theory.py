class Set(frozenset):
    pass


class OrderedPair(Set):
    @property
    def left(self):
        pass

    @property
    def right(self):
        pass


class Tuple(OrderedPair):
    def __iter__(self):
        yield self.left
        yield from self.right


class Function(Set):
    def __call__(self, x):
        y, = set(y | (x, y) in self)
        return y
