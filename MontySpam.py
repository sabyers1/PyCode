spam_amount = 0
print(spam_amount)

# Ordering Spam, egg, Spam, Spam, bacon and Spam (4 more services of Spam)
spam_amount = spam_amount + 4

if spam_amount > 0:
    print("But I don't want ANY spam")

viking_song = "Spam " * spam_amount
print(viking_song)

print(5 / 2)
print(float(6 / 2))

print(5 // 2)
print(5 % 2)

print(float(5/2))
def quiz_message(grade):
    if grade < 50:
        outcome = 'failed'
    else:
        outcome = 'passed'
    print('You '+ outcome + ' the quiz with a grade of ' + str(grade))

quiz_message(80)
quiz_message(45)

print(spam_amount.bit_length())
x=0.125
numerator, denominator = x.as_integer_ratio()
print(float(numerator / denominator))

def count_negatives(nums):
    return len([num for num in nums if num<0])

print("Total negative numbers are: " + str(count_negatives([0, 1, 4, -3, -5, 10])))

m = [['egg','spam']]

def menu_is_boring(meals):
    """Given a list of meals served over some period of time, return True if the
    same meal has ever been served two days in a row, and False otherwise.
    """
    #while n < len(meals)-1:
    totalm=len(meals)
    for n in range(totalm):
        if n < totalm-1:
            if meals[n]==meals[n+1]:
                return True
    return False

print(menu_is_boring(m))

print("{} added to the beginning then the end was {}.".format(x, 'infinity'))

class Point:
    def __init__(self, x, y):
        self.x, self.y = x,y
    def __str__(self):
        return 'Pointy({self.x}, {self.y})'.format(self=self)
print(str(Point(4,2)))
#help(str)
zip_code = '1234x'

print(zip_code.isdigit())

doc_list = ["The Learn Python Challenge Casino.", "They bought a car", "Casinoville"]
keyword = 'casino'
L=[]
for n in range(len(doc_list)):
    doc_list[n] = doc_list[n].rstrip('.,').lower
    print(doc_list[n])
    if doc_list[n].find(keyword.lower()) <> -1:
        L.append(n)
    
print(L)