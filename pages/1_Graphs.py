import streamlit as st

def main():
    st.set_page_config(
    page_title="Graphs",
    page_icon="📈",
)
    with st.sidebar:
        st.image("https://www.ustayinusa.com/logo.svg")
    
    st.title("Vizualization 📈")
    

if __name__ == '__main__':
    main()
