import streamlit as st
from football_stats.competitions import get_competitions, get_matches, get_raw_data_match
from football_stats.matches import get_lineups, get_events, get_player_stats
from football import summarization_match_details
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema import AIMessage, HumanMessage

from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import json


st.set_page_config(layout="wide",
                   page_title="Football Match Conversation App",
                   page_icon="⚽️")

msgs = StreamlitChatMessageHistory()


if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(messages=msgs, memory_key="chat_history", return_messages=True)

memory = st.session_state.memory

def memorize_message():
    user_input = st.session_state["user_input"]
    st.session_state["memory"].chat_memory.add_message(HumanMessage(content=user_input))
    
def load_competitions():
    """
    Simulates loading competitions from your function.
    Replace this with the actual call to fetch competitions.
    """
    return json.loads(get_competitions())

def load_matches(competition_id, season_id):
    """
    Simulates loading matches for a specific competition.
    Replace this with the actual call to fetch matches for a competition.
    """
    return  json.loads(get_matches(competition_id, season_id))

def load_line_up(match_id):
    """
    Simulates loading lineups for a specific match.
    Replace this with the actual call to fetch line_ups for a match.
    """
    return  json.loads(get_lineups(match_id))

def load_player_stats(match_id, player_name):
    """
    Simulates loading player stats for a specific match.
    Replace this with the actual call to fetch player stats for a match.
    """
    return  json.loads(get_player_stats(match_id, player_name))

def get_player_position(team: json, player_name: str) -> list:
    """
    Get the position of a player based on the lineup.
    """
    for player in team:
        if player["player_name"] == player_name:
            positions = player.get("positions", {}).get("positions", [])
            if positions:
                player_position = positions[0].get("position", "Unknown Position")
            break
    return player_position


# Streamlit Sidebar
st.sidebar.title("Football Match Selector")
# Step 1: Select a Competition
selected_competition = None
selected_season = None
selected_match = None
match_id = None
match_details = None
specialist_comments = None

st.sidebar.header("Step 1: Select a Competition")
competitions = load_competitions()
competition_names = sorted(set([comp['competition_name'] for comp in competitions]))
selected_competition = st.sidebar.selectbox("Choose a Competition",
                                            competition_names)
if selected_competition:
    # Step 2: Select a Season
    st.sidebar.header("Step 2: Select a Season")
    seasons = set(comp['season_name'] for comp in competitions
                  if comp['competition_name'] == selected_competition)
    selected_season = st.sidebar.selectbox("Choose a Season", sorted(seasons))
    
    
if selected_season:
    # Get the selected competition ID
    competition_id = next(
        (comp['competition_id'] for comp in competitions 
         if comp['competition_name'] == selected_competition),
        None
    )
    season_id = next(
        (comp['season_id'] for comp in competitions 
                               if comp['season_name'] == selected_season 
                               and comp['competition_name'] == selected_competition),
        None
    )
    # Step 2: Select a Match
    st.sidebar.header("Step 3: Select a Match")
    matches = load_matches(competition_id, season_id)
    match_names = sorted([f"{match['home_team']} vs {match['away_team']}" for match in matches])
    
    if selected_match:=st.sidebar.selectbox("Choose a Match", match_names):
        # Get the selected match ID
        match_details = next(
            (match for match in matches if f"{match['home_team']} vs {match['away_team']}" == selected_match),
            None
        ) 
        match_id = match_details['match_id']


match_events, narratives = st.tabs(['Match Events', 'Narratives'])

with match_events:
    st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    .stadium {
        text-align: left
    }
    .referee {
        text-align: right
    }
    </style>
    """,
    unsafe_allow_html=True)
    st.markdown(f'<h1 class="title">{match_details["competition"]}</h1> <h3 class="title">Season {selected_season}</h3>', unsafe_allow_html=True)
    # st.write(match_details['competition'])
    st.markdown(f'* :stadium: : {match_details["stadium"]}')
    st.markdown(f'* :male-judge: : {match_details["referee"]}')
    st.markdown(f'* Competition Stage : {match_details["competition_stage"]}')
    with st.container(border=True):
        st.write(summarization_match_details(match_id=match_id))

    home_team, away_team = st.columns(2)
    with home_team:
        st.subheader(match_details['home_team'])
        st.markdown(f"Manager: :blue-background[{match_details['home_managers']}]")
        st.metric(label="Home team", value=match_details['home_score'])


    with away_team:
        st.subheader(match_details['away_team'])
        st.markdown(f"Manager: :blue-background[{match_details['away_managers']}]")
        st.metric(label="Away team", value=match_details['away_score'])


    # match = get_raw_data_match(match_id)
    st.write(match_id)

    line_up = load_line_up(match_id=match_id)
    st.write(match_details)
    with home_team:
        # st.write(match_details)
        home_team_players = sorted(set(comp["player_name"] for comp in line_up[match_details['home_team']]))
        selected_home_team_player = st.selectbox("Choose a home team player", home_team_players)
        if selected_home_team_player:
            try:
                player_stats = load_player_stats(match_id=match_id, player_name=selected_home_team_player)
                player_position = get_player_position(line_up[match_details['home_team']], player_name=selected_home_team_player)
                st.write(f"Position: {player_position if player_position else 'Position not found'}")
                st.write(player_stats)
            except:
                st.write("Please select other player. No Events found for this player")

    with away_team:
        away_team_players = sorted(set(comp["player_name"] for comp in line_up[match_details['away_team']]))
        selected_away_team_player = st.selectbox("Choose a away team player", away_team_players)
        if selected_away_team_player:
            try:
                player_stats = load_player_stats(match_id=match_id, player_name=selected_away_team_player)
                player_position = get_player_position(line_up[match_details['away_team']], player_name=selected_away_team_player)
                st.write(f"Position: {player_position if player_position else 'Position not found'}")
                st.write(player_stats)
            except Exception as e:
                st.write("Please select other player. No Events found for this player")
