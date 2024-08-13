
from random import randint

def p(targets,turn):
    np = 1
    for i in range(targets):
        np *= ((12-i) - 3 - turn) / (12-i)
    return 1 - np

print('\t\tT1\tT2\tT3\tT4\tT5\tT6\tT7')
for n in range(1,9):
    print(n, "targets:",end='\t')
    for t in range(1,8):
        print(end=f"{p(n,t):.1%}\t")
    print()

