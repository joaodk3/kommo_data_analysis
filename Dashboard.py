#st.file_uploader
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    )

    #Title
    st.title("Kommo Data 📊 ")

    #Initial SideBar
    with st.sidebar:
        st.image("https://www.ustayinusa.com/logo.svg")

    #File Uploader
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        #Adicionar a Session State to persist the data
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['data'] = pd.read_csv(uploaded_file)
        data = st.session_state.data
        
        st.divider()
        expander = st.expander("Observe Data")
        expander.write(data)

        #Dated framed Data
        with st.sidebar:
            
            # Dated Metrics
            min_data_spam = data["Criado em"].min()
            max_data_spam = data["Criado em"].max()

            data["Criado em"] = pd.to_datetime(data["Criado em"], format="%d.%m.%Y %H:%M:%S")
            data["Month-Year"] = data["Criado em"].dt.strftime("%B-%Y")

            st.subheader("Date Spam for Total Data", divider="grey")
            st.info("Start Date: {}".format(min_data_spam))
            st.info("End Date: {}".format(max_data_spam))
            st.text("All rights reserved to @Ustay")
    
        data.rename(columns={"Lead venda R$": "Venda"}, inplace=True)

        #Leads Metrics 
        total_leads = data.ID.count()
        gain_leads = data.Venda[data.Venda != 0].count()
        lost_leads = data.Venda[data.Venda == 0].count()
        conversion_rate = gain_leads / lost_leads * 100
        formatted_conversion_rate = "%.2f" % conversion_rate + "%"

        st.subheader("Leads Metrics", divider="grey")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Leads", value=total_leads)
        col2.metric("Gain Leads", value=gain_leads)
        col3.metric("Lost Leads", value=lost_leads)
        col4.metric("Conversion Rate", value=formatted_conversion_rate)

        #Closing Dates Analysis
        gains_df = data[(data['Venda'] != 0) & (data['Fechado às'] != "não fechado") & (data['Origem'] != 'LTV')]
        gains_df['Fechado às'] = pd.to_datetime(gains_df['Fechado às'], format='mixed', dayfirst=True)
        gains_df['Criado em'] = pd.to_datetime(gains_df['Criado em'], format='mixed', dayfirst=True)

        # Calculate Spam CLosing Dates
        gains_df['Spam CLosing'] = gains_df['Fechado às'] - gains_df['Criado em']
        gains_df['Spam Closing Days'] = gains_df['Spam CLosing'].dt.days
        min_close_spam = gains_df['Spam Closing Days'].min()
        max_close_spam = gains_df['Spam Closing Days'].max()
        avg_close_spam = gains_df['Spam Closing Days'].mean()

        st.subheader("Closing Date Spam in Days", divider="grey")
        col5, col6, col7 = st.columns(3)
        col5.metric("Minimum Spam Closing", value=min_close_spam)
        col6.metric("Maximum Spam Closing", value=max_close_spam)
        col7.metric("Average Spam Closing", value=round(float(avg_close_spam),3))

        # Calculate Leads Status
        st.subheader("Leads Status", divider="grey")
        status_count = data.groupby(['Status Atual']).ID.count()
        st.bar_chart(status_count)

        # Calculate Leads Origin
        st.subheader("Leads Origin", divider="grey")    
        origin_count = data.groupby(['Origem']).ID.count()
        st.bar_chart(origin_count)

        data["Criado em"] = pd.to_datetime(data["Criado em"])
        data["Month-Year-Arrive"] = data["Criado em"].dt.to_period("M").dt.to_timestamp()
        leads_per_month = data.groupby("Month-Year-Arrive")["ID"].count().sort_index()

        # Total closed leads Per Month
        gains_df["Fechado às"] = pd.to_datetime(gains_df["Fechado às"])
        gains_df["Month-Year-Closed"] = gains_df["Fechado às"].dt.to_period("M").dt.to_timestamp()
        leads_closed_per_month = gains_df.groupby("Month-Year-Closed")["ID"].count().sort_index()

        # Calculate Conversion Rate per Month
        conversion_df = pd.DataFrame({
            "Total Leads": leads_per_month,
            "Closed Leads": leads_closed_per_month
        }).fillna(0)

        # Calculate the conversion rate and add it as a column
        conversion_df["Conversion Rate (%)"] = (conversion_df["Closed Leads"] / conversion_df["Total Leads"] * 100).round(2)

        # Display Histogram for All Leads Per Month
        st.subheader("Total Leads per Month", divider='grey')
        st.bar_chart(leads_per_month)

        # Display Histogram for Closed Leads Per Month
        st.subheader("Total Closed Leads per Month", divider='grey')
        st.bar_chart(leads_closed_per_month)

        # Display Conversion Rate per Month
        st.subheader("Conversion Rate per Month")
        st.line_chart(conversion_df["Conversion Rate (%)"])
                       

    else:
        st.warning("Upload a file first")
        with st.sidebar:
            st.subheader("Waiting for file to be uploaded")


if __name__ == "__main__":
    main()