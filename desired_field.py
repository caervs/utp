import functools
import itertools
import operator


class AlgebraicStructure(object):
    def __init__(self, elements, operations):
        self.elements = elements
        self.operations = operations

    def __iter__(self):
        return iter(self.elements)

    def __in__(self, elem):
        return elem in self.elements


def method(operation):
    return lambda *args: operation(*args)


def workon(structure):
    elem, = itertools.islice(structure.elements, 1)
    cls = type(elem)
    for name, operation in structure.operations.items():
        attr_name = "__{}__".format(name)
        setattr(cls, attr_name, method(operation))


class Field(AlgebraicStructure):
    def __init__(self, elements, add, mul):
        super().__init__(elements, {
            "add": add,
            "mul": mul,
            "sub": lambda x, y: x + self.add_inverse_of(y),
            "truediv": lambda x, y: x * self.mul_inverse_of(y),
            "neg": self.add_inverse_of,
            "pow": self.power
        })

    @property
    def adder(self):
        return self.operations["add"]

    @property
    def multiplier(self):
        return self.operations["mul"]

    # TODO memoize all functions
    @property
    def mul_identity(self):
        for possible in self.elements:
            if self.is_mul_identity(possible):
                return possible
        raise ValueError("No multiplicative identity found")

    @property
    def add_identity(self):
        for possible in self.elements:
            if self.is_add_identity(possible):
                return possible
        raise ValueError("No additive identity found")

    def is_add_identity(self, elem):
        return self.adder(elem, elem) == elem

    def is_mul_identity(self, elem):
        return (not self.is_add_identity(elem)) and \
            (self.multiplier(elem, elem) == elem)

    def add_inverse_of(self, elem):
        for possible in self.elements:
            if self.is_add_identity(self.adder(elem, possible)):
                return possible
        raise ValueError("No additive inverse found")

    def mul_inverse_of(self, elem):
        for possible in self.elements:
            if self.is_mul_identity(self.multiplier(elem, possible)):
                return possible
        raise ValueError("Not multiplicative inverse found")

    def power(self, elem, exponent):
        if not isinstance(exponent, int):
            raise TypeError("Unknown exponent type", type(exponent))
        if exponent == 0:
            return self.mul_identity
        elif exponent > 0:
            return elem * (elem**(exponent - 1))
        elif exponent < 0:
            return (elem**(exponent + 1)) / elem
        raise ValueError("Invalid exponent", exponent)


class Partition(object):
    def __init__(self, elements=None, canonical_form=None):
        if (elements, canonical_form) == (None, None):
            raise ValueError(
                "A partition cannot be defined without either elements or a canonical form")
        self.elements = elements
        self.canonical_form = canonical_form

    def __eq__(self, other):
        if self.canonical_form is not None:
            return self.canonical_form == other.canonical_form
        raise NotImplementedError(
            "Other forms of equivalence not yet implemented")

    def __hash__(self):
        if self.canonical_form is not None:
            return hash(self.canonical_form)
        raise NotImplementedError("Other forms of hashing not yet implemented")

    def __repr__(self):
        if self.canonical_form is not None:
            return "<Partition: {}>".format(self.canonical_form)
        raise NotImplementedError("Other forms of repping not yet implemented")


class PartitioningScheme(object):
    def __init__(self, eq_relation=None, elements=None, canonical=None):
        # NOTE need either a relation and elements or canonical function
        self.eq_relation = eq_relation
        self.elements = elements
        self.canonical = canonical

    def partition_of(self, elem):
        if self.canonical is not None:
            return Partition(canonical_form=self.canonical(elem))
        raise NotImplementedError("Only partitioning based on canonical done")

    def apply(self, operation, partition1, partition2):
        return self.partition_of(operation(partition1.canonical_form,
                                           partition2.canonical_form))


class FiniteField(Field):
    def __init__(self, modulus):
        scheme = PartitioningScheme(canonical=lambda n: n % modulus)
        partitions = set(map(scheme.partition_of, range(modulus)))
        add = functools.partial(scheme.apply, operator.add)
        mul = functools.partial(scheme.apply, operator.mul)
        super().__init__(partitions, add, mul)


def test_basic_field():
    field = FiniteField(7)
    workon(field)
    p = partitions = {partition.canonical_form: partition
                      for partition in field}

    assert p[5] + p[6] == p[4]
    assert p[5] * p[6] == p[2]
    assert p[5] - p[6] == p[6]

    assert p[1] / p[6] == p[6]
    assert p[5] / p[6] == p[2]
    assert -p[5] == p[2]

    assert p[2]**2 == p[4]
    assert p[2]**3 == p[1]
    assert p[2]** -1 == p[4]
    assert p[2]** -2 == p[2]


def test_rsa():
    p = 5
    q = 7
    N = p * q
    e = 5
    encryption_field = FiniteField(p * q)
    decryption_field = FiniteField((p - 1) * (q - 1))
    d_partitions = {partition.canonical_form: partition
                    for partition in decryption_field}
    E = lambda n: workon(encryption_field) or n**e
    d = decryption_field.mul_inverse_of(d_partitions[e]).canonical_form
    D = lambda n: workon(encryption_field) or n**d

    print("x\tE(x)\tD(E(x))")
    for partition in d_partitions.values():
        x = partition.canonical_form
        ex = E(partition).canonical_form
        dex = D(E(partition)).canonical_form
        print("{}\t{}\t{}".format(x, ex, dex))


def test_binary():
    class Bit(object):
        def __init__(self, value=0):
            self.value = value

        def __eq__(self, other):
            return self.value == other.value

        def __repr__(self):
            return "<Bit: {}>".format(self.value)


    ZERO = Bit(0)
    ONE = Bit(1)

    add = lambda b0, b1: Bit(b0.value ^ b1.value)
    mul = lambda b0, b1: Bit(b0.value | b1.value)

    f = Field([ZERO, ONE], add, mul)

    workon(f)
    print(ZERO + ZERO)
    print(ZERO + ONE)
    print(ONE + ZERO)
    print(ONE + ONE)

    print(ZERO * ZERO)
    print(ZERO * ONE)
    print(ONE * ZERO)
    print(ONE * ONE)

    print(ONE - ZERO)
    print(ONE - ONE)

    print(ONE / ONE)


def main():
    test_basic_field()
    test_rsa()
    test_binary()

if __name__ == "__main__":
    main()
