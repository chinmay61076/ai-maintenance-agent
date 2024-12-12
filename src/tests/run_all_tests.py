import unittest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import test cases
from src.tests.test_sensors import TestSensors
from src.tests.test_learning import TestLearning
from src.tests.test_decision import TestDecision

def run_all_tests():
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSensors))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLearning))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDecision))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    print("Running all maintenance agent tests...\n")
    runner.run(test_suite)

if __name__ == '__main__':
    run_all_tests()
