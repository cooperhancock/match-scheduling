from match_scheduling.simulated_annealing import simulated_annealing

teams = list(range(12))
num_matches = 3

out_schedule = simulated_annealing(teams, num_matches)
print(out_schedule.format_pretty())
