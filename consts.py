class TriggerFlags:
    eEnabled = 1 # enable trigger 
    eOmitFromLog = 2 # omit from log file 
    eOmitFromOutput = 4 # omit trigger from output 
    eKeepEvaluating = 8 # keep evaluating 
    eIgnoreCase = 16 # ignore case when matching 
    eTriggerRegularExpression = 32 # trigger uses regular expression 
    eExpandVariables = 512 # expand variables like @direction 
    eReplace = 1024 # replace existing trigger of same name 
    eLowercaseWildcard = 2048 # wildcards forced to lower-case
    eTemporary = 16384 # temporary - do not save to world file 

    KeepEval_Re_Replace = eKeepEvaluating|eTriggerRegularExpression|eReplace|eTemporary
    KeepEval_Re = eKeepEvaluating|eTriggerRegularExpression|eTemporary

class SendToFlags:
    eWorld = 0    # send to MUD                  
    eCommand = 1    # put in command window        
    eOutput = 2    # display in output window     
    eStatus = 3    # put in status line           
    eNewNotepad = 4    # new notepad                  
    eAppendNotepad = 5    # append to notepad            
    eLog = 6    # put in log file              
    eReplaceNotepad = 7    # replace notepad              
    eQueue = 8    # queue it                     
    eVariable = 9    # set a variable               
    eExecute = 10    # re-parse as command          
    eSpeedWalk = 11    # send to MUD as speedwalk     
    eScript = 12    # send to script engine        
    eBeforeQueue = 13    # send without queuing
    eScriptOmitFromOutput = 14    # Only Alias: send to script engine - after omitting from output

class TriggerColours:
    NOCHANGE = -1
    custom1 = 0
    custom2 = 1
    custom3 = 2 
    custom4 = 3
    custom5 = 4
    custom6 = 5
    custom7 = 6
    custom8 = 7
    custom9 = 8
    custom10 = 9
    custom11 = 10
    custom12 = 11
    custom13 = 12
    custom14 = 13
    custom15 = 14
    custom16 = 15

class AliasFlags:
    eEnabled = 1 # same as for AddTrigger 
    eIgnoreAliasCase = 32 # ignore case when matching 
    eOmitFromLogFile = 64 # omit this alias from the log file 
    eAliasRegularExpression = 128 # alias is regular expressions 
    eExpandVariables = 512 # same as for AddTrigger 
    eReplace = 1024 # same as for AddTrigger 
    eAliasSpeedWalk = 2048 # interpret send string as a speed walk string 
    eAliasQueue = 4096 # queue this alias for sending at the speedwalking delay interval 
    eAliasMenu = 8192 # this alias appears on the alias menu 
    eTemporary = 16384 # same as for AddTrigger

    Re_Replace = eAliasRegularExpression | eReplace | eTemporary
    Re = eAliasRegularExpression | eTemporary

class TimerFlags:
    eEnabled = 1 # same as for AddTrigger
    eAtTime = 2 # if not set, time is "every" 
    eOneShot = 4 # if set, timer only fires once 
    eTimerSpeedWalk = 8 # timer does a speed walk when it fires 
    eTimerNote = 16 # timer does a world.note when it fires 
    eActiveWhenClosed = 32  # timer fires even when world is disconnected
    eReplace = 1024 # same as for AddTrigger
    eTemporary = 16384 # same as for AddTrigger

    OneShot = eOneShot | eTemporary | eActiveWhenClosed

class ErrorNo:
    eOK = 0 # No error
    eWorldOpen = 30001 # The world is already open
    eWorldClosed = 30002 # The world is closed, this action cannot be performed
    eNoNameSpecified = 30003 # No name has been specified where one is required
    eCannotPlaySound = 30004 # The sound file could not be played
    eTriggerNotFound = 30005 # The specified trigger name does not exist
    eTriggerAlreadyExists = 30006 # Attempt to add a trigger that already exists
    eTriggerCannotBeEmpty = 30007 # The trigger "match" string cannot be empty
    eInvalidObjectLabel = 30008 # The name of this object is invalid
    eScriptNameNotLocated = 30009 # Script name is not in the script file
    eAliasNotFound = 30010 # The specified alias name does not exist
    eAliasAlreadyExists = 30011 # Attempt to add a alias that already exists
    eAliasCannotBeEmpty = 30012 # The alias "match" string cannot be empty
    eCouldNotOpenFile = 30013 # Unable to open requested file
    eLogFileNotOpen = 30014 # Log file was not open
    eLogFileAlreadyOpen = 30015 # Log file was already open
    eLogFileBadWrite = 30016 # Bad write to log file
    eTimerNotFound = 30017 # The specified timer name does not exist
    eTimerAlreadyExists = 30018 # Attempt to add a timer that already exists
    eVariableNotFound = 30019 # Attempt to delete a variable that does not exist
    eCommandNotEmpty = 30020 # Attempt to use SetCommand with a non-empty command window
    eBadRegularExpression = 30021 # Bad regular expression syntax
    eTimeInvalid = 30022 # Time given to AddTimer is invalid
    eBadMapItem = 30023 # Direction given to AddToMapper is invalid
    eNoMapItems = 30024 # No items in mapper
    eUnknownOption = 30025 # Option name not found
    eOptionOutOfRange = 30026 # New value for option is out of range
    eTriggerSequenceOutOfRange = 30027 # Trigger sequence value invalid
    eTriggerSendToInvalid = 30028 # Where to send trigger text to is invalid
    eTriggerLabelNotSpecified = 30029 # Trigger label not specified/invalid for 'send to variable'
    ePluginFileNotFound = 30030 # File name specified for plugin not found
    eProblemsLoadingPlugin = 30031 # There was a parsing or other problem loading the plugin
    ePluginCannotSetOption = 30032 # Plugin is not allowed to set this option
    ePluginCannotGetOption = 30033 # Plugin is not allowed to get this option
    eNoSuchPlugin = 30034 # Requested plugin is not installed
    eNotAPlugin = 30035 # Only a plugin can do this
    eNoSuchRoutine = 30036 # Plugin does not support that subroutine (subroutine not in script)
    ePluginDoesNotSaveState = 30037 # Plugin does not support saving state
    ePluginCouldNotSaveState = 30037 # Plugin could not save state (eg. no state directory)
    ePluginDisabled = 30039 # Plugin is currently disabled
    eErrorCallingPluginRoutine = 30040 # Could not call plugin routine
    eCommandsNestedTooDeeply = 30041 # Calls to "Execute" nested too deeply
    eCannotCreateChatSocket = 30042 # Unable to create socket for chat connection
    eCannotLookupDomainName = 30043 # Unable to do DNS (domain name) lookup for chat connection
    eNoChatConnections = 30044 # No chat connections open
    eChatPersonNotFound = 30045 # Requested chat person not connected
    eBadParameter = 30046 # General problem with a parameter to a script call
    eChatAlreadyListening = 30047 # Already listening for incoming chats
    eChatIDNotFound = 30048 # Chat session with that ID not found
    eChatAlreadyConnected = 30049 # Already connected to that server/port
    eClipboardEmpty = 30050 # Cannot get (text from the) clipboard
    eFileNotFound = 30051 # Cannot open the specified file
    eAlreadyTransferringFile = 30052 # Already transferring a file
    eNotTransferringFile = 30053 # Not transferring a file
    eNoSuchCommand = 30054 # There is not a command of that name
    eArrayAlreadyExists = 30055 # That array already exists
    eBadKeyName = 30056 # That name is not permitted for a key
    eArrayDoesNotExist = 30056 # That array does not exist
    eArrayNotEvenNumberOfValues = 30057 # Values to be imported into array are not in pairs
    eImportedWithDuplicates = 30058 # Import succeeded, however some values were overwritten
    eBadDelimiter = 30059 # Import/export delimiter must be a single character, other than backslash
    eSetReplacingExistingValue = 30060 # Array element set, existing value overwritten
    eKeyDoesNotExist = 30061 # Array key does not exist
    eCannotImport = 30062 # Cannot import because cannot find unused temporary character
    eItemInUse  = 30063	# Cannot delete trigger/alias/timer because it is executing a script
    eSpellCheckNotActive  = 30064	# Spell checker is not active
    eCannotAddFont  = 30065	# Cannot create requested font
    ePenStyleNotValid  = 30066	# Invalid settings for pen parameter
    eUnableToLoadImage  = 30067	# Bitmap image could not be loaded
    eImageNotInstalled  = 30068	# Image has not been loaded into window
    eInvalidNumberOfPoints  = 30069	# Number of points supplied is incorrect
    eInvalidPoint  = 30070	# Point is not numeric
    eHotspotPluginChanged  = 30071	# Hotspot processing must all be in same plugin
    eHotspotNotInstalled  = 30072	# Hotspot has not been defined for this window
    eNoSuchWindow  = 30073	# Requested miniwindow does not exist
    eBrushStyleNotValid  = 30074	# Invalid settings for brush parameter

