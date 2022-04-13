import itertools
import random
from typing import Any, Iterable, Protocol
from match_scheduling.match_schedule import Match, MatchSchedule


class Permuter(Protocol):
    def __call__(self, match_schedule: MatchSchedule) -> Iterable[MatchSchedule]:
        ...


## TYPES OF Permutations

# Swap two matches
def swap_two_matches(match_schedule: MatchSchedule) -> Iterable[MatchSchedule]:
    for i, match_i in enumerate(match_schedule.matches):
        for j, match_j in enumerate(match_schedule.matches[i + 1 :], start=i + 1):
            # swap matches i and j
            new_match_list = [*match_schedule.matches]
            new_match_list[i], new_match_list[j] = new_match_list[j], new_match_list[i]

            yield MatchSchedule(teams=match_schedule.teams, matches=new_match_list)


# Swap the positions of 2 teams in the same match
def swap_teams_inside_matches(match_schedule: MatchSchedule) -> Iterable[MatchSchedule]:
    def shuffle_teams_inside_match(match: Match) -> Iterable[Match]:
        for i in itertools.permutations(match):
            yield Match(*i)

    for i, match_i in enumerate(match_schedule.matches):
        for new_match_i in shuffle_teams_inside_match(match_i):
            new_matches = [
                *match_schedule.matches[:i],
                new_match_i,
                *match_schedule.matches[i + 1 :],
            ]
            yield MatchSchedule(teams=match_schedule.teams, matches=new_matches)


# Add a new match to the match schedule (?)
def add_match_to_schedule(match_schedule: MatchSchedule) -> Iterable[MatchSchedule]:
    for _ in range(1000):
        six_teams = random.sample(match_schedule.teams, 6)
        match = Match(*six_teams)
        new_match_list = [*match_schedule.matches, match]
        yield MatchSchedule(teams=match_schedule.teams, matches=new_match_list)


# Remove a match from the match schedule (?)
def delete_match_from_schedule(
    match_schedule: MatchSchedule,
) -> Iterable[MatchSchedule]:
    for i, _ in enumerate(match_schedule.matches):
        new_match_list = [*match_schedule.matches[:i], *match_schedule.matches[i + 1 :]]
        yield MatchSchedule(teams=match_schedule.teams, matches=new_match_list)


# Swap a team with a team in an adjacent match
def swap_team_with_one_in_adjacent_match(
    match_schedule: MatchSchedule,
) -> Iterable[MatchSchedule]:
    for (i, match_i), (j, match_j) in zip(
        enumerate(match_schedule.matches[:-1]), enumerate(match_schedule.matches[1:], start=1)
    ):
        # make a swap from match i with match j
        for t1_idx, t1 in enumerate(match_i):
            for t2_idx, t2 in enumerate(match_j[t1_idx + 1:], start=t1_idx + 1):
                new_match_i = Match(*(*match_i[:t1_idx], t2, *match_i[t1_idx + 1:]))
                new_match_j = Match(*(*match_j[:t2_idx], t1, *match_j[t2_idx + 1:]))

                new_match_schedule = [
                    *match_schedule.matches[:i], new_match_i, new_match_j, *match_schedule.matches[j+1:]
                ]

                yield MatchSchedule(teams=match_schedule.teams, matches=new_match_schedule)
