from functools import partial
from typing import Callable, List
from match_scheduling.constraints import alliance_station_evenness, has_correct_num_matches, num_repeated_allied_team, num_repeated_opposing_team, red_vs_blue_matches, spaces_between_matches
from match_scheduling.match_schedule import Match, MatchSchedule

# ideal num of matches per team
# IDEAL_NUM_MATCHES = 6

# constraint funcs that use team and match list arguments
team_cost_funcs: Callable[[int], List[Callable[[int, List[Match]], float]]] = lambda ideal_num_matches: [
    partial(has_correct_num_matches, ideal_num_matches),
    spaces_between_matches,
    num_repeated_allied_team,
    num_repeated_opposing_team,
    red_vs_blue_matches,
    alliance_station_evenness
]

# weights for each of the 6 functions in constraints.py in order of the functions
WEIGHTS = [10.0, 180.0, 7.0, 7.0, 5.0, 1.0]

# takes a schedule and returns its cost
def cost(schedule: MatchSchedule, ideal_num_matches: int) -> float:
    total_cost = 0.0
    for team in schedule.teams:
        cost_list = []
        for f in team_cost_funcs(ideal_num_matches):
            x = f(team, schedule.matches)
            if x < 0:
                print(f"what? {f} giving negative value")
            cost_list.append(x)
        # cost_list = [x(team, schedule.matches) for x in team_cost_funcs(ideal_num_matches)]
        total_cost += sum(x*y for x, y in zip(cost_list, WEIGHTS))
    return total_cost


        