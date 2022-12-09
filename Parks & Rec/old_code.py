
def rating_per_season(dataframe):
    averages = []
    for i in range(1, 8):
        chunk = dataframe.loc[:,'season']==i
        averages.append(round(dataframe.loc[chunk,'imdb_rating'].mean(), 2))
    
    dataframe['rating_per_season'] = 0
    for f in averages:
        chunk = dataframe.loc[:,'season']==(averages.index(f)+1)
        dataframe.loc[chunk,'rating_per_season'] = f
    return dataframe

def get_people(dataframe):
    bts = pd.concat((dataframe['directed_by'], dataframe['written_by']))
    producers = pd.DataFrame({'person':bts.unique(), 'writing_credits':0, 'directing_credits':0, 'total_credits':0})
    writers = []
    directors = []

    for b in bts.unique():
        writers.append(sum(dataframe.loc[:,'written_by']==b))
        directors.append(sum(dataframe.loc[:,'directed_by']==b))
    
    producers['writing_credits'] = writers
    producers['directing_credits'] = directors
    producers['total_credits'] = producers['writing_credits'] + producers['directing_credits']
    
    return producers

#WRITERS & DIRECTORS
writers = episodes.groupby('written_by')['episode_num_overall'].count().reset_index()
writers = writers.rename(columns={'written_by': 'person', 'episode_num_overall':'writing_credits'})
writers['directing_credits'] = 0

directors = episodes.groupby('directed_by')['episode_num_overall'].count().reset_index()
directors = directors.rename(columns={'directed_by': 'person', 'episode_num_overall':'directing_credits'})
directors['writing_credits'] = 0

people = writers.merge(directors, how='outer', sort=True)

stackpart1 = characters.T
stackpart1.reset_index(inplace=True)
stackpart1.rename(columns={'index':'person'}, inplace=True)

stackpart2 = pd.DataFrame(episodes['season'])
stackpart2.reset_index(inplace=True)
stackpart2 = stackpart2.T

""" writers = episodes.groupby('written_by')['episode_num_overall'].count().reset_index()
writers = writers.rename(columns={'written_by': 'person', 'episode_num_overall':'writing_credits'})
writers['directing_credits'] = 0

directors = episodes.groupby('directed_by')['episode_num_overall'].count().reset_index()
directors = directors.rename(columns={'directed_by': 'person', 'episode_num_overall':'directing_credits'})
directors['writing_credits'] = 0

people = writers.merge(directors, how='outer', sort=True)
people['total_credits'] = people['writing_credits'] + people['directing_credits'] """

def get_barplot(dataframe):
    list = []
    for column in dataframe:
        if column != 'season':
            character = dataframe.groupby('season')[column].sum().reset_index()
            character.rename(columns={column:'lines'}, inplace=True)
            character['person'] = column
            list.append(character)
    test =  pd.concat(list, axis=0)
    return test

sbarplot = get_barplot(forbarplot)
sbarplot.reset_index(inplace=True)
sbarplot.drop(['index'], axis=1, inplace=True)

def get_regplot(dataframe):
    dataframe['episode_type'] = 'middle'
    list = [5, 6, 29, 30, 45, 46, 67, 68, 89, 90, 111, 112, 123, 124]

    for l in list:
        last = dataframe['episode_num_overall'] == l
        dataframe.loc[last,'episode_type'] = 'end'
    
    for r in range(1, 3):
        first = dataframe['episode_num_in_season'] == r
        dataframe.loc[first,'episode_type'] = 'beginning'
    
    return dataframe