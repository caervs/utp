import functools


class Field(object):
    pass


class FieldElement(object):
    def __init__(self, field):
        self.field = field

    def __add__(self, other):
        return self.field.addition_operation(self, other)

    def __mul__(self, other):
        return self.field.multiplication_operation(self, other)

    def __pow__(self, integer):
        if integer == 0:
            return self.field.multiplicative_identity
        elif integer > 0:
            return self * (self ** (integer - 1))
        else:
            raise NotImplementedError

    def __eq__(self, other):
        return self.field.equivalence_operation(self, other)


class FiniteFieldElement(FieldElement):
    def __init__(self, field, integer_value):
        super().__init__(field)
        self.integer_value = integer_value

    def __hash__(self):
        return hash(self.integer_value)

    def __repr__(self):
        return str(self.integer_value)


class FiniteField(Field):
    addition_operation = lambda self, x0, x1: FiniteFieldElement(self, self.canonicalize(x0.integer_value + x1.integer_value))
    multiplication_operation = lambda self, x0, x1: FiniteFieldElement(self, self.canonicalize(x0.integer_value * x1.integer_value))
    equivalence_operation = lambda self, x0, x1: self.canonicalize(x0.integer_value) == self.canonicalize(x1.integer_value)

    def __init__(self, modulus):
        self.modulus = modulus
        self.additive_identity = FiniteFieldElement(self, 0)
        self.multiplicative_identity = FiniteFieldElement(self, 1)

    def canonicalize(self, integer):
        return integer % self.modulus

    def __iter__(self):
        return map(
            functools.partial(FiniteFieldElement, self), range(self.modulus))


def main():
    field = FiniteField(7)
    generator = FiniteFieldElement(field, 3)
    print(generator ** 3)


if __name__ == "__main__":
    main()
