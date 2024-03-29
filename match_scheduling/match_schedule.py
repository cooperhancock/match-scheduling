from nis import match
from random import randint, shuffle
from typing import Callable, Counter, TypeVar, List, NamedTuple, Tuple
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

    def format_pretty(self) -> str:
        ret: List[str] = []
        table_row_fstr = (
            "{0!s:3} || {1!s:5} | {2!s:5} | {3!s:5} || {4!s:5} | {5!s:5} | {6!s:5} |"
        )
        ret.append(table_row_fstr.format("match_num", "red1", "red2", "red3", "blue1", "blue2", "blue3"))
        for i, match in enumerate(self.matches):
            ret.append(table_row_fstr.format(i, *match))

        return "\n".join(ret)


def generate_random_schedule(teams: List[int], numMatchesPerTeam: int) -> MatchSchedule:
    schedule = MatchSchedule(teams, [])
    if len(teams) < 6:
        raise ValueError(teams, 'must have at least 6 teams') 
    counter = {x: 0 for x in teams}
    # iterate through teams exploded until 6 unique teams are found, pop them from list and make into Match
    while(min(counter.values()) < numMatchesPerTeam):
        matchTeams: List[int] = []
        # grab first 6 unique teams
        while len(matchTeams) < 6:
            team = teams[randint(0, len(teams)-1)]
            if team in matchTeams:
                continue
            else:
                matchTeams.append(team)
                counter[team] += 1
        # make match out of teams and add to schedule
        schedule.matches.append(Match(matchTeams[0], matchTeams[1], matchTeams[2], matchTeams[3], matchTeams[4], matchTeams[5]))
    return schedule

def generate_even_spaced_schedule(teams: List[int], numMatchesPerTeam: int) -> MatchSchedule:
    schedule = MatchSchedule(teams, [])
    if len(teams) < 6:
        raise ValueError(teams, 'must have at least 6 teams')
    matchTeams: List[int] = [] 
    i = 0
    while True:
        matchTeams.append(teams[i])
        if len(matchTeams) == 6:
            schedule.matches.append(Match(matchTeams[0], matchTeams[1], matchTeams[2], matchTeams[3], matchTeams[4], matchTeams[5]))
            matchTeams = []
        if i == len(teams)-1:
            i = -1
        if len(schedule.matches) > len(teams) * numMatchesPerTeam // 6:
            break
        i+=1
    return schedule
    

