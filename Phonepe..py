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

path1 = r'C:/Users/boopa/Downloads/pulse-master/data/aggregated/transaction/country/india/state/'
agg_trans_list = os.listdir(path1)

column1={"States":[],"Years":[],"Quarter":[],"Transaction_type":[],"Transaction_count":[],"Transaction_amount":[]}

for state in agg_trans_list:
    current_states=path1+state+"/"
    agg_year_list=os.listdir(current_states)

    for year in agg_year_list:
        current_year=current_states+year+"/"
        agg_file_list=os.listdir(current_year)

        for file in agg_file_list:
            current_file=current_year+file
            data=open(current_file,"r")

            ag_tr=json.load(data)
            
            for i in ag_tr["data"]["transactionData"]:
                name=i["name"]
                count=i["paymentInstruments"][0]["count"]
                amount=i["paymentInstruments"][0]["amount"]
                column1["Transaction_type"].append(name)
                column1["Transaction_count"].append(count)
                column1["Transaction_amount"].append(amount)
                column1["States"].append(state)
                column1["Years"].append(year)
                column1["Quarter"].append(int(file.strip(".json")))

aggregated_trdf=pd.DataFrame(column1)


aggregated_trdf["States"]=aggregated_trdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
aggregated_trdf["States"]=aggregated_trdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
aggregated_trdf["States"]=aggregated_trdf["States"].str.title()
aggregated_trdf["States"]=aggregated_trdf["States"].str.replace("-", " ")
aggregated_trdf['Years'] = aggregated_trdf['Years'].astype(int)


path2 = r'C:/Users/boopa/Downloads/pulse-master/data/aggregated/user/country/india/state/'
agg_user_list = os.listdir(path2)

column2={"States":[],"Years":[],"Quarter":[],"Brands":[],"Transaction_count":[],"Percentage":[]}

for state in agg_user_list:
    current_states=path2+state+"/"
    agg_year_list=os.listdir(current_states)

    for year in agg_year_list:
        current_year=current_states+year+"/"
        agg_file_list=os.listdir(current_year)

        for file in agg_file_list:
            current_file=current_year+file
            data=open(current_file,"r")

            

            try:
                ag_us=json.load(data) 
                                      
                for i in ag_us["data"]["usersByDevice"]:
                    brand=i["brand"]
                    count=i["count"]
                    amount=i["percentage"]
                    column2["Brands"].append(brand)
                    column2["Transaction_count"].append(count)
                    column2["Percentage"].append(amount)
                    column2["States"].append(state)
                    column2["Years"].append(year)
                    column2["Quarter"].append(int(file.strip(".json")))
            except:
                pass

aggregated_usdf=pd.DataFrame(column2)


aggregated_usdf["States"]=aggregated_usdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
aggregated_usdf["States"]=aggregated_usdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
aggregated_usdf["States"]=aggregated_usdf["States"].str.title()
aggregated_usdf["States"]=aggregated_usdf["States"].str.replace("-", " ")
aggregated_usdf['Years'] = aggregated_usdf['Years'].astype(int)


path3 = r'C:/Users/boopa/Downloads/pulse-master/data/map/transaction/hover/country/india/state/'
map_tran_list = os.listdir(path3)

column3={"States":[],"Years":[],"Quarter":[],"District":[],"Count":[],"Amount":[]}

for state in map_tran_list:
    current_states=path3+state+"/"
    map_year_list=os.listdir(current_states)

    for year in map_year_list:
        current_year=current_states+year+"/"
        map_file_list=os.listdir(current_year)

        for file in map_file_list:
            current_file=current_year+file
            data=open(current_file,"r")

            map_tr=json.load(data)
            
            for i in map_tr["data"]["hoverDataList"]:
                district=i["name"]
                count=i["metric"][0]["count"]
                amount=i["metric"][0]["amount"]
                column3["District"].append(district)
                column3["Count"].append(count)
                column3["Amount"].append(amount)
                column3["States"].append(state)
                column3["Years"].append(year)
                column3["Quarter"].append(int(file.strip(".json")))

map_trdf=pd.DataFrame(column3)


map_trdf["States"]=map_trdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
map_trdf["States"]=map_trdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
map_trdf["States"]=map_trdf["States"].str.title()
map_trdf["States"]=map_trdf["States"].str.replace("-", " ")
map_trdf['Years'] = map_trdf['Years'].astype(int)


path4 = r'C:/Users/boopa/Downloads/pulse-master/data/map/user/hover/country/india/state/'
map_user_list = os.listdir(path4)

column4 = {"States": [], "Years": [], "Quarter": [], "Districts": [], "Registered_Users": [], "App_Opens": []}

for state in map_user_list:
    current_states = os.path.join(path4, state)
    map_year_list = os.listdir(current_states)
    
    for year in map_year_list:
        current_year = os.path.join(current_states, year)
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = os.path.join(current_year, file)
            with open(current_file, "r") as data:
                try:
                    map_us = json.load(data)
                    
                    for i in map_us["data"]["hoverData"].items():
                        district = i[0]
                        reguser = i[1]["registeredUsers"]
                        appopen = i[1]["appOpens"]
                        column4["Districts"].append(district)
                        column4["App_Opens"].append(appopen)
                        column4["Registered_Users"].append(reguser)
                        column4["States"].append(state)
                        column4["Years"].append(year)
                        column4["Quarter"].append(int(file.strip(".json")))

                except:
                    pass
                   
map_usdf=pd.DataFrame(column4)


map_usdf["States"]=map_usdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
map_usdf["States"]=map_usdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
map_usdf["States"]=map_usdf["States"].str.title()
map_usdf["States"]=map_usdf["States"].str.replace("-", " ")
map_usdf['Years'] = map_usdf['Years'].astype(int)


path5 = r'C:/Users/boopa/Downloads/pulse-master/data/top/transaction/country/india/state/'
top_tran_list = os.listdir(path5)

column5 = {"States": [], "Years": [], "Quarter": [], "Pincodes":[],"Districts": [], "Count": [], "Amount": []}

for state in top_tran_list:
    current_states = os.path.join(path5, state)
    map_year_list = os.listdir(current_states)
    
    for year in map_year_list:
        current_year = os.path.join(current_states, year)
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = os.path.join(current_year, file)
            with open(current_file, "r") as data:

                try:                                      
                    top_tr = json.load(data)
                    
                    for i in top_tr["data"]["pincodes"]:
                        pincodes = i["entityName"]
                        districts = top_tr["data"]["districts"][0]["entityName"]
                        count = i["metric"]["count"]
                        amount = i["metric"]["amount"]
                        column5["Pincodes"].append(pincodes)
                        column5["Districts"].append(districts)
                        column5["Count"].append(count)
                        column5["Amount"].append(amount)
                        column5["States"].append(state)
                        column5["Years"].append(year)
                        column5["Quarter"].append(int(file.strip(".json")))
                except:
                    pass

top_trdf = pd.DataFrame(column5)


top_trdf["States"]=top_trdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
top_trdf["States"]=top_trdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
top_trdf["States"]=top_trdf["States"].str.title()
top_trdf["States"]=top_trdf["States"].str.replace("-", " ")
top_trdf['Years'] = top_trdf['Years'].astype(int)


path6 = r'C:/Users/boopa/Downloads/pulse-master/data/top/user/country/india/state/'

top_user_list = os.listdir(path6)

column6={"States":[],"Years":[],"Quarter":[], "Pincodes":[],"Districts":[],"Count":[],"Amount":[]}

for state in top_tran_list:
    current_states = os.path.join(path5, state)
    map_year_list = os.listdir(current_states)
    
    for year in map_year_list:
        current_year = os.path.join(current_states, year)
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = os.path.join(current_year, file)
            with open(current_file, "r") as data:
                    
                    try:
                        top_us = json.load(data)
                                
                        for i in top_us["data"]["pincodes"]:
                            pincodes=i["entityName"]
                            for district in top_us["data"]["districts"]:
                                districts = district["entityName"]
                                count = district["metric"]["count"]
                                amount = district["metric"]["amount"]
                                column6["Pincodes"].append(pincodes)
                                column6["Districts"].append(districts)
                                column6["Count"].append(count)
                                column6["Amount"].append(amount)
                                column6["States"].append(state)
                                column6["Years"].append(year)
                                column6["Quarter"].append(int(file.strip(".json")))
                    except:
                         pass


top_usdf=pd.DataFrame(column6)


top_usdf["States"]=top_usdf["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar ")
top_usdf["States"]=top_usdf["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
top_usdf["States"]=top_usdf["States"].str.title()
top_usdf["States"]=top_usdf["States"].str.replace("-", " ")
top_usdf['Years'] = top_usdf['Years'].astype(int)



engine = create_engine("postgresql+psycopg2://postgres:758595@localhost:5432/phonepe")

aggregated_trdf.to_sql(name='aggregated_transaction', con=engine, if_exists='append', index=False)
aggregated_usdf.to_sql(name='aggregated_user', con=engine, if_exists='append', index=False)
map_trdf.to_sql(name='map_transaction', con=engine, if_exists='append', index=False)
map_usdf.to_sql(name='map_users', con=engine, if_exists='append', index=False)
top_trdf.to_sql(name='top_transaction', con=engine, if_exists='append', index=False)
top_usdf.to_sql(name='top_users', con=engine, if_exists='append', index=False)



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
        fig_amount.show()

    with coll2:
        fig_count = px.bar(agtrg, x="State", y="Transaction Count", title=f"{year} Transaction Count",
                           color="Transaction Amount",color_continuous_scale="tempo",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()),height=650,width=600)
        fig_count.show()
        

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for features in data1["features"]:
        state_name.append(features["properties"]["ST_NM"])

    state_name.sort()

    fig_ind_1=px.choropleth(agtrg,geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color="Transaction Amount", color_continuous_scale="ylgnbu",
                            range_color=(agtrg["Transaction Amount"].min(), agtrg["Transaction Amount"].max()), hover_name="State",
                            title=f"{year}",fitbounds="locations",height=600,width=600)
    
    fig_ind_1.update_geos(visible=False)    
    fig_ind_1.show()


    fig_ind_2=px.choropleth(agtrg,geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                            color="Transaction Count", color_continuous_scale="tempo",
                            range_color=(agtrg["Transaction Count"].min(), agtrg["Transaction Count"].max()), hover_name="State",
                            title=f"{year}",fitbounds="locations",height=600,width=600)
    
    fig_ind_2.update_geos(visible=False)    
    fig_ind_2.show()

    

