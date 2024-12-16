from langchain.tools import tool
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

import streamlit as st

from football_stats.competitions import get_raw_data_match
from football_stats.competitions import get_matches
from football_stats.competitions import get_competitions
from football_stats.matches import get_events
import json
import yaml
import pandas as pd

load_dotenv()


def summarization_match_details(match_id: int):
    """
    Get the details of a specific match using the match ID.
    Args:
        match_id (int): The unique identifier of the match.
        
    Returns:
        str: The details of the match.
    """
    # df = get_raw_data_match(match_id)
    raw_data_match = get_raw_data_match(match_id=18245)

    agent_prompt = f"""
        You are a sports commentator with expertise in football (soccer). Respond as
        if you are delivering an engaging analysis for a TV audience. 
        Identify the most important events on the match (goals, fouls, assistant...)

        The match details are provided by the provided as follow: 
        {raw_data_match}

        The output should be a simple analysis of the match, em Português:

        ## EXAMPLE
        O time A venceu o time B por 3 a 1. [Jogador] marcou um gol com a assistência de [Jogador].
    """
    llm = GoogleGenerativeAI(model="gemini-1.5-flash")
    # input_variables = ["raw_data_match"]
    # prompt = PromptTemplate.from_template(agent_prompt)
    response = llm.invoke(agent_prompt)

    return response.content


print(summarization_match_details(match_id=18245))