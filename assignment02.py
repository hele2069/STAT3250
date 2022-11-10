##
## File: assignment02.py (STAT 3250)
## Topic: Assignment 2
##

## Two *very* important rules that must be followed in order for your 
## assignment to be graded correctly:
##
## a) The file name must be exactly "assignment02.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these 
##    names variable names should not be used anywhere else in your file.  Do   
##    not delete these variables, if you don't know how to find a value just  
##    leave it as is. (If a variable is missing the autograder will not grade  
##    any of your assignment.)


## Questions 1-7: For the questions in this part, use the following
##  lists as needed:
    
list01 = [5, -9, -1, 8, 0, -1, -2, -7, -1, 0, -1, 6, 7, -2, -1, -5]
list02 = [-2, -5, -2, 8, 7, -7, -11, 1, -1, 6, 6, -7, -9, 1, 5, -11]
list03 = [9, 0, -8, 3, 2, 9, 3, -4, 5, -9, -7, -3, -11, -6, -5, 1]
list04 = [-4, -6, 8, 8, -5, -5, -11, -3, -1, 7, 0, 2, -5, -2, 0, -5]
list05 = [-11, -3, 8, -9, 2, -8, -7, -12, 7, 3, 2, 0, 6, 4, -11, 6]
biglist = list01 + list02 + list03 + list04 + list05

## Questions 1-7: Use for loops to answer each of the following applied  
##  to the lists defined above.
 
## 1.  Add up the squares of the entries of biglist.
import numpy as np

q1 = 0
for i in biglist: 
    q1 += i ** 2
    
## 2.  Create "newlist01", which has 14 entries, each the sum of the 
##      corresponding entry from list01 added to the corresponding entry
##      from list02.  That is,
##     
##         newlist01[i] = list01[i] + list02[i] 
##
##      for each 0 <= i <= 13.

# for the first 14 elements in list01 & 02, add the sum of them to newlist01
newlist01 = []
for i in range(0,14):
    newlist01.append(list01[i]+list02[i])
q2 = newlist01   # newlist01


## 3.  Determine the number of entries in biglist that are less than 6.

# summing number of 1's (evaluating as True if an element in biglist is less than 6)
q3 = sum(i < 6 for i in biglist)   # number of entries in biglist less than 6

## 4.  Create a new list called "newlist02" that contains the elements of
##      biglist that are greater than 5, given in the same order as the
##      elements appear in biglist.

# for each element in biglist, add it to newlist02 if it is greater than 5
newlist02 = []
for i in biglist:
    if i > 5:
        newlist02.append(i)
    
q4 = newlist02   # newlist02

## 5.  Find the sum of the positive entries of biglist.

# for each element in biglist, if it's positive, add it to q5
q5 = 0  # sum of the positive entries of biglist
for i in biglist:
    if i > 0: 
        q5 += i

## 6.  Make a list of the first 19 negative entries of biglist, given in
##      the order that the values appear in biglist.

# first filter out the positive entries, then include only first 19 entries. 
q6 = [] # list of first 19 negative entries of biglist
for i in biglist: 
    if i < 0:
        q6.append(i)
q6 = q6[0:19]
      
##  7. Identify all elements of biglist that have a smaller element that 
##      immediately preceeds it.  Make a list of these elements given in
##      the same order that the elements appear in biglist.

# append the entry to q7 if its preceding entry is smaller 
q7 = []   # list of elements preceded by smaller element
for i in range(len(biglist)):
    if biglist[i-1] < biglist[i]:
        q7.append(biglist[i])

## Questions 8-9: These questions use simulation to estimate probabilities
##  and expected values.  

##  8. Consider the following game: You flip a fair coin.  If it comes up
##      tails, then you win $1.  If it comes up heads, then you get to 
##      simultaneously flip four more fair coins.  In this case you win $1 
##      for each head that appears on all flips, plus you get an extra $7 if 
##      all five flips are heads.
##
##      Use 100,000 simulations to estimate the average amount of money won 
##      when playing this game.
    
# when using random generation, 1 means head, 0 means tail
import numpy as np

overall_profit = [] # a list used to keep track of all simulations 
n = 0
while n < 100000:
    money = 0 # money = profit in each simulation; reset to 0 at the beginning of each simulation
    trial1 = np.random.choice([1,0],size=1)[0] # check if first flip is head (1) of tail(0)
    if trial1 == 1: # if first flip is head, proceed
        trial2 = np.random.choice([1,0],size=4) # flip four more times
        if (trial2 == 1).sum() == 4: # only add $7 if four flips are heads
            money += 7
        money += ((trial2 == 1).sum()+1) # each head adds $1 to profit (always happen regardless of the $7 condition)
    else:
        money += 1 # if first flip is tail, add $1 to profit
    n += 1 # number of simulations increases by 1
    overall_profit.append(money) # when one simulation ends, add the profit to overall profit list for calculating mean at the end

q8 = np.mean(overall_profit) # mean winnings from 100,000 times playing the game

##  9. Jay is taking a 15 question true/false quiz online.  The
##      quiz is configured to tell him whether he gets a question
##      correct before proceeding to the next question.  The 
##      responses influence Jay's confidence level and hence his 
##      exam performance.  In this problem we will use simulation
##      to estimate Jay's average score based on a simple model.
##      We make the following assumptions:
##    
##      * At the start of the quiz there is a 81% chance that 
##        Jay will answer the first question correctly.
##      * For all questions after the first one, if Jay got 
##        the previous question correct, then there is a
##        90% chance that he will get the next question
##        correct.  (And a 10% chance he gets it wrong.)
##      * For all questions after the first one, if Jay got
##        the previous question wrong, then there is a
##        72% chance that he will get the next question
##        correct.  (And a 28% chance he gets it wrong.)
##      * Each correct answer is worth 5 points, incorrect = 0.
##
##      Use 100,000 simulated quizzes to estimate Jay's average 
##      score.

# when using random generation, 1 means correct, 0 means wrong
overall_score = [] # a list that keeps track of all simulations 
n = 0
while n < 100000:
    simulation_score = 0 # quiz score in each simulation; reset to 0 each time
    question_1 = np.random.choice([1,0],size=1,p=[0.81,0.19])[0] # first answer generator 
    current_answer = question_1 # set a new variable that records correct/wrong for each upcoming questions 
    simulation_score += (question_1 * 5) # score on question 1; since it's 1(correct) or 0(wrong), by * 5 safely gives us the point worth
    questions_answered = 1 # keeps track of how many questions answered 
    while questions_answered < 15: # this while loop repeats 14 times, using 2 different percentage models based on if Jay gets the last question right/wrong
        if current_answer == 1:
            simulation_score += 5 # correct answer = 5 points
            current_answer = np.random.choice([1,0],size=1,p=[0.9,0.1])[0] # if last question is correct, 90% correct again and 10% wrong
        else:
            current_answer = np.random.choice([1,0],size=1,p=[0.72,0.28])[0] # if last question is wrong, 72% correct and 28% wrong again
        questions_answered += 1 # prevent while loop from running endlessly
        
    overall_score.append(simulation_score) # keeps a copy of quiz score from each simulation
    n += 1 # prevent while loop from running endlessly

q9 = np.mean(overall_score)  # mean score from 100,000 simulated quizzes

# solution
allscores = np.zeros(100000) # array to hold quiz scores
for i in range(100000):
    scoretotal = 0  # initialize quire score to 0
    q1score = np.random.choice([5,0], size=1, p=[.81,.19]) # random score, Q1
    scoretotal += q1score[0] # add quest 1 to score
    lastscore = q1score # keep track of score on previous problem
    for j in range(14): # the rest of the quiz; 1 loop per question
        if lastscore > 0: # check last result; generate next result
            nextscore = np.random.choice([5,0], size=1, p=[.90,.10])
        else:
            nextscore = np.random.choice([5,0], size=1, p=[.72,.28])
        scoretotal += nextscore[0] # add question score to scoretotal
        lastscore = nextscore # shift question score to last question
    allscores[i] = scoretotal # save the score total

q9 = np.mean(allscores)  # mean of 100,000 simulated quizzes











