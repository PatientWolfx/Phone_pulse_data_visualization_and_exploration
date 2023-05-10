import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy
from PIL import Image

#initializing mysql connection
user = 'root'
password = ''#use local server password inside the quotation
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
    state = pd.read_sql(q8, con = connection)
    
    return agg_tt, agg_ut, map_tt, map_ut, top_tt, top_ut, districts, state

agg_tt, agg_ut, map_tt, map_ut, top_tt, top_ut, districts, state = fetch_data()
#Transactions_by_map

#Facts function for first 10 datapoints
def facts(d_f):
    d_f = d_f.head(10).reset_index(drop=True)
    return d_f

#for two tables
def facts_plot1(d_f):
    p_bar = px.bar(d_f, 
                   x=d_f.columns[0], y=d_f.columns[1], 
                   color=d_f.columns[1], color_continuous_scale='viridis' 
                  )
    return st.plotly_chart(p_bar)

#for dataframes with three tables
def facts_plot2(d_f):
    p_bar = px.bar(d_f, 
                   x=d_f.columns[1], y=d_f.columns[2], 
                   color=d_f.columns[2], color_continuous_scale='viridis' 
                  )
    return st.plotly_chart(p_bar)

#Data_visualization
#creating a function for Map_data_Visualization
def indiamap_visual():
    selected = st.selectbox(
            options=['None','Transactions', 'Users'],
            label=':orange[Choropleth_visual]'
        )
    #Map_transactions
    if selected == "Transactions":
        #Choropleth map
        
        #Summing transactions
        map_tt_crp = map_tt.groupby(['State', 'Year', 'Quater']).sum()[['Transaction_count', 'Transaction_amount']].reset_index()
        
        #radio_part
        t_type = ['By Amount', 'By Count']
        t_types = st.radio(':orange[Type]',
                          t_type,
                          horizontal=True
          )
        if t_types == 'By Amount':
            Transaction = 'Transaction_amount'
        elif t_types == 'By Count':
            Transaction = 'Transaction_count'
        #radio ends
        
        df1 = map_tt_crp
        df1 = df1.query(f"Year == {year} & Quater == {quater}")
        df1 = df1[['Year','Quater','State','Transaction_amount', 'Transaction_count']]
        fig1 = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color=Transaction,
                            hover_name='State',
                            hover_data=['Year','Quater', 'Transaction_amount','Transaction_count'],
                            projection="robinson",
                            color_continuous_scale='jet_r',
                            range_color=(12, 0),
                            width=1200,
                            height=550
                            )
        fig1.update_geos(fitbounds='locations', visible=False)

        st.plotly_chart(fig1)
        
        select_map = st.selectbox(
            options = ['None','State','District'],
            label = ':orange[Select an option]'
        )
        #Insights
        
        #State_part
        if select_map == 'State':
            col1,col2 = st.columns([6,4])
            with col1:
                fig = px.bar(df1, x='State',y=Transaction,color='State', 
                             color_continuous_scale='jet',title=str(year)+'-Q'+str(quater), width=1100, height=700)
                st.plotly_chart(fig)
                
            with col2:
                with st.expander(f'States by {Transaction}'):
                    df1 = df1.sort_values(by=Transaction, ascending=False).reset_index()
                    st.write(df1[['State',Transaction]])
            d_f1 = df1.copy()
            d_f1 = d_f1[['State',Transaction]]
            d_f1 = facts(d_f1)
            
            col_1, col_2 = st.columns([4,6])
            
            with col_1:
                st.write(f'Top 10 States by {Transaction}',d_f1)
                
            with col_2:
                facts_plot1(d_f1)
        
        #District_part
        elif select_map == 'District':
            col1,col2 = st.columns([6,4])
            dst_tt = map_tt
            dst_tt = dst_tt.query(f"Year == {year} & Quater == {quater}")
            dst_tt = dst_tt.groupby(['State','Year','Quater','District']).sum().reset_index()
            dst_tt = dst_tt.sort_values(by='District', ascending=True)
            fig = px.bar(dst_tt, x='District', y=Transaction,
                        color='District', color_continuous_scale='rainbow', width=1100, height=700)
            with col1:
                st.plotly_chart(fig)
            
            with col2:
                with st.expander(f'Districts by {Transaction}'):
                    dst_tt = dst_tt.sort_values(by=Transaction, ascending=False).reset_index()
                    st.write(dst_tt[['District',Transaction]])
                    
            #Facts part
            d_f1 = dst_tt.copy()
            d_f1 = d_f1[['State','District',Transaction]]
            d_f1 = facts(d_f1)
            
            col_1, col_2 = st.columns([4,6])
            
            with col_1:
                st.write(f'Top 10 Districts by {Transaction}',d_f1)
                
            with col_2:
                facts_plot2(d_f1)
            
    #User_plot
    elif selected == "Users":
        map_ut_crp = map_ut.groupby(['State', 'Year', 'Quater']).sum()[['Users']].reset_index()
        df2 = map_ut_crp
        df2 = df2.query(f"Year == {year} & Quater == {quater}")
        df2 = df2[['State', 'Year', 'Quater','Users']]
        fig2 = px.choropleth(df2,
                             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                             featureidkey='properties.ST_NM',
                             locations='State',
                             color='Users',
                             hover_name='State',
                             hover_data=['State', 'Year', 'Quater','Users'],
                             projection="robinson",
                             color_continuous_scale='rainbow_r',
                             range_color=(12, 0),
                             width=1200,
                             height=550
                            )
        fig2.update_geos(fitbounds='locations', visible=False)
        fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig2)

        select_map = st.selectbox(
            options = ['None','State','District'],
            label = ':orange[Select an option]'
        )
        #State_part
        if select_map == 'State':
            col1,col2 = st.columns([6,4])
            with col1:
                fig = px.bar(df2, x='State',y='Users',color='State', 
                             color_continuous_scale='jet',title=str(year)+'-Q'+str(quater), width=1100, height=700
                            )
                st.plotly_chart(fig)
            with col2:
                with st.expander('States by users'):
                    df2 = df2.sort_values(by='Users', ascending=False).reset_index()
                    st.write(df2[['State','Users']])
                    
            #facts_part
            d_f2 = df2.copy()
            d_f2 = d_f2[['State','Users']]
            d_f2 = facts(d_f2)
            
            col_1, col_2 = st.columns([4,6])
            
            with col_1:
                st.write(f'Top 10 State by Users',d_f2)
                
            with col_2:
                facts_plot1(d_f2)
            
        
        #District_part
        elif select_map == 'District':
            col1,col2 = st.columns([6,4])
            dst_ut = map_ut
            dst_ut = dst_ut.query(f"Year == {year} & Quater == {quater}")
            dst_ut = dst_ut.groupby(['State','Year','Quater','District']).sum().reset_index()
            fig = px.bar(dst_ut, x='District', y='Users',
                        color='District', color_continuous_scale='rainbow', width=1100, height=700)
            with col1:
                st.plotly_chart(fig)
            with col2:
                with st.expander('Top Districts'):
                    dst_ut = dst_ut.sort_values(by='Users', ascending=False).reset_index()
                    st.write(dst_ut[['District','Users']])
                    
            #facts_part
            d_f2 = dst_ut.copy()
            d_f2 = d_f2[['State', 'District','Users']]
            d_f2 = facts(d_f2)
            
            col_1, col_2 = st.columns([4,6])
            
            with col_1:
                st.write(f'Top 10 Districts by Users',d_f2)
                
            with col_2:
                facts_plot2(d_f2)
                
                    

#creating a function for Aggregated_data_Visualization
def sunburst_v():
    selected = st.selectbox(
    options=['None','By Transaction type', 'By Brands'],
    label=':orange[Sunburst_visual]'
    )

    if selected == "By Transaction type":
        tran_type = st.selectbox(
        options=['None','Recharge & bill payments','Peer-to-peer payments',
                'Merchant payments','Financial Services','Others'],
        label = ':orange[Transaction type]'
        )
        #Summing transactions
        df3 = agg_tt
        df3 = df3.groupby(['State','Year','Quater','Transaction_type']).sum().reset_index()
        
        #radio_part
        t_type = ['By Amount', 'By Count']
        t_types = st.radio(':orange[Type]',
                          t_type,
                          horizontal=True
          )
        if t_types == 'By Amount':
            Transaction = 'Transaction_amount'
        elif t_types == 'By Count':
            Transaction = 'Transaction_count'
        #radio ends
        
        df3 = df3.query(f"Year =={year} & Quater =={quater} & Transaction_type == '{tran_type}'")
        fig3 = px.sunburst(df3, path=['State', 'Transaction_type', Transaction],
                           color=Transaction, hover_name='State', hover_data=[Transaction],
                           color_continuous_scale='rainbow',
                           width=1000, height=550
                          )
        #creating columns
        col1, col2 = st.columns([6,4])
        
        with col1:
            st.plotly_chart(fig3)
            
        with col2:
            with st.expander(f'States by {Transaction}'):
                df3 = df3.sort_values(by=Transaction, ascending=False).reset_index()
                st.write(df3[['State', Transaction]])
                
                
        #facts_part
        d_f3 = df3.copy()
        d_f3 = d_f3[['State', Transaction]]
        d_f3 = facts(d_f3)
        
        col_1, col_2 = st.columns([4,6])
            
        with col_1:
            st.write(f'Top 10 States with {tran_type} by {Transaction}', d_f3)
                
        with col_2:
            facts_plot1(d_f3)


    elif selected == "By Brands":
        #Sunburst plot
        df4 = agg_ut
        #Summing users and percentages
        df4 = df4.groupby(['State','Year','Quater','Brand']).sum().reset_index()
        
         #radio_part
        view_type = ['By Count', 'By Percentage']
        view_types = st.radio(':orange[Type]',
                          view_type,
                          horizontal=True
          )
        if view_types == 'By Count':
            views = 'Count'
        elif view_types == 'By Percentage':
            views = 'Percentage'
        #radio ends
        
        
        df4 = df4.query(f"Year =={year} & Quater =={quater}")
        fig4 = px.sunburst(df4, path=['State', 'Brand'],
                           color=views, hover_name='State', hover_data=[views],
                           color_continuous_scale='rainbow',
                           width=1000, height=550
                          )
        
        
        quaters = ['2','3','4']
        if year == '2022' and quater in quaters:
            st.success("stay tuned! Data not available")
            
        else:            
            #creating columns
            col1, col2 = st.columns([6,4])

            with col1:
                st.plotly_chart(fig4)

            with col2:
                with st.expander(f'States by {views}'):
                    df4 = df4.sort_values(by=views, ascending=False).reset_index()
                    st.write(df4[['State', 'Brand',views]])
                    
            #facts_part
            d_f4 = df4.copy()
            d_f4 = d_f4[['State','Brand', views]]
            
            d_f4 = facts(d_f4)
        
            col_1, col_2 = st.columns([4,6])
            
            with col_1:
                st.write(f'Top 10 Brands by {views}', d_f4)
                
            with col_2:
                facts_plot2(d_f4)
    

#Streamlit navigation
img1 = Image.open("image\\pelogo1.png")
st.set_page_config(page_title='PhonePe Pulse Data',page_icon=img1,layout='wide')
st.title(":violet[Phonepe Pulse Data Visualization & Exploration]")
home, data_insight = st.tabs(
    ['Home', 'Data Insights'])
#home
with home:
    st.image(img1, width=200)
    st.subheader(":violet[About Phonepe]")
    st.write('''PhonePe is an Indian digital payments and financial services company 
    headquartered in Bengaluru, Karnataka, India. PhonePe was founded in 
    December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. 
    The PhonePe app, based on the Unified Payments Interface, went live in August 2016.
    The PhonePe app is available in 11 Indian languages.
    ''')
    st.subheader(":violet[About Phonepe Pulse]")
    st.write('''
    The Indian digital payments story has truly captured the world's imagination. From 
    the largest towns to the remotest villages, there is a payments revolution being 
    driven by the penetration of mobile phones and data.
    ''')
    
    st.video("https://youtu.be/c_1H6vivsiA")
    
    st.write('''
    When PhonePe started 5 years back, we were constantly looking for definitive data 
    sources on digital payments in India. Some of the questions we were seeking answers 
    to were - How are consumers truly using digital payments? What are the top cases? 
    Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes? 
    This year as we became India's largest digital payments platform with 46% UPI market 
    share, we decided to demystify the what, why and how of digital payments in India.
    
    This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we 
    thought as India's largest digital payments platform with 46% UPI market share, we 
    have a ring-side view of how India sends, spends, manages and grows its money. So 
    it was time to demystify and share the what, why and how of digital payments in India.
    
    PhonePe Pulse is your window to the world of how India transacts with interesting trends, 
    deep insights and in-depth analysis based on our data put together by the PhonePe team.
    ''')

with data_insight:
    st.markdown(":violet[Phonepe Pulse Data Visualization]")
    
    col1, col2, col3 = st.columns([4,3,3])
    
    with col1:
        choice = st.selectbox(":orange[Select an option]",
                              ("None", "By Map","By Aggregated"))
        
    with col2:
        year = st.selectbox(':orange[Please select the Year]',
                            ('None','2018', '2019', '2020', '2021', '2022'))
        #slider
        #year = st.slider('Please select the Year',
         #                   min_value=2018, max_value=2022 )
            
    with col3:
        quater = st.selectbox(':orange[Please select the Quater]',
                              ('None','1', '2', '3', '4'))
        #slider
        #quater = st.slider('Please select the Quater',
         #                    min_value=0,max_value=4)
    
    if choice == 'By Map':
        indiamap_visual()
        
    elif choice == 'By Aggregated':
        sunburst_v()