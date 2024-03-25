import json
import os
import pandas as pd
import plotly.express as px
import mysql.connector
from sqlalchemy import create_engine
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

aggregated_transaction=pd.DataFrame(column1)


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

            ag_us=json.load(data)

            try:                       
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

aggregated_user=pd.DataFrame(column2)


path3 = r'C:/Users/boopa/Downloads/pulse-master/data/map/transaction/hover/country/india/state/'
map_tran_list = os.listdir(path3)

column3={"States":[],"Years":[],"Quarter":[],"Count":[],"Amount":[],"Name":[]}

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
                name=i["name"]
                count=i["metric"][0]["count"]
                amount=i["metric"][0]["amount"]
                column3["Name"].append(name)
                column3["Count"].append(count)
                column3["Amount"].append(amount)
                column3["States"].append(state)
                column3["Years"].append(year)
                column3["Quarter"].append(int(file.strip(".json")))

map_transaction=pd.DataFrame(column3)


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
                   
map_users=pd.DataFrame(column4)



path5 = r'C:/Users/boopa/Downloads/pulse-master/data/top/transaction/country/india/state/'
top_tran_list = os.listdir(path5)

column5 = {"States": [], "Years": [], "Quarter": [], "Districts": [], "Count": [], "Amount": []}

for state in top_tran_list:
    current_states = os.path.join(path5, state)
    map_year_list = os.listdir(current_states)
    
    for year in map_year_list:
        current_year = os.path.join(current_states, year)
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = os.path.join(current_year, file)
            with open(current_file, "r") as data:
                top_tr = json.load(data)
                
                for i in top_tr["data"]["districts"]:
                    districts = i["entityName"]
                    count = i["metric"]["count"]
                    amount = i["metric"]["amount"]
                    column5["Districts"].append(districts)
                    column5["Count"].append(count)
                    column5["Amount"].append(amount)
                    column5["States"].append(state)
                    column5["Years"].append(year)
                    column5["Quarter"].append(int(file.strip(".json")))

top_transaction = pd.DataFrame(column5)



path6 = r'C:/Users/boopa/Downloads/pulse-master/data/top/user/country/india/state/'

top_user_list = os.listdir(path6)

column6={"States":[],"Years":[],"Quarter":[],"Districts":[],"RegisteredUsers":[]}

for state in top_tran_list:
    current_states = os.path.join(path5, state)
    map_year_list = os.listdir(current_states)
    
    for year in map_year_list:
        current_year = os.path.join(current_states, year)
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = os.path.join(current_year, file)
            with open(current_file, "r") as data:

                top_us = json.load(data)
                        
                for i in top_us["data"]["districts"]:
                    districts = i["entityName"]
                    count = i["metric"]["count"]
                    column6["Districts"].append(districts)
                    column6["RegisteredUsers"].append(count)
                    column6["States"].append(state)
                    column6["Years"].append(year)
                    column6["Quarter"].append(int(file.strip(".json")))


top_users=pd.DataFrame(column6)



engine = create_engine("postgresql+psycopg2://postgres:758595@localhost:5432/phonepe")


aggregated_transaction.to_sql(name='aggregated_transaction', con=engine, if_exists='append', index=False)
aggregated_user.to_sql(name='aggregated_user', con=engine, if_exists='append', index=False)
map_transaction.to_sql(name='map_transaction', con=engine, if_exists='append', index=False)
map_users.to_sql(name='map_users', con=engine, if_exists='append', index=False)
top_transaction.to_sql(name='top_transaction', con=engine, if_exists='append', index=False)
top_users.to_sql(name='top_users', con=engine, if_exists='append', index=False)
