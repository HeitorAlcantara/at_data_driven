from pydantic import BaseModel

class Match(BaseModel):
    summary_match: str


class Player(BaseModel):
    pass