import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy

#initializing mysql connection
user = 'root'
password = 'Abu#%407899#'
host = 'localhost'
port = 3306
database = 'phonepe'
connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
user, password, host, port, database
))

#Fetching data from database with pandas using mysql

def fetch_data():
    q1 = 'select * from agg_transaction_table'
    agg_tt = pd.read_sql(q1, con = connection)
    q2 = 'select * from agg_user_table'
    agg_ut = pd.read_sql(q2, con = connection)
    q3 = 'select * from map_transaction_table'
    map_tt = pd.read_sql(q3, con = connection)
    q4 = 'select * from map_user_table'
    map_ut = pd.read_sql(q4, con = connection)
    q5 = 'select * from top_transaction_table'
    top_tt = pd.read_sql(q5, con = connection)
    q6 = 'select * from top_user_table'
    top_ut = pd.read_sql(q6, con = connection)
    q7 = 'select * from district_geo_table'
    districts = pd.read_sql(q7, con = connection)
    q8 = 'select * from state_geo_table'
    states = pd.read_sql(q8, con = connection)
    
    return agg_tt, agg_ut, map_tt, map_ut, top_tt, top_ut, districts, states

agg_tt, agg_ut, map_tt, map_ut, top_tt, top_ut, districts, states = fetch_data()
#Data_visualization

def indiamap_visual():
    selected = st.selectbox(
            options=['Transaction', 'User'],
            label='geovisualization'
        )
    if selected == "Transaction":
        df1 = map_tt.groupby(['State', 'Year', 'Quater'], as_index=False).sum()
        df1 = df1.query(f"Year == {Year} & Quater == {Quater}")
        df1 = df1[['State', 'Transaction_amount']]

        fig1 = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_amount',
                            hover_data=['State', 'Transaction_amount'],
                            projection="robinson",
                            color_continuous_scale='Plasma_r',
                                     range_color=(12, 0))
        fig1.update_geos(fitbounds='locations', visible=False)
        fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        st.plotly_chart(fig1)

        st.write(df1)
        if selected == "User":
            df2 = map_ut.groupby(['State','Year','Quater'], as_index=False).sum()
            df2 = df2.query(f"Year =={Year} & Quater =={Quater}")
            df2 = df2[['State', 'Users']]

            fig3 = px.choropleth(df3,
                                 geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
eatureidkey='properties.ST_NM',
locations='State',
color='Users',
hover_data=['State', 'Users'],
projection="robinson",
color_continuous_scale='Viridis_r',
range_color=(12, 0))
            fig3.update_geos(fitbounds='locations', visible=False)
            fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig3)

            st.write(df2)
            
def sunburst_v():
    selected = st.selectbox(
    options=['Top Transaction', 'Top User'],
    label='District wise visualization'
    )

    if selected == "Top Transaction":
        df3 = pd.read_csv("Data\\Top_transactions.csv")
        df3 = df3.query(f"Year =={Year} & Quater =={Quater}")
        fig2 = px.sunburst(df3, path=['State', 'District'], values='Transaction_amount',
                           color='Transaction_amount', hover_data=['Transaction_count'],
                           color_continuous_scale='rainbow',
                          )
        st.plotly_chart(fig2)
        st.write(df3)

    elif selected == "Top User":
        df4 = pd.read_csv("Data\\Top_users.csv")
        df4 = df4.query(f"Year =={Year} & Quater =={Quater}")
        fig4 = px.sunburst(df4, path=['State', 'District'], values='Users',
                           color='Users', hover_data=['Users'],
                           color_continuous_scale='turbo',
                          )
        st.plotly_chart(fig4)
        st.write(df4)

#Streamlit navigation
home, data_insight, about = st.tabs(
    ['Home', 'Data Insights', 'About'])
#home
with home:
    st.image("image\\pelogo1.png")
    st.subheader("About Phonepe")
    st.write('''PhonePe is an Indian digital payments and financial services company 
    headquartered in Bengaluru, Karnataka, India. PhonePe was founded in 
    December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. 
    The PhonePe app, based on the Unified Payments Interface, went live in August 2016.
    The PhonePe app is available in 11 Indian languages.''')
with data_insight:
    choice = st.selectbox("Phonepe Pulse Data Visualization",("State", "District"))
    choice_select = st.radio("choose an option to view:", choice)
    Year = st.selectbox('Please select the Year',
                    ('2018', '2019', '2020', '2021', '2022'))
    Quater = st.selectbox('Please select the Quater',
                       ('1', '2', '3', '4'))
    
    if choice_select == 'S':
        indiamap_visual()
        
    elif choice_select == 'D':
        sunburst_v()