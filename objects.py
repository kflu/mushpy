from common import *


class Dispatcher(object):
    def __init__(self, type_):
        self.type = type_
    def __call__(self, *args):
        '''Called by Mush when trigger/alias/timer fired.'''

        name = args[0]

        # Get the callbck list
        if self.type == 'trigger':
            cb_list = Trigger._callback_list
        elif self.type == 'alias':
            cb_list = Alias._callback_list
        elif self.type == 'timer':
            cb_list = Timer._callback_list

        # Find the callback to call
        assert name in cb_list
        cb = cb_list[name]

        # call the callback
        cb(*args)

        # delete the one_shot object's callback, etc.
        for obj in cb.mc_objects:
            if obj['name'] == name and obj._type == self.type:
                if obj['one_shot']:
                    del cb_list[name]
                    obj.delete()
                    break

_trigger_dispatcher = Dispatcher('trigger'); expose(_trigger_dispatcher, "DISPATCHER_TRIGGER")
_timer_dispatcher = Dispatcher('timer'); expose(_timer_dispatcher, "DISPATCHER_TIMER")
_alias_dispatcher = Dispatcher('alias'); expose(_alias_dispatcher, "DISPATCHER_ALIAS")

class McObject(object):

    _type = None
    _dispatcher = None  # a callable to be called on firing and to dispatch the object to callback
    _callback_list = None # a dict: obj_name => callback

    # ----------- VIRTUAL ----------------
    def _set_option(self, key, value):
        '''Proxy to set object option.
        
        It should return the corresponding MUSH return error code.'''
        raise NotImplementedError

    def _get_option(self, key):
        '''Proxy to get object option.'''
        raise NotImplementedError

    def _add(self, name, flags, **options):
        '''Proxy to add object'''
        raise NotImplementedError

    def _del(self):
        '''Proxy to del object.'''
        raise NotImplementedError

    def _exists(self, name):
        '''If object by the name already exists.
        
        Should return True/False
        '''
        raise NotImplementedError

    def create(self):
        '''Classes own create function.'''
        raise NotImplementedError
    # ----------- END VIRTUAL ----------------

    def __init__(self, name=""):
        '''Construct object.
        '''
        self.__name = name

    def __repr__(self):
        return '<%s__%s>' % (self._type, self.__name)

    def __cmp__(self, other):
        if repr(self) == repr(other): return 0

    def __hash__(self):
        return hash(self.__repr__())

    def __getitem__(self, key):
        if key == 'name':
            return self.__name
        res = self._get_option(key)
        if res == None: # FIXME Obj. not found handled???
            raise KeyError(key)
        return res

    def __setitem__(self, key, value):
        if key == 'name':
            raise KeyError(key, "Cannot set 'name'")

        res = self._set_option(key, value)
        if res != ErrorNo.eOK:
            raise KeyError(res, 'Error setting option %s => %s' % (key, value))

    def _create(self, flags, **options):
        if self.__name == "":
            self.__name = self.gen_uniq_name()
        if self.exists():
            raise ValueError(self.__name, "object already exists")
        self._add(self.__name, flags, **options)

    @property
    def callback(self):
        '''look up in the global list. return None if not found'''
        return self._callback_list.get(self.__name, None)

    @callback.setter
    def callback(self, value):
        '''Set a callback to call when match matches.

        A callback can be any python callable, which should meet the
        corresponding mush object's callback interface, i.e.,

            * trigger/alias: cb(name, line, wc)
            * timer: cb(name)
        '''

        # if self previously has a callback, remove self from the callback's mc_objects:
        if self.callback:
            self.callback.mc_objects.remove( self )

        #import rpdb2; rpdb2.start_embedded_debugger("kkkk")
        if not callable(value):
            raise TypeError(value, 'Not callable')

        # add to callback list
        assert self.__name
        self._callback_list[self.__name] = value

        # set dispatcher as "script"
        self['script'] = self._dispatcher.global_name

        # Add a reference to self in the callback object
        if not hasattr(value, "mc_objects"):
            value.mc_objects = set([])   # a set of objects


        value.mc_objects.add( self )


    @callback.deleter
    def callback(self):
        cb = self.callback
        if not cb: return
        del self._callback_list[self.__name]
        cb.mc_objects.remove(self)

    def gen_uniq_name(self):
        '''Return the first available (non-existing) name that has the form:

        "trigger__255"
        '''
        if self.__name:
            raise ValueError(self.__name, 'Already have a name.')
        ii = 1
        name = '%s__%s' % (self._type, ii)
        while self._exists(name):
            assert ii < 65536
            ii += 1
            name = '%s__%s' % (self._type, ii)
        # Got a uniq name
        return name

    def delete(self):
        # FIXME should fail on failure
        try:
            del self.callback
        except AttributeError:
            pass

        res = self._del()
        if res == ErrorNo.eItemInUse:
            pass
        elif res != ErrorNo.eOK:
            raise SystemError(res, "Error deleting object.")

    def exists(self):
        return self._exists(self.__name)

    def enable(self):
        self['enabled'] = 1
    def disable(self):
        self['enabled'] = 0

    def disable_group(self):
        raise NotImplementedError
    def enable_group(self):
        raise NotImplementedError

# ------------------------
#       Trigger
# ------------------------
class Trigger(McObject):
    _type = 'trigger'
    _dispatcher = _trigger_dispatcher
    _callback_list = {}

    @staticmethod
    def make(match, flags = None, **options):
        if 'script' in options:
            raise KeyError(options, '"script" cannot be used in this decorator')

        name = ""
        if 'name' in options:
            name = options['name']
            del options['name']

        def called_on_func(func):
            trig = Trigger(name)
            trig.create(match, flags, **options)
            trig.callback = func
            return func
        return called_on_func

    def _set_option(self, key, value):
        return world.SetTriggerOption(self['name'], key, value)

    def _get_option(self, key):
        return world.GetTriggerOption(self['name'], key)

    def _add(self, name, flags, **options):
        match = options['match']
        del options['match']
        res = world.AddTriggerEx(name, match, "", flags, -1, 0, "", "", 0, 100)
        if res != ErrorNo.eOK:
            raise SystemError(res, 'Adding failed')
        for (key, value) in options.items():
            self[key] = value

    def _del(self):
        return world.DeleteTrigger(self['name'])

    def _exists(self, name):
        '''If object by the name already exists.
        
        Should return True/False
        '''
        return ErrorNo.eOK == world.IsTrigger(name)

    def create(self, match, flags=None, **options):
        if not match:
            raise ValueError(match, "'match' cannot be empty")
        options['match'] = match

        if flags == None:
            flags = TriggerFlags.KeepEval_Re

        self._create(flags, **options)

# ------------------------
#       Alias
# ------------------------
class Alias(McObject):
    _type = 'alias'
    _dispatcher = _alias_dispatcher
    _callback_list = {}

    @staticmethod
    def make(match, flags = None, **options):
        if 'script' in options:
            raise KeyError(options, '"script" cannot be used in this decorator')

        name = ""
        if 'name' in options:
            name = options['name']
            del options['name']

        def called_on_func(func):
            alias = Alias(name)
            alias.create(match, flags, **options)
            alias.callback = func
            return func
        return called_on_func

    def _set_option(self, key, value):
        return world.SetAliasOption(self['name'], key, value)

    def _get_option(self, key):
        return world.GetAliasOption(self['name'], key)

    def _add(self, name, flags, **options):
        match = options['match']
        del options['match']
        res = world.AddAlias(name, match, "", flags, "")
        if res != ErrorNo.eOK:
            raise SystemError(res, 'Adding failed')
        for (key, value) in options.items():
            self[key] = value

    def _del(self):
        return world.DeleteAlias(self['name'])

    def _exists(self, name):
        '''If object by the name already exists.
        
        Should return True/False
        '''
        return ErrorNo.eOK == world.IsAlias(name)

    def create(self, match, flags=None, **options):
        if not match:
            raise ValueError(match, "'match' cannot be empty")
        options['match'] = match

        if flags == None:
            flags = AliasFlags.Re

        self._create(flags, **options)


class Timer(McObject):
    _type = 'timer'
    _dispatcher = _timer_dispatcher
    _callback_list = {}

    @staticmethod
    def make(hour, minute, second, flags = None, **options):
        if 'script' in options:
            raise KeyError(options, '"script" cannot be used in this decorator')

        name = ""
        if 'name' in options:
            name = options['name']
            del options['name']

        def called_on_func(func):
            timer = Timer(name)
            timer.create(hour, minute, second, flags, **options)
            timer.callback = func
            return func
        return called_on_func

    def _set_option(self, key, value):
        return world.SetTimerOption(self['name'], key, value)

    def _get_option(self, key):
        return world.GetTimerOption(self['name'], key)

    def _add(self, name, flags, **options):
        res = world.AddTimer(name, 0,0,1, "", flags, "")
        if res != ErrorNo.eOK:
            raise SystemError(res, 'Adding failed')
        for (key, value) in options.items():
            self[key] = value

    def _del(self):
        return world.DeleteTimer(self['name'])

    def _exists(self, name):
        '''If object by the name already exists.
        
        Should return True/False
        '''
        return ErrorNo.eOK == world.IsTimer(name)

    def create(self, hour,minute,second, flags=None, **options):
        options['hour'] = hour
        options['minute'] = minute
        options['second'] = second

        if flags == None:
            flags = TimerFlags.OneShot

        self._create(flags, **options)
