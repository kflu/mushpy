import unittest

suite = unittest.TestSuite()


# loading...

from test_trigger import suite as trigger_suite
suite.addTest(trigger_suite)


from test_timer import suite as timer_suite
suite.addTest(timer_suite)


from objects import suite as objects_suite
suite.addTest(objects_suite)

# Run
unittest.TextTestRunner().run(suite)
