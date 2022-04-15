correct = [1,1,2,2,2,8]

inString = '0 1 2 2 2 7'
inStringList = inString.split(' ')
numList = [int(element) for element in inStringList]

output = [(correct[i]-numList[i]) for i in range(len(correct))]
print(output)