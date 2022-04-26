from match_scheduling.constraints import spaces_between_matches
from match_scheduling.simulated_annealing import simulated_annealing

teams = list(range(36))
num_matches = 6

out_schedule = simulated_annealing(teams, num_matches)
print(out_schedule.format_pretty())
for team in out_schedule.teams:
    match_numbers = [i for i, match in enumerate(out_schedule.matches) if team in match]
    spacings = [snd - fst for fst, snd in zip(match_numbers[:-1], match_numbers[1:])]
    print('team', team, ':', sorted(spacings))
