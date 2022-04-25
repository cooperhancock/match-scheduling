from match_scheduling.constraints import spaces_between_matches
from match_scheduling.simulated_annealing import simulated_annealing

teams = list(range(36))
num_matches = 6

out_schedule = simulated_annealing(teams, num_matches)
print(out_schedule.format_pretty())
for team in out_schedule.teams:
            print('team', team, ':', spaces_between_matches(team, out_schedule.matches))
