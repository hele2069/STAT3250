##
## File: assignment09.py (STAT 3250)
## Topic: Assignment 9 
##

##  This assignment requires the data file 'airline-stats.txt'.  This file 
##  contains thousands of records of aggregated flight information, organized 
##  by airline, airport, and month.  The first record is shown below.  
##
##  The file is quite large (1.8M lines, 31MB) so may be difficult to open in
##  Spyder.  An abbreviated version 'airline-stats-brief.txt' is also 
##  provided that has the same structure as the original data set but is
##  easier to open in Spyder.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the airline-stats.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

# =============================================================================
# airport
#     code: ATL 
#     name: Atlanta GA: Hartsfield-Jackson Atlanta International
# flights 
#     cancelled: 5 
#     on time: 561 
#     total: 752 
#     delayed: 186 
#     diverted: 0
# number of delays 
#     late aircraft: 18 
#     weather: 28 
#     security: 2
#     national aviation system: 105 
#     carrier: 34
# minutes delayed 
#     late aircraft: 1269 
#     weather: 1722 
#     carrier: 1367 
#     security: 139 
#     total: 8314 
#     national aviation system: 3817
# dates
#     label: 2003/6 
#     year: 2003 
#     month: 6
# carrier
#     code: AA 
#     name: American Airlines Inc.
# =============================================================================

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the test data as text one line at a time
airlines = open('airline-stats.txt').read().splitlines()
airlines = pd.Series(airlines)

## 1.  Give the total number of hours delayed for all flights in all records,
##     based on the entries in (minutes delayed)/total

# find 2 kinds of totals, resulting in a pattern for every 2 rows 
# subset the data by starting from the first 'total' delay minutes, and only include every 2 rows afterwards, which gives us all total delay minutes 
# type-cast to int, find the sum, and divide by 60 to convert to hours 
temp1 = airlines[airlines.str.contains('total')][1::2].str.split(':').str[1].astype(int)
q1 = sum(temp1)/60  # total number of hours delayed for all flights in all records

## 2.  Which airlines appear in at least 500 records?  Give a Series with airline
##     names as index and record counts for values, in order of record count 
##     from largest to smallest.

# there are two 'name' in the dataset, so we pick those out
# start from the second 'name', which is the airline name, and only include every 2 rows afterwards 
# group by airline name and find count
# include count >=500 and sort by count in descending order 
temp2 = airlines[airlines.str.contains('name:')][1::2].str.split(':').str[1]
q2 = temp2.groupby(temp2).count()  # Series of airline names and record counts
q2 = q2[q2>=500].sort_values(ascending=False)

## 3.  The entry under 'flights/delayed' is not always the same as the total
##     of the entries under 'number of delays'.  (The reason for this is not
##     clear.)  Determine the percentage of records for which these two
##     values are different.

# flights/delayed, strippped of string characters and convert to int 
# include only entries under 'number of delays' 
# each category has the same pattern where the rows are every 10 rows starting from the first entry of each category 
# each category being stripped of string characters and converte to int 
# perform aggregation on all 5 categories, can compare each row to the original total 
# find out how many rows are not equal, and divide that by the total number of records 
total = pd.DataFrame()
total['original_total'] = airlines[airlines.str.contains('delayed:')].str.split(':').str[1].astype(int)

# need to do this because we need each delay type to have the same index values in order to perform stuff like adding 
temp3 = airlines[airlines.str.contains('late aircraft:|weather:|security:|national aviation system:|carrier:')]
agg1 = temp3[::10].str.split(':').str[1].astype(int) 
agg1.index = total.index
agg2 = temp3[1::10].str.split(':').str[1].astype(int)
agg2.index = total.index
agg3 = temp3[2::10].str.split(':').str[1].astype(int)
agg3.index = total.index
agg4 = temp3[3::10].str.split(':').str[1].astype(int)
agg4.index = total.index
agg5 = temp3[4::10].str.split(':').str[1].astype(int)
agg5.index = total.index

total['aggregated_total'] = agg1 + agg2 + agg3 + agg4 + agg5

q3 = sum(total['original_total'] != total['aggregated_total'])/len(total) * 100 # percentage of records with two values different

## 4.  Determine the percentage of records for which the number of delays due to
##     'late aircraft' exceeds the number of delays due to 'carrier'.

# same logic as problem#3, using slicing to skip every n rows to get either 'later aircraft' or 'carrier'
# and have these 2 columns share the same indices 
# then find the percentage 
temp4 = pd.DataFrame()
temp4['late_aircraft'] = airlines[airlines.str.contains('late aircraft:')][0::2].str.split(':').str[1].astype(int)
carrier_temp = airlines[airlines.str.contains('carrier:')][0::2].str.split(':').str[1].astype(int)
carrier_temp.index = temp4.index 
temp4['carrier'] = carrier_temp

q4 = sum(temp4['late_aircraft']>temp4['carrier'])/len(temp4)*100 # percentage of records as described above

## 5.  Find the top-8 airports in terms of the total number of minutes delayed.
##     Give a Series with the airport names (not codes) as index and the total 
##     minutes delayed as values, sorted order from largest to smallest total.
##     (Include any ties for 8th position as usual)

# similar logic. subset the rows containing 'total:' and skip every 2 rows to get the total number of minutes delayed 
# strip string and type-cast to get the actual int values 
# set index to airport names using the similar data-processing logic, we can simply set them without worry about the ordering becasue they retain the original relative order 
# group by airport and find total number of minutes delayed, then sort and keep 8 largest with ties 
temp5 = airlines[airlines.str.contains('total')][1::2].str.split(':').str[1].astype(int)
temp5.index = airlines[airlines.str.contains('name:')][::2].str.split(':').str[2]
q5 = temp5.groupby(temp5.index).sum().nlargest(8, keep='all')  # Series of airport names and total minutes delayed

## 6.  Find the top-12 airports in terms of rates (as percentages) of on-time flights.
##     Give a Series of the airport names (not codes) as index and percentages
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 12th position as usual)

# similar logic in data-processing to retrive 'on time', 'total', and 'name'
# set index to airport names 
# group the on time number of flights & total number of flights by airport name, then find sum 
# find the percentage and then keep top12 percentages with ties 
temp6a = airlines[airlines.str.contains('on time:')].str.split(':').str[1].astype(int)
temp6b = airlines[airlines.str.contains('total')][0::2].str.split(':').str[1].astype(int)
index_6 = airlines[airlines.str.contains('name:')][::2].str.split(':').str[2]

temp6a.index = index_6
temp6b.index = index_6

q6 = (temp6a.groupby(temp6a.index).sum()/temp6b.groupby(temp6b.index).sum()*100).nlargest(12, keep='all') # Series of airport names and percentages 

## 7.  Find the top-10 airlines in terms of rates (as percentages) of on time flights.
##     Give a Series of the airline names (not codes) as index and percentages  
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 10th position as usual)

# similar logic in data-processing to retrive 'on time', 'total', and 'name'
# set index to airline names 
# group the on time number of flights & total number of flights by airline name, then find sum 
# find the percentage and then keep top10 percentages with ties 
temp7a = airlines[airlines.str.contains('on time:')].str.split(':').str[1].astype(int)
temp7b = airlines[airlines.str.contains('total')][0::2].str.split(':').str[1].astype(int)
index_7 = airlines[airlines.str.contains('name:')][1::2].str.split(':').str[1]

temp7a.index = index_7
temp7b.index = index_7

q7 = (temp7a.groupby(temp7a.index).sum()/temp7b.groupby(temp7b.index).sum()*100).nlargest(10, keep='all')  # Series of airline names and percentages

## 8.  Determine the average length (in minutes) by airline of a delay due
##     to the national aviation system.  Give a Series of airline name (not 
##     code) as index and average delay lengths as values, sorted from largest 
##     to smallest average delay length.

# similar logic in data-processing to retrive the 'national aviation system' in delay minutes/flights and airline names
# assign index to airline names 
# group by index, find the total delay minutes and number of flights
# then find the proportion using minutes/flights, which is the avg length of delay
# finally sort in descending order 
temp8 = airlines[airlines.str.contains('national aviation system:')].str.split(':').str[1].astype(int)
temp8a = temp8[1::2] # minutes delayed 
temp8b = temp8[0::2] # number of flights delayed 

index_8 = airlines[airlines.str.contains('name:')][1::2].str.split(':').str[1] # I'm repeating this procedure for the reviewer to understand better
temp8a.index = index_8
temp8b.index = index_8

q8 = (temp8a.groupby(temp8a.index).sum()/temp8b.groupby(temp8b.index).sum()).sort_values(ascending=False)  # Series of airline names and average delay times

## 9.  For each month, determine the rates (as percentages) of flights delayed 
##     by weather. Give a Series sorted by month (1, 2, ..., 12) with the 
##     corresponding percentages as values.

# same logic as problem#8, with variables and indecies changed 
temp9a = airlines[airlines.str.contains('weather:')][0::2].str.split(':').str[1].astype(int)
temp9b = airlines[airlines.str.contains('total')][0::2].str.split(':').str[1].astype(int)
index_9 = airlines[airlines.str.contains('month:')].str.split(':').str[1].astype(int)

temp9a.index = index_9
temp9b.index = index_9

q9 = (temp9a.groupby(temp9a.index).sum()/temp9b.groupby(temp9b.index).sum()*100).sort_index()  # Series of months and percentages

## 10. Find all airports where the average length (in minutes) of 
##     security-related flight delays exceeds 35 minutes.  Give a Series with  
##     airport names (not codes) as index and average delay times as values, 
##     sorted from largest to smallest average delay.

# same logic as problem#8, with variabels and indecies changed 
# also a condition on >35 in the final subset before sorting 
temp10 = airlines[airlines.str.contains('security:')].str.split(':').str[1].astype(int)
delay_minutes = temp10[1::2]
delay_flights = temp10[0::2]

index_10 = airlines[airlines.str.contains('name:')][0::2].str.split(':').str[2] # I'm repeating this procedure for the reviewer to understand better
delay_minutes.index = index_10
delay_flights.index = index_10 

security_avg_delay = delay_minutes.groupby(delay_minutes.index).sum()/delay_flights.groupby(delay_flights.index).sum()
q10 = security_avg_delay[security_avg_delay>35].sort_values(ascending=False) # Series or airport names and average delay times

## 11. For each year, determine the airport that had the highest rate (as a 
##     percentage) of delays.  Give a Series with the years (least recent at top)  
##     and airport names (not code) as MultiIndex and the percentages as values.

# using dataframe instead of series for ease of coding (b/c we group by 2 columns)
# multi-index is hard to do since we have 2 separate series, and by combining them into data types like a list of lists is unnecessary 
# we can simply group by 2 columns of a dataframe, which automatically turns into a multi-index 
# add year, airport, number of delayed flights, and total number of flights, accordingly into the dataframe 
# first group delay by year and airport, find the sum, and divide it by sum(total) grouped by year and airport 
# then do another groupby to only include the airport associated with the highest delay rate each year 
# sort by year in ascending order

temp11 = pd.DataFrame()
temp11['year'] = airlines[airlines.str.contains('year:')].str.split(':').str[1].astype(int)

airport = airlines[airlines.str.contains('name:')][::2].str.split(':').str[2]
airport.index = temp11.index
temp11['airport'] = airport

delays = airlines[airlines.str.contains('delayed:')].str.split(':').str[1].astype(int)
delays.index = temp11.index 
temp11['delay'] = delays 

total_flights = airlines[airlines.str.contains('total:')][::2].str.split(':').str[1].astype(int)
total_flights.index = temp11.index 
temp11['total'] = total_flights 

q11 = (temp11['delay'].groupby([temp11['year'],temp11['airport']]).sum()/temp11['total'].groupby([temp11['year'],temp11['airport']]).sum())*100
q11 = q11.groupby(q11.index.names[0], group_keys=False).nlargest(1).sort_index(level=0)  # Series of years/airport names and percentages

## 12. For each airline, determine the airport where that airline had its 
##     greatest percentage of delayed flights.  Give a Series with airline
##     names (not code) and airport names (not code) as MultiIndex and the
##     percentage of delayed flights as values, sorted from smallest to
##     largest percentage.

# same logic as problem#11, only with different groupby conditions (airline, airport instead of year, airport)
# sort by percentage
temp12 = pd.DataFrame()
temp12['airline'] = airlines[airlines.str.contains('name:')][1::2].str[10:]

airport_12 = airlines[airlines.str.contains('name:')][::2].str.split(':').str[2]
airport_12.index = temp12.index
temp12['airport'] = airport_12

delays_12 = airlines[airlines.str.contains('delayed:')].str.split(':').str[1].astype(int)
delays_12.index = temp12.index 
temp12['delay'] = delays_12 

total_flights_12 = airlines[airlines.str.contains('total:')][::2].str.split(':').str[1].astype(int)
total_flights_12.index = temp12.index 
temp12['total'] = total_flights_12 

q12 = (temp12['delay'].groupby([temp12['airline'],temp12['airport']]).sum()/temp12['total'].groupby([temp12['airline'],temp12['airport']]).sum())*100
q12 = q12.groupby(q12.index.names[0], group_keys=False).nlargest(1).sort_values() # Series of airline/airport and percentages












