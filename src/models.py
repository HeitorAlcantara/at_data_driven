from pydantic import BaseModel
from typing import Dict, Any

class Match(BaseModel):
    summary_match: str


class Player(BaseModel):
    name: str
    match_id: int
    stats: Dict[str, Any]