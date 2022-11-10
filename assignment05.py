##
## File: assignment05.py (STAT 3250)
## Topic: Assignment 5 
##

##  This assignment requires the data file 'diabetic_data.csv'.  This file
##  contains records for over 100,000 hospitalizations for people who have
##  diabetes.  The file 'diabetic_info.pdf' contains information on the
##  codes used for a few of the entries.  Missing values are indicated by
##  a '?'.  You should be able to read in this file using the usual 
##  pandas methods.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the diabetic_data.csv data that includes about 35% of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values. 

##  Note: Many of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). Scoring will take
##  this into account.

import pandas as pd # load pandas as pd

dia = pd.read_csv('diabetic_data.csv')
dia1 = dia.loc[:10,:]

## 1.  Determine the average number of procedures ('num_procedures') for 
##     those classified as females and for those classified as males.

# first subset q1f and q1m to only Female and Male records respectivly
# include only 'num_procedures' and find the mean 
q1f = dia.loc[dia['gender']=='Female','num_procedures'].mean()  # female average number of procedures
q1m = dia.loc[dia['gender']=='Male','num_procedures'].mean()  # male average number of procedures


## 2.  Determine the average length of hospital stay ('time_in_hospital')
##     for each race classification.  (Omit those unknown '?' but include 
##     those classified as 'Other'.)  Give your answer as a Series with
##     race for the index sorted alphabetically.

# first use a temp variable to filter out '?' as race, and only include race and time_in_hospital as columns
# then use group by to find avg hospital stay in each race, sorted by index (race)
temp2 = dia.loc[dia['race']!='?',['race','time_in_hospital']]
q2 = temp2['time_in_hospital'].groupby(temp2['race']).mean().sort_index() # Series of average length of stay by race

## 3.  Determine the percentage of total days spent in the hospital due to
##     stays ("time_in_hospital") of at least 7 days. (Do not include the %
##     symbol in your answer.)

# use a temp that only includes time_in_hospital for coding simplicity
# then count # of rows where temp >= 7, and divide by total # of rows, and *100 to get percentage 
temp3 = dia['time_in_hospital']
q3 = len(temp3[temp3>=7])/len(temp3)*100 # percentage of days from stays of at least 7 days

## 4.  Among the patients in this data set, what percentage had at least
##     three recorded hospital visits?  Each distinct record can be assumed 
##     to be for a separate hospital visit. Do not include the % symbol in
##     your answer.

# first use a temp variable to group number of visits by patient number 
# then find out how many have >= 3 visits, and divide that number by overall number of patients
temp4 = dia.groupby(dia['patient_nbr']).size()
q4 = len(temp4[temp4>=3])/len(temp4)*100  # percentage patients with at least three visits=

## 5.  List the top-15 most common diagnoses, based on the codes listed 
##     collectively in the columns 'diag_1', 'diag_2', and 'diag_3'.
##     Give your response as a Series with the diagnosis code as the 
##     index and the number of occurances as the values, sorted by
##     values from largest to smallest.  If more than one value could
##     go in the 15th position, include all that could go in that 
##     position.  (This is the usual "include ties" policy.)

# create a temp variable that has rows containing diagnosis code from each of the three columns (resulting dataset is 3x larger than dia)
# use groupby to count how many occurances per diagnosis code, sorting top 15 while keeping ties 
temp5 = dia['diag_1']
temp5 = temp5.append(dia['diag_2'])
temp5 = temp5.append(dia['diag_3'])
q5 = temp5.groupby(temp5).count().nlargest(15,keep='all')  # top-15 diagnoses plus any ties

## 6.  The 'age' in each record is given as a 10-year range of ages.  Assume
##     that the age for a person is the middle of the range.  (For instance,
##     those with 'age' [40,50) are assumed to be 45.)  Determine the average
##     age for each classification in the column 'acarbose'.  Give your
##     answer as a Series with the classification as index and averages as
##     values, sorted from largest to smallest average.

# clean the 'age' column by removing the '[' and ')' first, and then split age range into two columns by '-'
# since we know the pattern, we can add 5 to the left age range 
# finally, goup age by acarbose and find the means, sorted in descending order 

temp6 = dia[['age','acarbose']]
temp6['age'] = temp6['age'].str.replace('[','')
temp6['age'] = temp6['age'].str.replace(')','')
temp6[['age','age2']] = temp6['age'].str.split('-',expand=True)
temp6['age'] = pd.to_numeric(temp6['age']) + 5

q6 = temp6['age'].groupby(temp6['acarbose']).mean().sort_values(ascending=False)  # Series of classifications and averages

## 7.  Determine all medical specialties that have an average hospital stay
##     (based on time_in_hospital) of at least 7 days.  Give a Series with
##     specialty as index and average hospital stay as values, sorted from
##     largest to smallest average stay.

# first remove all '?' records from medical specialty, then include only time_in_hospitla and medical_specialty; store as temp variable
# then group time_in_hospital by specialty and find the means 
# finally, filter out avg stays < 7 and sort the remaining in descending order 
temp7 = dia.loc[dia['medical_specialty']!='?',['time_in_hospital','medical_specialty']]
temp7 = temp7['time_in_hospital'].groupby(temp7['medical_specialty']).mean()

q7 = temp7[temp7>=7].sort_values(ascending=False)  # Series of specialities and average stays

##  8. Three medications for type 2 diabetes are 'glipizide', 'glimepiride',
##     and 'glyburide'.  There are columns in the data for each of these.
##     Determine the number of records for which at least two of these
##     are listed as 'Steady'.

# first find out the "sum" of each row by adding T/F values with condition == 'Steady'
# find out how many rows have "sum" >=2 which means the record has at least two 'Steady' medications 

temp8 = (dia['glipizide']=='Steady').astype(int) + (dia['glimepiride']=='Steady').astype(int) + (dia['glyburide']=='Steady').astype(int)
q8 = sum(temp8>=2)  # number of records with at least two 'Steady'

##  9. Find the percentage of "time_in_hospital" accounted for by the top-100 
##     patients in terms of number of times in file.  (Include all patients 
##     that tie the 100th patient.)

# use .agg to perform two aggregation functions on the same groupby setup
# use a variable to store top 100 patients with most number of visits, including ties, and find the sum of their hospital stays 
# divide that by overall sum of hospital stays
temp9 = dia['time_in_hospital'].groupby(dia['patient_nbr']).agg(Sum='sum',Count='count')
top100 = sum(temp9.nlargest(columns='Count',n=100,keep='all')['Sum'])
q9 = top100/sum(temp9['Sum'])*100  # Percentage of time from top-100 patients

## 10. What percentage of reasons for admission ('admission_source_id')
##     correspond to some form of transfer from another care source?

# use .isin() to find if admission reason id is in any of the following as contextualized in the pdf 
# then find the percentage of its row count vs. overall row count 
temp10 = dia[dia['admission_source_id'].isin((4,5,6,10,18,22,25,26))]
q10 = len(temp10)/len(dia)*100  # Percentage of admission by transfer

## 11. The column 'discharge_disposition_id' gives codes for discharges.
##     Determine the 5 codes that resulted in the greatest percentage of
##     readmissions.  Give your answer as a Series with discharge code
##     as index and readmission percentage as value, sorted by percentage
##     from largest to smallest.

# first creat two temp variables, one for not readmitted records and other for full record.
# then group each var by discharge id and count rows sorted by discharge id
# divide them and drop na values just to make sure if one of the variables has fewer disposition ids due to not "readmitted"
# sort in descending order and keep top 5
temp11_a = dia[dia['readmitted']!='NO'].groupby(dia.loc[dia['readmitted']!='NO','discharge_disposition_id']).size().sort_index()
temp11_b = dia.groupby(dia['discharge_disposition_id']).size().sort_index()
q11 = (temp11_a/temp11_b*100).dropna().sort_values(ascending=False).head(5)  # Series of discharge codes and readmission percentages

## 12. The columns from 'metformin' to 'citoglipton' are all medications, 
##     with "Up", "Down", and "Steady" indicating the patient is taking that 
##     medication.  For each of these medications, determine the average
##     number of medications from this group that patients are taking.
##     Give a Series of all medications with an average of at least 1.5,
##     with the medications as index and averages as values, sorted 
##     largest to smallest average.
##     (Hint: df.columns gives the column names of the data frame df.)

# filter and transform the values amongst the mediations into T/F
# then sum number of medications each record is taking 
# for each column(medication), find out the mean number of meds and store them in a pandas series 
# eventually filter out mean < 1.5 and drop na values to make sure there isn't mismatch, and sort in descending order 
temp12 = dia.loc[:,'metformin':'citoglipton'] != 'No'
dia['sum'] = temp12.sum(axis=1)


aggregated = pd.Series(dtype=float)
for med in temp12.columns:
    avg = (dia[temp12.loc[:,med]]['sum']).mean()
    aggregated = aggregated.append(pd.Series(avg,index=[med]))

q12 = aggregated[aggregated>=1.5].dropna().sort_values(ascending=False)  # Series of medications and averages







