from typing import Callable, List
from match_scheduling.constraints import spaces_between_matches
from match_scheduling.cost_calculation import cost as cost_based_on_num_matches
from match_scheduling.match_schedule import T, MatchSchedule, generate_even_spaced_schedule, generate_random_schedule
from match_scheduling.search_strategy import SearchStrategy
from match_scheduling.generate_neighbors import PERMUTERS

import time
import functools
import math
import random

def simulated_annealing(team_numbers: List[int], num_matches_per_team: int = 8) -> MatchSchedule:
    temperature = 100.0  # TODO: figure out starting value
    decay = 0.999
    iterations = 20_000

    cost: Callable[[MatchSchedule], float] = functools.partial(cost_based_on_num_matches, ideal_num_matches=num_matches_per_team)


    # Step 1: Generate an initial schedule
    # Step 2: iterate

    #current_schedule = generate_random_schedule(team_numbers, num_matches_per_team)
    current_schedule = generate_even_spaced_schedule(team_numbers, num_matches_per_team)
    print(current_schedule.format_pretty())
    current_cost = cost(current_schedule)

    try:
        for i in range(iterations):
            start = time.perf_counter()
            # TODO: come up with way to break out of loop once a good
            # enough schedule is reached

            neighbors: List[MatchSchedule] = []
            for permuter in PERMUTERS:
                neighbors.extend(permuter(current_schedule))
            
            next_potential_neighbor = random.choice(neighbors)
            #next_potential_neighbor = min(neighbors, key=cost)
            next_potential_cost = cost(next_potential_neighbor)

            if next_potential_cost < current_cost:
                current_schedule = next_potential_neighbor
                current_cost = next_potential_cost
            elif not math.isinf(next_potential_cost):
                threshold = math.exp(- (next_potential_cost - current_cost) / temperature)
                if random.random() < threshold:
                    current_schedule = next_potential_neighbor
                    current_cost = next_potential_cost
                    
                    temperature *= decay
            end = time.perf_counter()

            if i % 10 == 0:
                print(f"i {i} - time: {end - start} - cost: {current_cost} - temp: {temperature} - num matches in schedule {len(current_schedule.matches)}")
    except KeyboardInterrupt:
        print(current_schedule.format_pretty())
        for team in current_schedule.teams:
            match_numbers = [i for i, match in enumerate(current_schedule.matches) if team in match]
            spacings = [snd - fst for fst, snd in zip(match_numbers[:-1], match_numbers[1:])]
            print('team', team, ':', sorted(spacings))
        raise

    return current_schedule
