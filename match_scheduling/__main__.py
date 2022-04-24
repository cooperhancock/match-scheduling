from random import randint
from match_scheduling.match_schedule import generateRandomSchedule

print("hello world")

print("schedule generation test:\n")

matchesPerTeam = 4

teams = [i for i in range(100)]
print('teams:')
print(teams)
schedule = generateRandomSchedule(teams, matchesPerTeam)
print('\nschedule:')
for match in schedule.matches:
    print(match)
print('matches scheduled: ', len(schedule.matches), 'theoretical min number of matches: ', (len(teams) * matchesPerTeam // 6) +1)