import numpy as np

k = np.array([[2,3],[-4,-5],[6,7],[11,22]])
h = np.array([[-4,-5],[8,9]])
for m in k:
    for n in h:
        if (n==m).all():
            print(m)
        #print(((h==m).reshape(2,-1)))

# print(k)
# values = k==[2,7]
# print(values)
# print(k[values])
