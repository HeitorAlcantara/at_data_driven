import streamlit as st
from football_app.football import summarization_match_details



if __name__ == "__main__":
    st.write(summarization_match_details(match_id=303299))