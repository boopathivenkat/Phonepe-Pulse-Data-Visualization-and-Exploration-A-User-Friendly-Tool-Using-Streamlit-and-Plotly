import json
import os
import pandas as pd
import plotly.express as px
import mysql.connector
from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import numpy as np
import plotly.figure_factory as ff
import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="758595",
    database="phonepe",
    port="5432"
)

cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Transaction Type", "Transaction Count", "Transaction Amount"]
Aggregated_transaction= pd.DataFrame(table1, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Brands", "Transaction Count", "Transaction Percentage"]
Aggregated_user = pd.DataFrame(table2, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts", "Transaction Count", "Transaction Amount",]
Map_transaction = pd.DataFrame(table3, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_users")
mydb.commit()
table4 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts", "Registered Users", "App Opens",]
Map_users = pd.DataFrame(table4, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts","Pincodes", "Transaction Count", "Transaction Amount",]
Top_transaction = pd.DataFrame(table5, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_users")
mydb.commit()
table6 = cursor.fetchall()
columns = ["State", "Years", "Quarter","Pincodes", "Districts", "Count","Amount"]
Top_users = pd.DataFrame(table6, columns=columns)


def tran_amount_year(option, year):

    agtr = option[option["Years"] == year]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("State")[["Transaction Count", "Transaction Amount"]].sum()
    agtrg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    coll1, coll2 = st.columns(2)

    with coll1:
        fig_amount = px.bar(agtrg, x="State", y="Transaction Amount", title=f"{year} Transaction Amount",
                            color="Transaction Amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_amount)

        fig_ind_1 = px.choropleth(agtrg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                  color="Transaction Amount", color_continuous_scale="ylgnbu",
                                  range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), hover_name="State",
                                  title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_1.update_geos(visible=False)
        #st.plotly_chart(fig_ind_1)

    with coll2:
        fig_count = px.bar(agtrg, x="State", y="Transaction Count", title=f"{year} Transaction Count",
                           color="Transaction Amount", color_continuous_scale="tempo",
                           range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_count)

        fig_ind_2 = px.choropleth(agtrg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                  color="Transaction Count", color_continuous_scale="tempo",
                                  range_color=(agtrg["Transaction Count"].min(), agtrg["Transaction Count"].max()), hover_name="State",
                                  title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_2.update_geos(visible=False)
        #st.plotly_chart(fig_ind_2)

    return agtr


def tran_amount_year_quarter(option1, quarter):
    agtr = option1[option1["Quarter"] == quarter]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("State")[["Transaction Count", "Transaction Amount"]].sum()
    agtrg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)


    coll3, coll4 = st.columns(2)

    with coll3:
        fig_amount = px.bar(agtrg, x="State", y="Transaction Amount", title=f"{agtr['Years'].min()} Year {quarter} Quarter Transaction Amount",
                            color="Transaction Amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), height=650, width=600)
        st.plotly_chart(fig_amount)

        fig_ind_1 = px.choropleth(agtrg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                  color="Transaction Amount", color_continuous_scale="ylgnbu",
                                  range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), hover_name="State",
                                  title=f"{agtr['Years'].min()} Year {quarter} Quarter Transaction Amount", fitbounds="locations", height=650, width=600)
        fig_ind_1.update_geos(visible=False)
        st.plotly_chart(fig_ind_1)

    with coll4:
        fig_count = px.bar(agtrg, x="State", y="Transaction Count", title=f"{agtr['Years'].min()} Year {quarter} Quarter Transaction Count",
                           color="Transaction Amount", color_continuous_scale="tempo",
                           range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), height=650, width=600)
        st.plotly_chart(fig_count)

        fig_ind_2 = px.choropleth(agtrg, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                                  color="Transaction Count", color_continuous_scale="tempo",
                                  range_color=(agtrg["Transaction Count"].min(), agtrg["Transaction Count"].max()), hover_name="State",
                                  title=f"{agtr['Years'].min()} Year {quarter} Quarter Transaction Count", fitbounds="locations", height=650, width=600)
        fig_ind_2.update_geos(visible=False)
        st.plotly_chart(fig_ind_2)

    return agtr


def transaction_type(df, states):
    agtrg = df[df["State"]==(states)]
    agtrg.reset_index(drop=True, inplace=True) 

    coll3, coll4 = st.columns(2)
    with coll3:
        fig_pie1 = px.pie(data_frame=agtrg, names="Transaction Type", values="Transaction Amount",
                      width=650, title=f"{states} {agtrg['Years'].min()} - {quarter} Quarter Transaction Amount", hole=0.40)
        st.plotly_chart(fig_pie1)

    with coll4:
        fig_pie2 = px.pie(data_frame=agtrg, names="Transaction Type", values="Transaction Count",
                        width=650, title=f"{states} {agtrg['Years'].min()} - {quarter} Quarter Transaction Count", hole=0.40)
        st.plotly_chart(fig_pie2)

    return agtrg

import streamlit as st
import pandas as pd
import plotly.express as px

def brands(df, year):
    agusy = df[df["Years"] == year]
    agusy.reset_index(drop=True, inplace=True)

    agusyg = agusy.groupby("Brands")["Transaction Count"].sum()
    agusyg = agusyg.reset_index()

    colors = px.colors.qualitative.Plotly[:len(agusyg)]

    fig_bar = px.bar(data_frame=agusyg, x="Brands", y="Transaction Count", hover_name="Brands",
                     width=980, height=600, text_auto='.3s', title=f"{agusy['Years'].min()} Brands Transaction Count",
                     color=agusyg["Brands"], color_discrete_sequence=colors)
  
    #fig_bar.show()

    return agusy

def brandsqu(df,quarter):
    agusq = df[df["Quarter"] == quarter]
    agusq.reset_index(drop=True, inplace=True)

    agusqg = pd.DataFrame(agusq.groupby("Brands")["Transaction Count"].sum())
    agusqg = agusqg.reset_index()

    fig_bar = px.bar(data_frame=agusqg, x="Brands", y="Transaction Count", hover_name="Brands",
                     width=980, height=600, text_auto='.3s', title=f"All Over India's -{year}-{quarter} Quarter Brands wise Transaction Count",
                     color=agusqg["Brands"])
    
    st.plotly_chart(fig_bar)

    return agusq


def brandstate(df, state, year):
    state_df = df[(df["State"] == state) & (df["Years"] == year)]
    state_df.reset_index(drop=True, inplace=True)
    
    fig = px.sunburst(state_df, path=['State','Brands','Transaction Count'],title=f"{state}-Brands wise Transaction Count",
                      hover_name="Brands", values='Transaction Count')    
    st.plotly_chart(fig)

    return state_df



import streamlit as st

st.set_page_config(layout="wide")

with st.sidebar:
    
    st.image("PhonePe.png")
    st.caption("***:violet[Code written by Boopathi Venkatachalam]***")
    st.subheader('', divider='rainbow')

    selected = option_menu("Main Menu", ["Intro",'Top chart','Explore Data','Contact Us'], 
        icons=['house','search','gear','phone'])

if selected=="Intro":
    st.title("*:violet[Welcome to Boopathi's PhonePe] :sunglasses:*")
    st.subheader('', divider='rainbow')

    st.markdown('''
    :tulip::rose::hibiscus: :violet[PhonePe] :orange[is] :green[an] :blue[Indian] :violet[multinational]
    :gray[digital] :red[payments] :green[and] :blue[financial] :violet[services]
    :gray[company] :tulip::rose::hibiscus:''')
    st.subheader('', divider='rainbow')

    st.markdown(""":violet[**PhonePe is a payments app that allows you to use BHIM UPI,
                your credit card and debit card or wallet to recharge your mobile phone,
                pay all your utility bills and to make instant payments at your favourite offline and online stores.**]""")
    
    st.markdown(""":violet[**You can also invest in mutual funds and buy insurance plans on PhonePe. Get Car & Bike Insurance on our app.
                Link your bank account on PhonePe and transfer money with BHIM UPI instantly! 
                The PhonePe app is safe and secure, meets all your payment, investment, mutual funds,
                insurance and banking needs, and is much**]""")
    
    st.markdown("""
            
    **Type of business -**	Private 
                    
    **Type of site -** Digital payments & Financial services

    **Founded -**	 2015 ( 9 years ago )

    **Headquarters -** Salarpuria Softzone, Bangalore , Karnataka, India.

    **Founder(s)-** Sameer Nigam , (Co-Founder & CEO) Rahul Chari
                    
    **Revenue -** 	Increase ₹16.46 billion (US$206 million) (FY 2021–22)
                    
    **Parent -**  Walmart
                    
    **URL -**	phonepe.com
                    
    **Commercial -** Yes
                    
    **Registration Users -** 500 million
                
                    
    **Industry -** Internet, E-commerce, Fintech, Financial services, Mutual funds, Insurance, Digital gold, 
    Payment gateway, ONDC, Lending, Wealth Management.
                    
    **Services -** Digital payments Mobile payments Payment 
    systems Financial services Merchant payments Mutual funds Insurance Digital gold Payment gateway Account 
    Aggregator Merchant Lending Hyperlocal e-commerce app built on ONDC - Pincode Stock broking app and web platform - Share.Market
    
                    
    :green[*Note: Current status - Active]""")
    st.divider()
    import streamlit as st

    video_file = open('pulse.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.divider()


elif selected == "Explore Data":

    tab1, tab2, tab3 = st.tabs(["***Aggregated***", "***Map***", "***Top***"])  

    with tab1:
        anal = ["Aggregated_transaction", "Aggregated_user"]
        tab_selected = st.radio("Select Tab", anal)

        if tab_selected == "Aggregated_transaction":

            year = st.slider('Select a year', min_value=2018, max_value=2023, step=1, key='unique_slider_key_1')
            tacy=tran_amount_year(Aggregated_transaction,year)

            quarter = st.select_slider('Select a Quarter',options=[1,2,3,4])         
            tacyq=tran_amount_year_quarter(tacy,quarter) 

            state=st.selectbox('Select a State',tacy["State"].unique())
            transaction_type(tacyq,state)


        elif tab_selected == "Aggregated_user":             
            year = st.slider('Select a year', min_value=2018, max_value=2022, step=1, key='unique_slider_key_1') 
            quart = st.select_slider('Select a Quarter', options=[1, 2, 3, 4])      

            brandsf=brands(Aggregated_user, year)
            stus=brandsqu(brandsf, quart)

            state=st.selectbox('Select a State',Aggregated_user["State"].unique())
            brandstate(stus, state, year)
            

    with tab2:
        anal2 = ["Map_transaction", "Map_user"]
        tab_selected = st.radio("Select Tab", anal2)
       

        if tab_selected == "Map_transaction":
            #tran_amount_year(Map_transaction,year1)
            pass
            
        elif tab_selected == "Map_user":
            pass

    with tab3:
        anal3 = ["Top_transaction", "Top_user"]
        tab_selected = st.radio("Select Tab", anal3)
        year1 = st.slider('Select a year', min_value=2018, max_value=2023, step=1, key='unique_slider_key_3')

        if tab_selected == "Top_transaction":
            tran_amount_year(Top_transaction,year1)
            
        elif tab_selected == "Top_user":
            pass

            
elif selected=="Top chart":
    pass


elif selected=="Contact Us":
    
    st.title("Contact Us")
    st.divider()
    coll1, coll2 = st.columns(2)

    with coll1: 
        st.subheader('Boopathi Venkatachalam :sunglasses:')
        st.caption('Mobile:- 9751959575, E-Mail - boopathi762000@gmail.com')

        st.caption(":red[Note: * fill all mandatory fields]")     
        Name = st.text_input("Name*")
        Mobile = st.text_input("Mobile*")
        Email = st.text_input("Email*")
        Message = st.text_area("Message (optional)")

        from streamlit_star_rating import st_star_rating
        st.caption(":violet[* Please rate you experience]")  
        st_star_rating(label = " ", maxValue = 5, defaultValue = 3, key = "rating", emoticons = True )

        if st.button("Submit"):
            st.success('''Thank you for your Valuable Rationg and Message !
                        We will get back to you soon''')
    
        st.divider()  


    with coll2:
        st.image('photo.jpg')
        st.link_button("Git Hub", "https://streamlit.io/gallery")
        st.link_button("Linked in", "https://streamlit.io/gallery")
        st.link_button("Whatsapp", "https://streamlit.io/gallery")
        st.link_button("E-Mail", "https://streamlit.io/gallery")


  
    st.subheader('Phonepe Pulse Data Visualisation')

    st.markdown('''The goal of this project is to extract data from the Phonepe pulse Github repository,
                 transform and clean the data,insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python.
                 The dashboard will display the data in an interactive and visually appealing manner, with atleast 10 different dropdown options for users to select differentfacts and figures to display.
                 The solution must be secure, efficient,and user-friendly,providing valuable insights and informationabout the data in the Phonepe pulse Github repository.''')
    st.divider()
