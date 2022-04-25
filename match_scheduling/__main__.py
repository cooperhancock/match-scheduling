from match_scheduling.simulated_annealing import simulated_annealing

teams = list(range(36))
num_matches = 6

out_schedule = simulated_annealing(teams, num_matches)
print(out_schedule.format_pretty())
