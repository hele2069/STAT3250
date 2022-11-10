##
## File: assignment12.py (STAT 3250)
## Topic: Assignment 12
##


##  In this assignment we revisit past NCAA men's basketball tournaments 
##  (including the glorious 2019 edition) using data from the file 
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each 
##  team's tournament seed.  

##  Two important points:
##    1) Each team is assigned a "seed" at the start of the tournament.  The
##       teams thought to be better are assigned smaller number seeds.  (So 
##       the best teams are assigned 1 and the worst assigned 16.)  In this 
##       assignment a "lower seed" refers to a worse team and hence larger 
##       seed number, with the opposite meaning for "higher seed". 
##    2) All questions refer only to the data in this in 'ncaa.csv' so you
##       don't need to worry about tournaments prior to 1985.

##  Note: The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructor. (There was no 2020
##  tournament and the 2021 tournament didn't turn out to your instructor's
##  liking so that data is omitted.)

##  Submission Instructions: Submit your code in Gradescope under 
##  'Assignment 12 Code'.  The autograder will evaluate your answers to
##  Questions 1-8.  You will also generate a separate PDF for the graphs
##  in Questions 9-11, to be submitted in Gradescope under 'Assignment 12 Graphs'.

import pandas as pd 
import numpy as np
df = pd.read_csv('ncaa.csv')

## 1.  Find all schools that have won the championship. Report your results in
##     a Series that has the schools as index and number of championships for
##     values, sorted alphabetically by school.

# first subset the championship games 
# then create a column storing the champion schools based on scoring
    # if score > score.1, fill in Team 
    # the onces that don't get filled out, we fill those by Team.1 
# perform groupby on that column and count each school's number of championships 
# sort by index 
temp1 = df[df['Region Name'] == 'Championship']
temp1['who_won'] = temp1.loc[temp1['Score']>temp1['Score.1'],'Team']
temp1.loc[temp1['who_won'].isna(),'who_won'] = temp1['Team.1']
group1 = temp1['who_won'].groupby(temp1['who_won']).count()
q1 = group1.sort_index()  # Series of champions and counts

## 2.  Determine all schools that have been in the tournament at least 25 times.
##     Report your results as a Series with schools as index and number of times
##     in the tournament as values, sorted alphabetically by school.

# only include teams in round 1 since each tournmanet appear counts as 1 only (not games)
# first subset the data to include only team and team.1, then convert to numpy to use the flatten() function 
# flatten() expands the columns into one single column 
# then perform groupby on school names and find count 
# then include only schools that have count >= 25, and then sort by school name in alphabetical order 
temp2 = df[df['Round']==1]
temp2 = pd.Series(temp2[['Team','Team.1']].to_numpy().flatten())
group2 = temp2.groupby(temp2).count()
q2 = group2[group2>=25].sort_index()  # Series of schools and tournament appearance counts

## 3.  Find all years when the school that won the tournament was seeded 
##     3 or lower. (Remember that "lower" seed means a bigger number!) Give  
##     a DataFrame with years as index and corresponding school and seed
##     as columns (from left to right).  Sort by year from least to most recent.

# include only championship games 
# same logistics as Q1, only adding another seed column recording the winning team
# subset winning teams with a seed of >= 3
# set index to year 
# include the required columns and sort by index 
temp3 = df[df['Region Name'] == 'Championship']
temp3['who_won'] = df.loc[df['Score']>df['Score.1'],'Team']
temp3['who_won_seed'] = df.loc[df['Score']>df['Score.1'],'Seed']
temp3.loc[temp3['who_won'].isna(),'who_won'] = temp3.loc[temp3['who_won'].isna(),'Team.1']
temp3.loc[temp3['who_won_seed'].isna(),'who_won_seed'] = temp3.loc[temp3['who_won_seed'].isna(),'Seed.1']
group3 = temp3[temp3['who_won_seed']>=3]
group3.index = group3['Year']
q3 = group3[['who_won','who_won_seed']].sort_index()  # DataFrame of years, schools, seeds

## 4.  Determine the average tournament seed for each school.  Make a Series
##     of all schools that have an average seed of 5.0 or higher (that is,
##     the average seed number is <= 5.0).  The Series should have schools
##     as index and average seeds as values, sorted alphabetically by
##     school

# expand team,team1 and seed,seed1
# repeat year 2 times and expand 
# now we have a full record of teams played each year and their seeds
# then get unique items since each team is assigned 1 seed only in each year; 
    # we don't want to find mean seed based on all records since each team might play different # of games in each year 
# group by team and find mean seed number 
# include those with avg seed <= 5 and sort by team name 
temp4 = pd.DataFrame()
temp4['team'] = pd.Series(df[['Team','Team.1']].to_numpy().flatten())
temp4['seed'] = pd.Series(df[['Seed','Seed.1']].to_numpy().flatten())
temp4['year'] = df['Year'].repeat(2).reset_index(drop=True)
temp4 = temp4.drop_duplicates()
group4 = temp4['seed'].groupby(temp4['team']).mean()
q4 = group4[group4<=5].sort_index()  # Series of schools and average seed

## 5.  For each tournament round, determine the percentage of wins by the
##     higher seeded team. (Ignore games of teams with the same seed.)
##     Give a Series with round number as index and percentage of wins
##     by higher seed as values sorted by round in order 1, 2, ..., 6. 
##     (Remember, a higher seed means a lower seed number.)

# firt filter out games where seed = seed.1
# then create a column of 0s storing our condition 
    # if seed < seed.1 and team wins, we set 'condition' to 1
    # if seed.1 < seed and team.1 wins, we set'condition' to 1 
# group by overall count for each round 
# group by number of fulfilled conditions for each round 
# find the percentage 
# sort by index 
temp5 = df[df['Seed'] != df['Seed.1']]
temp5['condition'] = 0
temp5.loc[(temp5['Seed']<temp5['Seed.1']) & (temp5['Score']>temp5['Score.1']),'condition'] = 1
temp5.loc[(temp5['Seed.1']<temp5['Seed']) & (temp5['Score.1']>temp5['Score']),'condition'] = 1

group5a = temp5['condition'].groupby(temp5['Round']).count().sort_index()
group5b = temp5['condition'].groupby(temp5['Round']).sum().sort_index()
q5 = group5b/group5a*100  # Series of round number and percentage higher seed wins

## 6.  For each seed 1, 2, 3, ..., 16, determine the average number of games
##     won per tournament by a team with that seed.  Give a Series with seed 
##     number as index and average number of wins as values, sorted by seed 
##     number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
##     and each tournamentstarts with 4 teams of each seed.  We are not 
##     including "play-in" games which are not part of the data set.)

# set up a 'seed_won' representing each winning team's seed number in each game 
# group by seed_won and find count 
# divide by 140 to find avg and sort by index (seed number)
temp6 = df.copy()
temp6['seed_won'] = 0
temp6.loc[temp6['Score']>temp6['Score.1'],'seed_won'] = temp6.loc[temp6['Score']>temp6['Score.1'],'Seed']
temp6.loc[temp6['Score']<temp6['Score.1'],'seed_won'] = temp6.loc[temp6['Score']<temp6['Score.1'],'Seed.1']
group6 = temp6['seed_won'].groupby(temp6['seed_won']).count()

q6 = group6.sort_index()/140  # Series of seed and average number of wins

## 7.  For each year's champion, determine their average margin of victory 
##     across all of their games in that year's tournament. Find the champions
##     that have an average margin of victory of at least 15. Give a DataFrame 
##     with year as index and champion and average margin of victory as columns
##     (from left to right), sorted by from highest to lowest average victory 
##     margin.

# temp7 stores an additional column representing the winning team's names 
# champions stores the championship games
# champions_games initialized as empty
# for each row in temp7
    # if the team wins a game and it is in the list of champions and belongs to the year when it won championship 
    # add that game to our champions_games 
    # do the same steps for Team.1 
# then find margin of victory 
# then group margin of victory by year and team name and find avg 
# filter out teams with mov < 15 and sort by mov in descending order 
# reset index to have team name as a column
# then set index to year 
# and then remove year column 
temp7 = df.copy()
temp7['who_won'] = temp7.loc[temp7['Score']>temp7['Score.1'],'Team']
temp7.loc[temp7['who_won'].isna(),'who_won'] = temp7['Team.1']

champions = temp7[temp7['Region Name'] == 'Championship']

champions_games = pd.DataFrame()

for index, row in temp7.iterrows():
    if row['Team'] in list(champions['who_won']) and row['Score'] > row['Score.1']:
        if row['Year'] in list(champions.loc[champions['who_won'] == row['Team'], 'Year']):
            champions_games = champions_games.append(row)
    elif row['Team.1'] in list(champions['who_won']) and row['Score.1'] > row['Score']:
        if row['Year'] in list(champions.loc[champions['who_won'] == row['Team.1'], 'Year']):
            champions_games = champions_games.append(row)
        
champions_games['margin_of_victory'] = abs(champions_games['Score'] - champions_games['Score.1'])

group7 = champions_games['margin_of_victory'].groupby([champions_games['Year'].astype(int),champions_games['who_won']]).mean()
group7 = group7[group7>=15].sort_values(ascending=False)
q7 = group7.reset_index()  # DataFrame of years, schools, average margin of victory
q7.index = q7['Year']
q7 = q7.iloc[:,1:]

## 8.  Determine the 2019 champion.  Use code to extract the correct school,
##     not your knowledge of college backetball history.

# filter the exact game 
# since we only have one row, if-else is enough to extract the team name 
# use .squeeze() to extract element from 1x1 dataframe 
temp8 = df[(df['Year']==2019) & (df['Region Name'] == 'Championship')]
if int(temp8['Score']) > int(temp8['Score.1']):
    q8 = temp8['Team'].squeeze()
else:
    q8 = temp8['Team1'].squeeze()

##  Questions 9-11: These require the creation of several graphs. In addition to 
##  the code in your Python file, you will also upload a PDF document (not Word!)
##  containing your graphs (be sure they are labeled clearly).  Include the
##  required code in this file and put your graphs in a PDF document for separate
##  submission.  All graphs should have an appropriate title and labels for
##  the axes.  For these questions the only output required are the graphs.
##  When your PDF is ready submit it under 'Assignment 12 Graphs' in Gradescope.


## 9.  For each year of the tournament, determine the average margin of
##     victory for each round.  Then make a histogram of these averages,
##     using 16 bins and a range of [0,32].

# find margin of victory in each game by using absolute value between score and score.1 
# then group by year and round and find mean margin of victory
# plot data 

import matplotlib.pyplot as plt

temp9 = df.copy()
temp9['margin_of_victory'] = abs(temp9['Score']-temp9['Score.1'])
group9 = temp9['margin_of_victory'].groupby([temp9['Year'],temp9['Round']]).mean().sort_index().reset_index()

plt.hist(group9['margin_of_victory'],bins=16, range=[0,32]) 
plt.title('Histogram of Average Margin of Victory per Round per Tournament between 1985-2019')
plt.ylabel("Frequency")
plt.xlabel("Average Margin of Victory")
plt.show()

## 10. Produce side-by-side box-and-whisker plots, one using the Round 1
##     margin of victory for games where the higher seed wins, and one
##     using the Round 1 margin of victory for games where the lower
##     seed wins.  (Remember that higher seed = lower seed number.)
##     Orient the boxes vertically with the higher seed win data on the 
##     left.

## first subset to round-1 games 
# then find margin of victory 
# create two dataframes each storing higher/lower seed winning team data 
# insert data that match our condition 
# plot based on these two datasets 
temp10 = df[df['Round']==1]
temp10['margin_of_victory'] = abs(temp10['Score']-temp10['Score.1'])

higher_seed_wins = temp10[(temp10['Score']>temp10['Score.1']) & (temp10['Seed']<temp10['Seed.1'])]
higher_seed_wins = higher_seed_wins.append(temp10[(temp10['Score.1']>temp10['Score']) & (temp10['Seed.1']<temp10['Seed'])])    

lower_seed_wins = temp10[(temp10['Score']>temp10['Score.1']) & (temp10['Seed']>temp10['Seed.1'])]
lower_seed_wins = lower_seed_wins.append(temp10[(temp10['Score.1']>temp10['Score']) & (temp10['Seed.1']>temp10['Seed'])])    

data = [higher_seed_wins['margin_of_victory'], lower_seed_wins['margin_of_victory']]
plt.boxplot(data)
plt.xticks([1, 2], ['Higher Seed Wins', 'Lower Seed Wins']) # Specifies data group
plt.xlabel("Higher/Lower Seed Wins")
plt.ylabel("Margin of Victory")
plt.title("Boxplot of Margin of Victory in Round 1 between 1985-2019")
plt.show()

## 11. Produce a bar chart for the number of Round 2 victories by seed.
##     The bars should proceed left to right by seed number 1, 2, 3, ...

# first subset to round-2 games 
# then use previously-used logic to find the winning team's seed in each round-2 games
# use value_count to find count for each seed, and then sort by seed number in ascending order 
# plot the data
temp11 = df[df['Round']==2]
temp11['winning_seed'] = temp11.loc[temp11['Score']>temp11['Score.1'],'Seed']
temp11.loc[temp11['winning_seed'].isna(),'winning_seed'] = temp11.loc[temp11['Score.1']>temp11['Score'],'Seed.1']

group11 = temp11['winning_seed'].astype(int).value_counts().sort_index()

plt.bar(group11.index, group11, color='blue', edgecolor='black')
plt.xlabel("Winning Team's Seed Number")
plt.ylabel("Count")
plt.title("Barchart of Number of Round 2 Victories by Seed between 1985-2019")
plt.show()






