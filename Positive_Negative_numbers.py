num=[1,-2,3,-44,-88,-4,6,1,5,-66]
pos=[]
neg=[]
for i in num:
    if (i>=0):
        pos.append(i)
    else:
        neg.append(i)
print('positive    = ', pos)
print('negative = ', neg)