import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

import preprocessor,helper

df = pd.read_csv('athlete_events.csv')
reg_df = pd.read_csv('noc_regions.csv')
famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                 'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                 'Tennis', 'Golf', 'Softball', 'Archery',
                 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                 'Rhythmic Gymnastics', 'Rugby Sevens',
                 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

df = preprocessor.preprocess(df,reg_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal tally')

    elif selected_year!='Overall' and selected_country == 'Overall':
        st.title('Medal tally in ' + str(selected_year))

    elif selected_year=='Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')

    else:
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')

    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')

    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')

    fig = px.line(athletes_over_time, x='Edition', y='Athletes')
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    # Plotting the Heatmap
    st.title("No. of Events over time (Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    heatmap_data = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(heatmap_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    # Succesfull Atheletes of particular sport or overall
    st.title('Most Successfull Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sports_list)
    x = helper.most_successful_athlete_by_sports(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)

    st.title(selected_country + ' Medal tally over the years')
    if country_df.empty:
        st.text(selected_country + ' has not won any medals in any sports')
    else:
        fig = px.line(country_df, x='Year', y='Medal')
        fig.update_layout(xaxis=dict(dtick=8))
        st.plotly_chart(fig)

    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df,selected_country)
    if pt.empty:
       st.text(selected_country + ' has not won any medals in any sports')
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)


    st.title('Top 15 athletes of ' + selected_country)
    top15_df = helper.most_successful_athlete_of_country(df,selected_country)
    st.table(top15_df)

if user_menu == 'Athlete wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False, curve_type='normal')
    fig.update_layout(autosize=False,width=1000,height=600,xaxis_title='Age',yaxis_title='Density')
    st.title('Distribution Over Age')
    st.plotly_chart(fig)

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600,xaxis_title='Age',yaxis_title='Density')
    st.title("Distribution of Age with respect to Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport',sports_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    medal_palette = {'No Medal': 'Blue', 'Gold': 'gold', 'Silver': 'grey', 'Bronze': 'brown'}
    ax = sns.scatterplot(data=temp_df,x='Weight', y='Height',hue=temp_df['Medal'],palette=medal_palette,style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)