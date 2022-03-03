# pg. 126 in An Introduction to Cybernetics by W. Ross Ashby

from math import log2

def variety(x:int) -> float:
    ans = log2(x)
    return ans

print(variety(52))

# A set of vectors can have no more variety than the sum of the
# components' variety. The below vector has a maximum variety
# of 9.9 bits (the unit of variety is a bit)
print(sum([variety(10), variety(8), variety(12)]))
