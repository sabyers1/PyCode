import numpy as np
A = np.array(([1,3,3],[1,4,3],[1,3,4]))
print("Start array A:\n {}".format(A))
A_inv = np.linalg.inv(A)
print("Inverse array A^-1:\n {}".format(A_inv))
print("A*.A^-1 array:\n {}".format(A_inv.dot(A)))
A_det = np.linalg.det(A)
print("det(A):\n {}".format(A_det))
