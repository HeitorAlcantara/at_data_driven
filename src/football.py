from langchain.tools import tool
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

import streamlit as st

from football_stats.matches import get_player_stats
from football_stats.matches import get_lineups
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

    match_id = match_id

    line_up = json.loads(get_lineups(match_id))
    home_team = list(line_up.keys())[0]
    away_team = list(line_up.keys())[1]

    # print(home_team)

    home_team_line_up = line_up[home_team]
    away_team_line_up = line_up[away_team]
    
    home_team_players = [player['player_name'] for player in home_team_line_up]
    away_team_players = [player['player_name'] for player in away_team_line_up]

    home_player_stats = {
        home_team: {}
    }
    for name in home_team_players:
        try:
            response = get_player_stats(match_id, name)
            home_player_stats[home_team][name] = response
        except:
            home_player_stats[name] = None

    away_player_stats = {
        away_team: {}
    }
    for name in away_team_players:
        try:
            response = get_player_stats(match_id, name)
            away_player_stats[away_team][name] = response 
        except:
            away_player_stats[name] = None

    json_home_player_stats = json.dumps(home_player_stats, indent=4, ensure_ascii=False)
    json_away_player_stats = json.dumps(away_player_stats, indent=4, ensure_ascii=False)

    # print(json_home_player_stats)
    # print(json_away_player_stats)

    agent_prompt = f"""
        You are a sports commentator with expertise in football (soccer). Respond as
        if you are delivering an engaging analysis for a TV audience. 
        Identify the most important events on the match (goals, fouls, cards...)

        The match details are provided by the stats of each player in a team as a JSON.
        The first key is the name of the Team, followed by the player and it stats

        ## EXAMPLE
        {{
            'Real Madrid': {{
                'Francisco Román Alarcón Suárez': '[continue JSON]'
            }}
        }}

        Here's the JSON data of TEAM A and TEAM B:

        ## TEAM A 
        {json_home_player_stats}

        ## TEAM B
        {json_away_player_stats}

        With that information, you are able to tell which team won the match
        Who were the most important players on the match
        The output should be a simple analysis of the match, em Português:

        ## EXAMPLE
        O time A venceu o time B por 3 a 1. [Jogador x] marcou um gol com a assistência de [Jogador y]. [Jogador z] sofreu uma falta do [Jogador w], [Jogador w] tomou cartão amarelo.
        
    """
    llm = GoogleGenerativeAI(model="gemini-1.5-flash")
    # input_variables = ["raw_data_match"]
    # prompt = PromptTemplate.from_template(agent_prompt)
    response = llm.invoke(agent_prompt)

    return response


# summarization_match_details(match_id=18245)