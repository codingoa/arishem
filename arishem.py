from random import sample, shuffle, randint
from collections import defaultdict

def p(targets,turn):
    np = 1
    for i in range(targets):
        np *= ((24-i) - 3 - turn) / (24-i)
    return 1 - np

print('\t\tT1\tT2\tT3\tT4\tT5\tT6\tT7')
for n in range(1,9):
    print(n, "targets:",end='\t')
    for t in range(1,8):
        print(end=f"{p(n,t):.1%}\t")
    print()

all_cards = {}

header = None
with open("cards.txt","r") as fp:
    for l in fp.readlines():
        if header is None:
            header = l.split(",")
        else:
            name, cost, power, *ability = l.split(",")
            all_cards[name] = int(cost)

for c in range(9):
    print(c,sum(v==c for v in all_cards.values()))

costs = defaultdict(int)
for i in range(10000):
    deck = sample(sorted(all_cards), 12)
    for card in deck:
        costs[all_cards[card]]+=1

for i in range(9):
    print(f"{i} - {costs[i]/10000:.1f}")

def sim(deckcosts, n=1000, arishem=True):
    unspent_energy = 0
    for i in range(n):
        deck = list(deckcosts)

        if arishem:
            random_deck = sample(sorted(all_cards), 12)
            deck += [all_cards[c] for c in random_deck]
        shuffle(deck)
        hand = deck[:3]
        
        for turn in range(6):
            energy = 1 + arishem + turn
            hand.append(deck[3+turn])
            
            playable = [c for c in hand if c <= energy]
            double_play = 0
            if playable:
                single_play = max(playable)
                for i,a in enumerate(playable):
                    for b in playable[i+1:]:
                        if a+b <= energy and a+b > single_play and a+b > double_play:
                            double_play = a+b
                            c,d=a,b
                if double_play:
                    unspent_energy += energy - double_play
                    hand.remove(c)
                    hand.remove(d)
                else:
                    unspent_energy += energy - single_play
                    hand.remove(single_play)
            else:
                unspent_energy += energy

    return unspent_energy / n

def find_best(n_rand=100, play_arishem=False, steps=1000, arishem=True):
    sims = {}
    for i in range(n_rand):
        c = sample(sorted(all_cards), 11)
        c = list(map(all_cards.get, c))

        c.append(7 if play_arishem else 0)
        v = sim(c, steps, arishem)
        sims[tuple(sorted(c))] = v


    best = min(sims, key=sims.get)

    while True:
        for i in range(12):
            if arishem:
                if i == 0 and not play_arishem:
                    continue
                if i == 11 and play_arishem:
                    continue
            up = tuple(sorted(n + (j==i) for j,n in enumerate(best)))
            down = tuple(sorted(n - (j==i) for j,n in enumerate(best)))
            if not up in sims:
                sims[up]=sim(up, steps, arishem)
            if not down in sims:
                sims[down]=sim(down, steps, arishem)
        if min(sims, key=sims.get) == best:
            break
        else:
            best=min(sims, key=sims.get)

    return (best, sims[best])

print(f"{sim([0,2,3,3,3,3,4,4,5,5,3,6])=}")
print(f"meta {sim([0,1,2,3,4,4,4,5,5,6,6,4])=}")
print(f"{sim([2,3,3,3,3,4,4,5,5,3,6,6], arishem=False)=}")
print(f"{sim([1,1,1,2,2,3,3,3,4,4,5,5], arishem=False)=}")

start = 100
length = 1000

print("Without Arishem")
print(find_best(n_rand=start, steps=length, arishem=False))
print(find_best(n_rand=start, steps=length, arishem=False))
print(find_best(n_rand=start, steps=length, arishem=False))

print("With Arishem")
print(find_best(n_rand=start, steps=length))
print(find_best(n_rand=start, steps=length))
print(find_best(n_rand=start, steps=length))

