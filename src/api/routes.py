from fastapi import APIRouter
from models import Match

match_summary_router = APIRouter()
player_profile_router = APIRouter()


@match_summary_router.get("/match_summary/{id}")
async def match_summary(id: int) -> Match:
    return Match(summary_match=...)


@player_profile_router.get("/player_profile")
async def player_profile():
    pass