import os
import sys

import demo
from reader.json_reader import JSONReader
from reader.schema import JSONInput
from entity.inventory import Inventory

import unittest


PACKAGE_PARENT = '...'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


class TestDemo(unittest.TestCase):
    # All the cases also test successful execution of critical section
    def setUp(self):
        self.reader = JSONReader(schema=JSONInput)
        self.test_inputs_path = "tests/input/"

    def test_all_successful_orders(self):
        expected = ['hot_tea is prepared', 'black_tea is prepared']
        actual = demo.execute_demo_order(
            self.reader, source=self.test_inputs_path+"1.json",
            inv_refill_time=-1, inv_fetch_time=-1)

        self.assertEqual(expected, actual)

    def test_insufficient_ingredient(self):
        expected = ['hot_tea is prepared',
                    'black_tea cannot be prepared because item tea_leaves_syrup is not sufficient']
        actual = demo.execute_demo_order(
            self.reader, source=self.test_inputs_path+"2.json",
            inv_refill_time=-1, inv_fetch_time=0)

        self.assertEqual(expected, actual)

    def test_unvailable_ingredient(self):
        expected = ['hot_tea is prepared',
                    'black_tea cannot be prepared because maple_syrup is not available']
        actual = demo.execute_demo_order(
            self.reader, source=self.test_inputs_path+"3.json",
            inv_refill_time=-1, inv_fetch_time=0)

        self.assertEqual(expected, actual)

    def test_successful_order_pool_execution(self):
        expected = ['hot_tea is prepared',
                    'hot_coffee is prepared',
                    'black_tea cannot be prepared because items hot_water, sugar_syrup is not sufficient',
                    'green_tea cannot be prepared because green_mixture is not available and item sugar_syrup is not sufficient']
        actual = demo.execute_demo_order(
            self.reader, source=self.test_inputs_path+"4.json",
            inv_refill_time=-1, inv_fetch_time=0)

        self.assertEqual(expected, actual)

    def tearDown(self):
        Inventory.reset()


if __name__ == '__main__':
    unittest.main()
