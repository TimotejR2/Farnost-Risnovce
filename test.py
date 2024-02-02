import unittest
from functions import convert_date

class TestConvertDate(unittest.TestCase):
    def test_convert_date(self):
        self.assertEqual(convert_date('2022-02-15'), '15.2', "Failed for '2022-02-15'")
        self.assertEqual(convert_date('2023-10-05'), '5.10', "Failed for '2023-10-05'")
        self.assertEqual(convert_date('2021-12-01'), '1.12', "Failed for '2021-12-01'")
    

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    suite.addTest(TestConvertDate('test_convert_date'))

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests and get the result
    result = runner.run(suite)

    # Access the result information
    print("Number of tests run:", result.testsRun)
    print("Number of failures:", len(result.failures))
    print("Number of errors:", len(result.errors))
