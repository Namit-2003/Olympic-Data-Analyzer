import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0

    if year=='Overall' and country=='Overall':
        temp_df = medal_df

    elif year=='Overall' and country!='Overall':
        flag = 1
        temp_df = medal_df[medal_df['region']==country]

    elif year!='Overall' and country=='Overall':
        temp_df = medal_df[medal_df['Year']==int(year)]

    else:
        temp_df = medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]


    if(flag):
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    if col=='Name':
        nations_over_time.columns = ['Edition', 'Athletes']
    else:
        nations_over_time.columns = ['Edition', col]
    nations_over_time = nations_over_time.sort_values('Edition').reset_index().drop(columns=['index'])
    return nations_over_time


# Top 15 athletes who have won the medal in a particular sport or Overall
def most_successful_athlete_by_sports(df, sport):
    # Remove the rows of athletes that haven't won any medal
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    ans_df = temp_df['Name'].value_counts().reset_index().head(15)
    ans_df.rename(columns={'Medals':'Name','count':'Medals'},inplace='True')
    ans_df = ans_df.merge(df, on='Name')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name').reset_index()
    ans_df = ans_df.drop(columns=['index'])

    return ans_df

def yearwise_medal_tally(df,country):

    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    if new_df.empty:
        return new_df
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    if new_df.empty:
        return new_df
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt

def most_successful_athlete_of_country(df, country):
    # Remove the rows of athletes that haven't won any medal
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    ans_df = temp_df['Name'].value_counts().reset_index().head(15)
    ans_df.rename(columns={'Medals':'Name','count':'Medals'},inplace='True')
    ans_df = ans_df.merge(df, on='Name')[['Name', 'Medals', 'Sport']].drop_duplicates('Name').reset_index()
    ans_df = ans_df.drop(columns=['index'])

    return ans_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athlete_df
    if(sport!='Overall'):
        temp_df = athlete_df[athlete_df['Sport'] == sport]

    return temp_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final