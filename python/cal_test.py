import unittest
from fractions import Fraction
from unittest.mock import patch
import Calculate

class TestCalculate(unittest.TestCase):

    def test_instead(self):
        a = "(1+2**3**2/5**3)"
        self.assertEqual(Calculate.instead(a), "(1+2^3^2/5^3)")

    def test_precedence(self):
        self.assertEqual(Calculate.precedence("+"), 2)
        self.assertEqual(Calculate.precedence("-"), 2)
        self.assertEqual(Calculate.precedence("*"), 3)
        self.assertEqual(Calculate.precedence("^"), 4)
        self.assertEqual(Calculate.precedence("/"), 3)
        self.assertEqual(Calculate.precedence("("), 1)
        self.assertEqual(Calculate.precedence(")"), 1)

    def test_exps_cal(self):
        self.assertEqual(Calculate.exps_cal(["(", 1, "+", 3, "^", "(", 3, "+", 4, "/", 2, ")", "-", 300, ")"]), Fraction(-56))
        self.assertEqual(Calculate.exps_cal(["(", 1, "*", 3, "^", "(", 3, "+", 4, "/", 2, ")", "/", 300, ")"]), Fraction(81,100))

    def test_separate(self):
        self.assertEqual(Calculate.separate("((1+3^3)/(1*3-4))"), ["(", "(", 1, "+", 3, "^", 3, ")", "/", "(", 1, "*", 3, "-", 4, ")", ")"])

if __name__ == '__main__':
    unittest.main()
