from fastapi import APIRouter, HTTPException
from models import Match, Player


from football_stats.matches import get_player_stats
from football import summarization_match_details

match_summary_router = APIRouter()
player_profile_router = APIRouter()


@match_summary_router.get("/match_summary/{id}")
async def match_summary(id: int) -> Match:
    return Match(summary_match=...)


@player_profile_router.post("/player_profile")
async def player_profile(player: Player):
    player_name = player.name
    match_id = player.match_id

    stats = get_player_stats(player_name=player_name, match_id=match_id)
    return {
        "name": player_name,
        "match_id": match_id,
        "stats": stats
    }
    