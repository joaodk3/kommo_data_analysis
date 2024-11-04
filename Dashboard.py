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
        st.divider()
        data = pd.read_csv(uploaded_file)
        st.dataframe(data)

        #Dated framed Data
        with st.sidebar:
            
            # Dated Metrics
            min_data_spam = data["Criado em"].min()
            max_data_spam = data["Criado em"].max()

            data["Criado em"] = pd.to_datetime(data["Criado em"], format="%d.%m.%Y %H:%M:%S")
            data["Month-Year"] = data["Criado em"].dt.strftime("%B-%Y")
            unique_dates = data["Month-Year"].unique()
            
            data_selection = st.selectbox(
                "Select the data spam",
                unique_dates
            )

            st.write("You selected: ", data_selection)
            st.subheader("Date Spam for Total Data", divider="grey")
            st.info("Start Date: {}".format(min_data_spam))
            st.info("End Date: {}".format(max_data_spam))
    
        data.rename(columns={"Lead venda R$": "Venda"}, inplace=True)

        #Total Metrics 
        total_leads = data.ID.count()
        gain_leads = data.Venda[data.Venda != 0].count()
        lost_leads = data.Venda[data.Venda == 0].count()
        conversion_rate = gain_leads / lost_leads * 100
        formatted_conversion_rate = "%.2f" % conversion_rate + "%"

        st.subheader("Leads Metrics", divider="red")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Leads", value=total_leads)
        col2.metric("Gain Leads", value=gain_leads)
        col3.metric("Lost Leads", value=lost_leads)
        col4.metric("Conversion Rate", value=formatted_conversion_rate)

        #Closing Dates Analysis
        gains_df = data[(data['Venda'] != 0) & (data['Fechado às'] != "não fechado") & (data['Origem'] != 'LTV')]
        gains_df['Fechado às'] = pd.to_datetime(gains_df['Fechado às'], format='mixed', dayfirst=True)
        gains_df['Criado em'] = pd.to_datetime(gains_df['Criado em'], format='mixed', dayfirst=True)

        # Calculate 'Spam CLosing'
        gains_df['Spam CLosing'] = gains_df['Fechado às'] - gains_df['Criado em']

        # Display the DataFrame
        st.write("DataFrame de Clientes que fecharam")
        st.dataframe(gains_df)

        gains_df['Spam Closing Days'] = gains_df['Spam CLosing'].dt.days
        min_close_spam = gains_df['Spam Closing Days'].min()
        max_close_spam = gains_df['Spam Closing Days'].max()
        avg_close_spam = gains_df['Spam Closing Days'].mean()

        st.subheader("Closing Date Spam in Days", divider="red")
        col5, col6, col7 = st.columns(3)
        col5.metric("Minimum Spam Closing", value=min_close_spam)
        col6.metric("Maximum Spam Closing", value=max_close_spam)
        col7.metric("Average Spam Closing", value=avg_close_spam)

        st.subheader("Leads Status", divider="red")

        status_count = data.groupby(['Status Atual']).ID.count()
        st.dataframe(status_count, width=700)

        st.subheader("Leads Origin", divider="red")
            
        origin_count = data.groupby(['Origem']).ID.count()
        st.dataframe(origin_count, width=700)
        
    else:
        st.warning("Upload a file first")
        with st.sidebar:
            st.subheader("Waiting for file to be uploaded")

if __name__ == "__main__":
    main()