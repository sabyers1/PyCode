'''
File: mlSlideBoxHillClimb.py
File Create: 6th May 2020
Author: Stephen Byers
-----
 Machine Learning Exercise to mimic sliding tile
 toy exercise using the Hill-Climbing search algorithm.
 
-----
Last Modified: 6th May 2020 2:28:37 pm
Modified By: Stephen Byers
-----
Copyright 2020
'''
dbugFlag = False

if dbugFlag:
    import unittest
    class TestSlideMoves(unittest.TestCase):
        def test_slide(self):
            self.assertFalse(fs.valid_slide('up',4))
            self.assertTrue(fs.valid_slide('up',5))
            self.assertFalse(fs.valid_slide('up',9))
            self.assertFalse(fs.valid_slide('up',1))
            self.assertFalse(fs.valid_slide('up',3))

            self.assertTrue(fs.valid_slide('dn',5))
            self.assertFalse(fs.valid_slide('dn',4))
            self.assertFalse(fs.valid_slide('dn',6))
            self.assertFalse(fs.valid_slide('dn',7))
            self.assertFalse(fs.valid_slide('dn',9))

            self.assertFalse(fs.valid_slide('lf',3))
            self.assertTrue(fs.valid_slide('lf',5))
            self.assertFalse(fs.valid_slide('lf',9))
            self.assertFalse(fs.valid_slide('lf',1))
            self.assertFalse(fs.valid_slide('lf',7))

            self.assertFalse(fs.valid_slide('rt',1))
            self.assertTrue(fs.valid_slide('rt',5))
            self.assertFalse(fs.valid_slide('rt',7))
            self.assertFalse(fs.valid_slide('rt',3))
            self.assertFalse(fs.valid_slide('rt',9))

class TileBox (object):
    #mTB = [[1, 2, 3],
    #       [8, 0, 4],
    #       [7, 6, 5]]
    #mLoc = 0

    def __init__(self, object):
        self.mTB = object
        i=j=0  # row = col = 0
        # iterate through matrix look for zero value
        while (self.mTB[i][j] != 0):
            j+=1 #next col
            if (j > 2):
                i+=1  #next row
                j=0   #reset col
                if (i > 2):
                    i=-1  # not found
                    break

        self.mloc = (i+1)+(3*j)
        self.calc_signature()
    
    def show(self):
        print ("{}\n{}\n{}\nSig: {}\n".format(self.mTB[0],self.mTB[1],self.mTB[2],self.signature))

    #make long integer describing the 3x3 matrix to represent states in compact form.
    def calc_signature(self):
        self.signature  = 100000000 * self.mTB[0][0] 
        self.signature += 10000000 * self.mTB[0][1]
        self.signature += 1000000 * self.mTB[0][2]
        self.signature += 100000 * self.mTB[1][0]
        self.signature += 10000 * self.mTB[1][1]
        self.signature += 1000 * self.mTB[1][2]
        self.signature += 100 * self.mTB[2][0]
        self.signature += 10 * self.mTB[2][1]
        self.signature += self.mTB[2][2]
        return self.signature

    def swap(self,dir,loc):
        if (0 < loc & loc < 10) & self.valid_slide(dir,loc):
            idx = slide_offset(dir)
            tmp = self.mTB[int((loc-1)/3)][(loc-1)%3]
            self.mTB[int((loc-1)/3)][(loc-1)%3] = self.mTB[int((loc-1+idx)/3)][(loc-1+idx)%3]
            self.mTB[int((loc+idx-1)/3)][(loc-1+idx)%3] = tmp
            print("Swapping: M{},{} with M{},{}\n"
                .format(int((loc-1)/3),(loc-1)%3, int((loc-1+idx)/3), (loc-1+idx)%3))
            self.calc_signature()  # Update signature
        else:
            print("ERROR**Invalid swap request: at loc: {} dir: {}".format(loc,dir))
        #print("Slide: {} {} is {}\n".format(loc, dir, self.valid_slide(dir,loc)))

    def valid_slide(self,dir,loc):
        # Given a location in matrix and direction return whether OK to slide.
        # needs to be more elegant method to calculate acceptable moves!!
        # must be at empty (zero) value location and within boundaries
        slide_rules = {'up':range(4,10),
                    'dn':range(1,7),
                    'rt':{1,2,4,5,7,8},
                    'lf':{2,3,5,6,8,9}}
        #print("valid_slides for {} are {}\n".format(dir,slide_rules.get(dir)))
        if loc != self.mloc:
            return False
        if slide_rules.get(dir) == None:
            return False
        return bool(loc in slide_rules.get(dir))

    # In order to slide the tilebox:
    # 1. The empty ('0') tile index needs to be located (stored in mloc)
    # 2. The direction of the slide needs to be provided
    # 3. Tile in direction needs to be swapped if valid.
    # Slide can not occur outside of the frame edges
    def slide(self,dir):
        """ Slide swaps data at appropriate location in matrix in the direction specified"""
        if self.valid_slide(dir,self.mloc):
            self.swap(dir,self.mloc)
            self.mloc = self.mloc + slide_offset(dir)
            print("Zero moved to loc: {}".format(self.mloc))
            return True
        else:
            print("ERROR**Invalid slide {} at {}".format(dir,self.mloc))
            return False

def slide_offset(dir):
    """ Slide uses dictionary to perform mapping of empty tile movement """
    switcher = {
        'up':-3,
        'dn':3,
        'lf':-1,
        'rt':1
    }
    return switcher.get(dir,0) # if not valid return 0

# take the difference between the two matrixes to compare for start.
def TileBoxes_Compare(tb1, tb2):
    rTB = TileBox([[0,0,0],[0,0,0],[0,0,0]])
    sum = 0
    for i in range (len(tb1.mTB)):
        for j in range(len(tb1.mTB[0])):
            rTB.mTB[i][j] = tb1.mTB[i][j] - tb2.mTB[i][j]
            sum += abs(rTB.mTB[i][j])

    return sum

def TileBox_Compare(tb1):
    return TileBoxes_Compare(tb1,fs)

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
        

if __name__ == "__main__":
    fs = TileBox([[1,2,3],[8,0,4],[7,6,5]])
    ss = TileBox([[0,2,1],[6,7,4],[3,8,5]])
    fs.show()
    ss.show()
    #print("The difference between matrixes is: {}".format(TileBox_Compare(fs,ss)))
    #print("The difference between matrixes is: {}".format(TileBox_Compare(ss,ss)))

    L = [ss]
    Ls = []
    LsSigs = []
    maxLoops = 100
    for nTB in L:
        if TileBox_Compare(nTB) == 0:
            print("Found final state!")
            break
        else:
            #generate Lseen signature list
            for tTB in Ls:
                LsSigs.insert(0,tTB.signature)

        #Build search options, the four possible slide movement directions
        for d in {'up','dn','rt','lf'}:
            tTB = nTB         #save signature & state before slide
            if tTB.slide(d):  #if valid slide add to state check.
                if not tTB.signature in LsSigs:  #Discard signature already in Lseen
                    L.insert(0,tTB)

        #sort options and place at beginning of List.  We want options with smallest
        #comparision value, so it is a reverse sort.
        L.sort(key = TileBox_Compare, reverse=True)
        #L.sort(key = TileBox_Compare())

        #transfer evaluated item into Lseen and remove from L
        Ls.insert(0,nTB)
        L.remove(nTB)
        if len(L)==0:
            print("ERROR**No further options avaiable")
            nTB.show()
            break

#     ss.swap('rt',1)
#     ss.show()
#     ss.swap('rt',2)
#     ss.show()
#     ss.swap('dn',3)
#     ss.show()
#     ss.swap('dn',6)
#     ss.show()
#     ss.swap('lf',9)
#     ss.show()
#     ss.swap('lf',8)
#     ss.show()
#     ss.swap('up',7)
#     ss.show()
#     ss.swap('up' ,4)
#     ss.show()
#     ss.slide('rt')
#     ss.slide('rt')
#     ss.slide('rt')
#     ss.slide('dn')
#     ss.slide('dn')
#     ss.slide('dn')
#     ss.slide('lf')
#     ss.slide('up')
#     ss.show()
#     print("State is {}".format(ss.calc_signature()))


    #print("Slide up: {} dn: {} rt: {} lf: {}\n"
    #    .format(slide('up',ss),slide('dn',ss),slide('rt',ss),slide('lf',ss)))
    
    if dbugFlag:
        unittest.main()