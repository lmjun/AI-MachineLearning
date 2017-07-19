
import numpy as np
from numpy.linalg import inv
from numpy import linalg as LA
import sys


X = np.matrix('1 2 3; 3 4 5')
print X.shape
Y = np.matrix('5 6; 7 8')
print(X)
print(Y)
#norm
print(LA.norm(X))


print (((inv(np.eye((X.dot(X.getT())).ndim) + X.dot(X.getT()))).dot(X)).dot(Y))
print(X.ndim)

#dot
print(X.dot(Y))
#trans
print(X.getT())
print(inv(X))
