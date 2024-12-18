from fastapi import APIRouter, HTTPException
from models import Match, Player
import json


from football_stats.matches import get_player_stats
from football_stats.competitions import get_matches
from football_llm_data import summarization_match_details

match_summary_router = APIRouter()
player_profile_router = APIRouter()


@match_summary_router.get("/match_summary/{competition_id}/{season_id}")
async def match_summary(competition_id: int, season_id: int) -> Match:
    match = json.loads(get_matches(competition_id, season_id))
    match_id = match[0]['match_id']
    team_score = [(match[0]['home_team'], match[0]['home_score']), (match[0]['away_team'], match[0]['away_score'])]

    response = summarization_match_details(match_id, team_score)

    return {
        "summary_match": response
    }



@player_profile_router.post("/player_profile")
async def player_profile(player: Player):
    player_name = player.name
    match_id = player.match_id

    try:
        stats = json.loads(get_player_stats(player_name=player.name, match_id=match_id))
        # print(stats)
        return {
            "name": player_name,
            "match_id": match_id,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# print(type(get_player_stats(player_name="Daniel Carvajal Ramos", match_id=18245)))

# match = json.loads(get_matches(competition_id=16, season_id=1))
# print(match[0])