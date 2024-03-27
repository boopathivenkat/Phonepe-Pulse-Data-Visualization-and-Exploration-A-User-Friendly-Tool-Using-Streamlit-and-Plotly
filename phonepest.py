import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import plotly.express as px


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
aggre_trans= pd.DataFrame(table1, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Brands", "Transaction Count", "Transaction Percentage"]
aggre_user = pd.DataFrame(table2, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts", "Transaction Count", "Transaction Amount",]
map_trtb = pd.DataFrame(table3, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM map_users")
mydb.commit()
table4 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts", "Registered Users", "App Opens",]
map_ustb = pd.DataFrame(table4, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5 = cursor.fetchall()
columns = ["State", "Years", "Quarter", "Districts","Pincodes", "Transaction Count", "Transaction Amount",]
top_trtb = pd.DataFrame(table5, columns=columns)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM top_users")
mydb.commit()
table6 = cursor.fetchall()
columns = ["State", "Years", "Quarter","Pincodes", "Districts", "Count","Amount"]
top_ustb = pd.DataFrame(table6, columns=columns)


import pandas as pd
import plotly.express as px
import streamlit as st

def aggre_tran_year(aa,year):

    agtr = aa[aa["Years"] == year]
    agtr.reset_index(drop=True, inplace=True)

    agtrg = agtr.groupby("State")[["Transaction Count", "Transaction Amount"]].sum()
    agtrg.reset_index(inplace=True)

    fig_amount = px.bar(agtrg, x="State", y="Transaction Amount", title=f"{year} Transaction Amount")
    st.plotly_chart(fig_amount)

    fig_count = px.bar(agtrg, x="State", y="Transaction Count", title=f"{year} Transaction Count")
    st.plotly_chart(fig_count)



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
    tab1, tab2, tab3 = st.tabs(["Aggregated Transaction", "Map Analysis", "Top Analysis"])
    year = st.slider('Select a year', 2018, 2023)
    
    if tab1:        
        aggre_tran_year(aggre_trans, year)

    elif tab2 == "Map Analysis":
        aggre_tran_year(map_trtb, year)
        
    elif tab3 == "Top Analysis":
        aggre_tran_year(top_trtb, year)
            
            
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


