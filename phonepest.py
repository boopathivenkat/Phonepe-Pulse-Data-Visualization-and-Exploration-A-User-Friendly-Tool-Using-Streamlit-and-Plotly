import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu


with st.sidebar:
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/PhonePe_Logo.svg/300px-PhonePe_Logo.svg.png")
    st.caption("***Code Written by Boopathi Venkatachalam***")
    st.divider()

    selected = option_menu("Main Menu", ["Intro",'Top chart','Explore Data','Contact Us'], 
        icons=['play-btn','search','info-circle','search','info-circle'])

if selected=="Intro":

    st.title("*Welcome to Boopathi's PhonePe*")

    st.markdown('''
    :rainbow[PhonePe] :orange[is] :green[an] :blue[Indian] :violet[multinational]
    :gray[digital] :red[payments] :green[and] :blue[financial] :violet[services]
    :gray[company] :tulip::rose::hibiscus:''')

    st.divider()




    st.markdown("""**PhonePe is a payments app that allows you to use BHIM UPI,
                your credit card and debit card or wallet to recharge your mobile phone,
                pay all your utility bills and to make instant payments at your favourite offline and online stores.**""")
    
    st.markdown("""**You can also invest in mutual funds and buy insurance plans on PhonePe. Get Car & Bike Insurance on our app.
                Link your bank account on PhonePe and transfer money with BHIM UPI instantly! 
                The PhonePe app is safe and secure, meets all your payment, investment, mutual funds,
                insurance and banking needs, and is much**""")
    st.divider()
    
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


elif selected=="Top chart":

    tab1, tab2, tab3 = st.tabs(["***Aggregated Analysis***", "***Map Analysis***", "***Top Analysis***"])

    with tab1:
        analysis1 = st.selectbox("***Select analysis type***", ["Transaction Base", "User Base"], key="unique_key_2")                         
    with tab2:
        analysis2 = st.selectbox("***Select analysis type***", ["Transaction Base", "User Base"], key="unique_key_3")
    with tab3:
        analysis3 = st.selectbox("***Select analysis type***",  ["Transaction Base", "User Base"], key="unique_key_4")

            
elif selected=="Explore Data":
    st.markdown(
        """
        - _Explore Data"""
    )


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






