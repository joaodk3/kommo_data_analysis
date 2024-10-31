'''
import streamlit as st
import os
from openai import OpenAI
import pandas as pd
from Dashboard import data

def main():

    #Page config
    st.set_page_config(
    page_title="Chatbot",
    page_icon="💬",
    )

    #Data Load

    if not data:
        st.warning("Upload data in Dashboard Page")

    with st.sidebar:
        st.image("https://www.ustayinusa.com/logo.svg")
        
        if data is not None:
            st.subheader("Data Status:")
            st.success("Loaded", icon="✅")
        else:
            st.warning("Error", icon="❌")

        st.divider()
        if st.button("Clear Chat"):
            st.session_state["messages"] = []  # Reset chat history
    
    st.title("Chatbot 💬")

    #Chat Variables
    open_ai_key = os.getenv('OPENAI_API_KEY')

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    def chat():
        prompt = st.chat_input("Say something")  
        if prompt: 
            system_role = """
            You are a CRM Data Insights Assistant designed to help João Victor analyze and extract insights from his CRM data: {} in a Streamlit application. Your goal is to assist him by summarizing data, providing actionable insights, identifying trends, and advising on possible next steps based on the data. Prioritize clarity, relevance, and strategic advice. Keep responses concise but informative, and adapt to varying data contexts. You are capable of:

            Summarizing key data metrics in response to specific queries.
            Identifying patterns and trends in customer behaviors, sales, and engagement based on CRM data.
            Recommending data-driven actions to improve metrics like customer retention, engagement, and sales growth.
            Providing insights on KPIs such as customer acquisition costs, conversion rates, lifetime value, and seasonal performance.
            Suggesting marketing or sales tactics based on historical data, like ideal times for promotions or strategies for targeting specific customer segments.
            Always keep recommendations actionable and grounded in the context provided, using historical data to inform predictive insights when relevant. If possible, link responses to tangible business outcomes to maximize CRM data utility.
            """.format(data)

            client = OpenAI(api_key=open_ai_key)

            try:
                completion = client.chat.completions.create(
                    model="gpt-4",  
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": prompt}
                    ]
                )

                assistant_message = completion.choices[0].message.content

                
                st.session_state["messages"].append(("user", prompt))
                st.session_state["messages"].append(("assistant", assistant_message))

            except Exception as e:
                st.error(f"An error occurred: {e}")

        for role, message in st.session_state["messages"]:
            st.chat_message(role).write(message)
    
    chat()

if __name__ == '__main__':

    main()
'''