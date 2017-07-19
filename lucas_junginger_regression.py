import numpy as np
from numpy.linalg import inv
from numpy import linalg as LA
import sys


# Given coefficients w,
# generate noisy random data points X, Y
# Where Y is approximately (X transpose)*w
# This is used to test gradient_descent
def generate_data(npoints, w):
	dim = np.size(w)
	X = np.random.uniform(-10, 10, (dim, npoints))
	Y = np.dot(X.T, w)
	err = np.random.normal(0, 1, (npoints))
	return X, Y+err


# Returns the exact best fit w to the data
def exact_solution(X, Y):
	X2 = np.asmatrix(X)
	Y2 = (np.asmatrix(Y)).getT()
	
	#w = (I + X*X^T)^-1 *X*Y
	use = X2.dot(X2.getT())
	I = np.eye(use.shape[0])
	
	w = (((inv(I+use)).dot(X2)).dot(Y)).getT()

	w2 = np.zeros(X.shape[0])
	for x in range(0, w.shape[0]):
		w2[x] = float(w[x])

	return w2

# Starts with an initial guess for w
# and performs gradient descent until it converges
def gradient_descent(X, Y, alpha=0.00001):
	w = np.zeros(X.shape[0])

	#w2 = k rows, 1 col
	w2 = np.asmatrix(w).getT()
	#Y2 = n rows, 1 col
	Y2 = np.asmatrix(Y).getT()
	#X2 = n cols, k rows
	X2 = np.asmatrix(X)
	
	#USE: w2 - X2.dot(Y2 - (X2.getT()).dot(w2))
	#||loss|| = LA.norm(w2 - X2.dot(Y2 - (X2.getT()).dot(w2)))

	while(LA.norm(w2 - X2.dot(Y2 - (X2.getT()).dot(w2))) >= 0.001):
		#print w2[[-0.78610983]

		#print((alpha * (w2 - X2.dot(Y2 - (X2.getT()).dot(w2)))))
		w2 = w2 - (alpha * (w2 - X2.dot(Y2 - (X2.getT()).dot(w2))))

	for x in range(0, w2.shape[0]):
		w[x] = (float(w2[x]))
	return w


if __name__ == '__main__':
	if len(sys.argv) == 1:
		# Test if gradient descent was implemented properly
		w = np.random.normal(0,1,(10))
		X, Y = generate_data(100, w)
		w_exact = exact_solution(X, Y)
		w_solved = gradient_descent(X, Y)
		print w_exact
		print w_solved
		if np.max(abs(w_exact-w_solved)) < 0.01:
			print "Gradient descent working!"
		else:
			print "Gradient descent not working"

	else:
		# Extract the online_shares dataset
		fp = open(sys.argv[1], 'r')
		lines = fp.readlines()
		features = [st.strip() for st in lines[0].split(',')]
		features.pop() # Get rid of shares label
		data = np.genfromtxt(sys.argv[1], delimiter=',')

		X = data[1:, :data.shape[1]-1].T
		Y = data[1:, data.shape[1]-1]

		xmeans = np.mean(X, axis=0)
		ymean = np.mean(Y)
		xstdevs = np.std(X,axis=0)
		ystdev = np.std(Y)

		# Normalize the data for numerical stability
		X_normalized = (X-xmeans)/xstdevs
		Y_normalized = (Y-ymean)/ystdev

		w_exact = exact_solution(X_normalized, Y_normalized)

		y_pred = ystdev*np.dot(X_normalized.T, w_exact)+ymean

		rmse = np.linalg.norm(Y-y_pred)/np.sqrt(len(Y))
		print "Root mean squared error = ", rmse
		print "Standard deviation", np.std(Y)

		# Sort descending by absolute value of weights
		sorted_inds = np.argsort(abs(w_exact))[::-1]

		# Print out weights
		for i in range(len(w_exact)):
			print w_exact[sorted_inds[i]], ',', features[sorted_inds[i]]


