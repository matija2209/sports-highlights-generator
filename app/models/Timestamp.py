from pydantic import BaseModel
from typing import List, Tuple

class FootballEvent(BaseModel):
    timestamp: int
    type: str
    scorer: str
    team: str | None  # Since team can be NaN/None in the CSV for 'start' events


class TopPlayer(BaseModel):
    name: str
    count: int

class MatchScore(BaseModel):
    match: str
    scores: str