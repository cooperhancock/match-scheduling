import statistics
from typing import Dict
from match_scheduling.match_schedule import MatchSchedule
from collections import defaultdict, Counter

# TODO: a constraint maps from a match schedule to a cost value (cost is infinity if hard constraint is broken)
#       these constraints are only soft

def has_correct_num_matches(ideal_num_matches: int, team: int, match_schedule: MatchSchedule) -> float:
    match_count = sum(1 for match in match_schedule if team in match)
    if match_count < ideal_num_matches:
        return float('inf')
    return ideal_num_matches - match_count # penalize the use of surrogate matches

def spaces_between_matches(team: int, match_schedule: MatchSchedule) -> float:
    match_numbers = [i for i, match in enumerate(match_schedule) if team in match]
    spacings = [snd - fst for fst, snd in zip(match_numbers[:-1], match_numbers[1:])]
    return statistics.median(spacings)


def num_repeated_allied_team(team: int, match_schedule: MatchSchedule) -> float:
    allied_team_counter: Dict[int, int] = defaultdict(lambda: 0)
    for match in match_schedule:
        if team in match:
            for ally in match.allies_of(team):
                allied_team_counter[ally] += 1

    allied_team_counter.pop(team)
    return max(allied_team_counter.values())


def num_repeated_opposing_team(team: int,  match_schedule: MatchSchedule) -> float:
    opposing_team_counter: Dict[int, int] = defaultdict(lambda: 0)
    for match in match_schedule:
        if team in match:
            for opponent in match.opponents_of(team):
                opposing_team_counter[opponent] += 1
    

    opposing_team_counter.pop(team)
    return max(opposing_team_counter.values())


def red_vs_blue_matches(team: int, match_schedule: MatchSchedule) -> float:
    return sum(
        1 if match.on_red(team) else -1 for match in match_schedule
    )

def alliance_station_evenness(team: int, match_schedule: MatchSchedule) -> float:
    num = Counter(match.alliance_station_num(team) for match in match_schedule if team in match)
    return max(num.values()) - min(num.values())
