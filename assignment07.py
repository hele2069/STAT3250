##
## File: assignment07.py (STAT 3250)
## Topic: Assignment 7 
##

##  This assignment requires the data file 'movies.txt'.  This file
##  contains records for nearly 3900 movies, including a movie ID number, 
##  the title (with year of release, which is not part of the title), and a 
##  list of movie genre classifications (such as Romance, Comedy, etc).  Note
##  that a given movie can be classified into more than one genre -- for
##  instance Toy Story is classified as "Animation", "Children's", and 
##  "Comedy".

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the movie data as text; leave in encoding = 'utf8'
movielines = open('movies.txt', encoding = 'utf8').read().splitlines()
data = pd.Series(movielines).str.split('::',expand=True)
data.columns = ['ID','Title','Genre']

## 1.  Determine the number of movies included in genre "Animation", the number
##     in genre "Horror", and the number in both "Comedy" and "Crime".

# same procedure for first two 
# first locate Genre column, and then check whether each entry contains the respective genre
# setting case=False to avoid case sensitivity issues e.g. some entries have 'animation' instead of 'Animation', which won't be counted 
# since the resulting data will be Ts and Fs, by summing them gives the count
q1a = sum(data['Genre'].str.contains('Animation',case=False))  # Genre includes Animation
q1b = sum(data['Genre'].str.contains('Horror',case=False))  # Genre includes Horror
# adding the 'sum' of two identical datasets where each returns bool condition on whether the genre contains 'Comedy' or 'Crime'
# when the 'sum' is 2, the movie contains belongs to both Comedy and Crime 
q1c = sum((data['Genre'].str.contains('Comedy').astype(int) + data['Genre'].str.contains('Crime').astype(int))==2) # Genre includes both Comedy and Crime

## 2.  Among the movies in the genre "Horror", what percentage have the word
##     "massacre" in the title?  What percentage have 'Texas'? (Upper or lower
##     cases are allowed here.) 

# temp2 includes only horror movies 
# check whether the respective string appears in the title, and find how many movies have it 
# then divide that by number of horror movies and *100
temp2 = data.loc[data['Genre'].str.contains('Horror',case=False),]
q2a = sum(temp2['Title'].str.contains('Massacre',case=False))/len(temp2)*100 # percentage in Horror that includes 'massacre'
q2b = sum(temp2['Title'].str.contains('Texas',case=False))/len(temp2)*100  # percentage in Horror that includes 'texas'

## 3.  Among the movies with exactly one genre, determine the genres that
##     have at least 50 movies classified with that genre.  Give a Series 
##     with genre as index and counts as values, sorted largest to smallest 
##     by count.

# temp3 includes movies with only 1 genre, and by using regex=False prevents the function from reading '|' as regex
# group by genre and find how many movies
# include only genres with at least 50 movies sorted in descending order 
temp3 = data.loc[data['Genre'].str.contains('|',regex=False)==False,]
group3 = temp3['Genre'].groupby(temp3['Genre']).count()
q3 = group3[group3>=50].sort_values(ascending=False) # Series of genres for at least 50 movies and counts

## 4.  Determine the number of movies that have 1 genre, 2 genres, 3 genres, 
##     and so on.  Give your results in a Series, with the number of genres
##     as the index and the counts as values, sorted by index values from
##     smallest to largest. 

# first split genre by '|' into columns 
# then mark those with 'na' as 0, other values as '1', and calculate column rum, which indicates how many genres does each movie have 
# group by number of genres, and sort by number of genres in ascending order 
temp4 = data['Genre'].str.split('|',expand=True)
temp4 = (temp4.isna()==False).astype(int).sum(axis=1)
q4 = temp4.groupby(temp4).count().sort_index()  # Series of number of genres and counts

## 5.  How many remakes are in the data? We say a movie is a remake if the title is
##     exactly the same as the title of an older movie. For instance, if 'Hamlet'  
##     is in the data set 4 times, then 3 of those should be counted as remakes.
##     (Note that a sequel is not the same as a remake -- "Jaws 2" is completely
##     different from "Jaws".)

# first remove the 'year' part 
# group by movie names and find out counts 
# find those with 'count' >= 2 (essentially the number of remakes) and minus 1 to exclude the 'first' movie 
# sum them to get total number of remakes 
temp5 = data['Title'].str[:-6]
group5 = temp5.groupby(temp5).count()
q5 = (group5[group5>=2]-1).sum()  # number of remakes in data set


## 6.  Determine for each genre the percentage of movies in the data set that
##     are classified as that genre.  Give a Series of all with 8% or more,
##     with genre as index and percentage as values, sorted from highest to 
##     lowest percentage. 

# first split genre into columns and flatten the genres to find unique genres across all columns 
# for each genre, check if the movie dataset contains that genre, and find out how many 
# find percentage and keep >= 8%, sorted in descending order 
temp6 = data['Genre'].str.split('|',expand=True)
temp6 = pd.Series(temp6.to_numpy().flatten()).dropna().unique()

q6 = pd.Series() # Series of genres and percentages
for i in temp6: 
    temp6a = pd.Series(sum(data['Genre'].str.contains(i,case=False)),index=[i])
    q6 = q6.append(temp6a)

q6 = q6/len(data)*100
q6 = q6[q6>=8].sort_values(ascending=False)

## 7.  It is thought that musicals have become less popular over time.  We 
##     judge that assertion here as follows: Compute the median release year 
##     for all movies that have genre "Musical", and then do the same for all
##     other movies.  

# same for both Musical and non-Musical movies 
# subset the title column from either datasets 
# locate the 'year', which is string location from -5 to -1, and type-cast to int 
# find median respectively 
temp7a = (data.loc[data['Genre'].str.contains('Musical',case=False),'Title'].str[-5:-1]).astype(int)
temp7b = (data.loc[data['Genre'].str.contains('Musical',case=False)==False,'Title'].str[-5:-1]).astype(int)

q7a = np.median(temp7a)  # median release year for Musical
q7b = np.median(temp7b)  # median release year for non-Musical 

##  8. Determine how many movies came from each decade in the data set.
##     An example of a decade: The years 1980-1989, which we would label as
##     1980.  (Use this convention for all decades in the data set.) 
##     Give your answer as a Series with decade as index and counts as values,
##     sorted by decade 2000, 1990, 1980, ....

# first extract the year portion
# then //10 and *10 to get decades 
temp8 = data['Title'].str[-5:-1].astype(int)//10*10
q8 = temp8.groupby(temp8).count().sort_index(ascending=False)  # Series of decades and counts

##  9. For each decade in the data set, determine the percentage of titles
##     that have exactly one word.  (Note: "Jaws" is one word, "Jaws 2" is not)
##     Give your answer as a Series with decade as index and percentages as values,
##     sorted by decade 2000, 1990, 1980, ....

# first create a decade column
# create a dataframe that only includes movies with 1-word title (indicated by one space within the title column)
# find the percentage with groupby (decade), filling None with 0 since there might be some decades with no one-word title movies 
temp9 = data.copy()
temp9['Decade'] = temp9['Title'].str[-5:-1].astype(int)//10*10
one_word = temp9[temp9['Title'].str.count(' ')==1]
q9 = (one_word['Decade'].groupby(one_word['Decade']).count().sort_index(ascending=False)/temp9['Decade'].groupby(temp9['Decade']).count().sort_index(ascending=False)*100).fillna(0).sort_index(ascending=False) # Series of percentage 1-word titles by decade

## 10. For each genre, determine the percentage of movies classified in
##     that genre also classified in at least one other genre.  Give your 
##     answer as a Series with genre as index and percentages as values, 
##     sorted largest to smallest percentage.

# similar to quesiton 6, first find all genres 
# then loop through each genre, checking whether the movies contain that genre and has other genres (indicated containing '|')
# also keep a genre count 
# find the proportion in descending order 
temp10 = data['Genre'].str.split('|',expand=True)
temp10 = pd.Series(temp10.to_numpy().flatten()).dropna().unique()

q10 = pd.Series() # Series of genres, percentages
group10 = pd.Series()
for i in temp10: 
    temp10a = pd.Series(len(data[data['Genre'].str.contains(i,case=False) & data['Genre'].str.contains('|',regex=False)]),index=[i])
    temp10b = pd.Series(len(data[data['Genre'].str.contains(i,case=False)]),index=[i])
    q10 = q10.append(temp10a)
    group10 = group10.append(temp10b)

q10 = (q10/group10*100).sort_values(ascending=False)
