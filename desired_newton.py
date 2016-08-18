class DynamicSystem(object):
    pass


class NewtonianSystem(object):
    G = (6.674 * N * m ^ 2) / kg ^ 2
    forces = {
        (lambda o1, o2: (G * o1.mass * o2.mass) / (o1.location - o2.location) ^ 2
         ),
    }

    laws = []
