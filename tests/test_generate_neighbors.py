import unittest
from match_scheduling import generate_neighbors
from match_scheduling.match_schedule import Match, MatchSchedule


class TestGenerateNeighbors(unittest.TestCase):
    def setUp(self) -> None:
        self.one_match_schedule = MatchSchedule(
            teams=[1, 2, 3, 4, 5, 6],
            matches=[Match(1, 2, 3, 4, 5, 6)]
        )
        self.two_match_schedule = MatchSchedule(
            teams=[1, 2, 3, 4, 5, 6],
            matches=[Match(1, 2, 3, 4, 5, 6), Match(4, 5, 6, 1, 2, 3)],
        )

    def test_swap_two_matches(self) -> None:
        swapped = [*generate_neighbors.swap_two_matches(self.two_match_schedule)]
        self.assertEqual(len(swapped), 1)
        expected_matches = [Match(4, 5, 6, 1, 2, 3), Match(1, 2, 3, 4, 5, 6)]

        self.assertEqual(
            swapped[0].matches,
            expected_matches,
        )

    def test_swap_teams_inside_matches(self) -> None:
        swapped = [*generate_neighbors.swap_teams_inside_matches(self.one_match_schedule)]
         # all possible permutations of the match, minus the one that we already had
        expected_num_of_schedules = (6 * 5 * 4 * 3 * 2 * 1) - 1
        self.assertEqual(len(swapped), expected_num_of_schedules)
        self.assertTrue(all(match.is_valid() for schedule in swapped for match in schedule.matches))