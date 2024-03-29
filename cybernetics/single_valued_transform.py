from math import log10

operands = [n for n in range(10)]

def transition(n):
    try:
        return int(str(log10(n+4))[4])
    except:
        return 0

transforms = list(map(transition, operands))

print('-'*60)
print(operands)
print(transforms)
print('-'*60)
if len(set(transforms))==len(transforms):
    print('one-one transformation!')
else:
    print('many-one transformation!')
