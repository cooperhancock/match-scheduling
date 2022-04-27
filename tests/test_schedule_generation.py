import unittest
from match_scheduling.match_schedule import generate_random_schedule

class ScheduleGenerationTest(unittest.TestCase):
    def test_schedule_generation(self) -> None:
        print("schedule generation test:\n")

        matchesPerTeam = 4

        teams = [i for i in range(100)]
        print('teams:')
        print(teams)
        schedule = generate_random_schedule(teams, matchesPerTeam)
        print('\nschedule:')
        for match in schedule.matches:
            print(match)
        print('matches scheduled: ', len(schedule.matches), 'theoretical min number of matches: ', (len(teams) * matchesPerTeam // 6) +1)