##
## File: assignment11.py (STAT 3250)
## Topic: Assignment 11 
##

##  The file Stocks.zip is a zip file containing nearly 100 sets of price 
##  records for various stocks.  A sample of the type of files contained
##  in Stocks.zip is ABT.csv, which we have seen previously and is posted
##  in recent course materials. Each file includes daily data for a specific
##  stock, with stock ticker symbol given in the file name. Each line of
##  a file includes the following:
##
##   Date = date for recorded information
##   Open = opening stock price 
##   High = high stock price 
##   Low = low stock price 
##   Close = closing stock price 
##   Volume = number of shares traded
##   Adj Close = closing price adjusted for stock splits (ignored for this assignment)

##   The time interval covered varies from stock to stock. For many files
##   there are dates when the market was open but the data is not provided, so
##   those records are missing. Note that some dates are not present because the 
##   market is closed on weekends and holidays.  Those are not missing records.  

##  The Gradescope autograder will be evaluating your code on a subset 
##  of the set of files in the folder Stocks.  Your code needs to automatically 
##  handle all assignments to the variables q1, q2, ... to accommodate the 
##  reduced set, so do not copy/paste things from the console window, and
##  take care with hard-coding values. 

##  The autograder will contain a folder Stocks containing the stock data sets.
##  This folder will be in the working directory so your code should be written
##  assuming that is the case.


import pandas as pd # load pandas
import numpy as np # load numpy
import glob # 'glob' searches for files

pd.set_option('display.max_columns', 10) # Display 10 columns in console

# read files as df and change index to stock ticker sybols along the way 
filelist = glob.glob('Stocks/*.csv') # 'glob.glob' is the directory search
df = pd.DataFrame()  # empty dataframe
for file in filelist:
    newdf = pd.read_csv(file)  # read in the file
    index = [file[7:-4]]*len(newdf)
    newdf = newdf.set_index([index])
    df = pd.concat([df,newdf], sort=False)  # concatenate to existing dataframe
    
## 1.  Find the mean for the Open, High, Low, and Close entries for all 
##     records for all stocks.  Give your results as a Series with index
##     Open, High, Low, Close (in that order) and the corresponding means
##     as values.

# apply mean function to each column (columns 1-5 which are open, high, low, and close)
q1 = df.iloc[:,1:5].apply(np.mean) # Series of means of Open, High, Low, and Close

## 2.  Find all stocks with an average Close price less than 30.  Give your
##     results as a Series with ticker symbol as index and average Close price. 
##     price as value.  Sort the Series from lowest to highest average Close
##     price.  (Note: 'MSFT' is the ticker symbol for Microsoft.  'MSFT.csv',
##     'Stocks/MSFT.csv' and 'MSFT ' are not ticker symbols.)

# group 'close' by index (ticker) and find mean 
# include only those with mean < 30 and sort mean in ascending order 
temp2 = df['Close'].groupby(df.index).mean()
q2 = temp2[temp2<30].sort_values()  # Series of stocks with average close less than 30

## 3.  Find the top-10 stocks in terms of the day-to-day volatility of the
##     price, which we define to be the mean of the daily differences 
##     High - Low for each stock. Give your results as a Series with the
##     ticker symbol as index and average day-to-day volatility as value. 
##     Sort the Series from highest to lowest average volatility.

# group diff between high and low by index(ticker) and find mean
# include only top 10 
temp3 = df['High'] - df['Low']
q3 = temp3.groupby(temp3.index).mean().nlargest(10)  # Series of top-10 mean volatility

## 4.  Repeat the previous problem, this time using the relative volatility, 
##     which we define to be the mean of
## 
##                       (High − Low)/(0.5(Open + Close))
##
##     for each day. Provide your results as a Series with the same specifications
##     as in the previous problem.

# same as #3, except using a different formula 
temp4 = (df['High'] - df['Low'])/(0.5*(df['Open'] + df['Close']))
q4 = temp4.groupby(temp4.index).mean().nlargest(10)  # Series of top-10 mean relative volatility

## 5.  For each day the market was open in October 2008, find the average 
##     daily Open, High, Low, Close, and Volume for all stocks that have
##     records for October 2008.  (Note: The market is open on a given
##     date if there is a record for that date in any of the files.)
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close, Volume (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2008-10-01, the same form as in the files.   

# math date with '2008-10' for october 2008
# then group by date and find mean of all 5 required columns 
# sort by index in ascending order 
temp5 = df[df['Date'].str.contains('2008-10')].iloc[:,:-1]
q5 = temp5.groupby(temp5['Date']).mean().sort_index()  # DataFrame of means for each open day of Oct '08.

## 6. For 2011, find the date with the maximum average relative volatility 
##    for all stocks and the date with the minimum average relative 
##    volatility for all stocks. Give your results as a Series with 
##    the dates as index and corresponding average relative volatility
##    as values, with the maximum first and the minimum second.

# match date with '2011-' which indicates records in 2011
# find the relative volatility 
# then group the relative volatility by date and find mean 
# extract both max and min of mean entries into q6
temp6 = df[df['Date'].str.contains('2011-')]
temp6['rel_vol'] = (temp6['High'] - temp6['Low'])/(0.5*(temp6['Open'] + temp6['Close']))
group6 = temp6['rel_vol'].groupby(temp6['Date']).mean()

q6 = group6[group6 == max(group6)] # Series of average relative volatilities
q6 = q6.append(group6[group6 == min(group6)])

## 7. For 2010-2012, find the average relative volatility for all stocks on
##    Monday, Tuesday, ..., Friday.  Give your results as a Series with index
##    'Mon','Tue','Wed','Thu','Fri' (in that order) and corresponding
##    average relative volatility as values. 

# extract year for our slicing conditions 
# then get weekday names and format them like 'mon' 'tue', etc, and store them into a new column
# also have a custom_sort column since we cannot sort weekday names properly 
# then groupby relative volatility on weekday and custom_sort (so we get a multiindex, with the 2nd level for sorting)
# find mean based on groupby 
# sort index using level 1 (which is the day# of week)
# after sort, drop that level so we are left with only abbreviated weekday names as index 
temp7 = df[pd.to_datetime(df['Date']).dt.year.isin([2010,2011,2012])]
temp7['Weekday'] = pd.to_datetime(temp7['Date']).dt.day_name().str[0:3]
temp7['Custom_sort'] = pd.to_datetime(temp7['Date']).dt.weekday
temp7['rel_vol'] = (temp7['High'] - temp7['Low'])/(0.5*(temp7['Open'] + temp7['Close']))
q7 = temp7['rel_vol'].groupby([temp7['Weekday'],temp7['Custom_sort']]).mean().sort_index(level=1).droplevel(level=1) # Series of average relative volatility by day of week

## 8.  For each month of 2009, determine which stock had the maximum average 
##     relative volatility. Give your results as a Series with MultiIndex
##     that includes the month (month number is fine) and corresponding stock 
##     ticker symbol (in that order), and the average relative volatility
##     as values.  Sort the Series by month number 1, 2, ..., 12.

# match 'date' with '2009-' which indicates records in 2009
# then extract month and store them into a new column
# store relative volatility as well
# then group by month and index (stock ticker) and find mean relative volatility 
# group by again by month and find max mean relative volatility 
# sort by month 
temp8 = df[df['Date'].str.contains('2009-')]
temp8['Month'] = pd.to_datetime(temp8['Date']).dt.month
temp8['rel_vol'] = (temp8['High'] - temp8['Low'])/(0.5*(temp8['Open'] + temp8['Close']))
group8 = temp8['rel_vol'].groupby([temp8['Month'],temp8.index]).mean().sort_index(level=0)
q8 = group8.groupby(group8.index.names[0], group_keys=False).nlargest(1).sort_index(level=0)  # Series of maximum relative volatilities by month

## 9.  The “Python Index” is designed to capture the collective movement of 
##     all of our stocks. For each date, this is defined as the average price 
##     for all stocks for which we have data on that day, weighted by the 
##     volume of shares traded for each stock.  That is, for stock values 
##     S_1, S_2, ... with corresponding volumes V_1, V_2, ..., the average
##     weighted volume is
##
##           (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
##
##     Find the Open, High, Low, and Close for the Python Index for each date
##     the market was open in January 2013. 
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2013-01-31, the same form as in the files.   

# match 'date' with '2013-01' which indicates records in jan 2013
# use lambda function to calculate the above equation when grouped by date 
# repeat groupby for Open, High, Low, and Close, and add them as columns in our group9 variable 
# finally sort by index (date)
temp9 = df[df['Date'].str.contains('2013-01')]
group9 = pd.DataFrame()

for i in ['Open', 'High', 'Low', 'Close']:
    group9[i] = temp9.groupby(temp9['Date']).apply(lambda temp9,a,b: sum(temp9[a]*temp9[b])/sum(temp9[a]),'Volume', i)

q9 = group9.sort_index()  # DataFrame of Python Index values for each open day of Jan 2013. 

## 10. For the years 2007-2012 determine the top-8 month-year pairs in terms 
##     of average relative volatility of the Python Index. Give your results
##     as a Series with MultiIndex that includes the month (month number is 
##     fine) and year (in that order), and the average relative volatility
##     as values.  Sort the Series by average relative volatility from
##     largest to smallest.

# extract year portion of 'date' to match our slicing conditions 
# find Python Index the same way as Q9
# find relative volatility using equation mentioned preivous, using the Python Index values 
# set column 'date' as the index values for group by 
# group relative volatility by month and then year and find the average 
# sort by mean relative volatility in descending order 
temp10 = df[pd.to_datetime(df['Date']).dt.year.isin([2007,2008,2009,2010,2011,2012])]
group10 = pd.DataFrame()

for i in ['Open', 'High', 'Low', 'Close']:
    group10[i] = temp10.groupby(temp10['Date']).apply(lambda temp10,a,b: sum(temp10[a]*temp10[b])/sum(temp10[a]),'Volume', i)

group10['rel_vol'] = (group10['High'] - group10['Low'])/(0.5*(group10['Open'] + group10['Close']))
group10['Date'] = group10.index

q10 = group10['rel_vol'].groupby([pd.to_datetime(group10['Date']).dt.month,pd.to_datetime(group10['Date']).dt.year]).mean().nlargest(8)  # Series of month-year pairs and average rel. volatilities

## 11. Each stock in the data set contains records starting at some date and 
##     ending at another date.  In between the start and end dates there may be 
##     dates when the market was open but there is no record -- these are the
##     missing records for the stock.  For each stock, determine the percentage
##     of records that are missing out of the total records that would be
##     present if no records were missing. Give a Series of those stocks
##     with less than 1.3% of records missing, with the stock ticker as index 
##     and the corresponding percentage as values, sorted from lowest to 
##     highest percentage.

# store unique dates, which indicates potential missing records for some stocks on some dates 
# group df['date'] by indx (ticker) and find min, max, and total number of records 
# then create a 'full' column, which finds how many total records are supposed to be present for each stock 
# reset index for forloop in parsing rows (while creating a column identifying our tickers)
# for each row (stock), check how many total records are supposed to be included between the starting and end dates 
# find the percentage of missing records for each stock 
# reset index to tickers 
# filter out stocks with missing rate >= 1.3 and sort by missing rate in ascending order 
full_dates = pd.Series(df['Date'].unique())
group11 = df['Date'].groupby(df.index).agg(['min', 'max', 'count'])
group11['full'] = None
group11 = group11.reset_index()

for i in range(len(group11)):
    group11.iloc[i,4] = sum(full_dates.between(group11.iloc[i,1], group11.iloc[i,2]))

temp11 = pd.Series((group11['full'] - group11['count'])/group11['full']*100)
temp11.index = group11['index']

q11 = temp11[temp11<1.3].sort_values()  # Series of stocks and percent missing
