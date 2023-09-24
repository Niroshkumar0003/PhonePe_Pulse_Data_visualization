import streamlit as st
import pymysql 
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="phonepe",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'This website helps the users to analyse the datas contains transaction by the users in india'  }
)

#st.sidebar.header(':green[Phonepe Pulse]')

# Creating connection with mysql workbench
my_db = pymysql.connect(host="localhost",
                   user="root",
                   password="12345678",
                   database= "ppp"
                  )
cursor = my_db.cursor()

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu(None, ["Home","Top Charts","Visualization"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                default_index=0,
                orientation="vertical",
                styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "-2px", "--hover-color": "#ed4a3b"},
                         "icon": {"font-size": "30px"},
                        "nav-link-selected": {"background-color": "#ed4a3b"}}) #f29dcb
    

if selected=="Home":
    image = Image.open("/Users/nirosh/Downloads/Others/phone pepng.jpeg")
    st.sidebar.image(image , width=310)
    #pic = Image.open("/Users/joesnowafc/Downloads/aamir.jpeg")
    #st.sidebar.image(pic)
    #st.image("phonepeimg.png") 
    st.title(" :violet[Phonepe Pulse Data Visualization and Exploration ]")
    st.markdown(" ")
    st.markdown(" ")
    st.image("/Users/nirosh/Downloads/Others/phonepe-upi.png",width = 600)


    #col1,col2 = st.columns([3,2],gap="medium")
    #with col1:
    st.write(" ")
    st.markdown("### :blue[Technologies used ] : Github, Python, Pandas, MYSQL, Streamlit, and Plotly.")
    st.markdown("### :blue[Overview ] : Using this website , you can visualize the data and the business of phonepe pulse by chart and visualization metrics ")

    #with col2:
        #st.write(" ")
        #st.image("/Users/joesnowafc/Downloads/aamir.jpeg")

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.image('/Users/nirosh/Downloads/Others/phonepe-upi.png')
    Type = st.sidebar.selectbox("**Type**", ("TRANSACTION", "USERS"))
    colum1,colum2 = st.columns([1.5,5],gap='large')
    #st.image('/Users/joesnowafc/Downloads/ppey.jpeg',width=1200)
    with colum1:
        Year = st.selectbox('Year',('2018','2019','2020','2021','2022'))
    with colum2:
        Quarter = st.selectbox("Quarter",('1','2','3','4'))
        
    if Type == "TRANSACTION":

        #st.image('/Users/joesnowafc/Downloads/ppey.jpeg',width=1200)
        col1,col2,col3 = st.columns([1.5,1.5,1.5],gap='large')
        
        with col1:
            cursor.execute(f"select Transaction_type as type,sum(Transaction_count) as Total_no_of_transactions,sum(Transaction_amount) as Total_amount from agg_trans where year = {Year} and quarter={Quarter} group by type order by Total_amount desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(),columns=['Transaction_type','Transaction_count','Total_amount'])
            chart = px.bar(df,x='Transaction_type',y='Total_amount',color='Transaction_type',title="TRANSACTION TYPE")
            #colors = ['limegreen','limegreen','limegreen','limegreen','limegreen']
            #chart.update_traces(marker_color = colors)
            st.plotly_chart(chart,use_container_width=True)

        with col2:
            cursor.execute(f"select State as state,sum(Count) as Total_no_of_transactions,sum(Amount) as Total_amount from map_trans where year = {Year} and quarter={Quarter} group by state order by Total_amount desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(),columns = ['State','Transaction_count','Total_amount'])
            chart = px.bar(df,x='State',y='Total_amount',color = 'State',title='            TOP 10 STATES')
            #colors = ['skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue']
            #chart.update_traces(marker_color = colors)
            st.plotly_chart(chart,use_container_width=True)

        with col3:            
            cursor.execute(f"select District as district,sum(Count) as Total_no_of_transactions,sum(Amount) as Total_amount from map_trans where year = {Year} and quarter={Quarter} group by district order by Total_amount desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(),columns=['District','Transaction_count','Total_amount'])
            chart = px.bar(df,x='District',y='Total_amount',color = 'District',title='         TOP 10 DISTRICTS')
            #colors = ['violet','violet','violet','violet','violet','violet','violet','violet','violet','violet']
            #chart.update_traces(marker_color = colors)
            st.plotly_chart(chart,use_container_width=True)

    
    if Type == "USERS":
        #st.image('/Users/joesnowafc/Downloads/ppey.jpeg',width=1200)
        col1,col2,col3 = st.columns([2,2,2],gap='large')

        with col1:
            
            if Year == "2022" and Quarter in ['2','3','4']:
                st.markdown("#### :red[Sorry No Data found  ❗️❗️❗️]")
                st.write("#### :green[Try with dfferent Timeframe ♨︎ ]")
            else:
                cursor.execute(f"select Brand, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by Brand order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                chart = px.bar(df,x='Brand',y='Total_Users',color = 'Brand',title='            TOP 10 BRANDS')
                #colors = ['limegreen','limegreen','limegreen','limegreen','limegreen','limegreen','limegreen','limegreen','limegreen','limegreen']
                #chart.update_traces(marker_color = colors)
                st.plotly_chart(chart,use_container_width=True) 

        with col2:
            cursor.execute(f"select State as state,sum(RegisteredUsers) as Total_users,sum(Appopens) as Total_Appopens from map_user where year={Year} and quarter={Quarter} group by state order by Total_users desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_users','Total_Appopens'])
            df.Total_Users = df.Total_users.astype(float)
            chart = px.bar(df,x='State',y='Total_users',color = 'State',title='TOP 10 STATES')
            #colors = ['skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue','skyblue']
            #chart.update_traces(marker_color = colors)
            st.plotly_chart(chart,use_container_width=True)

        with col3:
            cursor.execute(f"select District as district,sum(RegisteredUsers) as Total_users,sum(Appopens) as Total_Appopens from map_user where year={Year} and quarter={Quarter} group by district order by Total_users desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_users','Total_Appopens'])
            df.Total_Users = df.Total_users.astype(float)
            chart = px.bar(df,x='District',y='Total_users',color = 'District' ,title='TOP 10 DISTRICTS')
            #colors = ['violet','violet','violet','violet','violet','violet','violet','violet','violet','violet']
            #chart.update_traces(marker_color = colors)
            st.plotly_chart(chart,use_container_width=True)

                                            #####################VISUALIZATION#########################
if selected == "Visualization":
    st.image('/Users/nirosh/Downloads/Others/phonepe-upi.png',width=900)
    Type = st.sidebar.selectbox("**Type**", ("TRANSACTION", "USERS"))
    col1,col2 = st.columns([1.5,5],gap='large')

    with col1:
        Year = st.selectbox('Year',('2018','2019','2020','2021','2022'))
    with col2:
        Quarter = st.selectbox("Quarter",('1','2','3','4'))

    if Type == "TRANSACTION":


        with st.sidebar:
            selected = option_menu(None, ["Agg_Transaction","Map_Transaction","Top_Transaction"], 
                icons=["graph-up-arrow","bi bi-geo-alt", "bi bi-trophy"],
                default_index=0,
                orientation="vertical",
                styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "-2px", "--hover-color": "#ed4a3b"},
                         "icon": {"font-size": "30px"},
                        "nav-link-selected": {"background-color": "#ed4a3b"}}) #f29dcb
        
        
        if selected == "Agg_Transaction":
                #Transaction amount on indian map 
            
            cursor.execute(f"select State as state,sum(Count) as Total_counts,sum(Amount) as Total_amount from map_trans where year = {Year} and quarter={Quarter} group by state order by state;")
            df = pd.DataFrame(cursor.fetchall(),columns=['State','Total_counts','Total_amount'])
            df2 = pd.read_csv('/Users/nirosh/Downloads/pp/Statenames.csv')
            df.State = df2
            fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_amount',
                    width=1200,
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

        
        if selected == "Map_Transaction":
            cursor.execute(f"select state as state, sum(count) as Total_transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_transactions', 'Total_amount'])
            df2 = pd.read_csv('/Users/nirosh/Downloads/pp/Statenames.csv')
            df.Total_transactions = df.Total_transactions.astype(int)
            df.State = df2

            fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_transactions',
                    width=1200,
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

        if selected == "Top_Transaction":

            col1,col2 = st.columns([2,2],gap='large')

            with col1:


                cursor.execute(f"select State as state,sum(Transaction_count) as Total_no_of_transactions,sum(Transaction_amount) as Total_amount from top_trans where Year={Year} and Quarter={Quarter} group by 1 order by 3 desc limit 10;")
                df = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_transactions', 'Total_amount'])
                df.Total_transactions = df.Total_transactions.astype(float)
                df.Total_amount = df.Total_amount.astype(float)
                chart = px.bar(df,x='State',y='Total_amount',color = 'State',title='TOP 10 STATES',height=500,width=100)
                
                #chart.update_traces(marker_color = color)
                st.plotly_chart(chart,use_container_width=True)
                

            with col2:
                cursor.execute(f"select State as state,Pincode ,sum(Transaction_count) as Total_no_of_transactions,sum(Transaction_amount) as Total_amount from top_trans where Year={Year} and Quarter={Quarter} group by 2,1 order by 4 desc limit 10;")
                df = pd.DataFrame(cursor.fetchall(),columns= ['State','Pincode', 'Total_transactions', 'Total_amount'])
                df.Total_transactions = df.Total_transactions.astype(float)
                df.Total_amount = df.Total_amount.astype(float)
                df.Pincode = df.Pincode.astype(str)
                chart = px.bar(df,x='State',y='Total_amount',color = 'Pincode',title='TOP 10 STATES & PINCODES',height=500,width=100)
                
                #chart.update_traces(marker_color = color)
                st.plotly_chart(chart,use_container_width=True)
    
    
    if Type == "USERS":

        with st.sidebar:
            selected = option_menu(None, ["Agg_Users","Map_Users","Top_Users"], 
                icons=["graph-up-arrow","bi bi-geo-alt", "bi bi-trophy"],
                default_index=0,
                orientation="vertical",
                styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "-2px", "--hover-color": "#ed4a3b"},
                         "icon": {"font-size": "30px"},
                        "nav-link-selected": {"background-color": "#ed4a3b"}}) #f29dcb
            
        if selected == "Agg_Users":

            cursor.execute(f"select State , Brand , sum(Count) as Total_count from agg_user where Year = {Year} and Quarter = {Quarter} group by 1,2 order by 3 desc ")
            df = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Brand', 'Total_count'])
            df.Total_count = df.Total_count.astype(float)
            chart = px.bar(df,x='Brand',y='Total_count',color = 'State',title='TOP 10 BRANDS & STATES',height=500,width=100)
                
            #chart.update_traces(marker_color = color)
            st.plotly_chart(chart,use_container_width=True)

        if selected == "Map_Users":

            st.markdown("## :violet[Select any State to get District wise Data]")

            with st.sidebar:
                selected_state = option_menu(None, ['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
                
            cursor.execute(f"select State , District , sum(RegisteredUsers) as Total_user from map_user where Year = {Year} and Quarter = {Quarter} anD State = '{selected_state}' group by 1,2 order by 3 desc ;")
            df = pd.DataFrame(cursor.fetchall(),columns= ['State', 'District', 'Total_user'])
            df.Total_user = df.Total_user.astype(float)
            chart = px.bar(df,x='District',y='Total_user',color = 'District',title='TOP 10 DISTRICTS & STATES',height=500,width=100)
                
            #chart.update_traces(marker_color = color)
            st.plotly_chart(chart,use_container_width=True)

        if selected == "Top_Users":

            st.markdown("## :violet[Select any State to get Pincode wise Data]")

            with st.sidebar:
                selected_state = option_menu(None, ['andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
                
            cursor.execute(f"select State , Pincode , sum(RegisteredUsers) as Total_users from top_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by 1,2 order by 3 desc ;")
            df = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Pincode', 'Total_user'])
            df.Total_user = df.Total_user.astype(float)
            df.Pincode = df.Pincode.astype(str)
            chart = px.bar(df,x='Pincode',y='Total_user',color = 'Pincode',title='TOP 10 PINCODE & STATES',height=500,width=1000)
                
            #chart.update_traces(marker_color = color)
            st.plotly_chart(chart,use_container_width=True)

