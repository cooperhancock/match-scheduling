from functools import partial
from typing import Callable, List
from match_scheduling.constraints import alliance_station_evenness, has_correct_num_matches, num_repeated_allied_team, num_repeated_opposing_team, red_vs_blue_matches, spaces_between_matches
from match_scheduling.match_schedule import Match, MatchSchedule

# ideal num of matches per team
IDEAL_NUM_MATCHES = 6

# constraint funcs that use team and match list arguments
TEAM_MATCH_FUNCS: List[Callable[[int, List[Match]], float]] = [
    partial(has_correct_num_matches, IDEAL_NUM_MATCHES),
    spaces_between_matches,
    num_repeated_allied_team,
    num_repeated_opposing_team,
    red_vs_blue_matches,
    alliance_station_evenness
]

# weights for each of the 6 functions in constraints.py in order of the functions
WEIGHTS = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

# takes a schedule and returns its cost
def cost(schedule: MatchSchedule) -> float:
    total_cost = 0.0
    for team in schedule.teams:
        cost_list = [x(team, schedule.matches) for x in TEAM_MATCH_FUNCS]
        total_cost += sum(x*y for x, y in zip(cost_list, WEIGHTS))
    return total_cost


        