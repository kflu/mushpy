from common import *
_gbl = ax._scriptEngine_.globalNameSpaceModule

_COROUTINE_TABLE = []

def coroutine_(func):
    '''Decorator suspensible.

    This decorator is used to make a generator be used exactly as a function
    and can be suspended and resumed.
    
    There's special usage when defining the suspensible function:

    * a "args = yield None" call must be at the begining of the function.
    * Every time a suspension is needed, call "args = yield ret_val", ret_val
      is the value to be returned to the caller.
    * args is a tuple containing the argument passed by the resuming call in
      the format: (args, kwargs)

    [More] TODO
    * If the coroutine yields ( 'regexp', 'some_regexp_pattern' ), we should
      create a temp trigger which will be fired on matching the pattern.
    * If the coroutine yields ( 'timer', seconds ), we should create a temp
      timer which will be fired on elapsing the specified amount of seconds.


    See the example function "_gg()" as below.
    '''
    def ret_func(*args, **kwargs):
        # if ret_func is exposed, that means this call is a call by a temp trigger/timer. So unexpose it.
        if hasattr(_gbl, ret_func.__script_name):
            delattr(_gbl, ret_func.__script_name)
        try:
            if not hasattr(ret_func, 'gen'):
                ret_func.gen = ret_func.__func() # instantiate generator
                ret_func.gen.send(None) # consume the 1st one
            ret = ret_func.gen.send( (args, kwargs) )
            if not isinstance(ret, (list, tuple)): return ret
            if ret[0] == 'regexp':
                pattern = ret[1]
                # Expose the script function to global namespace
                expose(ret_func, ret_func.__script_name)
                add_tri(ret_func.__script_name, "", pattern, ret_func.__script_name, enable=1, oneshot=1)
                return
            elif ret[0] == 'timer':
                duration = ret[1]
                (hour, min, sec) = tuple(ret[1:])
                expose(ret_func, ret_func.__script_name)
                add_timer(ret_func.__script_name, hour, min, sec, ret_func.__script_name, enable=1)
                return
            else:
                raise TypeError

        except StopIteration:
            del ret_func.gen
        except Exception, e:
            # something else happend, also reset status
            import traceback
            world.appendtonotepad("suspensible error", u"error during generator call:\r\n"\
                    "%s" % '\r\n'.join(traceback.format_exc().splitlines())  )
            world.appendtonotepad("\r\nclear the execution status.")
            del ret_func.gen
            raise
    # ------ Register the coroutine, assign id, and global script name ---------
    ret_func.__func = func
    _COROUTINE_TABLE.append(ret_func)
    ret_func.id = len(_COROUTINE_TABLE)
    ret_func.__script_name = 'coroutine__%s__%s' % (func.__name__, ret_func.id)
    return ret_func

import collections
from objects import Trigger, Timer
class coroutine(object):
    '''Decorate a callable to use it as a coroutine.

    Usage:
        @coroutine()
        def bla():
            pass

    or
        def bla(): pass
        bla = coroutine()(bla)

    To write a coroutine, there is a protocol to follow:
        
        1. The decorated callable takes the arguments to generate the
        generator. If you don't know what it is, just ignore it and use no
        arguments.

        2. On the first line of the coroutine, you must use the following yield
        statement to receive the arguments from the caller.

            args, kwargs = yield

        3. Likewise, each time you yield, the return value of the yield
        statement will be (args, kwargs) from the caller.

        4. (Feature) You can use the following yields to specify when to resume
        running the code below the yields:

            # resume after 5 seconds
            args, kwargs = yield ('timer', 0,0,5)

            # resume when the pattern matched
            args, kwargs = yield ('match', r'some regular expression pattern')

        5. When the coroutine returns, the caller will receive the return value
        StopIteration. Otherwise, the caller will always receive the return
        value None. Since it's not the attemp of a coroutine to return
        something to the caller, but resume doing something at times, I
        currently do not plan to provide a protocol for returning a meaningfull
        value to the caller.

    An example of using coroutines:

    @coroutine(arg_to_aCoroutine)
    def aCoroutine(arg_to_aCoroutine):
        args, kwargs = yield    # Must have this at the first line
        print 'arguments of the first call', args, kwargs

        args, kwargs = yield ('timer', 0,0,3)
        print '3 seconds have passed. Arguments:', args, kwargs

        args, kwargs = yield ('match', r'hello world')
        print 'I see "hello world" from the MUD output. Arguments:', args, kwargs

        # Coroutine returns here. Caller will receive StopIteration
        return

    '''
    def __init__(self, *args, **kwargs):
        '''Arguments should be used to instantiate a generator object'''
        self.args = args
        self.kwargs = kwargs
        if len(args) and isinstance(args[0], collections.Callable):
            raise TypeError(args[0], 'Do you mean @dec() ???')

    def __call__(self, func):
        '''Called on the decorated function.
        
        Should return a function.'''
        gen = func(*self.args, **self.kwargs)
        # consume the first run
        gen.send(None)

        def ret_func(*args, **kwargs):
            '''This is the resumable function.'''
            try:
                ret = gen.send( (args, kwargs) )
                if not isinstance(ret, collections.Iterable):
                    return
                if ret[0] == 'match':
                    match = ret[1]
                    trig = Trigger()
                    trig.create(match, one_shot=1, enabled=1)
                    trig.callback = ret_func
                    return
                elif ret[0] == 'timer':
                    hh,mm,ss = ret[1:4]
                    timer = Timer()
                    timer.create(hh,mm,ss, one_shot=1, enabled=1)
                    timer.callback = ret_func
                    return
                else:
                    raise TypeError(ret[0], 'Invalid return value')
            except StopIteration:
                # FIXME is this appropriate?
                return StopIteration
            
        return ret_func

