from match_scheduling.match_schedule import MatchSchedule
from typing import Any, List, Protocol

class SearchStrategy(Protocol):
    def __call__(self, team_numbers: List[int]) -> MatchSchedule:
        ...
