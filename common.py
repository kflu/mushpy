from consts import *

def errlog(what):
    print '(E)', what

def gn(a,b):
    '''Combine string a,b to get the new name.

    e.g., 'group', 'name' -> 'group_name'
    '''
    return u'%s_%s' % (a,b)

def add_timer(name, hh, mm, ss, script, flags=TimerFlags.OneShot, enable=0):
    if enable: flags = flags | TimerFlags.eEnabled
    world.AddTimer(name, hh,mm,ss, "", flags, script)

def add_tri(name, group, pattern, script, flags=TriggerFlags.KeepEval_Re_Replace, enable=0, oneshot=0):
    if enable:
        flags = flags | TriggerFlags.eEnabled
    errno = world.AddTriggerEx(name, pattern, "", flags, -1,0,"", script, 0, 100)
    assert errno == ErrorNo.eOK, "trigger: error while adding trigger (%s)" % errno
    errno = world.SetTriggerOption(name, "group", group)
    assert errno == ErrorNo.eOK, "trigger: error while setting group name (%s)" % errno
    if oneshot:
        errno = world.SetTriggerOption(name, "one_shot", 1)
        assert errno == ErrorNo.eOK, "trigger: error while setting one_shot (%s)" % errno

def add_alias(name, group, pattern, script, flags=AliasFlags.Re_Replace, enable=0):
    if enable:
        flags = flags | AliasFlags.eEnabled
    errno = world.AddAlias(name, pattern, "", flags, script)
    assert errno == ErrorNo.eOK, "alias: error while adding alias (%s)" % errno
    errno = world.SetAliasOption(name, "group", group)
    assert errno == ErrorNo.eOK, "alias: error while setting alias group (%s)" % errno

class trigger:
    '''Decorator to add a trigger.

    The trigger name will be converted to group_name.
    The callable function will be exposed to global namespace, with name:
      group_name__FuncName.
    '''
    def __init__(self, name, group, pattern, flags=TriggerFlags.KeepEval_Re_Replace):
        self.__name = gn(group, name)
        self.__group = group
        self.__pattern = pattern
        self.__flags = flags

    def __call__(self, func):
        # register the function to global namespace
        func_name = "%s__%s" % (self.__name, func.__name__)
        expose(func, func_name)
        add_tri(self.__name, self.__group, self.__pattern, func_name, self.__flags)
        return func

class alias:
    '''Decorator to add a trigger.

    The trigger name will be converted to group_name.
    The callable function will be exposed to global namespace, with name:
      group_name__FuncName.
    '''
    def __init__(self, name, group, pattern, flags=AliasFlags.Re_Replace):
        self.__name = gn(group, name)
        self.__group = group
        self.__pattern = pattern
        self.__flags = flags

    def __call__(self, func):
        func_name = "%s__%s" % (self.__name, func.__name__)
        expose(func, func_name)
        add_alias(self.__name, self.__group, self.__pattern, func_name, self.__flags)
        return func

def expose(*args):
    '''Expose the functino to global namespace.

    After exposing, the global name is set to an attribute in the callable
    object as "global_name"

    Can be used as decorator as well as a function:

    @expose("global_name")
    def func: ...
    
    or

    expose(func, "global name")
    '''
    if len(args) == 2:
        # called as a function
        func, name = args[0:2]
        if not callable(func):
            raise TypeError(func, 'Not callable')   #FIXME
        print "exposing func: %s with name: %s" % (str(func), name)
        print 'expose(): global name space already has %s exposed.' % name
        setattr(ax._scriptEngine_.globalNameSpaceModule, name, func.__call__)
        setattr(func, 'global_name', name)
        return

    if len(args) == 1:
        # called as a decorator
        name = args[0]
        def CalledOnFunc(func):
            expose(func, name)
            return func
        return CalledOnFunc
