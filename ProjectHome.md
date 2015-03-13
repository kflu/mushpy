A Python framework built on top of the [Mushclient](http://www.gammon.com.au/mushclient/mushclient.htm) API. Provides a more "Pythonic" to build MUD robots. Currently, there are several modules available:

## terminal.py ##
Construct a Python file-like object for the Mushclient's notepads

## objects.py ##
  * Trigger
  * Alias
  * Timer

## coroutine.py ##
  * Decorate a callable to use it as a coroutine.

The package can be downloaded from here: http://code.google.com/p/mushpy/downloads/list

Here's the documentation and usage retrieved from the source code:

<pre>

=============<br>
Terminal<br>
=============<br>
<br>
Help on class McTerminal in module mushpy.terminals:<br>
<br>
class McTerminal<br>
<br>
|  Construct a Python file-like object for the Mushclient's notepads.<br>
|<br>
|  This is an abstraction of Mushclient's notepads for the ease of use in<br>
|  Python. An example is better than thousand words:<br>
|<br>
|      >>> import sys<br>
|      >>> sys.stdout = McTerminal("Standard Output")<br>
|<br>
|      >>> print "Hello world"<br>
|<br>
|  Once sys.stdout is been replace by an McTerminal instance, all codes that<br>
|  write to stdout (print, etc.) will be directed to a Mushclient's notepad<br>
|  titled "Standard Output". Fancy, heh?<br>
|<br>
|  When instantiating, several keyword options can be used:<br>
|<br>
|      * time_stamp: (boolean) prefix a time stamp to each line, default to False<br>
|      * prompt_to_save: (boolean) prompt to save on exit, default to False<br>
|      * read_only: (boolean) if the notepad is readonly. default to True<br>
|<br>
|  An example:<br>
|<br>
|      >>> notepad = McTerminal( "An McTerminal Example", time_stamp=True, read_only=True )<br>
|      >>> print >> notepad, "Hello world!"<br>
|      >>> print >> notepad, "Yeah! It's so easy to use Mushclient!"<br>
|<br>
|  The output:<br>
|<br>
|      05/14/10 22:01:26: Initializing...<br>
|      05/14/10 22:03:41: Hello world!<br>
|      05/14/10 22:03:57: Yeah! It's so easy to use Mushclient!<br>
<br>
==============<br>
Alias<br>
==============<br>
<br>
Help on class Alias in module mushpy.objects:<br>
<br>
class Alias(McObject)<br>
<br>
|  The Python wrapper of Mushclient's Alias<br>
|<br>
|  Usage is the same as Trigger.<br>
<br>
=============<br>
Timer<br>
=============<br>
<br>
Help on class Timer in module mushpy.objects:<br>
<br>
class Timer(McObject)<br>
<br>
|  Python wrapper of Mushclient's Timer.<br>
|<br>
|  Usage is similar to Trigger/Alias, with a few exceptions.<br>
|<br>
|  To instantiate:<br>
|<br>
|      >>> timer = Timer( hour, minute, second, option1=value1, option2=value2, ... )<br>
|<br>
|  To use as a decorator<br>
|<br>
|      >>> @Timer.make( hour, minute, second, [keyword options...] )<br>
|      >>> def callback( name ):<br>
|      ...     pass<br>
<br>
==============<br>
Coroutine<br>
==============<br>
<br>
Help on class coroutine in module mushpy.coroutine:<br>
<br>
class coroutine(__builtin__.object)<br>
<br>
|  Decorate a callable to use it as a coroutine.<br>
|<br>
|  Usage:<br>
|      >>> @coroutine()<br>
|      >>> def bla():<br>
|      ...     pass<br>
|<br>
|  or<br>
|      >>> def bla(): pass<br>
|      >>> bla = coroutine()(bla)<br>
|<br>
|  To write a coroutine, there is a protocol to follow:<br>
|<br>
|      1. The decorated callable takes the arguments to generate the<br>
|      generator. If you don't know what it is, just ignore it and use no<br>
|      arguments.<br>
|<br>
|      2. On the first line of the coroutine, you must use the following yield<br>
|      statement to receive the arguments from the caller.<br>
|<br>
|          >>> args, kwargs = yield<br>
|<br>
|      3. Likewise, each time you yield, the return value of the yield<br>
|      statement will be (args, kwargs) from the caller.<br>
|<br>
|      4. (Feature) You can use the following yields to specify when to resume<br>
|      running the code below the yields:<br>
|<br>
|          >>> # resume after 5 seconds<br>
|          >>> args, kwargs = yield ('timer', 0,0,5)<br>
|<br>
|          >>> # resume when the pattern matched<br>
|          >>> args, kwargs = yield ('match', r'some regular expression pattern')<br>
|<br>
|      5. When the coroutine returns, the caller will receive the return value<br>
|      StopIteration. Otherwise, the caller will always receive the return<br>
|      value None. Since it's not the attemp of a coroutine to return<br>
|      something to the caller, but resume doing something at times, I<br>
|      currently do not plan to provide a protocol for returning a meaningfull<br>
|      value to the caller.<br>
|<br>
|  An example of using coroutines:<br>
|<br>
|  >>> @coroutine(arg_to_aCoroutine)<br>
|  ... def aCoroutine(arg_to_aCoroutine):<br>
|  ...     args, kwargs = yield    # Must have this at the first line<br>
|  ...     print 'arguments of the first call', args, kwargs<br>
|  ...<br>
|  ...     args, kwargs = yield ('timer', 0,0,3)<br>
|  ...     print '3 seconds have passed. Arguments:', args, kwargs<br>
|  ...<br>
|  ...     args, kwargs = yield ('match', r'hello world')<br>
|  ...     print 'I see "hello world" from the MUD output. Arguments:', args, kwargs<br>
|  ...<br>
|  ...     # Coroutine returns here. Caller will receive StopIteration<br>
|  ...     return<br>
<br>
</pre>