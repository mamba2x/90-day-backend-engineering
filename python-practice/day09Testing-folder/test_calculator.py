import unittest
import calculator

class TestCalculator(unittest.TestCase):
    def test_normal_scores_average(self):
        result= calculator.calculate_average([70,60,80])
        self.assertEqual(result,70)

    def test_all_student_pass(self):
        scores =[55,68,77,80]
        result= calculator.count_Distinction(scores)
        self.assertEqual(result,2)

    def test_all_student_fail(self):
        scores =[42,38,41,40]
        result= calculator.count_Fail(scores)
        self.assertEqual(result,4)

    def test_mixed_scores(self):
        scores =[85,60,41,38]
        result= calculator.count_Distinction(scores)
        fail_result=calculator.count_Fail(scores)
        self.assertEqual(result,1)
        self.assertEqual(fail_result,2)

    def test_highest(self):
        result= calculator.find_highest([40,75,90])
        self.assertEqual(result,90)

    def test_lowest(self):
        result= calculator.find_lowest([40,75,90])
        self.assertEqual(result,40)

    def test_distinction(self):
        result= calculator.calculate_grade(70)
        self.assertEqual(result,"distinction")

    def test_merit(self):
        result= calculator.calculate_grade(60)
        self.assertEqual(result,"merit")

    def test_pass(self):
        result= calculator.calculate_grade(50)
        self.assertEqual(result,"pass")

    def test_fail(self):
        result= calculator.calculate_grade(49)
        self.assertEqual(result,"fail")   

if __name__ == "__main__":
    unittest.main()