##
## File: assignment08.py (STAT 3250)
## Topic: Assignment 8 
##

##  This assignment requires data from three files: 
##
##      'movies.txt':  A file of nearly 3900 movies
##      'reviewers.txt':  A file of over 6000 reviewers who provided ratings
##      'ratings.txt':  A file of over 1,000,000 movie ratings
##
##  The file 'readme.txt' has more information about these files.
##  You will need to consult the readme.txt file to answer some of the questions.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import pandas as pd

## It is recommended that you read in the data sets in the manner shown below.
movietext = open('movies.txt', encoding='utf8').read().splitlines()
reviewertext = open('reviewers.txt', encoding='utf8').read().splitlines()
ratingtext = open('ratings.txt', encoding='utf8').read().splitlines()

# these data processing will be used in future questions 
# we turn these string lists into dataframes, with columns representing each part of the string separated by '::'
# also assign proper column names for easier interpretation 
movie = pd.Series(movietext).str.split('::',expand=True)
movie.columns = ['movie_id','title','genre']
reviewer = pd.Series(reviewertext).str.split('::',expand=True)
reviewer.columns = ['reviewer_id','gender','age','occupation','zipcode','state']
rating = pd.Series(ratingtext).str.split('::',expand=True)
rating.columns = ['reviewer_id','movie_id','rating','timestamp']
rating['rating'] = rating['rating'].astype(int)

## 1.  Based on the data in 'reviewers.txt': Determine the percentage of all 
##     reviewers that are female.  Determine the percentage of all reviewers in
##     the 35-44 age group.  Among the 18-24 age group, find the percentage 
##     of reviewers that are male.

# same logistics for all three sub-problems
# we subset the column(s) based on what information (e.g. gender) is needed
# and then find percentage based on conditions via dividing lengths of subsetted datasets by overall lengths
temp1a = reviewer['gender']
q1a = len(temp1a[temp1a=='F'])/len(temp1a)*100  # percentage of female reviewers

temp1b = reviewer['age']
q1b = len(temp1b[temp1b=='35'])/len(temp1b)*100  # percentage age 35-44

temp1c = reviewer[reviewer['age']=='18']
q1c = len(temp1c[temp1c['gender']=='M'])/len(temp1c)*100  # percentage of males reviewers in 18-24 age group

## 2.  Give a year-by-year Series of counts for the number of ratings, with
##     the rating year as index and the counts as values, sorted by rating
##     year in ascending order.

# first convert timestamp into datetime, and extract the year portion
# then group the data by year and find out counts, sorted by year in ascending order
temp2 = pd.to_datetime(rating['timestamp'], unit='s').dt.year
q2 = temp2.groupby(temp2).count().sort_index()  # Series of rating counts by year rated

## 3.  Determine the average rating from female reviewers and the average  
##     rating from male reviewers.

# merge rating and reviewer on reviewer id
# then subset data to contain only female/male reviewers and their associated ratings 
# find the mean 
temp3 = pd.merge(rating, reviewer, on='reviewer_id')
q3a = temp3.loc[temp3['gender']=='F','rating'].mean()  # average rating for female reviewers
q3b = temp3.loc[temp3['gender']=='M','rating'].mean()  # average rating for male reviewers

## 4.  Determine the number of movies that received an average rating of 
##     less than 1.75.  (Movies and remakes should be considered as
##     different.)

# since each movie_id uniquely identifies a movie and movies and remakes are considered as different (as proven in line#87), 
# we can simply group by the rating dataset by movie_id 
# type-change rating to int, and find mean ratings based on movie_id
# check how many of those have less than 1.75 mean ratings 
sum(movie['movie_id'].value_counts()>1)
temp4 = rating['rating'].groupby(rating['movie_id']).mean()
q4 = len(temp4[temp4<1.75])  # count of number with average rating less than 1.75

## 5.  Determine the number of movies listed in 'movies.txt' for which there
##     is no rating in 'ratings.txt'.  

# since each movie_id uniquely identifies a movie and movies and remakes are considered as different,  
# we can find how many movies are rated using .unique() 
# and find the difference between that and total number of movies 
q5 = len(movie) - len(rating['movie_id'].unique())

## 6.  Among the ratings from male reviewers, determine the average  
##     rating for each occupation classification (including 'other or not 
##     specified'), and give the results in a Series sorted from highest to 
##     lowest average with the occupation title (not the code) as index.

# first merge rating and reviewer on review_id
# then subset the dataset to contain only ratings by male reviewers 
# then for each occupation id, find the mean rating, and at last sort by occupation id
# since the occupation ids are in ascending order, and we can simply put the original order of occupation titles from readme.txt as new indecies
# do another sort on avg rating in descending order

temp6 = pd.merge(rating, reviewer, on='reviewer_id')
temp6 = temp6[temp6['gender']=='M']
temp6_group = temp6['rating'].groupby(temp6['occupation'].astype(int)).mean().sort_index()
temp6_group.index = ['other','academic/educator','artist','clerical/admin','college/grad student','customer service','doctor/health care',
                     'executive/managerial','farmer','homemaker','K-12 student','lawyer','programmer','retired','sales/marketing','scientist',
                     'self-employed','technician/engineer','tradesman/craftsman','unemployed','writer']
q6 = temp6_group.sort_values(ascending=False)  # Series of average ratings by occupation

## 7.  Determine the average rating for each genre, and give the results in
##     a Series with genre as index and average rating as values, sorted 
##     alphabetically by genre.

# find all genres by splitting movie's genre column by '|'
# then use flatten() to turn the columns into 1 single column, dropping None values, and find the unique genre names 
# also merge rating and movie so ratings can know each movie's genre
# create a blank pd series for future append
# for each genre, subset the movie_rating to movies that contain such genre, and find the ratings.
# then, find the mean rating for each genre, and set the index to i (that genre)
# append into the empty series we created
# eventually, after all genres and associated averages are inserted, do a final sort on index 
genre = movie['genre'].str.split('|',expand=True)
genre = pd.Series(genre.to_numpy().flatten()).dropna().unique()
movie_rating = pd.merge(rating, movie, on='movie_id')
genre_rating = pd.Series()
for i in genre: 
    temp7 = pd.Series(movie_rating.loc[movie_rating['genre'].str.contains(i),'rating'].mean(),index=[i])
    genre_rating = genre_rating.append(temp7)

q7 = genre_rating.sort_index()  # Series of average rating by genre   

## 8.  For the reviewer age category, assume that the reviewer has age at the 
##     midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the reviewers
##     giving that rating.  Give your answer as a Series with rating as index
##     and average age as values, sorted by rating from 1 to 5.

# first merge rating and reviewer on reviewer_id 
# then change the age groups to proper midpoint ages 
# group by rating and find mean age, sorted by rating in ascending order 
temp8 = pd.merge(rating, reviewer, on='reviewer_id')
temp8.loc[temp8['age']=='1','age'] = 16
temp8.loc[temp8['age']=='18','age'] = (18+24)/2
temp8.loc[temp8['age']=='25','age'] = (25+34)/2
temp8.loc[temp8['age']=='35','age'] = (35+44)/2
temp8.loc[temp8['age']=='45','age'] = (45+49)/2
temp8.loc[temp8['age']=='50','age'] = (50+55)/2
temp8.loc[temp8['age']=='56','age'] = 60

q8 = temp8['age'].groupby(temp8['rating']).mean().sort_index()  # Series of average age by rating

## 9.  Find the top-5 "states" in terms of average rating.  Give as a Series
##     with the state as index and average rating as values, sorted from 
##     highest to lowest average rating. (Include any ties as usual)
##     Note: "states" includes US territories and military bases. See the 
##     readme.txt file for more information on what constitutes a "state"
##     for this assignment.

# first merge rating and reviewer on reviewer_id 
# then exlucde state values that are 'unknown' 
# group by state and find mean rating, keeping top 5 mean ratings with ties 
temp9 = pd.merge(rating, reviewer, on='reviewer_id')
temp9 = temp9[temp9['state']!='Unknown']
q9 = temp9['rating'].groupby(temp9['state']).mean().nlargest(5,keep='all')  # top-5 states by average rating

## 10. For each age group, determine the occupation that gave the lowest 
##     average rating.  Give a Series that includes the age group code and 
##     occupation title as a multiindex, and average rating as values.  Sort  
##     the Series by age group code from youngest to oldest. 

# first merge rating and reviewer on reviewer_id 
# then we have a dictionary storing occupation id and its respective title 
# replace our temp10's occupation column with .replace(), which matches the column occupation ids with our dictionary's key, and use the value as replacement
# then find avg ratings grouped by age and occupation 
# find the minimum avg ratings grouped by age, keeping the occupation index
# sort by age index in ascending order (level=0 indicates sorting the first index column)
occupation_dict = {'0':'other','1':'academic/educator','2':'artist','3':'clerical/admin','4':'college/grad student','5':'customer service','6':'doctor/health care','7':'executive/managerial','8':'farmer','9':'homemaker','10':'K-12 student','11':'lawyer','12':'programmer','13':'retired','14':'sales/marketing','15':'scientist','16':'self-employed','17':'technician/engineer','18':'tradesman/craftsman','19':'unemployed','20':'writer'}

temp10 = pd.merge(rating, reviewer, on='reviewer_id')
temp10 = temp10.replace({'occupation': occupation_dict})

avg_ratings = temp10['rating'].groupby([temp10['age'].astype(int),temp10['occupation']]).mean() 

q10 = avg_ratings.groupby('age', group_keys=False).nsmallest(1).sort_index(level=0) # Series of average ratings by age code and occupation title








