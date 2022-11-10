 ##
## File: assignment06.py (STAT 3250)
## Topic: Assignment 6
##

##  The questions this assignment are based on "timing_log.txt".
##  The file "timing_log.txt" contains the set of all WeBWorK
##  log entries on April 1, 2011.  The entries are organized by
##  one log entry per line, with each line including the following:
##
##  --the date and time of the entry
##  --a number that is related to the user (but is not unique)
##  --something that appears to be the epoch time stamp
##  --a hyphen
##  --the "WeBWorK element" that was accessed
##  --the "runTime" required to process the problem
##
##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the timing_log.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values. 

    
## Load pandas and read in the data set
import pandas as pd # load pandas as pd

loglines = open('timing_log.txt').read().splitlines()

## 1.  How many log entries were for requests for a PDF version of an
##     assignment?  Those are indicated by "hardcopy" appearing in the 
##     WeBWorK element.

# first use a temp var to split the text by space 
# column 8 will be the 'WeBWorK' element, and we know it will always be column 8 because all records follow the same spacing pattern
# and we check how many contains 'hardcopy'
temp1 = pd.Series(loglines).str.split(' ',expand=True)
q1 = len(temp1[8][temp1[8].str.contains('hardcopy')]) # number of log entries requesting a PDF

## 2.  What percentage of log entries involved a Spring '12 section of MATH 1320?

# assuming computer-generated files follow the same text pattern for each record
# using temp1, find column 8 records that contains 'Spring12-MATH1320' 
# find percentage 
q2 = len(temp1[8][temp1[8].str.contains('Spring12-MATH1320')])/len(temp1[8])*100  # percentage of log entries, Spring '12 MATH 1320

## 3. How many different classes use the system? Treat each different name 
##    as a different class, even if there is more than one section of a course.  

# split 'WeBWork' by '/', and looking at column 2 we know it will always identify a class
# count unique names in column 2 and ignore those with na values or ] or space as the only value 
temp3 = temp1[8].str.split('/',expand=True)
count = temp3[2]
count = count.dropna()
count = count.str.replace(']','')
count = count.str.replace(' ','')
count = count[count!='']
q3 = len(count.unique())  # number of different classes using the system

## 4.  Find the percentage of log entries that came from an initial
##     log in.  For those, the WeBWorK element has the form
##
##          [/webwork2/ClassName] or [/webwork2/ClassName/]
##
##     where "ClassName" is the name of a class.   

# split original data into sub-strings and clean them by dropping ']' and '/'
# then find those that only contains the first three sub-strings, which indicates that it is an initial login 
# then find the percentage
temp4 = pd.Series(loglines).str.split('[').str[2].str.split(']').str[0].str[:-1].str.split('/')
q4 = 100*len(temp4[temp4.str.len()==3])/len(temp1) # percentage of log entries from initial log in

## 5.  Determine the percentage of log entries for each section of MATH 1310
##     from Spring 2012, among the total number of log entries for MATH 1310,
##     Spring 2012.  Give the percentages as a Series with class name as
##     index and percentages as values, sorted by percentage largest to smallest.
##     (The class name should be of the form 'Spring12-MATH1310-InstructorName')

# temp5 cleasn the column 'webwork' to include only spring12 math1310 entries, and without ']' since some may miss stuff like homework that follows 
# then group by each section and count them, and divide by total entries of spring12 math1310
# sort in descending order 
temp5 = temp1[8]
temp5 = temp5[temp5.str.contains('Spring12-MATH1310')]
temp5 = temp5.str.split('/',expand=True)[2].str.replace(']','')
sections = temp5.groupby(temp5).count()
q5 = (sections/len(temp5)*100).sort_values(ascending=False)  # Series of MATH 1310 sections and percentage within MATH 1310

## 6.  How many log entries were from instructors performing administrative
##     tasks?  Those are indicated by "instructor" alone in the 3rd position of
##     the WeBWorK element.  

# first locate 'webwork' and include only those that contain 'instructor' anywhere
# then, split by '/' and check the fourth column since the first column will be '[' which doesn't count 
# find how many in that column contains exclusively 'instructor' and no other strings 
temp6 = temp1[8]
temp6 = temp6[temp6.str.contains('instructor')]
third_element = temp6.str.split('/',expand=True)[3]
q6 = len(third_element[third_element=='instructor'])  # number of instructor administrative log entries

## 7.  Find the number of log entries for each hour of the day. Give the
##     counts for the top-5 (plus ties as usual) as a Series, with hour of day
##     as index and the count as values, sorted by count from largest to 
##     smallest.

# find 3rd column in temp1, which is time 
# split by ':' and resulting column1 will be the hour 
# groupby hour and find count, keeping top 5 counts with ties 
temp7 = temp1[3].str.split(':',expand=True)[0]
q7 = temp7.groupby(temp7).count().nlargest(5,keep='all')  # Series of entry count by hour, top 5

## 8.  Find the number of log entries for each minute of each hour of the day. 
##     Give the counts for the top-8 (plus ties as usual) as a Series, with 
##     hour:minute pairs as index and the count as values, sorted by count 
##     from largest to smallest.  (An example of a possible index entry
##     is 15:47)

# same as question#7, except we group by two columns insteade of one
# and keep 8 largest instead of 5
# also change the column names to avoid column names being generated differently on gradescope 
temp8 = temp1[3].str.split(':',expand=True).iloc[:,0:2]
temp8.columns = ['hour','minute']
q8 = temp8.groupby(['hour','minute']).size().nlargest(8,keep='all')  # Series of counts by hour:minute, top-8 plus ties

## 9. Determine which 5 classes had the largest average "runTime".  Give a 
##    Series of the classes and their average runTime, with class as index
##    and average runTime as value, sorted by value from largest to smallest.

# first locate the class and runtime column and add them to temp9
# then drop na records 
# renaming columns for clarity
# drop records containing only ']' as classname and replace records with ']' by ''
# then groupby each classname and find the mean runtime, keeping top 5 without ties 
temp9 = pd.DataFrame(temp3[2])
temp9['runtime'] = temp1[11].astype(float)
temp9=temp9.dropna()
temp9.columns = ('course','runtime')
temp9 = temp9[temp9['course']!=']']
temp9['course'] = temp9['course'].str.replace(']','')
q9 = temp9['runtime'].groupby(temp9['course']).mean().sort_values(ascending=False).head(5)  # Series of classes and average runTimes

## 10. Determine the percentage of log entries that were accessing a problem.  
##     For those, the WeBWorK element has the form
##
##           [/webwork2/ClassName/AssignmentName/Digit]
##     or
##           [/webwork2/ClassName/AssignmentName/Digit/]
##
##     where "ClassName" is the name of the class, "AssignmentName" the
##     name of the assignment, and "Digit" is a positive digit.

# first use the 5th column in temp3 as it is the 'digit' part 
# then drop na and ']' to exclude those who are not accessing a problem
# then find percentage
temp10 = temp3[4]
temp10 = temp10.dropna()
temp10 = temp10[temp10!=']']
q10 = len(temp10)/len(temp1)*100  # percentage of log entries accessing a problem

## 11. Find the top-10 (plus tied) WeBWorK problems that had the most log entries,
##     and the number of entries for each (plus ties as usual).  Sort the 
##     table from largest to smallest.
##     (Note: The same problem number from different assignments and/or
##     different classes represent different WeBWorK problems.) 
##     Give your answer as a Series with index entries of the form
##
##          ClassName/AssignmentName/Digit
##
##     and counts for values, sorted by counts from largest to smallest.

# from temp3 we get the classname/assignment/digit as 3 columns 
# then drop na values and digit = ']' since we want those who actually accessed the problems 
# create column names for clarity 
# then group by class/assignment/digit and find 10 largest counts with ties 
temp11 = temp3.iloc[:,2:5]
temp11 = temp11.dropna()
temp11.columns = ('class','assignment','digit')
temp11 = temp11[temp11['digit']!=']']

q11 = temp11.groupby(['class','assignment','digit']).size().nlargest(10,keep='all')  # Series of problems and counts













