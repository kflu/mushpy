import unittest
from ..timer import Timer
from ..consts import *

class TestTimerClass(unittest.TestCase):
    def setUp(self):
        self.timer = Timer(second=10, hour=2, one_shot=1, active_closed=1, script=lambda x:x)
    
    def test_100_add_timer(self):
        self.assert_( world.IsTimer(self.timer.name) == 0 )

suite = unittest.TestLoader().loadTestsFromTestCase(TestTimerClass)
