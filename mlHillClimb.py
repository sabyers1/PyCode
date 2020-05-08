'''
File: mlHillClimb.py
File Create: 8th May 2020
Author: Stephen Byers
-----
 Example of Hill Climb search algorithm for machine learning.
 
-----
Last Modified: 8th May 2020 11:16:23 am
Modified By: Stephen Byers
-----
No Copyright 2020
'''
import random
import copy

# Hill-climbing search algorithm
# 1. Create two lists, L and Lseen.
#    Initialize L to initial state and Lseen is empty
# 2. Let n be the first element of L.  Compare this state with the final state.
#    If they are identical, stop with success.
# 3. Apply to n all available search operators, thus obtaining a set of new states.
#    Discard those states that already exist in Lseen.  As for the rest, sort them by
#    Evaluation function and place them at the front of L.
# 4. Transfer n from L into the list, Lseen, of the states that have been investigated.
# 5. If L is empty, stop and report failure, otherwise loop to step 2.

dbugFlag = False

def RList():
    ''' Creates randomized list '''
    return list(random.sample(range(0,9),9))

def dprint(*argkv):
    if dbugFlag:
        print(*argkv)

def SearchList(xL):
    foundList = False
    for sL in Ls:                        # get the next sublist in Lseen
        sLlen=len(sL)
        if sLlen == len(xL):             # check same length lists
            for i in range(0,sLlen):     # loop through sublist
                if xL[i] != sL[i]:
                    break                # not the same lists
            if i == sLlen:
                foundList = True

    return foundList

def SortList(xL):
    '''Calculates the absolute sum of differences in the lists
       on a position by position basis. '''
    sum = 0
    for i in range(len(xL)):
        sum += abs(xL[i]-fs[i])

    #dprint("SortList: {} fs:{} d:{}".format(xL,fs,sum))
    return sum        

def Slide(tL):
    ''' Slides zero position left or right in list.
        however this doesn't get us to the final desired
        state because it doesn't swap values.'''
    # find position of zero within list.
    j=1
    for i in tL:
        if i == 0:
            zPos = j
            break
        j+=1
    
    addList = []                # list of states to be added once sorted

    if zPos < 8:                # check for 'left slide' OK
        lL = copy.copy(tL)      # copy current state
        lL[zPos-1] = lL[zPos]   # copy left elemnt over zero
        lL[zPos] = 0
        dprint("lL: {} from: {} delta: {}".format(lL,tL,SortList(lL)))
        if not SearchList(lL):  # if not in Lseen, sort, insert in L
            addList.append(lL)

    if zPos > 1 :               # check for 'right slide' OK
        rL = copy.copy(tL)      # copy current state
        rL[zPos-1] = rL[zPos-2]   # copy right elemnt over zero
        rL[zPos-2] = 0
        dprint("rL: {} from: {} delta: {}".format(rL,tL,SortList(rL)))
        if not SearchList(rL):  # if not in Lseen, sort, insert in L
            addList.append(rL)

    if len(addList)>0:
        addList.sort(key = SortList)  # lowest is best, so keep in high to low order
        for i in range(len(addList)): # this loop reverses the sort order (reverse=True)
            L.insert(0,addList[i])
        dprint("Slide insert: {}".format(L))
    else:
        dprint("Didn't find any new states for {}".format(tL))

    return zPos

# main application code
if __name__ == "__main__":
    L = []                          # create L list
    Ls = []                         # create Lseen list    
    L.insert(0,RList())             # initialize L with random list item
    fs = [8,7,6,5,4,3,2,1,0]        # final state of list (reverse sort)
    dprint("L {} LSize: {}\nfs: {}".format(L,len(L),fs))

    maxLoops = 5000
    while (len(L)>0):
        for n in tuple(L):              # get first element, n, of L list, tuple so list doesn't grow
            if n == fs:                 # compare element state with final state
                print("Found final state!\n{}".format(n))
                break
            else:
                # Apply to n all available search operators.
                Slide(n)
                # Remove n from L and transfer to Ls
                L.remove(n)
                Ls.append(n)
                maxLoops -= 1
                if maxLoops%100 == 0:
                    print(".", end ='')


        if maxLoops < 1 :
            print("\nERROR** exceeded maximum loops!")
            print("List size: {} Evaluated size {}\n".format(len(L),len(Ls)))
            break

    if len(L) == 0:
        print("ERROR** exhausted states without finding final state.") 