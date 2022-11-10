##
## File: assignment13.py (STAT 3250)
## Topic: Assignment 13 
##


##  These questions are similar to reviewed lecture material, but 
##  provide some experience with Dask.

import dask.dataframe as dd #import libraries
import numpy as np
from datetime import datetime 

dtypes = {
 'Date First Observed': str, 'Days Parking In Effect    ': str,
 'Double Parking Violation': str, 'Feet From Curb': np.float32,
 'From Hours In Effect': str, 'House Number': str,
 'Hydrant Violation': str, 'Intersecting Street': str,
 'Issue Date': str, 'Issuer Code': np.float32,
 'Issuer Command': str, 'Issuer Precinct': np.float32,
 'Issuer Squad': str, 'Issuing Agency': str,
 'Law Section': np.float32, 'Meter Number': str,
 'No Standing or Stopping Violation': str,
 'Plate ID': str, 'Plate Type': str,
 'Registration State': str, 'Street Code1': np.uint32,
 'Street Code2': np.uint32, 'Street Code3': np.uint32,
 'Street Name': str, 'Sub Division': str,
 'Summons Number': np.uint32, 'Time First Observed': str,
 'To Hours In Effect': str, 'Unregistered Vehicle?': str,
 'Vehicle Body Type': str, 'Vehicle Color': str,
 'Vehicle Expiration Date': str, 'Vehicle Make': str,
 'Vehicle Year': np.float32, 'Violation Code': np.uint16,
 'Violation County': str, 'Violation Description': str,
 'Violation In Front Of Or Opposite': str, 'Violation Legal Code': str,
 'Violation Location': str, 'Violation Post Code': str,
 'Violation Precinct': np.float32, 'Violation Time': str
}

nyc = dd.read_csv('nyc-parking-tickets2015.csv', dtype=dtypes, usecols=dtypes.keys())

## 1.  There are several missing values in the 'Vehicle Body Type' column. Impute 
##     missing values of 'Vehicle Body Type' with the mode. What is the mode?

# find value count (accounts for missing value)
# sort in descending order and then locate index 0 to get the mode, set mode to q1
# then fill the missing values by what we found in q1 
count_vehicle_body_type = nyc['Vehicle Body Type'].value_counts().compute()
q1 = count_vehicle_body_type.sort_values(ascending=False).index[0] # Report the mode, the most common Vehicle Body Type.
nyc = nyc.fillna({'Vehicle Body Type': q1}) 

## 2.  How many missing data points are there in the 'Intersecting Street' column?

# use isnull() to turn the column into 1s and 0s and find sum 
q2 = nyc['Intersecting Street'].isnull().sum().compute() # Number of missing data points

## 3.  What percentage of vehicle makes are Jeeps during the months of March - 
##     September (inclusive) of 2015?

# convert date to our desired format (month/day/year)
# replace the original column by our parsed data 
# filter data based on our desired time range, and locate rows with make == jeep
# divide number of records with jeep by total records and times 100
date_converted = nyc['Issue Date'].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"), meta=datetime)
nyc = nyc.drop('Issue Date', axis=1)
nyc = nyc.assign(IssueDate=date_converted)
nyc = nyc.rename(columns={'IssueDate':'Issue Date'})

date_filter = (nyc['Issue Date'] >= '2015-03-01') & (nyc['Issue Date'] <= '2015-09-30')
temp3 = nyc[date_filter]
Jeeps = temp3[temp3['Vehicle Make']=='JEEP']

q3 = (100*(Jeeps.index.size/temp3.index.size)).compute() # Percentage of Jeeps

## 4.  What's the most common color of a car in 2015? Maintain the color in all caps.

# include only records in 2015
# check the mode using value_counts in vehicle color column
# extract the string, and turn into upper case 
date_filter4 = (nyc['Issue Date'] >= '2015-01-01') & (nyc['Issue Date'] <= '2015-12-31')
temp4 = nyc[date_filter4]
group4 = temp4['Vehicle Color'].value_counts().compute()
q4 = group4.sort_values(ascending=False).index[0].upper() # Most common car color

## 5.  Find all the cars in any year that are the same color as q4. What percentage of 
##     those care are sedans?

# extract records with the same color
# store sedan records
# find percentage 
temp5 = nyc[nyc['Vehicle Color']==q4]
sedans = temp5[temp5['Vehicle Body Type']=='SDN']
q5 = (100*(sedans.index.size/temp5.index.size)).compute() # Percentage of sedans

## 6.  Make a table of the top 5 registration states, sorted greatest to least.

# value_count the states and sort in descending order 
# keep top 5 records 
temp6 = nyc['Registration State'].value_counts().compute()
q6 = temp6.sort_values(ascending=False)[0:5] # Series of top 5 registration states

## 7.  Perhaps someone bought a new vehicle and kept the same license plate. How many license 
##     plates have more than one 'Vehicle Make' associated with the respective plate?

# drop duplicates first 
# then group by plate id and find how many makes each id has 
# find how many ids have 2 or more makes 
temp7 = nyc.drop_duplicates(subset=['Vehicle Make', 'Plate ID'],keep='last').reset_index(drop=True)
group7 = temp7['Vehicle Make'].groupby(temp7['Plate ID']).count().compute()
q7 = len(group7[group7>=2]) # Number of license plates

## 8.  Determine the top three hours that result in the most parking violations. 
##     "0011A" would be 12:11 AM and "0318P" would be 3:18 PM. Report the solution 
##     with the index in the format of "01A" and the count.

# append the first 2 characters and the last character in 'violation time' 
# replace the original violation time by the new one 
# find this new column's value counts 
# sort in descending order and keep the tio 3
temp8 = nyc['Violation Time'].str[:2] + nyc['Violation Time'].str[4:]
nyc = nyc.drop('Violation Time', axis=1)
nyc = nyc.assign(ViolationTime=temp8)
nyc = nyc.rename(columns={'ViolationTime':'Violation Time'})

q8 = nyc['Violation Time'].value_counts().compute().nlargest(3) # Series with top three hours

## 9.  Among the tickets issued by Precinct 99, what is the average distance from the
##     curb in feet?

# include only records with precinct == 99
# find mean distance from curb 
temp9 = nyc[nyc['Issuer Precinct']==99]
q9 = temp9['Feet From Curb'].mean().compute() # Average distance from the curb







