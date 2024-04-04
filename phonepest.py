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
    port="5432")

cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1 = cursor.fetchall()
columns = ["states", "years", "quarter", "transactiont_type", "transaction_count", "transaction_amount"]
Aggregated_transaction= pd.DataFrame(table1, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
columns = ["states", "years", "quarter", "brands", "transaction_count", "transaction_percentage"]
Aggregated_user = pd.DataFrame(table2, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3 = cursor.fetchall()
columns = ["states", "years", "quarter", "districts", "transaction_count", "transaction_amount",]
Map_transaction = pd.DataFrame(table3, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_users")
mydb.commit()
table4 = cursor.fetchall()
columns = ["states", "years", "quarter", "districts", "registered_users", "app_opens",]
Map_users = pd.DataFrame(table4, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5 = cursor.fetchall()
columns = ["states", "years", "quarter", "pincodes","districts", "transaction_count", "transaction_amount",]
Top_transaction = pd.DataFrame(table5, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_users")
mydb.commit()
table6 = cursor.fetchall()
columns = ["states", "years", "quarter","pincodes", "registered_users"]
Top_users = pd.DataFrame(table6, columns=columns)


def tran_transaction_amount_year(option, year):

    agtr = option[option["years"] == year]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    agtrg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    coll1, coll2 = st.columns(2)

    with coll1:
        fig_transaction_amount = px.bar(agtrg, x="states", y="transaction_amount", title=f"{year} transaction_amount",
                            color="transaction_amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_transaction_amount)

        fig_ind_1 = px.choropleth(agtrg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                  color="transaction_amount", color_continuous_scale="ylgnbu",
                                  range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), hover_name="states",
                                  title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_1.update_geos(visible=False)
        #st.plotly_chart(fig_ind_1)

    with coll2:
        fig_transaction_count = px.bar(agtrg, x="states", y="transaction_count", title=f"{year} transaction_count",
                           color="transaction_amount", color_continuous_scale="tempo",
                           range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_transaction_count)

        fig_ind_2 = px.choropleth(agtrg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                  color="transaction_count", color_continuous_scale="tempo",
                                  range_color=(agtrg["transaction_count"].min(), agtrg["transaction_count"].max()), hover_name="states",
                                  title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_2.update_geos(visible=False)
        #st.plotly_chart(fig_ind_2)

    return agtr


def tran_transaction_amount_year_quarter(option1, quarter):
    agtr = option1[option1["quarter"] == quarter]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    agtrg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)


    coll3, coll4 = st.columns(2)

    with coll3:
        fig_transaction_amount = px.bar(agtrg, x="states", y="transaction_amount", title=f"{agtr['years'].min()} Year {quarter} quarter transaction_amount",
                            color="transaction_amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), height=650, width=600)
        st.plotly_chart(fig_transaction_amount)

        fig_ind_1 = px.choropleth(agtrg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                  color="transaction_amount", color_continuous_scale="ylgnbu",
                                  range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), hover_name="states",
                                  title=f"{agtr['years'].min()} Year {quarter} quarter transaction_amount", fitbounds="locations", height=650, width=600)
        fig_ind_1.update_geos(visible=False)
        st.plotly_chart(fig_ind_1)

    with coll4:
        fig_transaction_count = px.bar(agtrg, x="states", y="transaction_count", title=f"{agtr['years'].min()} Year {quarter} quarter transaction_count",
                           color="transaction_amount", color_continuous_scale="tempo",
                           range_color=(agtrg["transaction_amount"].min(), agtrg["transaction_amount"].max()), height=650, width=600)
        st.plotly_chart(fig_transaction_count)

        fig_ind_2 = px.choropleth(agtrg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                  color="transaction_count", color_continuous_scale="tempo",
                                  range_color=(agtrg["transaction_count"].min(), agtrg["transaction_count"].max()), hover_name="states",
                                  title=f"{agtr['years'].min()} Year {quarter} quarter transaction_count", fitbounds="locations", height=650, width=600)
        fig_ind_2.update_geos(visible=False)
        st.plotly_chart(fig_ind_2)

    return agtr


def transaction_type(df, states):
    agtrg = df[df["states"]==(states)]
    agtrg.reset_index(drop=True, inplace=True) 

    coll3, coll4 = st.columns(2)
    with coll3:
        fig_pie1 = px.pie(data_frame=agtrg, names="transactiont_type", values="transaction_amount",
                      width=650, title=f"{states} {agtrg['years'].min()} - {quarter} quarter transaction_amount", hole=0.40)
        st.plotly_chart(fig_pie1)

    with coll4:
        fig_pie2 = px.pie(data_frame=agtrg, names="transactiont_type", values="transaction_count",
                        width=650, title=f"{states} {agtrg['years'].min()} - {quarter} quarter transaction_count", hole=0.40)
        st.plotly_chart(fig_pie2)

    return agtrg


def brands(df, year):
    agusy = df[df["years"] == year]
    agusy.reset_index(drop=True, inplace=True)

    agusyg = agusy.groupby("brands")["transaction_count"].sum()
    agusyg = agusyg.reset_index()

    colors = px.colors.qualitative.Plotly[:len(agusyg)]

    fig_bar = px.bar(data_frame=agusyg, x="brands", y="transaction_count", hover_name="brands",
                     width=980, height=600, text_auto='.3s', title=f"{agusy['years'].min()} brands transaction_count",
                     color=agusyg["brands"], color_discrete_sequence=colors)
  
    #fig_bar.show()

    return agusy

def brandsqu(df,quarter):
    agusq = df[df["quarter"] == quarter]
    agusq.reset_index(drop=True, inplace=True)

    agusqg = pd.DataFrame(agusq.groupby("brands")["transaction_count"].sum())
    agusqg = agusqg.reset_index()

    fig_bar = px.bar(data_frame=agusqg, x="brands", y="transaction_count", hover_name="brands",
                     width=980, height=600, text_auto='.3s', title=f"All Over India's -{year}-{quarter} quarter brands wise transaction_count",
                     color=agusqg["brands"])
    
    st.plotly_chart(fig_bar)

    return agusq


def brandstates(df, states, year):
    states_df = df[(df["states"] == states) & (df["years"] == year)]
    states_df.reset_index(drop=True, inplace=True)
    
    fig = px.sunburst(states_df, path=['states','brands','transaction_count'],title=f"{states}-brands wise transaction_count",
                      hover_name="brands", values='transaction_count')    
    
    st.plotly_chart(fig)

    return states_df

def mapdisttr(df,states):
    agusst = df[df["states"] == states]
    agusst.reset_index(drop=True, inplace=True)

    agusstg = agusst.groupby("districts")[["transaction_count","transaction_amount"]].sum()
    agusstg = agusstg.reset_index()
    
    colors = px.colors.qualitative.Plotly[:len(agusst)]

    fig_bar = px.bar(data_frame=agusstg, x="districts", y="transaction_count", hover_name="districts",
                    width=980, height=600,text_auto='.3s', title=f"{states} quarter districts Wise transaction_count",
                    color="districts", color_discrete_sequence=colors)

    fig_bar1 = px.bar(data_frame=agusstg, x="districts", y="transaction_amount", hover_name="districts",
                width=980, height=600,text_auto='.3s', title=f"{states} districts Wise transaction_amount",
                color="districts", color_discrete_sequence=colors)

    st.plotly_chart(fig_bar)
    st.plotly_chart(fig_bar1)
    return agusst

def mapdistus(df, states):
    agusst = df[df["states"] == states]
    agusst.reset_index(drop=True, inplace=True)

    agusstg = agusst.groupby("districts")[["registered_users", "app_opens"]].sum()
    agusstg = agusstg.reset_index()
    
    fig = px.sunburst(agusstg, values="app_opens", path=["districts","registered_users","app_opens"],hover_data="registered_users",
                      hover_name="districts",width=980, height=600)
    
    st.plotly_chart(fig)
    return agusst 
    

def top_tran_transaction_amount_year(option, year):

    toptry = option[option["years"] == year]
    toptry.reset_index(drop=True, inplace=True)

    toptryqg = toptry.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    toptryqg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    coll3, coll4 = st.columns(2)

    with coll3:
        fig_transaction_amount = px.bar(toptryqg, x="states", y="transaction_amount", title=f"{year} transaction_amount",
                                color="transaction_amount", color_continuous_scale="ylgnbu",
                                range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_transaction_amount)

        fig_ind_1 = px.choropleth(toptryqg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_amount", color_continuous_scale="ylgnbu",
                                    range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()), hover_name="states",
                                    title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_1.update_geos(visible=False)
        #st.plotly_chart(fig_ind_1)

    with coll4:
        fig_transaction_count = px.bar(toptryqg, x="states", y="transaction_count", title=f"{year} transaction_count",
                            color="transaction_amount", color_continuous_scale="tempo",
                            range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()), height=650, width=600)
        #st.plotly_chart(fig_transaction_count)

        fig_ind_2 = px.choropleth(toptryqg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_count", color_continuous_scale="tempo",
                                    range_color=(toptryqg["transaction_count"].min(), toptryqg["transaction_count"].max()), hover_name="states",
                                    title=f"{year}", fitbounds="locations", height=650, width=600)
        fig_ind_2.update_geos(visible=False)
        #st.plotly_chart(fig_ind_2)
    return toptry


def top_tran_transaction_amount_year_quarter(option1, quarter):

    toptryq = option1[option1["quarter"] == quarter]
    toptryq.reset_index(drop=True, inplace=True)

    toptryqg = toptryq.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    toptryqg.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    coll3, coll4 = st.columns(2)

    with coll3:
        fig_transaction_amount = px.bar(toptryqg, x="states", y="transaction_amount", title=f"{quarter}-quarter transaction_amount",
                                color="transaction_amount", color_continuous_scale="ylgnbu",
                                range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()),height=600, width=700)
        st.plotly_chart(fig_transaction_amount)
        
        fig_ind_1 = px.choropleth(toptryqg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_amount", color_continuous_scale="ylgnbu",
                                    range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()), hover_name="states",
                                    title=f"{quarter}", fitbounds="locations",height=600, width=700)
        fig_ind_1.update_geos(visible=False)
        st.plotly_chart(fig_ind_1)

    with coll4:

        fig_transaction_count = px.bar(toptryqg, x="states", y="transaction_count", title=f"{quarter}-quarter transaction_count",
                            color="transaction_count", color_continuous_scale="tempo",
                            range_color=(toptryqg["transaction_amount"].min(), toptryqg["transaction_amount"].max()), height=600, width=700)
        
        st.plotly_chart(fig_transaction_count)


        fig_ind_2 = px.choropleth(toptryqg, geojson=data1, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_count", color_continuous_scale="tempo",
                                    range_color=(toptryqg["transaction_count"].min(), toptryqg["transaction_count"].max()), hover_name="states",
                                    title=f"{quarter}", fitbounds="locations", height=600, width=700)
        fig_ind_2.update_geos(visible=False)
        
        st.plotly_chart(fig_ind_2)

    return toptryq
   
def toptrpins(df, states):
    ttyqu = df[df["states"]==states]
    ttyqu.reset_index(drop=True, inplace=True)

    coll3, coll4 = st.columns(2)
    with coll3:    
        fig = px.bar(ttyqu, y="transaction_amount", x="quarter",hover_data="pincodes",color="transaction_amount",
                    hover_name="pincodes", width=650, height=600)
        st.plotly_chart(fig)

    with coll4:
        fig1 = px.bar(ttyqu, y="transaction_count", x="quarter",hover_data="pincodes",color="transaction_count", 
                    hover_name="pincodes", width=650, height=600)
        st.plotly_chart(fig1)
    return ttyqu


def tpuser(df, year):
    tpus = df[df["years"]==year]
    tpus.reset_index(drop=True, inplace=True)

    tpusg = tpus.groupby(["states", "quarter"])["registered_users"].sum().reset_index()
    tpusg.reset_index(inplace=True)
    
    fig = px.bar(tpus, y="registered_users", x="states",hover_name="states",color="quarter",title=f"{year}-registered_users ",width=900, height=650)
    st.plotly_chart(fig)
    return tpus

def topuspins(df, states):
    ttyqu = df[df["states"]==states]
    ttyqu.reset_index(drop=True, inplace=True)
  
    fig = px.bar(ttyqu, y="registered_users", x="quarter",hover_data="pincodes",color= "registered_users",
                hover_name="pincodes", width=650, height=600)   

    st.plotly_chart(fig)    
    return ttyqu

def ques_transaction_count(tabname):
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="758595",
        database="phonepe",
        port="5432")

    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,sum(transaction_count) as transaction_count
                from {tabname} group by states order by transaction_count desc limit 10;''')

    mydb.commit()
    table1 = cursor.fetchall()
    columns = ["states","transaction_count"]
    transaction_dec= pd.DataFrame(table1, columns=columns)


    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,sum(transaction_count) as transaction_count
                   from {tabname} group by states order by transaction_count limit 10;''')
    mydb.commit()
    table2 = cursor.fetchall()
    columns = ["states","transaction_count"]
    transaction_ase= pd.DataFrame(table2, columns=columns)


    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,avg(transaction_count) as transaction_count
                from {tabname} group by states order by transaction_count;''')

    mydb.commit()
    table3 = cursor.fetchall()
    columns = ["states","transaction_count"]
    transaction_avg= pd.DataFrame(table3, columns=columns)

    fig = px.bar(transaction_dec, y="transaction_count", x="states",color="states",hover_name="states",width=650, height=600)
    st.plotly_chart(fig)

    fig1 = px.bar(transaction_ase, y="transaction_count", x="states",color="states",hover_name="states",width=650, height=600)
    st.plotly_chart(fig1)

    fig2 = px.bar(transaction_avg, y="transaction_count", x="states",color="states",hover_name="states",width=1080, height=720)
    st.plotly_chart(fig2)


def ques_transaction_amount(tabname):
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="758595",
        database="phonepe",
        port="5432")

    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,sum(transaction_amount) as transaction_amount
                from {tabname} group by states order by transaction_amount desc limit 10;''')

    mydb.commit()
    table1 = cursor.fetchall()
    columns = ["states","transaction_amount"]
    transaction_dec= pd.DataFrame(table1, columns=columns)


    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,sum(transaction_amount) as transaction_amount
                   from {tabname} group by states order by transaction_amount limit 10;''')
    mydb.commit()
    table2 = cursor.fetchall()
    columns = ["states","transaction_amount"]
    transaction_ase= pd.DataFrame(table2, columns=columns)


    cursor = mydb.cursor()
    cursor.execute(f'''SELECT states,avg(transaction_amount) as transaction_amount
                from {tabname} group by states order by transaction_amount;''')

    mydb.commit()
    table3 = cursor.fetchall()
    columns = ["states","transaction_amount"]
    transaction_avg= pd.DataFrame(table3, columns=columns)

    fig = px.bar(transaction_dec, y="transaction_amount", x="states",color="states",hover_name="states",width=650, height=600)
    st.plotly_chart(fig)

    fig1 = px.bar(transaction_ase, y="transaction_amount", x="states",color="states",hover_name="states",width=800, height=650)
    st.plotly_chart(fig1)

    fig2 = px.bar(transaction_avg, y="transaction_amount", x="states",color="states",hover_name="states",width=1080, height=720)
    st.plotly_chart(fig2)

import streamlit as st

st.set_page_config(layout="wide")

with st.sidebar:
    
    st.image("PhonePe.png")
    st.caption("***:violet[Code written by Boopathi Venkatachalam]***")

    selected = option_menu("Main Menu", ["Intro",'Top Chart','Explore Data','Contact Us'], 
        icons=['house','search','gear','phone'])


if selected=="Intro":
    st.title("*:violet[Welcome to Boopathi's PhonePe] :sunglasses:*")


    st.markdown('''
    :tulip::rose::hibiscus: :violet[PhonePe] :orange[is] :green[an] :blue[Indian] :violet[multinational]
    :gray[digital] :red[payments] :green[and] :blue[financial] :violet[services]
    :gray[company] :tulip::rose::hibiscus:''')


    st.markdown(""":violet[**PhonePe is a payments app that allows you to use BHIM UPI,
                your credit card and debit card or wallet to recharge your mobile phone,
                pay all your utility bills and to make instant payments at your favourite offline and online stores.**]""")
    
    st.markdown(""":violet[**You can also invest in mutual funds and buy insurance plans on PhonePe. Get Car & Bike Insurance on our app.
                Link your bank actransaction_count on PhonePe and transfer money with BHIM UPI instantly! 
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
    systems Financial services Merchant payments Mutual funds Insurance Digital gold Payment gateway Actransaction_count 
    Aggregator Merchant Lending Hyperlocal e-commerce app built on ONDC - Pincode Stock broking app and web platform - Share.Market
    
                    
    :green[*Note: Current status - Active]""")

    import streamlit as st

    video_file = open('pulse.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)


elif selected == "Top Chart":
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="758595",
        database="phonepe",
        port="5432")

    cursor = mydb.cursor()

    question= st.selectbox("Select the Question",[ 
                "1. Top 10 State in Aggregated Transaction",

                "2. Top 10 State in Map Transaction",

                "3. Top 10 State in Top Transaction",
                 
                "4. Total transaction_amount and transaction_count of Aggregated Transaction",

                "5. Total transaction_amount and transaction_count of Map Transaction",

                "6. Total transaction_amount and transaction_count of Top Transaction",

                "7. transaction_count of Aggregated User",

                "8. Registered users of Map User",

                "9. App opens of Map User",

                "10. Registered users of Top User"])
    
    if question =="4. Total transaction_amount and transaction_count of Aggregated Transaction":
        st.subheader="Aggregated Transaction Amount"
        ques_transaction_amount("Aggregated_transaction")
        st.subheader="Aggregated Transaction Count"
        ques_transaction_count("Aggregated_transaction")

    if question =="5. Total transaction_amount and transaction_count of Map Transaction":
        st.subheader="Map Transaction Amount"
        ques_transaction_amount("Map_transaction")
        st.subheader="Map Transaction Count"
        ques_transaction_count("Map_transaction")
    
    if question =="6. Total transaction_amount and transaction_count of Top Transaction":
        st.subheader="Top Transaction Amount"
        ques_transaction_amount("Top_transaction")
        st.subheader="Map Transaction Count"
        ques_transaction_count("Top_transaction")

        


elif selected == "Explore Data":

    tab1, tab2, tab3 = st.tabs(["***Aggregated Analysis***", "***Map Analysis***", "***Top Analysis***"])  

    with tab1:
        anal = ["Aggregated_transaction", "Aggregated_user"]
        tab_selected = st.radio("Select Tab", anal)

        if tab_selected == "Aggregated_transaction":

            year = st.slider('Select a year', min_value=2018, max_value=2023, step=1, key='unique_slider_key_1')
            tacy=tran_transaction_amount_year(Aggregated_transaction,year)

            quarter = st.select_slider('Select a quarter',options=[1,2,3,4])         
            tacyq=tran_transaction_amount_year_quarter(tacy,quarter) 

            states=st.selectbox('Select a states',tacy["states"].unique())
            transaction_type(tacyq,states)


        elif tab_selected == "Aggregated_user":             
            year = st.slider('Select a year', min_value=2018, max_value=2022, step=1, key='unique_slider_key_1') 
            quart = st.select_slider('Select a quarter', options=[1, 2, 3, 4])      

            brandsf=brands(Aggregated_user, year)
            stus=brandsqu(brandsf, quart)

            states=st.selectbox('Select a states',Aggregated_user["states"].unique())
            brandstates(stus, states, year)
            

    with tab2:
        anal2 = ["Map_transaction", "Map_user"]
        tab_selected = st.radio("Select Tab", anal2)       

        if tab_selected == "Map_transaction":
            states = st.selectbox('Select a states', Aggregated_user["states"].unique(), key='states_selectbox')
            mapdisttr(Map_transaction,states)
            
        elif tab_selected == "Map_user":
            states = st.selectbox('Select a states', Aggregated_user["states"].unique(), key='states_selectbox')
            mapdistus(Map_users, states)

    with tab3:
        anal3 = ["Top_transaction", "Top_user"]
        tab_selected = st.radio("Select Tab", anal3)        

        if tab_selected == "Top_transaction":
            year = st.slider('Select a year', min_value=2018, max_value=2023, step=1, key='unique_slider_key_3')
            tty=top_tran_transaction_amount_year(Top_transaction, year)

            quarter = st.select_slider('Select a quarter',options=[1,2,3,4],key='unique_slider_key_9')
            ttyq=top_tran_transaction_amount_year_quarter(tty,quarter)

            states = st.selectbox('Select a states', Top_transaction["states"].unique(), key='states_selectbox_9')
            toptrpins(tty,states)
            
        elif tab_selected == "Top_user":
            year = st.slider('Select a year', min_value=2018, max_value=2023, step=1, key='unique_slider_key_8')
            tpusy=tpuser(Top_users, year)

            states = st.selectbox('Select a states', Top_transaction["states"].unique(), key='states_selectbox_9')
            topuspins(tpusy, states)


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
