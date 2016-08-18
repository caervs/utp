import time

modulus = 23
generator = 3

all_elems = sorted(range(modulus))

generated = []

current = 0
while len(generated) != len(all_elems):
    current = (current + generator) % modulus
    generated.append(current)


for i in range(1, modulus + 1):
    sublist = generated[:i]
    s = " ".join((str(elem) if elem in sublist else " " * len(str(elem))) for elem in all_elems)
    print(s, end="\r")
    time.sleep(1)
print()
