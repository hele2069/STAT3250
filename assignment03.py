##
## File: assignment03.py (STAT 3250)
## Topic: Assignment 3 
##

##  The questions in this assignment refer to the data in the
##  file 'absent.csv'.  The data contains 740 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros 
##  are clearly not appropriate.)  The file 'absent.pdf' has
##  a summary of the meanings for the variables.
##
##  All of these questions can be completed without loops.  You 
##  should try to do them this way, "code efficiency" will take 
##  this into account.

import numpy as np  # load numpy as np
import pandas as pd # load pandas as pd

absent = pd.read_csv('absent.csv')  # import the data set as a pandas dataframe
absent

## 1.  Find the mean absent time among all records.
## first subset to only absent time column, then find mean
q1 = np.mean(absent["Absenteeism time in hours"])  # mean of "Absenteeism" hours


## 2.  Determine the number of records corresponding to
##     being absent on a Thursday.

## first subset rows with weekday = Thursday, then find how many records are there using len()
q2 = len(absent[absent["Day of the week"] == 5])  # days absent on Thursday


## 3.  Find the number of unique employees IDs represented in 
##     this data.  
## first subset to all IDs then find the distinct IDs, and finally use len() to count how many rows are there
q3 = len(absent["ID"].unique())  # number of unique employee IDs


## 4.  Find the average transportation expense for the employee 
##     with ID = 34.
## first subset ID=34 with expense as the only column, then calculate the mean 
q4 = np.mean(absent.loc[absent["ID"] == 34,"Transportation expense"])  # Average transportation expense, ID = 34


## 5.  Find the total number of hours absent for the records
##     for employee ID = 11.
## first subset ID=11 with absent time as the only column, then calculate sum of absent time
q5 = sum(absent.loc[absent["ID"] == 11,"Absenteeism time in hours"])  # total hours absent, ID = 11


## 6.  Find (a) the mean number of hours absent for the records of those who 
##     have no pets, then (b) do the same for those who have more than one pet.

## for both of these, first subset to those who do not own/own more than 1 pet with associated absent time as the only column, 
## then find mean absent hours 
q6a = np.mean(absent.loc[absent["Pet"] == 0,"Absenteeism time in hours"]) # mean hours absent, no pet
q6b = np.mean(absent.loc[absent["Pet"] > 1,"Absenteeism time in hours"]) # mean hours absent, more than one pet


## 7.  Among the records for absences that exceeded 8 hours, find (a) the 
##     proportion that involved smokers.  Then (b) do the same for absences 
##     of no more then 4 hours.

## for both of these, have a temp variable set up for filtering absent time, and include 'social smoker' as the only variable 
## then, use sum to find how many smokers since the variable only contains 0s and 1s (1 indicates smoker); 
## len() is used to find overall how many people's absence exceed 8 hours/no more than 4 hours
absent_larger8 = absent.loc[absent["Absenteeism time in hours"] > 8,"Social smoker"]
absent_nomore4 = absent.loc[absent["Absenteeism time in hours"] <= 4,"Social smoker"]
q7a = sum(absent_larger8)/len(absent_larger8) # proportion of smokers, absence greater than 8 hours
q7b = sum(absent_nomore4)/len(absent_nomore4) # proportion of smokers, absence no more than 4 hours

## 8.  Repeat Question 7, this time for social drinkers in place of smokers.

## the same logistics as the previous qustion except filtering drinkers instead of smokers
absent_drink_larger8 = absent.loc[absent["Absenteeism time in hours"] > 8,"Social drinker"]
absent_drink_nomore4 = absent.loc[absent["Absenteeism time in hours"] <= 4,"Social drinker"]
q8a = sum(absent_drink_larger8)/len(absent_drink_larger8) # proportion of social drinkers, absence greater than 8 hours
q8b = sum(absent_drink_nomore4)/len(absent_drink_nomore4) # proportion of social drinkers, absence no more than 4 hours


## 9.  Find the top-5 employee IDs in terms of total hours absent.  Give
##     the IDs and corresponding total hours absent as a Series with ID
##     for the index, sorted by the total hours absent from most to least.

## find sum of absence hours by each ID (groupby), then sort them in descending order
## limit top 5 rows using head(5)
temp = absent['Absenteeism time in hours'].groupby(absent['ID']).sum()
q9 = temp.sort_values(ascending=False).head(5)  # Series of top-5 employee IDs in terms of total hours absent

 
## 10. Find the average hours absent per record for each day of the week.
##     Give the day number and average as a Series with the day number
##     as the index, sorted by day number from smallest to largest.

## find mean of absence hours by each day of week (groupby), then sort them
## sort_index() sorts data based on index on default 
temp2 = absent['Absenteeism time in hours'].groupby(absent['Day of the week']).mean()
q10 = temp2.sort_index()  # Series of average hours absent by day of week.

## 11. Repeat Question 10 replacing day of the week with month.
##     Give the month number and average as a Series with the month number
##     as the index, sorted by month number from smallest to largest.

## same logistics as the previous quesiton, except we use month instead of day of week
## one difference is that I need to filter out month = 0 since that does not make sense contextually (we don't have a month 0)
temp3 = absent.loc[absent['Month of absence'] != 0,'Absenteeism time in hours'].groupby(absent['Month of absence']).mean()
q11 = temp3.sort_index()  # Series of average hours absent by month.


## 12. Find the top 3 most common reasons for absence for the social smokers.
##      Give the reason code and number of occurances as a Series with the 
##      reason code as the index, sorted by number of occurances from
##      largest to smallest.  (If there is a tie for 3rd place,
##      include all that tied for that position.)

## first use a temp variable to filter out non-smokers and any record with reason# = 1 since it does not correspond to any reason categories as indicated in the pdf 
## then find out how many absence records are there per absence reason (groupby)
## finally use nlargest() to keep top 3 occurances with ties, use keep = 'all' to keep duplicates  
temp4 = absent[(absent['Social smoker'] == 1) & (absent['Reason for absence'] != 0)]
temp4 = temp4.groupby(['Reason for absence']).size() # Series of reason codes and counts 
q12 = temp4.nlargest(3,keep='all')










