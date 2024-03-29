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


import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff


def tran_amount_year(option,year):

    agtr = option[option["Years"] == year]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("State")[["Transaction Count", "Transaction Amount"]].sum()
    agtrg.reset_index(inplace=True)

    coll1,coll2= st.columns(2)
    
    with coll1:
        fig_amount = px.bar(agtrg, x="State", y="Transaction Amount", title=f"{year} Transaction Amount",
                            color="Transaction Amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()),height=650,width=600)
        st.plotly_chart(fig_amount)

    with coll2:
        fig_count = px.bar(agtrg, x="State", y="Transaction Count", title=f"{year} Transaction Count",
                           color="Transaction Amount",color_continuous_scale="tempo",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()),height=650,width=600)
        st.plotly_chart(fig_count)
        

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for features in data1["features"]:
        state_name.append(features["properties"]["ST_NM"])

    state_name.sort()

    coll3,coll4= st.columns(2)

    with coll3:
        fig_ind_1=px.choropleth(agtrg,geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction Amount", color_continuous_scale="ylgnbu",
                                range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), hover_name="State",
                                title=f"{year}",fitbounds="locations",height=600,width=600)
        
        fig_ind_1.update_geos(visible=False)    
        st.plotly_chart(fig_ind_1)

    with coll4:
        fig_ind_2=px.choropleth(agtrg,geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                color="Transaction Count", color_continuous_scale="tempo",
                                range_color=(agtrg["Transaction Count"].min(), agtrg["Transaction Count"].max()), hover_name="State",
                                title=f"{year}",fitbounds="locations",height=600,width=600)
        
        fig_ind_2.update_geos(visible=False)    
        st.plotly_chart(fig_ind_2)


with st.sidebar:
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/PhonePe_Logo.svg/300px-PhonePe_Logo.svg.png")
    st.caption("***Code Written by Boopathi Venkatachalam***")
    st.subheader('', divider='rainbow')

    selected = option_menu("Main Menu", ["Intro",'Top chart','Explore Data','Contact Us'], 
        icons=['play-btn','search','info-circle','search','info-circle'])

if selected=="Intro":
    st.title("*Welcome to Boopathi's PhonePe*")
    st.subheader('', divider='rainbow')

    st.markdown('''
    :tulip::rose::hibiscus: :rainbow[PhonePe] :orange[is] :green[an] :blue[Indian] :violet[multinational]
    :gray[digital] :red[payments] :green[and] :blue[financial] :violet[services]
    :gray[company] :tulip::rose::hibiscus:''')
    st.subheader('', divider='rainbow')

    st.markdown("""              
                **PhonePe is a payments app that allows you to use BHIM UPI,
                your credit card and debit card or wallet to recharge your mobile phone,
                pay all your utility bills and to make instant payments at your favourite offline and online stores.**""")
    
    st.markdown("""**You can also invest in mutual funds and buy insurance plans on PhonePe. Get Car & Bike Insurance on our app.
                Link your bank account on PhonePe and transfer money with BHIM UPI instantly! 
                The PhonePe app is safe and secure, meets all your payment, investment, mutual funds,
                insurance and banking needs, and is much**""")
    
    st.markdown("""
            
    **Type of business -**	Private 
                    
    **Type of site -** Digital payments & Financial services

    **Founded -**	 2015 ( 9 years ago )

    **Headquarters -** Salarpuria Softzone, Bengaluru, Karnataka, India

    **Founder(s)-** Sameer Nigam , (Co-Founder & CEO) Rahul Chari
                    
    **Revenue -** 	Increase ₹16.46 billion (US$206 million) (FY 2021–22)
                    
    **Parent -**  Walmart
                    
    **URL -**	phonepe.com
                    
    **Commercial -** Yes
                    
    **Registration Users -** 500 million
                
                    
    **Industry -** Internet, E-commerce, Fintech, Financial services, Mutual funds, Insurance, Digital gold, 
    Payment gateway, ONDC, Lending, Wealth Management.
                    
    **Services -** Digital paymentsMobile paymentsPayment 
    systemsFinancial servicesMerchant paymentsMutual fundsInsuranceDigital goldPayment gatewayAccount 
    AggregatorMerchant LendingHyperlocal e-commerce app built on ONDC - PincodeStock broking app and web platform - Share.Market
    
                    
    :green[*Note: Current status - Active]""")

    st.divider()


elif selected == "Top chart":

    tab1, tab2, tab3 = st.tabs(["Aggregated", "Map", "Top"])
    year = st.select_slider('Select a year',options=[2018,2019,2020,2021,2022,2023])
  

    with tab1:
        anal = ["Aggregated_transaction", "Aggregated_user"]
        tab_selected = st.radio("Select Tab", anal)

        if tab_selected == "Aggregated_transaction":
            tran_amount_year(Aggregated_transaction,year)

        elif tab_selected == "Aggregated_user":
            pass

    with tab2:
        anal2 = ["Map_transaction", "Map_user"]
        tab_selected = st.radio("Select Tab", anal2)

        if tab_selected == "Map_transaction":
            tran_amount_year(Map_transaction,year)
            
        elif tab_selected == "Map_user":
            pass

    with tab3:
        anal3 = ["Top_transaction", "Top_user"]
        tab_selected = st.radio("Select Tab", anal3)

        if tab_selected == "Top_transaction":
            tran_amount_year(Top_transaction,year)
            
        elif tab_selected == "Top_user":
            pass

            
elif selected=="Explore Data":
    pass


elif selected=="Contact Us":
    st.title("Contact Us")
    st.subheader('Boopathi Venkatachalam :sunglasses:')
    st.caption('Mobile:- 9751959575, E-Mail - boopathi762000@gmail.com')
    st.divider()

    st.caption("Any Enquiry")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")


    if st.button("Submit"):
        st.success("Thank you for your message! We will get back to you soon.")


