import unittest

from student import Student


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(
            "Nonso",
            [78, 65, 82],
            "22CD032179"
        )

    def test_calculate_average(self):
        self.assertEqual(
            self.student.calculate_average(),
            75
        )

    def test_find_highest(self):
        self.assertEqual(
            self.student.find_highest(),
            82
        )

    def test_find_lowest(self):
        self.assertEqual(
            self.student.find_lowest(),
            65
        )

    def test_calculate_grade(self):
        self.assertEqual(
            self.student.calculate_grade(),
            "Distinction"
        )


if __name__ == "__main__":
    unittest.main()