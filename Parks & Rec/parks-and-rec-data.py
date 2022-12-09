
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
import seaborn as sns

#

episodes = pd.read_csv('parks_and_rec_episodes.csv')
ratings = pd.read_csv('parks_and_rec_imdb.csv')

episodes.drop([124], inplace=True)
ratings.drop(['desc'], axis=1, inplace=True)

newepisodes = episodes.drop(['title'], axis=1)
newratings = ratings.drop(['season', 'episode_num', 'original_air_date'], axis=1)
fullinfo = pd.concat([newepisodes, newratings], axis=1)

sns.set_theme(style='ticks', font='Arial Rounded MT Bold')
sns.set_palette('husl', 11)

sizedist = np.linspace(10, 200, len(fullinfo['imdb_rating'].unique()))
sizedist = sizedist.tolist()

#VIEWERS & RATING PER EPISODE & SEASON
""" sns.lineplot(x='episode_num_overall', y='us_viewers', hue='season', palette='husl', legend='full', data=episodes)
plt.title('U.S. Viewers Per Episode')
plt.xticks(np.arange(0, 130, 5))
plt.xlabel('Episode')
plt.ylabel('U.S. Viewers') """

""" sns.boxplot(x='season', y='us_viewers', palette='husl', data=episodes)
plt.title('Distribution of U.S. Viewers')
plt.xlabel('Season')
plt.ylabel('U.S. Viewers') """

""" sns.scatterplot(x='episode_num_overall', y='imdb_rating', size='imdb_rating', sizes=sizedist, hue='season', palette='husl', legend=False, data=fullinfo)
plt.title('IMDB Ratings Per Episode')
plt.xticks(np.arange(0, 130, 5))
plt.xlabel('Episode')
plt.ylabel('Rating') """

""" sns.boxplot(x='season', y='imdb_rating', palette='husl', data=ratings)
plt.title('Distribution of IMDB Ratings')
plt.xlabel('Season')
plt.ylabel('Rating') """

def get_script(filename):
    dataframe = pd.read_csv(filename)
    characters = {'Leslie Knope':0, 'Ann Perkins':0, 'Mark Brendanawicz':0, 'Tom Haverford':0, 'Ron Swanson':0, 'April Ludgate':0, 'Andy Dwyer':0, 'Ben Wyatt':0, 'Chris Traeger':0, 'Donna Meagle':0}
    
    for c in characters:
        chunk = dataframe.loc[:,'Character']==c
        characters[c] = dataframe[chunk].shape[0]
    
    return characters

def get_files(path):
    filelist = os.listdir(path)
    return sorted(filter(lambda x: os.path.isfile(os.path.join(path, x)), filelist))

scripts = get_files('/Users/yaelmargolis/Downloads/scripts')

def get_table(list):
    directory = []
    for l in list:
        directory.append(get_script(l))
    
    table = pd.DataFrame(directory, index=list)
    table.loc['s6e21.csv',:] = np.nan
    table.loc['s6e22.csv',:] = np.nan
    table.sort_index(inplace=True)
    table.reset_index(level=None, drop=True, inplace=True)
    table['total_lines'] = table.sum(axis=1)

    return table

def get_percentages(dataframe):
    for column in dataframe:
        if column != 'total_lines':
            dataframe[column] = 100*(dataframe[column] / dataframe['total_lines'])
    dataframe['total_lines'] = 100
    return dataframe

percentages = get_percentages(get_table(scripts))
percentages = pd.concat([episodes['season'], episodes['episode_num_in_season'], percentages], axis=1)

def get_barplot(dataframe, number):
    chunk = dataframe['season'] == number
    toreturn = dataframe[chunk]
    shortened = toreturn.drop(['season', 'total_lines'], axis=1)
    shortened.set_index('episode_num_in_season', inplace=True)
    return shortened

#PERCENT LINES PER CHARACTER PER EPISODE
""" one = get_barplot(percentages, 1)
g1 = one.plot(kind='bar', stacked=True, title='Season 1: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g1.legend().remove()

two = get_barplot(percentages, 2)
g2 = two.plot(kind='bar', stacked=True, title='Season 2: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g2.legend().remove()

three = get_barplot(percentages, 3)
g3 = three.plot(kind='bar', stacked=True, title='Season 3: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g3.legend().remove()

four = get_barplot(percentages, 4)
g4 = four.plot(kind='bar', stacked=True, title='Season 4: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g4.legend().remove()

five = get_barplot(percentages, 5)
g5 = five.plot(kind='bar', stacked=True, title='Season 5: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g5.legend().remove()

six = get_barplot(percentages, 6)
g6 = six.plot(kind='bar', stacked=True, title='Season 6: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g6.legend().remove()

seven = get_barplot(percentages, 7)
g7 = seven.plot(kind='bar', stacked=True, title='Season 7: Percent Lines Per Character Per Episode',
yticks=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], xlabel='Episode', ylabel='Lines', rot=0, linewidth=.5)
g7.legend().remove() """

raw = pd.concat([episodes['season'], get_table(scripts)], axis=1)

def get_groupby(dataframe, character):
    calculate = dataframe.drop(['total_lines'], axis=1)
    toreturn = calculate.groupby('season')[character].sum().reset_index()
    return toreturn[character]

rawtotal = pd.concat([get_groupby(raw, 'Leslie Knope'), get_groupby(raw, 'Ann Perkins'),
get_groupby(raw, 'Mark Brendanawicz'), get_groupby(raw, 'Tom Haverford'), get_groupby(raw, 'Ron Swanson'),
get_groupby(raw, 'April Ludgate'), get_groupby(raw, 'Andy Dwyer'), get_groupby(raw, 'Ben Wyatt'),
get_groupby(raw, 'Chris Traeger'), get_groupby(raw, 'Donna Meagle')], axis=1)

rawtotal.set_index(rawtotal.index + 1, inplace=True)

#LINES PER CHARACTER PER SEASON
""" graph8 = rawtotal.plot(kind='bar', stacked=True, title='Total Lines Per Character Per Season',
yticks=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000],
xlabel='Season', ylabel='Lines', rot=0, linewidth=.5)

sns.move_legend(graph8, 'upper right', fontsize='x-small') """

def get_fractions(dataframe):
    dataframe['episode_fraction'] = 0

    for r in range(1, 8):
        chunk = dataframe['season'] == r
        length = len(dataframe[chunk]['episode_num_in_season'])
        dataframe.loc[chunk,'episode_fraction_in_season'] = dataframe[chunk]['episode_num_in_season'] / length
    
    dataframe.drop(['written_by', 'directed_by', 'original_air_date'], axis=1, inplace=True)
    return dataframe

fractions = pd.concat([newratings, get_fractions(newepisodes)], axis=1)
correlations = get_percentages(get_table(scripts))
correlations = pd.concat([fullinfo, correlations], axis=1)

#CORRELATIONS
""" sns.regplot(x='episode_fraction_in_season', y='imdb_rating', order=3, color='tab:purple', data=fractions)
plt.title('IMDB Rating Per Episode In Season')
plt.xticks(np.arange(0, 1.05, .05))
plt.xlabel('Episode In Season')
plt.ylabel('IMDB Rating') """

""" sns.regplot(x='episode_fraction_in_season', y='us_viewers', robust=True, color='tab:purple', data=fractions)
plt.title('IMDB Rating Per Episode In Season')
plt.xticks(np.arange(0, 1.05, .05))
plt.xlabel('Episode In Season')
plt.ylabel('U.S. Viewers') """

""" sns.regplot(x='Ron Swanson', y='imdb_rating', color='tab:pink', data=correlations)
plt.title('Ron Swanson: Correlation Between Percent Lines & IMDB Rating?')
plt.xlabel('Percent Lines')
plt.ylabel('IMDB Rating') """

""" sns.regplot(x='total_votes', y='us_viewers', robust=True, ci=None, color='tab:green', data=fullinfo)
plt.title('Correlation Between Number of IMDB Ratings & U.S. Viewers')
plt.xlabel('Number of IMDB Ratings')
plt.ylabel('U.S. Viewers') """

plt.show()