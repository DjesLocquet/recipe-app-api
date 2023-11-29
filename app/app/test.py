"""
Sample test file
"""

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """Sample test class"""

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        result = calc.add(3, 8)
        self.assertEqual(result, 11)

    def test_subtract_numbers(self):
        """Test substraction of two numbers"""
        result = calc.subtract(5, 11)
        self.assertEqual(result, 6)

