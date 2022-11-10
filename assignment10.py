##
## File: assignment10.py (STAT 3250)
## Topic: Assignment 10 
##

##  For this assignment you will be working with Twitter data related
##  to the season opening of Game of Thrones on April 14, 2019.  You will use 
##  a set of over 10,000 tweets for this purpose.  The data is in the file 
##  'GoTtweets.txt'.  

##  Note: On this assignment it makes sense to use loops to extract 
##  information from the tweets. Go wild.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the GoTtweets.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  
import pandas as pd
import numpy as np 
import json

tweets = []
with open('GoTtweets.txt') as f:
    for line in f:
        tweets.append(json.loads(line))

## 1.  The tweets were downloaded in several groups at about the same time.
##     Are there any that appear in the file more than once?  Give a Series 
##     with the tweet ID for any repeated tweets as the index and the number 
##     of times each ID appears in the file as values.  Sort by the index from
##     smallest to largest.

# first traverse the list of dictionaries using loop
# for each dict, find the value associated with key 'id_str', append all of them into a pd series 
# group by 'id_str' and find count 
# include those with count > 1 and sort by 'id_str' in ascending order which is the index 
# note that using 'id_str' or 'id' produces the same index ordering despite the type difference since the Tweet ids are integers
temp1 = pd.Series(tweet['id_str'] for tweet in tweets)
group1 = temp1.groupby(temp1).count()
q1 = group1[group1>1].sort_index() # Series of tweet IDs that appear > 1 time

## Note: For the remaining questions in this assignment, do not worry about 
##       any duplicate tweets.  Just answer the questions based on the 
##       existing data set.
    

## 2.  Determine the number of tweets that include 'Daenerys' (any combination
##     of upper and lower case; part of another word OK) in the text of the 
##     tweet.  Then do the same for 'Snow'.

# as usual, find all values associated with key 'text'
# turn them into lower-case and find if 'daenerys' or 'snow' appear in the strings 
# find how many by summing the T/F list 
temp2 = pd.Series(tweet['text'] for tweet in tweets)
q2a = sum(temp2.str.lower().str.contains('daenerys'))  # number of tweets including 'daenerys'
q2b = sum(temp2.str.lower().str.contains('snow'))  # number of tweets including 'snow'

## 3.  Find the average number of hashtags included in the tweets. (You may get 
##     the wrong answer if you use the text of the tweets instead of the
##     hashtag lists.)

# as usual, find the hashtag lists associated with each tweet 
# for each tweet, find length of list of hashtag in each tweet, which indicates how many hashtags per tweet
# then take average 
temp3 = pd.Series(len(tweet['entities']['hashtags']) for tweet in tweets)
q3 = np.mean(temp3) # average number of hashtags per tweet

## 4.  Determine the tweets that have 0 hashtags, 1 hashtag, 2 hashtags,
##     and so on.  Give your answer as a Series with the number of hashtags
##     as index (sorted smallest to largest) and the corresponding number of
##     tweets as values. Include in your Series index only number of hashtags  
##     that occur for at least one tweet. (Note: See warning in #3)

# extract the hashtag lists per tweet 
# extract the length of each hashtag list (which indicates how many hashtages were used per tweet)
# filter out tweets with 0 hashtags 
# groupby the lengths, find count, and sort by index in ascending order 
# we won't need to worry about only including number of hashtags that occur for at least one tweet since the .count() satisfies that condition 
# .count() won't 'count' something if it doesn't appear in the dataset
temp4 = pd.Series(len(tweet['entities']['hashtags']) for tweet in tweets)
q4 = temp4.groupby(temp4).count().sort_index()  # Series of number of hashtags and counts

## 5.  Determine the number of tweets that include the hashtag '#GoT', then
##     repeat for '#GameofThrones'.  (You may get the wrong answer if you
##     use the text of the tweets instead of the hashtag lists.)
##     Note: Hashtags are not case sensitive, so any of '#GOT', '#got', 'GOt' 
##     etc are all considered matches.

# first locate hashtags and store them in temp5
# for each tweet's hashtag(s), check if its lower-case equals to 'got' or 'gameofthrones' 
# if yes, increment our counters by 1 
# after each tweet is done processed, add our counter to a series and restore the counter to 0 (because we are looking for number of tweets instead of number of hashtags)
# finally, check how many counters for each series have positive values; doing so ensures we only count each tweet once 
temp5 = [tweet['entities']['hashtags'] for tweet in tweets]

got_list = pd.Series()
gameofthrones_list = pd.Series()
for i in temp5:
    got = 0
    gameofthrones = 0
    for j in i: 
        if j['text'].lower() == 'got':
            got += 1 
        if j['text'].lower() == 'gameofthrones':
            gameofthrones += 1
    got_list = got_list.append(pd.Series(got))
    gameofthrones_list = gameofthrones_list.append(pd.Series(gameofthrones))

q5a = sum(got_list > 0)  # number of tweets with '#GoT' hashtag and upper/lower variants               
q5b = sum(gameofthrones_list > 0)  # number of tweets with '#GameofThrones' hashtags and upper/lower variants             

## 6.  Some tweeters like to tweet a lot.  Find the screen name for all 
##     tweeters with at least 3 tweets in this data.  Give a Series with 
##     the screen name (in lower case) as index and the number of tweets as 
##     value, sorting by the index in alphbetical order.  

# first create a series that contains all screen names in lower case, each associated with one tweet
# group by screen name and find count 
# subset to those names with count >= 3 and sort by screen names (index)
temp6 = pd.Series(tweet['user']['screen_name'] for tweet in tweets).str.lower()
group6 = temp6.groupby(temp6).count()
q6 = group6[group6 >= 3].sort_index()  # Series of screen name and counts

## 7.  Among the screen names with 3 or more tweets, find the average
##     'followers_count' for each and then give a table with the screen  
##     and average number of followers.  (Note that the number of
##     followers might change from tweet to tweet.)  Give a Series with
##     screen name (in lower case) as index and the average number of followers  
##     as value, sorting by the index in alphbetical order.  

# similar to #6
# difference is that we also extract the followers count for each tweet 
# and add another groupby aggregation (mean) on followers
# at last, include users with 3 or more tweets, and get their average number of followers 
# sorted by index in alphabetical order 
temp7 = pd.DataFrame() 
temp7['screen_name'] = [tweet['user']['screen_name'].lower() for tweet in tweets]
temp7['followers'] = [tweet['user']['followers_count'] for tweet in tweets]
group7 = temp7['followers'].groupby(temp7['screen_name']).agg(['count', 'mean'])

q7 = group7.loc[group7['count'] >= 3, 'mean'].sort_index()  # Series of screen names and mean follower counts  

## 8.  Determine the hashtags that appeared in at least 50 tweets.  Give
##     a Series with the hashtags (lower case) as index and the corresponding 
##     number of tweets as values, sorted alphabetically by hashtag.

# first locate hashtag(s) for each tweet
# for each hashtag in each hashtag list in each tweet, check if the lower-case version is in the unique[] we set up ; if not, add that to unique[]
# then check if the hashtag is an index in our group8; if yes, incremenet the value by 1, if not, set the value to 1 
# group8 at last will contain all hashtags and their count amongst the tweets 
# the unique[] is used to avoid situations like one hashtag appearing for more than 1 time in each tweet
# by having unique[], we only count the hashtag once per tweet; avoid duplicates 
# finally include those hashtags with count >= 50 and sort by hashtag names 
temp8 = pd.Series(tweet['entities']['hashtags'] for tweet in tweets)
group8 = pd.Series()

for hashtags in temp8:
    unique = []
    for hashtag in hashtags:
        if hashtag['text'].lower() not in unique:
            unique.append(hashtag['text'].lower())
            if hashtag['text'].lower() in group8.index: 
                group8[hashtag['text'].lower()] += 1
            else: 
                group8[hashtag['text'].lower()] = 1

q8 = group8[group8>=50].sort_index()  # Series of hashtags and counts
        
##  9.  Some of the tweets include the location of the tweeter. Give a Series
##      of the names of countries with at least three tweets, with country 
##      name as index and corresponding tweet count as values.  Sort the
##      Series alphabetically by country name.

# first find the 'place' key associated wtih each tweet
# then remove empty entries 
# then find 'country' key 
# then groupby country and find count, keeping those with count >= 3
# sort by index in alphabetical order
temp9 = pd.Series(tweet['place'] for tweet in tweets).dropna()
temp9 = pd.Series(tweet['country'] for tweet in temp9)
group9 = temp9.groupby(temp9).count()
q9 = group9[group9 >= 3].sort_index()   # Series of countries with at least three tweets

## Questions 10-11: The remaining questions should be done using regular 
##                  expressions as described in the class lectures.

## 10.  Determine the percentage of tweets (if any) with a sequence of 3 or more
##      consecutive digits.  (No spaces between the digits!)  For such tweets,
##      apply 'split()' to create a list of substrings.  Among all the 
##      substrings with a sequence of at least three consecutive digits,
##      determine the percentage where the substring starts with a '@' at the 
##      beginning of the substring.

# find10_a indicates tweets that contains 3 or more consecutive digits, which automatically account for spaces when finding 
# since we need percentage of tweets instead of substrings, we don't need to split the tweets into substrings at this point 
# for q10a, simply divide length of find10_a by length of overall number of tweets and multiply by 100

# find10_b splits tweets that contains 3 or more consecutive digits into columns 
# then we turn that into numpy and flatten() gives us an one-column dataset containing all subtrings 
# drop the None values, and at this point we have all substrings that can either contain/not contain 3 or more consecutive digits 
# substring_three_consec contains all substrings that have 3 or more consecutive digits 
# substring_start_with_tag contains all substrings that have 3 or more consecutive digits & start with '@'
# q10b divides substring_start_with_tag by substring_three_consec and multiply by 100 
temp10 = pd.Series(tweet['text'] for tweet in tweets)

find10_a = temp10[temp10.str.contains("[0-9]{3,}", regex=True)]
find10_b = pd.Series(find10_a.str.split(' ', expand=True).to_numpy().flatten()).dropna()

substring_three_consec = find10_b[find10_b.str.contains("[0-9]{3,}", regex=True)]
substring_start_with_tag = substring_three_consec[substring_three_consec.str.contains("^@", regex=True)]

q10a = len(find10_a)/len(temp10)*100  # percentage of tweets with three consecutive digits
q10b = len(substring_start_with_tag)/len(substring_three_consec)*100  # percentage starting with @ among substrings with 3 consec digits

## 11.  Determine if there are any cases of a tweet with a 'hashtag' that is
##      actually not a hashtag because there is a character (letter or digit)
##      immediately before the "#".  An example would be 'nota#hashtag'.
##      Count the number of tweets with such an incorrect 'hashtag'.

# find tweet content and store them in temp11
# then check whether the content follows pattern (# is preceeded by digits/characters) via regex
# find how many using len()
temp11 = pd.Series(tweet['text'] for tweet in tweets)
hashtag11 = temp11[temp11.str.contains('[a-zA-Z0-9][#]', regex=True)]

q11 = len(hashtag11)  # count of tweets with bad hashtag




