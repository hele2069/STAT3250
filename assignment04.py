##
## File: assignment04.py (STAT 3250)
## Topic: Assignment 4
##

##  This assignment requires the data file 'airline_tweets.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.

##  Gradescope will review your code using a version of airline_tweets.csv
##  that has had about 50% of the records removed.  You will need to write
##  your code in such a way that your file will automatically produce the
##  correct answers on the new set of data.  

import pandas as pd # load pandas as pd
import numpy as np  # load numpy as np

air = pd.read_csv('airline_tweets.csv')  # Read in the data set
temp = air.loc[0:10,:]
## Questions 1-8: These questions should be done without the use of loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##      name in the 'airline' column of the data set.  Give the airline 
##      name and corresponding number of tweets as a Series with airline
##      name as the index, sorted by tweet count from most to least.

air.columns
# first group the data set by airline, 
# then use .size() to find out row counts based on groups, 
# and lastly rank by decreasing order. 
q1 = air.groupby(air['airline']).size().sort_values(ascending=False)  # Series of airlines and number of tweets

air['airline_sentiment'].unique()

## 2.  For each airline's tweets, determine the percentage that are positive,
##      based on the classification in 'airline_sentiment'.  Give the airline 
##      name and corresponding percentage as a Series with airline
##      name as the index, sorted by percentage from largest to smallest

# first create a temp variable for storing positive tweet counts per airline. 
# then use another groupby for overall tweet counts per airline, and find out their percentage. 
# both groupby will be sorted by index before hand for safety (in case AA positive count/UA overall count)
# finally sort them in decreasing order 
temp = air.loc[air['airline_sentiment']=='positive','airline_sentiment'].groupby(air['airline']).size().sort_index()
q2 = (temp/air.groupby(air['airline']).size().sort_index()).sort_values(ascending=False)*100  # Series of airlines and percentage of positive tweets

## 3.  Find all user names (in the 'name' column) with at least 25 tweets
##      along with the number of tweets for each.  Give the user names and
##      corresponding counts as a Series with user name as index, sorted
##      by count from largest to smallest

# first group data by name column, then find out number of tweets per username by using size()
# then filter out username with < 25 tweets, and sort them in decreasing order 
temp2 = air.groupby(air['name']).size()
q3 = temp2[temp2>=25].sort_values(ascending=False)  # Series of users with at least 25 tweets

## 4.  Determine the percentage of tweets from users who have more than five
##      tweets in this data set. (Note that this is not the same as the
##      percentage of users with more than five tweets.)

# first find out each username's tweet count, then filter out those with <= 5 tweets, and find the sum of these tweets. 
# finally, find the percentage by dividing the overall number of rows and * 100
temp3 = air.groupby(air['name']).size()
q4 = temp3[temp3>5].sum()/len(air)*100  # Percentage of tweets from users with more than 5 tweets                            
                               
## 5.  Among the negative tweets, determine the four reasons are the most common.
##      Give the percentage among all negative tweets for each as a Series 
##      with reason as index, sorted by percentage from most to least

# create a temp variable that includes only negative posts 
# then find out how many posts within each group (reasons), sort it in descending order, and keep only top 4 reasons 
# divid overall number of negative tweets and *100 to find percentage 
temp4 = air[air['airline_sentiment']=='negative']
q5 = temp4.groupby(air['negativereason']).size().sort_values(ascending=False).head(4)/len(temp4)*100
  # Series of reasons and percentages


## 6.  How many tweets include a link to a web site? (Indicated by the 
##      presence of "http" anywhere in the tweet.)

# include those that have 'http' in their text, and count them by len()
q6 = len(air[air['text'].str.contains('http')])  # Number of tweets that include a link


## 7.  How many tweets include the word "air" (upper or lower case,
##      not part of another word)?

# first subset to text column
# then use regular expression to make all texts lowercase and replace symbols with spaces to better detect the word 'air'
# eventually subset to those rows that contain 'air' as a word, and use len() to count how many rows are there 
temp5 = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ')
q7 = len(temp5[temp5.str.contains(' air ')])  # Number of tweets that include 'air'


## 8.  How many times total does the word "help" appear in a tweet, either in
##      upper or lower case and not part of another word.

# first subset to text column
# then use regular expression to make all texts lowercase and replace symbols with spaces to better detect the word 'help'
# eventually count how many times 'help' appear in each tweet, and sum them 
temp6 = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ')
q8 = sum(temp6.str.count(' help '))  # Number of times that 'help' is included


## Questions 9-13: Some of these questions can be done without the use of 
##  loops, while others cannot.  It is preferable to minimize the use of
##  loops where possible, so grading will reflect this.
##
##  Some of these questions involve hashtags and @'s.  These are special 
##  Twitter objects subject to special rules.  For these problems we assume
##  that a "legal" hashtag:
##
##  (a) Starts with the "#" (pound) symbol, followed by letter and/or numbers 
##       until either a space or punctuation mark (other than "#") is encountered.
##   
##      Example: "#It'sTheBest" produces the hashtag "#It"
##
##  (b) The "#" symbol can be immediately preceded by punctuation, which is 
##       ignored. If "#" is immediately preceded by a letter or number then
##       it is not a hashtag.
##
##      Examples: "The,#dog,is brown"  produces the hashtag "#dog"
##                "The#dog,is brown" does not produce a hashtag
##                "#dog1,#dog2" produces hashtags "#dog1" and "#dog2"
##                "#dog1#dog2" produces the hashtag "#dog1#dog2"
##
##  (c) Hashtags do not care about case, so "#DOG" is the same as "#dog"
##       which is the same as "#Dog".
##
##  (d) The symbol "#" by itself is not a hashtag
##
##  The same rules apply to Twitter handles (user names) that begin with the
##   "@" symbol.         

## 9.  How many of the tweets have at least two Twitter handles?

# first use regular expression to format the rows. After that, each handle can be identified with a space and a @ after it. 
# then, include only those tweets with >= 2 handles, and find how many using len()
temp7 = air['text']
temp7 = temp7.str.replace(r'[^\w\s@]+', ' ')
temp7 = (' ' + temp7.str.replace(r'\s@\s', ' ') + ' ').str.count(' @')  
q9 = len(temp7[temp7>=2])   # number of tweets with @ directed at a user besides the target airline

## 10. Suppose that a score of 3 is assigned to each positive tweet, 1 to
##      each neutral tweet, and -2 to each negative tweet.  Determine the
##      mean score for each airline and give the results as a Series with
##      airline name as the index, sorted by mean score from highest to lowest.

# first subset a temp variable containing only airline and sentiment columns; then create a new column 'score', which is used to fill in according scores based on sentiment in each row
# after that, group temp by airline and find the mean score associated with each airline, and sort in descending order 
temp8 = air.loc[:,['airline','airline_sentiment']]
temp8['score'] = ''
temp8.loc[air['airline_sentiment']=='positive','score'] = 3
temp8.loc[air['airline_sentiment']=='negative','score'] = -2
temp8.loc[air['airline_sentiment']=='neutral','score'] = 1 

q10 = temp8['score'].groupby(temp8['airline']).mean().sort_values(ascending=False) # Series of airlines and mean scores 

## 11. What is the total number of hashtags in tweets associated with each
##      airline?  Give a Series with the airline name as index and the
##      corresponding totals for each, sorted from most to least.

# first use regular expression to format the rows. After that, each hashtag can be identified with a space and a # after it. 
# then, count how many hashtags per tweet, group by airlines, and find out the sum of hashtags per airline 
temp9 = air[['airline','text']]
temp9['text'] = (' ' + temp9['text'] + ' ').str.replace(r'[^\w\s#]+', ' ')
temp9['text'] = temp9['text'].str.replace(r'\s#\s', ' ').str.count(' #')
q11 = temp9['text'].groupby(temp9['airline']).sum().sort_values(ascending=False)  # Series of airlines and hashtag counts

## 12. Among the tweets that "@" a user besides the indicated airline, 
##      find the percentage that include an "@" directed at the other  
##      airlines in this file. 

# first, include only airline and text columns, and clean the dataset
# then create a list for recording tag counts per tweet
# then loop through each airline and see if all of the tweets have tagged these airlines, and record them in counts 
# finally find the percentage (temp7 is calculated in quesiton 9)
temp10 = air[['airline','text']]
temp10['text'] = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ')

# tag counts per tweet
counts = np.zeros(len(temp10))
airlines =[' @virginamerica ',' @united ',' @southwestair ',' @jetblue ', ' @usairways ',' @americanair ']

for i in airlines:
    x = 1*temp10['text'].str.contains(i) # turn into ints 
    counts = counts + x # append
    
q12 = np.sum(counts>1)/len(temp7[temp7>=2])*100 # Percentage of tweets 

## 13. Suppose the same user has two or more tweets in a row, based on how they 
##      appear in the file. For such tweet sequences, determine the percentage
##      for which the most recent tweet (which comes nearest the top of the
##      file) is a positive tweet.

# set an overall and positive counter first
# then subset columns names and sentiment to temp variable 
# then use for loop to traverse the rows, only add 1 to overall count if the username posts the first tweet in the sequence, ignoring the other tweets in the same sequence 
# and only add 1 to positive count if the first tweet is positive
overall_count = 0
positive_count = 0
temp11 = air[['name','airline_sentiment']]
for i in range(len(temp11)-1):
    if i == 0 and temp11.loc[i,'name'] == temp11.loc[i+1,'name']:
        overall_count+= 1
        if temp11.loc[i,'airline_sentiment'] == 'positive':
            positive_count += 1
    
    if i != 0 and temp11.loc[i,'name'] == temp11.loc[i+1,'name'] and temp11.loc[i,'name'] != temp11.loc[i-1,'name']:
        overall_count += 1
        if temp11.loc[i,'airline_sentiment'] == 'positive':
            positive_count += 1
    
q13 = positive_count/overall_count*100  # Percentage of tweets









