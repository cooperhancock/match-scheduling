from typing import Callable, TypeVar, List, NamedTuple, Tuple
from dataclasses import dataclass
from functools import wraps

T = TypeVar('T')
def must_contain_team(method: Callable[['Match', int], T]) -> Callable[['Match', int], T]:
    @wraps(method)
    def checked(self: 'Match', team: int) -> T:
        if team not in self:
            raise LookupError(f"team {team} not in match {self!r}")
        
        return method(self, team)
    
    return checked

class Match(NamedTuple):
    red1: int
    red2: int
    red3: int
    blue1: int
    blue2: int
    blue3: int

    def is_valid(self) -> bool:
        # all teams in the match are unique
        return len(set(self)) == 6

    @must_contain_team
    def allies_of(self, team: int) -> Tuple[int, ...]:
        if team in self[:3]:
            return self[:3]
        else:
            return self[3:]
    
    @must_contain_team
    def opponents_of(self, team: int) -> Tuple[int, ...]:
        if team in self[:3]:
            return self[3:]
        else:
            return self[:3]
    
    @must_contain_team
    def on_red(self, team: int) -> bool:
        return team in self[:3]

    @must_contain_team
    def alliance_station_num(self, team: int) -> int:
        if team == self.red1 or team == self.blue1:
            return 1
        elif team == self.red2 or team == self.blue2:
            return 2
        else:
            return 3


@dataclass
class MatchSchedule:
    teams: List[int]
    matches: List[Match]
