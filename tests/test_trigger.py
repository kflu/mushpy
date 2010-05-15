import unittest
from ..trigger import Trigger
from ..consts import *

class TestTriggerClass(unittest.TestCase):
    def setUp(self):
        trig = Trigger("pattern")
        self.trig = trig

    def test_100_add_trig(self):
        # verify trigger name is not ""
        self.failIf( self.trig.name == "", 'trig name cannot be ""')

        # verify trigger can be found by name
        self.failIf( ErrorNo.eTriggerNotFound == world.IsTrigger(self.trig.name),
                "cannot found the trigger by its name: %s"%self.trig.name)


    def test_200_get_pattern(self):
        # testing getting trig option
        self.assert_( self.trig['match'] == self.trig.pattern,
                'testing getting trig. option: %s != %s' % (self.trig['match'], self.trig.pattern) )
    # FIXME does not work in MC
    def test_210_get_name(self):
        self.assert_( self.trig['name'] == self.trig.name)
    def test_220_get_group(self):
        self.assert_( self.trig['group'] == "",
                "group name mismatch: %s != ''" % self.trig['group'])


    # FIXME broken in MC
    def test_300_set_name(self):
        # testing setting trig option
        self.trig['name'] = 'hello_name'
        self.assert_( self.trig['name'] == 'hello_name',
                'verify setting/getting trigger name')

    def test_400_set_match(self):
        self.trig['match'] = 'new_match'
        self.assert_( self.trig['match'] == 'new_match' )
        self.assert_( self.trig.pattern == 'new_match' )
        self.assert_( self.trig.options['match'] == 'new_match' )

    def test_500_set_one_shot(self):
        self.trig['one_shot'] = 1
        self.assert_( self.trig['one_shot'] == 1 )
        self.assert_( self.trig.options['one_shot'] == 1 )

    def test_600_decorate(self):
        def HelloDec(name, line, wc):
            pass
        HelloDec = Trigger.decorate("dec_pattern")(HelloDec)
        self.assert_( hasattr(HelloDec, 'trigger') )
        self.assert_( 0 == world.IsTrigger(HelloDec.trigger[0].name) )

    def test_700_decorate_exception(self):
        def HelloDec(name, line, wc):
            pass
        def dec_test():
            TestTriggerClass.test_700_decorate_exception.HelloDec = \
                    Trigger.decorate("dec_pattern", script=HelloDec)(HelloDec)
        self.assertRaises(KeyError, dec_test)


suite = unittest.TestLoader().loadTestsFromTestCase(TestTriggerClass)

