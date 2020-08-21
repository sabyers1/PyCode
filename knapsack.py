# knapsack.py
# Recursive algorithm for classic knapsack problem.
# Limited by weight which can fit into knapsack,
# include items which produce the greatest total value.  Only one of each item available.

""" Input:
    Values (stored in array v)
    Weights (stored in array w)
    Number of distinct items (n)
    Knapsack capacity (W)
    Note: the array v and w are assumed to store all relevant values at index 1.
    source: https://en.wikipedia.org/wiki/Knapsack_problem
"""
n = 10
W = 100

w = [0,23,26,20,18,32,27,29,26,30,27]
v = [0,505,352,458,220,354,414,498,545,473,543]
value = [[-1 for j in range(W+1)] for i in range(n+1)]
inSack = [0 for j in range(n+1)]

def m(i,j):
    """ Represents the maximum value that can be achieved under the condition : use i items
    and total weight limit is j"""
    if i == 0 or j <= 0:     # check for boundaries, greater than zero item and positive weight
        return 0
    
    if value[i-1][j] == -1:  # value hasn't been calculated, so call function to determine
        value[i-1][j] = m(i-1,j)
    
    if w[i] > j:            # item cannot fit in knapsack.  Too heavy
        value[i][j] = value[i-1][j]
        #inSack[j-1] = 0
        inSack[i-1] = 0
    else:
        if value[i-1][j-w[i]] == -1:
            value[i-1][j-w[i]] = m(i-1,j-w[i])  # if previous weight not calculated, need to call method.
        value [i][j] = max(value[i-1][j], value[i-1][j-w[i]] + v[i])
        #inSack[j-1] = 1
        inSack[i-1] = 1
    return value[i][j]

if __name__ == "__main__":
    for it in range(1,n+1):
        print("Max value is: {:5,} for {:2} items and {:3} weight.".format(m(it,W),it,W))
        print(inSack)

    valWt = list([(it,v[it]/w[it]) for it in range(1,n+1)])
    valWt.sort(key=lambda x:x[1],reverse=True)
    
    for i in range(0,n):
        print("Item({:2}) {:,.2f} = {}/{} Value/Weight".format(valWt[i][0],valWt[i][1],v[i+1],w[i+1]))