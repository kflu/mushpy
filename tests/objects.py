import unittest
from ..objects import Trigger
from ..consts import *

class TestTrigger(unittest.TestCase):
    def test_100_instantiating(self):
        trig = Trigger()
        trig = Trigger("test")

    def test_200_creating(self):

        options = {'match':'some match', 'group':'some_group'}
        trig = Trigger().create(**options)

        trig = Trigger()
        trig.create(match='somematch', 
                send='world.send("matched")',
                send_to=SendToFlags.eScript)

        self.assert_( trig['match'] == 'somematch' )
        self.assert_( trig['send'] == 'world.send("matched")' )
        self.assert_( trig['send_to'] == SendToFlags.eScript )
        self.assert_( trig.exists() )

        trig.delete()

    def test_300_callback(self):
        trig = Trigger()
        def dummy(name, line, wc):
            print name, line, wc

        trig.create("somepattern")

        trig.callback = dummy

        self.assert_( trig.callback == dummy )

        # verify dispatcher is there
        self.assert_(hasattr( trig, '_dispatcher' ))
        self.assert_(hasattr( ax._scriptEngine_.globalNameSpaceModule, 
            trig._dispatcher.global_name ))

        # verify trig is in the Trigger callback list
        self.assert_( trig['name'] in trig._callback_list )
        self.assert_( trig._callback_list[ trig['name'] ] == dummy )

        # verify trig is in the callback mc_objects:
        self.assert_( hasattr(dummy, 'mc_objects'))
        self.assert_( trig in dummy.mc_objects )

        def dummy2(name, line, wc):
            print "hello", name, line, wc

        trig.callback = dummy2
        self.assert_( trig.callback == dummy2 )

        # make sure trig has been remove from dummy.mc_objects
        self.failIf( trig in dummy.mc_objects )
        # make sure trig is now in dummy2.mc_objects
        self.assert_( trig in dummy2.mc_objects )
        self.assert_( trig._callback_list[ trig['name'] ] == dummy2 )

        del trig.callback
        self.assert_( trig.callback == None )
        self.failIf( trig['name'] in trig._callback_list )
        self.failIf( trig in dummy2.mc_objects )

    def test_400_del(self):
        trig = Trigger('a_uniqe_name')
        trig.create('hello world')

        self.assert_( trig.exists() )

        def dummy(*args):
            print args
        trig.callback = dummy

        self.assert_( trig in dummy.mc_objects )

        trig.delete()

        self.failIf( trig in dummy.mc_objects )
        self.failIf( trig['name'] in trig._callback_list )

    def test_500_enable(self):
        trig = Trigger()
        trig.create('pattern')

        name = trig['name']

        # default disabled
        self.assert_( not world.GetTriggerOption(name, 'enabled') )
        self.assert_( not trig['enabled'] )

        # turned on
        trig.enable()

        self.assert_( world.GetTriggerOption(name, 'enabled') )
        self.assert_( trig['enabled'] )

        # turned off
        trig.disable()

        self.assert_( not world.GetTriggerOption(name, 'enabled') )
        self.assert_( not trig['enabled'] )

        # turned on
        trig['enabled'] = 1

        self.assert_( world.GetTriggerOption(name, 'enabled') )
        self.assert_( trig['enabled'] )

        # turned off
        trig['enabled'] = 0

        self.assert_( not world.GetTriggerOption(name, 'enabled') )
        self.assert_( not trig['enabled'] )

        trig.delete()

    def test_600_decorator(self):

        options = {'enabled':1, 'group':'group_name', 'match':'some match', 'one_shot':1}

        @Trigger.make(**options)
        def dummy(*args):
            print args

        self.assert_( len(dummy.mc_objects) == 1 )
        for trig in dummy.mc_objects:
            self.assert_( trig._callback_list[ trig['name'] ] == dummy )

            for (key, value) in options.items():
                self.assert_( trig[key] == value, "key '%s' don't have value '%s' ('%s')" % (key, value, trig[key]) )

        try:
            @Trigger.make('some pattern', script="blabla")
            def dummy2(*args):
                print args
        except KeyError:
            pass
        except Exception, e:
            self.fail( '%s raised (unexpected)' % e )
        else:
            self.fail( 'a KeyError expected.' )

suite = unittest.TestLoader().loadTestsFromTestCase(TestTrigger)
