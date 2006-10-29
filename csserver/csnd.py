# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _csnd
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


try:
    import weakref
    weakref_proxy = weakref.proxy
except:
    weakref_proxy = lambda x: x


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self): raise AttributeError, "No constructor defined"
    __repr__ = _swig_repr
    __swig_destroy__ = _csnd.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _csnd.PySwigIterator_value(*args)
    def incr(*args): return _csnd.PySwigIterator_incr(*args)
    def decr(*args): return _csnd.PySwigIterator_decr(*args)
    def distance(*args): return _csnd.PySwigIterator_distance(*args)
    def equal(*args): return _csnd.PySwigIterator_equal(*args)
    def copy(*args): return _csnd.PySwigIterator_copy(*args)
    def next(*args): return _csnd.PySwigIterator_next(*args)
    def previous(*args): return _csnd.PySwigIterator_previous(*args)
    def advance(*args): return _csnd.PySwigIterator_advance(*args)
    def __eq__(*args): return _csnd.PySwigIterator___eq__(*args)
    def __ne__(*args): return _csnd.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _csnd.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _csnd.PySwigIterator___isub__(*args)
    def __add__(*args): return _csnd.PySwigIterator___add__(*args)
    def __sub__(*args): return _csnd.PySwigIterator___sub__(*args)
    def __iter__(self): return self
PySwigIterator_swigregister = _csnd.PySwigIterator_swigregister
PySwigIterator_swigregister(PySwigIterator)

CSOUND_SUCCESS = _csnd.CSOUND_SUCCESS
CSOUND_ERROR = _csnd.CSOUND_ERROR
CSOUND_INITIALIZATION = _csnd.CSOUND_INITIALIZATION
CSOUND_PERFORMANCE = _csnd.CSOUND_PERFORMANCE
CSOUND_MEMORY = _csnd.CSOUND_MEMORY
CSOUND_SIGNAL = _csnd.CSOUND_SIGNAL
CSOUND_EXITJMP_SUCCESS = _csnd.CSOUND_EXITJMP_SUCCESS
CSOUNDINIT_NO_SIGNAL_HANDLER = _csnd.CSOUNDINIT_NO_SIGNAL_HANDLER
CSOUNDINIT_NO_ATEXIT = _csnd.CSOUNDINIT_NO_ATEXIT
CSOUND_CONTROL_CHANNEL = _csnd.CSOUND_CONTROL_CHANNEL
CSOUND_AUDIO_CHANNEL = _csnd.CSOUND_AUDIO_CHANNEL
CSOUND_STRING_CHANNEL = _csnd.CSOUND_STRING_CHANNEL
CSOUND_CHANNEL_TYPE_MASK = _csnd.CSOUND_CHANNEL_TYPE_MASK
CSOUND_INPUT_CHANNEL = _csnd.CSOUND_INPUT_CHANNEL
CSOUND_OUTPUT_CHANNEL = _csnd.CSOUND_OUTPUT_CHANNEL
CSOUND_CONTROL_CHANNEL_INT = _csnd.CSOUND_CONTROL_CHANNEL_INT
CSOUND_CONTROL_CHANNEL_LIN = _csnd.CSOUND_CONTROL_CHANNEL_LIN
CSOUND_CONTROL_CHANNEL_EXP = _csnd.CSOUND_CONTROL_CHANNEL_EXP
CSOUND_CALLBACK_KBD_EVENT = _csnd.CSOUND_CALLBACK_KBD_EVENT
CSOUND_CALLBACK_KBD_TEXT = _csnd.CSOUND_CALLBACK_KBD_TEXT
class csRtAudioParams(_object):
    """Proxy of C++ csRtAudioParams class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csRtAudioParams, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csRtAudioParams, name)
    __repr__ = _swig_repr
    __swig_setmethods__["devName"] = _csnd.csRtAudioParams_devName_set
    __swig_getmethods__["devName"] = _csnd.csRtAudioParams_devName_get
    if _newclass:devName = property(_csnd.csRtAudioParams_devName_get, _csnd.csRtAudioParams_devName_set)
    __swig_setmethods__["devNum"] = _csnd.csRtAudioParams_devNum_set
    __swig_getmethods__["devNum"] = _csnd.csRtAudioParams_devNum_get
    if _newclass:devNum = property(_csnd.csRtAudioParams_devNum_get, _csnd.csRtAudioParams_devNum_set)
    __swig_setmethods__["bufSamp_SW"] = _csnd.csRtAudioParams_bufSamp_SW_set
    __swig_getmethods__["bufSamp_SW"] = _csnd.csRtAudioParams_bufSamp_SW_get
    if _newclass:bufSamp_SW = property(_csnd.csRtAudioParams_bufSamp_SW_get, _csnd.csRtAudioParams_bufSamp_SW_set)
    __swig_setmethods__["bufSamp_HW"] = _csnd.csRtAudioParams_bufSamp_HW_set
    __swig_getmethods__["bufSamp_HW"] = _csnd.csRtAudioParams_bufSamp_HW_get
    if _newclass:bufSamp_HW = property(_csnd.csRtAudioParams_bufSamp_HW_get, _csnd.csRtAudioParams_bufSamp_HW_set)
    __swig_setmethods__["nChannels"] = _csnd.csRtAudioParams_nChannels_set
    __swig_getmethods__["nChannels"] = _csnd.csRtAudioParams_nChannels_get
    if _newclass:nChannels = property(_csnd.csRtAudioParams_nChannels_get, _csnd.csRtAudioParams_nChannels_set)
    __swig_setmethods__["sampleFormat"] = _csnd.csRtAudioParams_sampleFormat_set
    __swig_getmethods__["sampleFormat"] = _csnd.csRtAudioParams_sampleFormat_get
    if _newclass:sampleFormat = property(_csnd.csRtAudioParams_sampleFormat_get, _csnd.csRtAudioParams_sampleFormat_set)
    __swig_setmethods__["sampleRate"] = _csnd.csRtAudioParams_sampleRate_set
    __swig_getmethods__["sampleRate"] = _csnd.csRtAudioParams_sampleRate_get
    if _newclass:sampleRate = property(_csnd.csRtAudioParams_sampleRate_get, _csnd.csRtAudioParams_sampleRate_set)
    def __init__(self, *args): 
        """__init__(self) -> csRtAudioParams"""
        this = _csnd.new_csRtAudioParams(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csRtAudioParams
    __del__ = lambda self : None;
csRtAudioParams_swigregister = _csnd.csRtAudioParams_swigregister
csRtAudioParams_swigregister(csRtAudioParams)

class RTCLOCK(_object):
    """Proxy of C++ RTCLOCK class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RTCLOCK, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RTCLOCK, name)
    __repr__ = _swig_repr
    __swig_setmethods__["starttime_real"] = _csnd.RTCLOCK_starttime_real_set
    __swig_getmethods__["starttime_real"] = _csnd.RTCLOCK_starttime_real_get
    if _newclass:starttime_real = property(_csnd.RTCLOCK_starttime_real_get, _csnd.RTCLOCK_starttime_real_set)
    __swig_setmethods__["starttime_CPU"] = _csnd.RTCLOCK_starttime_CPU_set
    __swig_getmethods__["starttime_CPU"] = _csnd.RTCLOCK_starttime_CPU_get
    if _newclass:starttime_CPU = property(_csnd.RTCLOCK_starttime_CPU_get, _csnd.RTCLOCK_starttime_CPU_set)
    def __init__(self, *args): 
        """__init__(self) -> RTCLOCK"""
        this = _csnd.new_RTCLOCK(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_RTCLOCK
    __del__ = lambda self : None;
RTCLOCK_swigregister = _csnd.RTCLOCK_swigregister
RTCLOCK_swigregister(RTCLOCK)

class opcodeListEntry(_object):
    """Proxy of C++ opcodeListEntry class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, opcodeListEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, opcodeListEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__["opname"] = _csnd.opcodeListEntry_opname_set
    __swig_getmethods__["opname"] = _csnd.opcodeListEntry_opname_get
    if _newclass:opname = property(_csnd.opcodeListEntry_opname_get, _csnd.opcodeListEntry_opname_set)
    __swig_setmethods__["outypes"] = _csnd.opcodeListEntry_outypes_set
    __swig_getmethods__["outypes"] = _csnd.opcodeListEntry_outypes_get
    if _newclass:outypes = property(_csnd.opcodeListEntry_outypes_get, _csnd.opcodeListEntry_outypes_set)
    __swig_setmethods__["intypes"] = _csnd.opcodeListEntry_intypes_set
    __swig_getmethods__["intypes"] = _csnd.opcodeListEntry_intypes_get
    if _newclass:intypes = property(_csnd.opcodeListEntry_intypes_get, _csnd.opcodeListEntry_intypes_set)
    def __init__(self, *args): 
        """__init__(self) -> opcodeListEntry"""
        this = _csnd.new_opcodeListEntry(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_opcodeListEntry
    __del__ = lambda self : None;
opcodeListEntry_swigregister = _csnd.opcodeListEntry_swigregister
opcodeListEntry_swigregister(opcodeListEntry)

class CsoundRandMTState(_object):
    """Proxy of C++ CsoundRandMTState class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundRandMTState, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundRandMTState, name)
    __repr__ = _swig_repr
    __swig_setmethods__["mti"] = _csnd.CsoundRandMTState_mti_set
    __swig_getmethods__["mti"] = _csnd.CsoundRandMTState_mti_get
    if _newclass:mti = property(_csnd.CsoundRandMTState_mti_get, _csnd.CsoundRandMTState_mti_set)
    __swig_setmethods__["mt"] = _csnd.CsoundRandMTState_mt_set
    __swig_getmethods__["mt"] = _csnd.CsoundRandMTState_mt_get
    if _newclass:mt = property(_csnd.CsoundRandMTState_mt_get, _csnd.CsoundRandMTState_mt_set)
    def __init__(self, *args): 
        """__init__(self) -> CsoundRandMTState"""
        this = _csnd.new_CsoundRandMTState(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundRandMTState
    __del__ = lambda self : None;
CsoundRandMTState_swigregister = _csnd.CsoundRandMTState_swigregister
CsoundRandMTState_swigregister(CsoundRandMTState)

class CsoundChannelListEntry(_object):
    """Proxy of C++ CsoundChannelListEntry class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundChannelListEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundChannelListEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__["name"] = _csnd.CsoundChannelListEntry_name_set
    __swig_getmethods__["name"] = _csnd.CsoundChannelListEntry_name_get
    if _newclass:name = property(_csnd.CsoundChannelListEntry_name_get, _csnd.CsoundChannelListEntry_name_set)
    __swig_setmethods__["type"] = _csnd.CsoundChannelListEntry_type_set
    __swig_getmethods__["type"] = _csnd.CsoundChannelListEntry_type_get
    if _newclass:type = property(_csnd.CsoundChannelListEntry_type_get, _csnd.CsoundChannelListEntry_type_set)
    def __init__(self, *args): 
        """__init__(self) -> CsoundChannelListEntry"""
        this = _csnd.new_CsoundChannelListEntry(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundChannelListEntry
    __del__ = lambda self : None;
CsoundChannelListEntry_swigregister = _csnd.CsoundChannelListEntry_swigregister
CsoundChannelListEntry_swigregister(CsoundChannelListEntry)

class PVSDATEXT(_object):
    """Proxy of C++ PVSDATEXT class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PVSDATEXT, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PVSDATEXT, name)
    __repr__ = _swig_repr
    __swig_setmethods__["N"] = _csnd.PVSDATEXT_N_set
    __swig_getmethods__["N"] = _csnd.PVSDATEXT_N_get
    if _newclass:N = property(_csnd.PVSDATEXT_N_get, _csnd.PVSDATEXT_N_set)
    __swig_setmethods__["overlap"] = _csnd.PVSDATEXT_overlap_set
    __swig_getmethods__["overlap"] = _csnd.PVSDATEXT_overlap_get
    if _newclass:overlap = property(_csnd.PVSDATEXT_overlap_get, _csnd.PVSDATEXT_overlap_set)
    __swig_setmethods__["winsize"] = _csnd.PVSDATEXT_winsize_set
    __swig_getmethods__["winsize"] = _csnd.PVSDATEXT_winsize_get
    if _newclass:winsize = property(_csnd.PVSDATEXT_winsize_get, _csnd.PVSDATEXT_winsize_set)
    __swig_setmethods__["wintype"] = _csnd.PVSDATEXT_wintype_set
    __swig_getmethods__["wintype"] = _csnd.PVSDATEXT_wintype_get
    if _newclass:wintype = property(_csnd.PVSDATEXT_wintype_get, _csnd.PVSDATEXT_wintype_set)
    __swig_setmethods__["format"] = _csnd.PVSDATEXT_format_set
    __swig_getmethods__["format"] = _csnd.PVSDATEXT_format_get
    if _newclass:format = property(_csnd.PVSDATEXT_format_get, _csnd.PVSDATEXT_format_set)
    __swig_setmethods__["framecount"] = _csnd.PVSDATEXT_framecount_set
    __swig_getmethods__["framecount"] = _csnd.PVSDATEXT_framecount_get
    if _newclass:framecount = property(_csnd.PVSDATEXT_framecount_get, _csnd.PVSDATEXT_framecount_set)
    __swig_setmethods__["frame"] = _csnd.PVSDATEXT_frame_set
    __swig_getmethods__["frame"] = _csnd.PVSDATEXT_frame_get
    if _newclass:frame = property(_csnd.PVSDATEXT_frame_get, _csnd.PVSDATEXT_frame_set)
    def __init__(self, *args): 
        """__init__(self) -> PVSDATEXT"""
        this = _csnd.new_PVSDATEXT(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_PVSDATEXT
    __del__ = lambda self : None;
PVSDATEXT_swigregister = _csnd.PVSDATEXT_swigregister
PVSDATEXT_swigregister(PVSDATEXT)


def csoundInitialize(*args):
  """csoundInitialize(int argc, char argv, int flags) -> int"""
  return _csnd.csoundInitialize(*args)

def csoundCreate(*args):
  """csoundCreate(void hostData) -> CSOUND"""
  return _csnd.csoundCreate(*args)

def csoundPreCompile(*args):
  """csoundPreCompile(CSOUND ?) -> int"""
  return _csnd.csoundPreCompile(*args)

def csoundInitializeCscore(*args):
  """csoundInitializeCscore(CSOUND ?, FILE insco, FILE outsco) -> int"""
  return _csnd.csoundInitializeCscore(*args)

def csoundQueryInterface(*args):
  """csoundQueryInterface(char name, void iface, int version) -> int"""
  return _csnd.csoundQueryInterface(*args)

def csoundDestroy(*args):
  """csoundDestroy(CSOUND ?)"""
  return _csnd.csoundDestroy(*args)

def csoundGetVersion(*args):
  """csoundGetVersion() -> int"""
  return _csnd.csoundGetVersion(*args)

def csoundGetAPIVersion(*args):
  """csoundGetAPIVersion() -> int"""
  return _csnd.csoundGetAPIVersion(*args)

def csoundGetHostData(*args):
  """csoundGetHostData(CSOUND ?) -> void"""
  return _csnd.csoundGetHostData(*args)

def csoundSetHostData(*args):
  """csoundSetHostData(CSOUND ?, void hostData)"""
  return _csnd.csoundSetHostData(*args)

def csoundGetEnv(*args):
  """csoundGetEnv(CSOUND csound, char name) -> char"""
  return _csnd.csoundGetEnv(*args)

def csoundSetGlobalEnv(*args):
  """csoundSetGlobalEnv(char name, char value) -> int"""
  return _csnd.csoundSetGlobalEnv(*args)

def csoundCompile(*args):
  """csoundCompile(CSOUND ?, int argc, char argv) -> int"""
  return _csnd.csoundCompile(*args)

def csoundPerform(*args):
  """csoundPerform(CSOUND ?) -> int"""
  return _csnd.csoundPerform(*args)

def csoundPerformKsmps(*args):
  """csoundPerformKsmps(CSOUND ?) -> int"""
  return _csnd.csoundPerformKsmps(*args)

def csoundPerformKsmpsAbsolute(*args):
  """csoundPerformKsmpsAbsolute(CSOUND ?) -> int"""
  return _csnd.csoundPerformKsmpsAbsolute(*args)

def csoundPerformBuffer(*args):
  """csoundPerformBuffer(CSOUND ?) -> int"""
  return _csnd.csoundPerformBuffer(*args)

def csoundStop(*args):
  """csoundStop(CSOUND ?)"""
  return _csnd.csoundStop(*args)

def csoundCleanup(*args):
  """csoundCleanup(CSOUND ?) -> int"""
  return _csnd.csoundCleanup(*args)

def csoundReset(*args):
  """csoundReset(CSOUND ?)"""
  return _csnd.csoundReset(*args)

def csoundGetSr(*args):
  """csoundGetSr(CSOUND ?) -> float"""
  return _csnd.csoundGetSr(*args)

def csoundGetKr(*args):
  """csoundGetKr(CSOUND ?) -> float"""
  return _csnd.csoundGetKr(*args)

def csoundGetKsmps(*args):
  """csoundGetKsmps(CSOUND ?) -> int"""
  return _csnd.csoundGetKsmps(*args)

def csoundGetNchnls(*args):
  """csoundGetNchnls(CSOUND ?) -> int"""
  return _csnd.csoundGetNchnls(*args)

def csoundGet0dBFS(*args):
  """csoundGet0dBFS(CSOUND ?) -> float"""
  return _csnd.csoundGet0dBFS(*args)

def csoundGetStrVarMaxLen(*args):
  """csoundGetStrVarMaxLen(CSOUND ?) -> int"""
  return _csnd.csoundGetStrVarMaxLen(*args)

def csoundGetSampleFormat(*args):
  """csoundGetSampleFormat(CSOUND ?) -> int"""
  return _csnd.csoundGetSampleFormat(*args)

def csoundGetSampleSize(*args):
  """csoundGetSampleSize(CSOUND ?) -> int"""
  return _csnd.csoundGetSampleSize(*args)

def csoundGetInputBufferSize(*args):
  """csoundGetInputBufferSize(CSOUND ?) -> long"""
  return _csnd.csoundGetInputBufferSize(*args)

def csoundGetOutputBufferSize(*args):
  """csoundGetOutputBufferSize(CSOUND ?) -> long"""
  return _csnd.csoundGetOutputBufferSize(*args)

def csoundGetInputBuffer(*args):
  """csoundGetInputBuffer(CSOUND ?) -> float"""
  return _csnd.csoundGetInputBuffer(*args)

def csoundGetOutputBuffer(*args):
  """csoundGetOutputBuffer(CSOUND ?) -> float"""
  return _csnd.csoundGetOutputBuffer(*args)

def csoundGetSpin(*args):
  """csoundGetSpin(CSOUND ?) -> float"""
  return _csnd.csoundGetSpin(*args)

def csoundGetSpout(*args):
  """csoundGetSpout(CSOUND ?) -> float"""
  return _csnd.csoundGetSpout(*args)

def csoundGetOutputFileName(*args):
  """csoundGetOutputFileName(CSOUND ?) -> char"""
  return _csnd.csoundGetOutputFileName(*args)

def csoundSetHostImplementedAudioIO(*args):
  """csoundSetHostImplementedAudioIO(CSOUND ?, int state, int bufSize)"""
  return _csnd.csoundSetHostImplementedAudioIO(*args)

def csoundGetScoreTime(*args):
  """csoundGetScoreTime(CSOUND ?) -> double"""
  return _csnd.csoundGetScoreTime(*args)

def csoundIsScorePending(*args):
  """csoundIsScorePending(CSOUND ?) -> int"""
  return _csnd.csoundIsScorePending(*args)

def csoundSetScorePending(*args):
  """csoundSetScorePending(CSOUND ?, int pending)"""
  return _csnd.csoundSetScorePending(*args)

def csoundGetScoreOffsetSeconds(*args):
  """csoundGetScoreOffsetSeconds(CSOUND ?) -> float"""
  return _csnd.csoundGetScoreOffsetSeconds(*args)

def csoundSetScoreOffsetSeconds(*args):
  """csoundSetScoreOffsetSeconds(CSOUND ?, float time)"""
  return _csnd.csoundSetScoreOffsetSeconds(*args)

def csoundRewindScore(*args):
  """csoundRewindScore(CSOUND ?)"""
  return _csnd.csoundRewindScore(*args)

def csoundScoreSort(*args):
  """csoundScoreSort(CSOUND ?, FILE inFile, FILE outFile) -> int"""
  return _csnd.csoundScoreSort(*args)

def csoundScoreExtract(*args):
  """csoundScoreExtract(CSOUND ?, FILE inFile, FILE outFile, FILE extractFile) -> int"""
  return _csnd.csoundScoreExtract(*args)

def csoundMessage(*args):
  """csoundMessage(CSOUND ?, char format, v(...) ?)"""
  return _csnd.csoundMessage(*args)

def csoundMessageS(*args):
  """csoundMessageS(CSOUND ?, int attr, char format, v(...) ?)"""
  return _csnd.csoundMessageS(*args)

def csoundGetMessageLevel(*args):
  """csoundGetMessageLevel(CSOUND ?) -> int"""
  return _csnd.csoundGetMessageLevel(*args)

def csoundSetMessageLevel(*args):
  """csoundSetMessageLevel(CSOUND ?, int messageLevel)"""
  return _csnd.csoundSetMessageLevel(*args)

def csoundInputMessage(*args):
  """csoundInputMessage(CSOUND ?, char message)"""
  return _csnd.csoundInputMessage(*args)

def csoundKeyPress(*args):
  """csoundKeyPress(CSOUND ?, char c)"""
  return _csnd.csoundKeyPress(*args)

def csoundScoreEvent(*args):
  """csoundScoreEvent(CSOUND ?, char type, float pFields, long numFields) -> int"""
  return _csnd.csoundScoreEvent(*args)

def csoundNewOpcodeList(*args):
  """csoundNewOpcodeList(CSOUND ?, opcodeListEntry opcodelist) -> int"""
  return _csnd.csoundNewOpcodeList(*args)

def csoundDisposeOpcodeList(*args):
  """csoundDisposeOpcodeList(CSOUND ?, opcodeListEntry opcodelist)"""
  return _csnd.csoundDisposeOpcodeList(*args)

def csoundAppendOpcode(*args):
  """
    csoundAppendOpcode(CSOUND ?, char opname, int dsblksiz, int thread, char outypes, 
        char intypes, int iopadr, int kopadr, 
        int aopadr) -> int
    """
  return _csnd.csoundAppendOpcode(*args)

def csoundOpenLibrary(*args):
  """csoundOpenLibrary(void library, char libraryPath) -> int"""
  return _csnd.csoundOpenLibrary(*args)

def csoundCloseLibrary(*args):
  """csoundCloseLibrary(void library) -> int"""
  return _csnd.csoundCloseLibrary(*args)

def csoundGetLibrarySymbol(*args):
  """csoundGetLibrarySymbol(void library, char symbolName) -> void"""
  return _csnd.csoundGetLibrarySymbol(*args)

def csoundGetDebug(*args):
  """csoundGetDebug(CSOUND ?) -> int"""
  return _csnd.csoundGetDebug(*args)

def csoundSetDebug(*args):
  """csoundSetDebug(CSOUND ?, int debug)"""
  return _csnd.csoundSetDebug(*args)

def csoundTableLength(*args):
  """csoundTableLength(CSOUND ?, int table) -> int"""
  return _csnd.csoundTableLength(*args)

def csoundTableGet(*args):
  """csoundTableGet(CSOUND ?, int table, int index) -> float"""
  return _csnd.csoundTableGet(*args)

def csoundTableSet(*args):
  """csoundTableSet(CSOUND ?, int table, int index, float value)"""
  return _csnd.csoundTableSet(*args)

def csoundGetTable(*args):
  """csoundGetTable(CSOUND ?, float tablePtr, int tableNum) -> int"""
  return _csnd.csoundGetTable(*args)

def csoundCreateThread(*args):
  """csoundCreateThread(uintptr_t threadRoutine, void userdata) -> void"""
  return _csnd.csoundCreateThread(*args)

def csoundGetCurrentThreadId(*args):
  """csoundGetCurrentThreadId() -> void"""
  return _csnd.csoundGetCurrentThreadId(*args)

def csoundJoinThread(*args):
  """csoundJoinThread(void thread) -> uintptr_t"""
  return _csnd.csoundJoinThread(*args)

def csoundRunCommand(*args):
  """csoundRunCommand(char argv, int noWait) -> long"""
  return _csnd.csoundRunCommand(*args)

def csoundCreateThreadLock(*args):
  """csoundCreateThreadLock() -> void"""
  return _csnd.csoundCreateThreadLock(*args)

def csoundWaitThreadLock(*args):
  """csoundWaitThreadLock(void lock, size_t milliseconds) -> int"""
  return _csnd.csoundWaitThreadLock(*args)

def csoundWaitThreadLockNoTimeout(*args):
  """csoundWaitThreadLockNoTimeout(void lock)"""
  return _csnd.csoundWaitThreadLockNoTimeout(*args)

def csoundNotifyThreadLock(*args):
  """csoundNotifyThreadLock(void lock)"""
  return _csnd.csoundNotifyThreadLock(*args)

def csoundDestroyThreadLock(*args):
  """csoundDestroyThreadLock(void lock)"""
  return _csnd.csoundDestroyThreadLock(*args)

def csoundCreateMutex(*args):
  """csoundCreateMutex(int isRecursive) -> void"""
  return _csnd.csoundCreateMutex(*args)

def csoundLockMutex(*args):
  """csoundLockMutex(void mutex_)"""
  return _csnd.csoundLockMutex(*args)

def csoundLockMutexNoWait(*args):
  """csoundLockMutexNoWait(void mutex_) -> int"""
  return _csnd.csoundLockMutexNoWait(*args)

def csoundUnlockMutex(*args):
  """csoundUnlockMutex(void mutex_)"""
  return _csnd.csoundUnlockMutex(*args)

def csoundDestroyMutex(*args):
  """csoundDestroyMutex(void mutex_)"""
  return _csnd.csoundDestroyMutex(*args)

def csoundSleep(*args):
  """csoundSleep(size_t milliseconds)"""
  return _csnd.csoundSleep(*args)

def csoundInitTimerStruct(*args):
  """csoundInitTimerStruct( ?)"""
  return _csnd.csoundInitTimerStruct(*args)

def csoundGetRealTime(*args):
  """csoundGetRealTime( ?) -> double"""
  return _csnd.csoundGetRealTime(*args)

def csoundGetCPUTime(*args):
  """csoundGetCPUTime( ?) -> double"""
  return _csnd.csoundGetCPUTime(*args)

def csoundGetRandomSeedFromTime(*args):
  """csoundGetRandomSeedFromTime() -> uint32_t"""
  return _csnd.csoundGetRandomSeedFromTime(*args)

def csoundSetLanguage(*args):
  """csoundSetLanguage(cslanguage_t lang_code)"""
  return _csnd.csoundSetLanguage(*args)

def csoundLocalizeString(*args):
  """csoundLocalizeString(char s) -> char"""
  return _csnd.csoundLocalizeString(*args)

def csoundCreateGlobalVariable(*args):
  """csoundCreateGlobalVariable(CSOUND ?, char name, size_t nbytes) -> int"""
  return _csnd.csoundCreateGlobalVariable(*args)

def csoundQueryGlobalVariable(*args):
  """csoundQueryGlobalVariable(CSOUND ?, char name) -> void"""
  return _csnd.csoundQueryGlobalVariable(*args)

def csoundQueryGlobalVariableNoCheck(*args):
  """csoundQueryGlobalVariableNoCheck(CSOUND ?, char name) -> void"""
  return _csnd.csoundQueryGlobalVariableNoCheck(*args)

def csoundDestroyGlobalVariable(*args):
  """csoundDestroyGlobalVariable(CSOUND ?, char name) -> int"""
  return _csnd.csoundDestroyGlobalVariable(*args)

def csoundGetSizeOfMYFLT(*args):
  """csoundGetSizeOfMYFLT() -> int"""
  return _csnd.csoundGetSizeOfMYFLT(*args)

def csoundGetRtRecordUserData(*args):
  """csoundGetRtRecordUserData(CSOUND ?) -> void"""
  return _csnd.csoundGetRtRecordUserData(*args)

def csoundGetRtPlayUserData(*args):
  """csoundGetRtPlayUserData(CSOUND ?) -> void"""
  return _csnd.csoundGetRtPlayUserData(*args)

def csoundRunUtility(*args):
  """csoundRunUtility(CSOUND ?, char name, int argc, char argv) -> int"""
  return _csnd.csoundRunUtility(*args)

def csoundListUtilities(*args):
  """csoundListUtilities(CSOUND ?) -> char"""
  return _csnd.csoundListUtilities(*args)

def csoundDeleteUtilityList(*args):
  """csoundDeleteUtilityList(CSOUND ?, char lst)"""
  return _csnd.csoundDeleteUtilityList(*args)

def csoundGetUtilityDescription(*args):
  """csoundGetUtilityDescription(CSOUND ?, char utilName) -> char"""
  return _csnd.csoundGetUtilityDescription(*args)

def csoundGetChannelPtr(*args):
  """csoundGetChannelPtr(CSOUND ?, float p, char name, int type) -> int"""
  return _csnd.csoundGetChannelPtr(*args)

def csoundListChannels(*args):
  """csoundListChannels(CSOUND ?,  lst) -> int"""
  return _csnd.csoundListChannels(*args)

def csoundDeleteChannelList(*args):
  """csoundDeleteChannelList(CSOUND ?,  lst)"""
  return _csnd.csoundDeleteChannelList(*args)

def csoundSetControlChannelParams(*args):
  """
    csoundSetControlChannelParams(CSOUND ?, char name, int type, float dflt, float min, 
        float max) -> int
    """
  return _csnd.csoundSetControlChannelParams(*args)

def csoundGetControlChannelParams(*args):
  """csoundGetControlChannelParams(CSOUND ?, char name, float dflt, float min, float max) -> int"""
  return _csnd.csoundGetControlChannelParams(*args)

def csoundSetChannelIOCallback(*args):
  """csoundSetChannelIOCallback(CSOUND ?, CsoundChannelIOCallback_t func)"""
  return _csnd.csoundSetChannelIOCallback(*args)

def csoundRand31(*args):
  """csoundRand31(int seedVal) -> int"""
  return _csnd.csoundRand31(*args)

def csoundSeedRandMT(*args):
  """csoundSeedRandMT( p, uint32_t initKey, uint32_t keyLength)"""
  return _csnd.csoundSeedRandMT(*args)

def csoundRandMT(*args):
  """csoundRandMT( p) -> uint32_t"""
  return _csnd.csoundRandMT(*args)

def csoundChanIKSet(*args):
  """csoundChanIKSet(CSOUND ?, float value, int n) -> int"""
  return _csnd.csoundChanIKSet(*args)

def csoundChanOKGet(*args):
  """csoundChanOKGet(CSOUND ?, float value, int n) -> int"""
  return _csnd.csoundChanOKGet(*args)

def csoundChanIASet(*args):
  """csoundChanIASet(CSOUND ?, float value, int n) -> int"""
  return _csnd.csoundChanIASet(*args)

def csoundChanOAGet(*args):
  """csoundChanOAGet(CSOUND ?, float value, int n) -> int"""
  return _csnd.csoundChanOAGet(*args)

def csoundPvsinSet(*args):
  """csoundPvsinSet(CSOUND ?,  fin, int n) -> int"""
  return _csnd.csoundPvsinSet(*args)

def csoundPvsoutGet(*args):
  """csoundPvsoutGet(CSOUND csound,  fout, int n) -> int"""
  return _csnd.csoundPvsoutGet(*args)

def csoundSetCallback(*args):
  """csoundSetCallback(CSOUND ?, int func, void userData, unsigned int typeMask) -> int"""
  return _csnd.csoundSetCallback(*args)

def csoundRemoveCallback(*args):
  """csoundRemoveCallback(CSOUND ?, int func)"""
  return _csnd.csoundRemoveCallback(*args)
class csCfgVariableHead_t(_object):
    """Proxy of C++ csCfgVariableHead_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableHead_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableHead_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableHead_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableHead_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableHead_t_nxt_get, _csnd.csCfgVariableHead_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableHead_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableHead_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableHead_t_name_get, _csnd.csCfgVariableHead_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableHead_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableHead_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableHead_t_p_get, _csnd.csCfgVariableHead_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableHead_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableHead_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableHead_t_type_get, _csnd.csCfgVariableHead_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableHead_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableHead_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableHead_t_flags_get, _csnd.csCfgVariableHead_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableHead_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableHead_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableHead_t_shortDesc_get, _csnd.csCfgVariableHead_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableHead_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableHead_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableHead_t_longDesc_get, _csnd.csCfgVariableHead_t_longDesc_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableHead_t"""
        this = _csnd.new_csCfgVariableHead_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableHead_t
    __del__ = lambda self : None;
csCfgVariableHead_t_swigregister = _csnd.csCfgVariableHead_t_swigregister
csCfgVariableHead_t_swigregister(csCfgVariableHead_t)

class csCfgVariableInt_t(_object):
    """Proxy of C++ csCfgVariableInt_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableInt_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableInt_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableInt_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableInt_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableInt_t_nxt_get, _csnd.csCfgVariableInt_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableInt_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableInt_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableInt_t_name_get, _csnd.csCfgVariableInt_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableInt_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableInt_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableInt_t_p_get, _csnd.csCfgVariableInt_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableInt_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableInt_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableInt_t_type_get, _csnd.csCfgVariableInt_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableInt_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableInt_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableInt_t_flags_get, _csnd.csCfgVariableInt_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableInt_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableInt_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableInt_t_shortDesc_get, _csnd.csCfgVariableInt_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableInt_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableInt_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableInt_t_longDesc_get, _csnd.csCfgVariableInt_t_longDesc_set)
    __swig_setmethods__["min"] = _csnd.csCfgVariableInt_t_min_set
    __swig_getmethods__["min"] = _csnd.csCfgVariableInt_t_min_get
    if _newclass:min = property(_csnd.csCfgVariableInt_t_min_get, _csnd.csCfgVariableInt_t_min_set)
    __swig_setmethods__["max"] = _csnd.csCfgVariableInt_t_max_set
    __swig_getmethods__["max"] = _csnd.csCfgVariableInt_t_max_get
    if _newclass:max = property(_csnd.csCfgVariableInt_t_max_get, _csnd.csCfgVariableInt_t_max_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableInt_t"""
        this = _csnd.new_csCfgVariableInt_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableInt_t
    __del__ = lambda self : None;
csCfgVariableInt_t_swigregister = _csnd.csCfgVariableInt_t_swigregister
csCfgVariableInt_t_swigregister(csCfgVariableInt_t)

class csCfgVariableBoolean_t(_object):
    """Proxy of C++ csCfgVariableBoolean_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableBoolean_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableBoolean_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableBoolean_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableBoolean_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableBoolean_t_nxt_get, _csnd.csCfgVariableBoolean_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableBoolean_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableBoolean_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableBoolean_t_name_get, _csnd.csCfgVariableBoolean_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableBoolean_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableBoolean_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableBoolean_t_p_get, _csnd.csCfgVariableBoolean_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableBoolean_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableBoolean_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableBoolean_t_type_get, _csnd.csCfgVariableBoolean_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableBoolean_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableBoolean_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableBoolean_t_flags_get, _csnd.csCfgVariableBoolean_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableBoolean_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableBoolean_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableBoolean_t_shortDesc_get, _csnd.csCfgVariableBoolean_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableBoolean_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableBoolean_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableBoolean_t_longDesc_get, _csnd.csCfgVariableBoolean_t_longDesc_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableBoolean_t"""
        this = _csnd.new_csCfgVariableBoolean_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableBoolean_t
    __del__ = lambda self : None;
csCfgVariableBoolean_t_swigregister = _csnd.csCfgVariableBoolean_t_swigregister
csCfgVariableBoolean_t_swigregister(csCfgVariableBoolean_t)

class csCfgVariableFloat_t(_object):
    """Proxy of C++ csCfgVariableFloat_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableFloat_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableFloat_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableFloat_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableFloat_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableFloat_t_nxt_get, _csnd.csCfgVariableFloat_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableFloat_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableFloat_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableFloat_t_name_get, _csnd.csCfgVariableFloat_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableFloat_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableFloat_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableFloat_t_p_get, _csnd.csCfgVariableFloat_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableFloat_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableFloat_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableFloat_t_type_get, _csnd.csCfgVariableFloat_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableFloat_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableFloat_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableFloat_t_flags_get, _csnd.csCfgVariableFloat_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableFloat_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableFloat_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableFloat_t_shortDesc_get, _csnd.csCfgVariableFloat_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableFloat_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableFloat_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableFloat_t_longDesc_get, _csnd.csCfgVariableFloat_t_longDesc_set)
    __swig_setmethods__["min"] = _csnd.csCfgVariableFloat_t_min_set
    __swig_getmethods__["min"] = _csnd.csCfgVariableFloat_t_min_get
    if _newclass:min = property(_csnd.csCfgVariableFloat_t_min_get, _csnd.csCfgVariableFloat_t_min_set)
    __swig_setmethods__["max"] = _csnd.csCfgVariableFloat_t_max_set
    __swig_getmethods__["max"] = _csnd.csCfgVariableFloat_t_max_get
    if _newclass:max = property(_csnd.csCfgVariableFloat_t_max_get, _csnd.csCfgVariableFloat_t_max_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableFloat_t"""
        this = _csnd.new_csCfgVariableFloat_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableFloat_t
    __del__ = lambda self : None;
csCfgVariableFloat_t_swigregister = _csnd.csCfgVariableFloat_t_swigregister
csCfgVariableFloat_t_swigregister(csCfgVariableFloat_t)

class csCfgVariableDouble_t(_object):
    """Proxy of C++ csCfgVariableDouble_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableDouble_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableDouble_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableDouble_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableDouble_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableDouble_t_nxt_get, _csnd.csCfgVariableDouble_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableDouble_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableDouble_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableDouble_t_name_get, _csnd.csCfgVariableDouble_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableDouble_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableDouble_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableDouble_t_p_get, _csnd.csCfgVariableDouble_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableDouble_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableDouble_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableDouble_t_type_get, _csnd.csCfgVariableDouble_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableDouble_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableDouble_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableDouble_t_flags_get, _csnd.csCfgVariableDouble_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableDouble_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableDouble_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableDouble_t_shortDesc_get, _csnd.csCfgVariableDouble_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableDouble_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableDouble_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableDouble_t_longDesc_get, _csnd.csCfgVariableDouble_t_longDesc_set)
    __swig_setmethods__["min"] = _csnd.csCfgVariableDouble_t_min_set
    __swig_getmethods__["min"] = _csnd.csCfgVariableDouble_t_min_get
    if _newclass:min = property(_csnd.csCfgVariableDouble_t_min_get, _csnd.csCfgVariableDouble_t_min_set)
    __swig_setmethods__["max"] = _csnd.csCfgVariableDouble_t_max_set
    __swig_getmethods__["max"] = _csnd.csCfgVariableDouble_t_max_get
    if _newclass:max = property(_csnd.csCfgVariableDouble_t_max_get, _csnd.csCfgVariableDouble_t_max_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableDouble_t"""
        this = _csnd.new_csCfgVariableDouble_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableDouble_t
    __del__ = lambda self : None;
csCfgVariableDouble_t_swigregister = _csnd.csCfgVariableDouble_t_swigregister
csCfgVariableDouble_t_swigregister(csCfgVariableDouble_t)

class csCfgVariableMYFLT_t(_object):
    """Proxy of C++ csCfgVariableMYFLT_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableMYFLT_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableMYFLT_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableMYFLT_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableMYFLT_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableMYFLT_t_nxt_get, _csnd.csCfgVariableMYFLT_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableMYFLT_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableMYFLT_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableMYFLT_t_name_get, _csnd.csCfgVariableMYFLT_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableMYFLT_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableMYFLT_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableMYFLT_t_p_get, _csnd.csCfgVariableMYFLT_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableMYFLT_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableMYFLT_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableMYFLT_t_type_get, _csnd.csCfgVariableMYFLT_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableMYFLT_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableMYFLT_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableMYFLT_t_flags_get, _csnd.csCfgVariableMYFLT_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableMYFLT_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableMYFLT_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableMYFLT_t_shortDesc_get, _csnd.csCfgVariableMYFLT_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableMYFLT_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableMYFLT_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableMYFLT_t_longDesc_get, _csnd.csCfgVariableMYFLT_t_longDesc_set)
    __swig_setmethods__["min"] = _csnd.csCfgVariableMYFLT_t_min_set
    __swig_getmethods__["min"] = _csnd.csCfgVariableMYFLT_t_min_get
    if _newclass:min = property(_csnd.csCfgVariableMYFLT_t_min_get, _csnd.csCfgVariableMYFLT_t_min_set)
    __swig_setmethods__["max"] = _csnd.csCfgVariableMYFLT_t_max_set
    __swig_getmethods__["max"] = _csnd.csCfgVariableMYFLT_t_max_get
    if _newclass:max = property(_csnd.csCfgVariableMYFLT_t_max_get, _csnd.csCfgVariableMYFLT_t_max_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableMYFLT_t"""
        this = _csnd.new_csCfgVariableMYFLT_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableMYFLT_t
    __del__ = lambda self : None;
csCfgVariableMYFLT_t_swigregister = _csnd.csCfgVariableMYFLT_t_swigregister
csCfgVariableMYFLT_t_swigregister(csCfgVariableMYFLT_t)

class csCfgVariableString_t(_object):
    """Proxy of C++ csCfgVariableString_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariableString_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariableString_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["nxt"] = _csnd.csCfgVariableString_t_nxt_set
    __swig_getmethods__["nxt"] = _csnd.csCfgVariableString_t_nxt_get
    if _newclass:nxt = property(_csnd.csCfgVariableString_t_nxt_get, _csnd.csCfgVariableString_t_nxt_set)
    __swig_setmethods__["name"] = _csnd.csCfgVariableString_t_name_set
    __swig_getmethods__["name"] = _csnd.csCfgVariableString_t_name_get
    if _newclass:name = property(_csnd.csCfgVariableString_t_name_get, _csnd.csCfgVariableString_t_name_set)
    __swig_setmethods__["p"] = _csnd.csCfgVariableString_t_p_set
    __swig_getmethods__["p"] = _csnd.csCfgVariableString_t_p_get
    if _newclass:p = property(_csnd.csCfgVariableString_t_p_get, _csnd.csCfgVariableString_t_p_set)
    __swig_setmethods__["type"] = _csnd.csCfgVariableString_t_type_set
    __swig_getmethods__["type"] = _csnd.csCfgVariableString_t_type_get
    if _newclass:type = property(_csnd.csCfgVariableString_t_type_get, _csnd.csCfgVariableString_t_type_set)
    __swig_setmethods__["flags"] = _csnd.csCfgVariableString_t_flags_set
    __swig_getmethods__["flags"] = _csnd.csCfgVariableString_t_flags_get
    if _newclass:flags = property(_csnd.csCfgVariableString_t_flags_get, _csnd.csCfgVariableString_t_flags_set)
    __swig_setmethods__["shortDesc"] = _csnd.csCfgVariableString_t_shortDesc_set
    __swig_getmethods__["shortDesc"] = _csnd.csCfgVariableString_t_shortDesc_get
    if _newclass:shortDesc = property(_csnd.csCfgVariableString_t_shortDesc_get, _csnd.csCfgVariableString_t_shortDesc_set)
    __swig_setmethods__["longDesc"] = _csnd.csCfgVariableString_t_longDesc_set
    __swig_getmethods__["longDesc"] = _csnd.csCfgVariableString_t_longDesc_get
    if _newclass:longDesc = property(_csnd.csCfgVariableString_t_longDesc_get, _csnd.csCfgVariableString_t_longDesc_set)
    __swig_setmethods__["maxlen"] = _csnd.csCfgVariableString_t_maxlen_set
    __swig_getmethods__["maxlen"] = _csnd.csCfgVariableString_t_maxlen_get
    if _newclass:maxlen = property(_csnd.csCfgVariableString_t_maxlen_get, _csnd.csCfgVariableString_t_maxlen_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariableString_t"""
        this = _csnd.new_csCfgVariableString_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariableString_t
    __del__ = lambda self : None;
csCfgVariableString_t_swigregister = _csnd.csCfgVariableString_t_swigregister
csCfgVariableString_t_swigregister(csCfgVariableString_t)

class csCfgVariable_t(_object):
    """Proxy of C++ csCfgVariable_t class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, csCfgVariable_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, csCfgVariable_t, name)
    __repr__ = _swig_repr
    __swig_setmethods__["h"] = _csnd.csCfgVariable_t_h_set
    __swig_getmethods__["h"] = _csnd.csCfgVariable_t_h_get
    if _newclass:h = property(_csnd.csCfgVariable_t_h_get, _csnd.csCfgVariable_t_h_set)
    __swig_setmethods__["i"] = _csnd.csCfgVariable_t_i_set
    __swig_getmethods__["i"] = _csnd.csCfgVariable_t_i_get
    if _newclass:i = property(_csnd.csCfgVariable_t_i_get, _csnd.csCfgVariable_t_i_set)
    __swig_setmethods__["b"] = _csnd.csCfgVariable_t_b_set
    __swig_getmethods__["b"] = _csnd.csCfgVariable_t_b_get
    if _newclass:b = property(_csnd.csCfgVariable_t_b_get, _csnd.csCfgVariable_t_b_set)
    __swig_setmethods__["f"] = _csnd.csCfgVariable_t_f_set
    __swig_getmethods__["f"] = _csnd.csCfgVariable_t_f_get
    if _newclass:f = property(_csnd.csCfgVariable_t_f_get, _csnd.csCfgVariable_t_f_set)
    __swig_setmethods__["d"] = _csnd.csCfgVariable_t_d_set
    __swig_getmethods__["d"] = _csnd.csCfgVariable_t_d_get
    if _newclass:d = property(_csnd.csCfgVariable_t_d_get, _csnd.csCfgVariable_t_d_set)
    __swig_setmethods__["m"] = _csnd.csCfgVariable_t_m_set
    __swig_getmethods__["m"] = _csnd.csCfgVariable_t_m_get
    if _newclass:m = property(_csnd.csCfgVariable_t_m_get, _csnd.csCfgVariable_t_m_set)
    __swig_setmethods__["s"] = _csnd.csCfgVariable_t_s_set
    __swig_getmethods__["s"] = _csnd.csCfgVariable_t_s_get
    if _newclass:s = property(_csnd.csCfgVariable_t_s_get, _csnd.csCfgVariable_t_s_set)
    def __init__(self, *args): 
        """__init__(self) -> csCfgVariable_t"""
        this = _csnd.new_csCfgVariable_t(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_csCfgVariable_t
    __del__ = lambda self : None;
csCfgVariable_t_swigregister = _csnd.csCfgVariable_t_swigregister
csCfgVariable_t_swigregister(csCfgVariable_t)

CSOUNDCFG_INTEGER = _csnd.CSOUNDCFG_INTEGER
CSOUNDCFG_BOOLEAN = _csnd.CSOUNDCFG_BOOLEAN
CSOUNDCFG_FLOAT = _csnd.CSOUNDCFG_FLOAT
CSOUNDCFG_DOUBLE = _csnd.CSOUNDCFG_DOUBLE
CSOUNDCFG_MYFLT = _csnd.CSOUNDCFG_MYFLT
CSOUNDCFG_STRING = _csnd.CSOUNDCFG_STRING
CSOUNDCFG_POWOFTWO = _csnd.CSOUNDCFG_POWOFTWO
CSOUNDCFG_SUCCESS = _csnd.CSOUNDCFG_SUCCESS
CSOUNDCFG_INVALID_NAME = _csnd.CSOUNDCFG_INVALID_NAME
CSOUNDCFG_INVALID_TYPE = _csnd.CSOUNDCFG_INVALID_TYPE
CSOUNDCFG_INVALID_FLAG = _csnd.CSOUNDCFG_INVALID_FLAG
CSOUNDCFG_NULL_POINTER = _csnd.CSOUNDCFG_NULL_POINTER
CSOUNDCFG_TOO_HIGH = _csnd.CSOUNDCFG_TOO_HIGH
CSOUNDCFG_TOO_LOW = _csnd.CSOUNDCFG_TOO_LOW
CSOUNDCFG_NOT_POWOFTWO = _csnd.CSOUNDCFG_NOT_POWOFTWO
CSOUNDCFG_INVALID_BOOLEAN = _csnd.CSOUNDCFG_INVALID_BOOLEAN
CSOUNDCFG_MEMORY = _csnd.CSOUNDCFG_MEMORY
CSOUNDCFG_STRING_LENGTH = _csnd.CSOUNDCFG_STRING_LENGTH
CSOUNDCFG_LASTERROR = _csnd.CSOUNDCFG_LASTERROR

def csoundCreateConfigurationVariable(*args):
  """
    csoundCreateConfigurationVariable(CSOUND csound, char name, void p, int type, int flags, 
        void min, void max, char shortDesc, char longDesc) -> int
    """
  return _csnd.csoundCreateConfigurationVariable(*args)

def csoundSetConfigurationVariable(*args):
  """csoundSetConfigurationVariable(CSOUND csound, char name, void value) -> int"""
  return _csnd.csoundSetConfigurationVariable(*args)

def csoundParseConfigurationVariable(*args):
  """csoundParseConfigurationVariable(CSOUND csound, char name, char value) -> int"""
  return _csnd.csoundParseConfigurationVariable(*args)

def csoundQueryConfigurationVariable(*args):
  """csoundQueryConfigurationVariable(CSOUND csound, char name)"""
  return _csnd.csoundQueryConfigurationVariable(*args)

def csoundListConfigurationVariables(*args):
  """csoundListConfigurationVariables(CSOUND csound)"""
  return _csnd.csoundListConfigurationVariables(*args)

def csoundDeleteCfgVarList(*args):
  """csoundDeleteCfgVarList( lst)"""
  return _csnd.csoundDeleteCfgVarList(*args)

def csoundDeleteConfigurationVariable(*args):
  """csoundDeleteConfigurationVariable(CSOUND csound, char name) -> int"""
  return _csnd.csoundDeleteConfigurationVariable(*args)

def csoundCfgErrorCodeToString(*args):
  """csoundCfgErrorCodeToString(int errcode) -> char"""
  return _csnd.csoundCfgErrorCodeToString(*args)
CSOUNDMSG_DEFAULT = _csnd.CSOUNDMSG_DEFAULT
CSOUNDMSG_ERROR = _csnd.CSOUNDMSG_ERROR
CSOUNDMSG_ORCH = _csnd.CSOUNDMSG_ORCH
CSOUNDMSG_REALTIME = _csnd.CSOUNDMSG_REALTIME
CSOUNDMSG_WARNING = _csnd.CSOUNDMSG_WARNING
CSOUNDMSG_FG_BLACK = _csnd.CSOUNDMSG_FG_BLACK
CSOUNDMSG_FG_RED = _csnd.CSOUNDMSG_FG_RED
CSOUNDMSG_FG_GREEN = _csnd.CSOUNDMSG_FG_GREEN
CSOUNDMSG_FG_YELLOW = _csnd.CSOUNDMSG_FG_YELLOW
CSOUNDMSG_FG_BLUE = _csnd.CSOUNDMSG_FG_BLUE
CSOUNDMSG_FG_MAGENTA = _csnd.CSOUNDMSG_FG_MAGENTA
CSOUNDMSG_FG_CYAN = _csnd.CSOUNDMSG_FG_CYAN
CSOUNDMSG_FG_WHITE = _csnd.CSOUNDMSG_FG_WHITE
CSOUNDMSG_FG_BOLD = _csnd.CSOUNDMSG_FG_BOLD
CSOUNDMSG_FG_UNDERLINE = _csnd.CSOUNDMSG_FG_UNDERLINE
CSOUNDMSG_BG_BLACK = _csnd.CSOUNDMSG_BG_BLACK
CSOUNDMSG_BG_RED = _csnd.CSOUNDMSG_BG_RED
CSOUNDMSG_BG_GREEN = _csnd.CSOUNDMSG_BG_GREEN
CSOUNDMSG_BG_ORANGE = _csnd.CSOUNDMSG_BG_ORANGE
CSOUNDMSG_BG_BLUE = _csnd.CSOUNDMSG_BG_BLUE
CSOUNDMSG_BG_MAGENTA = _csnd.CSOUNDMSG_BG_MAGENTA
CSOUNDMSG_BG_CYAN = _csnd.CSOUNDMSG_BG_CYAN
CSOUNDMSG_BG_GREY = _csnd.CSOUNDMSG_BG_GREY
CSOUNDMSG_TYPE_MASK = _csnd.CSOUNDMSG_TYPE_MASK
CSOUNDMSG_FG_COLOR_MASK = _csnd.CSOUNDMSG_FG_COLOR_MASK
CSOUNDMSG_FG_ATTR_MASK = _csnd.CSOUNDMSG_FG_ATTR_MASK
CSOUNDMSG_BG_COLOR_MASK = _csnd.CSOUNDMSG_BG_COLOR_MASK
CS_PACKAGE_NAME = _csnd.CS_PACKAGE_NAME
CS_PACKAGE_STRING = _csnd.CS_PACKAGE_STRING
CS_PACKAGE_TARNAME = _csnd.CS_PACKAGE_TARNAME
CS_PACKAGE_VERSION = _csnd.CS_PACKAGE_VERSION
CS_VERSION = _csnd.CS_VERSION
CS_SUBVER = _csnd.CS_SUBVER
CS_PATCHLEVEL = _csnd.CS_PATCHLEVEL
CS_APIVERSION = _csnd.CS_APIVERSION
CS_APISUBVER = _csnd.CS_APISUBVER
class Csound(_object):
    """Proxy of C++ Csound class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Csound, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Csound, name)
    __repr__ = _swig_repr
    def GetCsound(*args):
        """GetCsound(self) -> CSOUND"""
        return _csnd.Csound_GetCsound(*args)

    def PreCompile(*args):
        """PreCompile(self) -> int"""
        return _csnd.Csound_PreCompile(*args)

    def InitializeCscore(*args):
        """InitializeCscore(self, FILE insco, FILE outsco) -> int"""
        return _csnd.Csound_InitializeCscore(*args)

    def GetHostData(*args):
        """GetHostData(self) -> void"""
        return _csnd.Csound_GetHostData(*args)

    def SetHostData(*args):
        """SetHostData(self, void hostData)"""
        return _csnd.Csound_SetHostData(*args)

    def GetEnv(*args):
        """GetEnv(self, char name) -> char"""
        return _csnd.Csound_GetEnv(*args)

    def Compile(*args):
        """
        Compile(self, int argc, char argv) -> int
        Compile(self, char csdName) -> int
        Compile(self, char orcName, char scoName) -> int
        Compile(self, char arg1, char arg2, char arg3) -> int
        Compile(self, char arg1, char arg2, char arg3, char arg4) -> int
        Compile(self, char arg1, char arg2, char arg3, char arg4, char arg5) -> int
        """
        return _csnd.Csound_Compile(*args)

    def Perform(*args):
        """
        Perform(self) -> int
        Perform(self, int argc, char argv) -> int
        Perform(self, char csdName) -> int
        Perform(self, char orcName, char scoName) -> int
        Perform(self, char arg1, char arg2, char arg3) -> int
        Perform(self, char arg1, char arg2, char arg3, char arg4) -> int
        Perform(self, char arg1, char arg2, char arg3, char arg4, char arg5) -> int
        """
        return _csnd.Csound_Perform(*args)

    def PerformKsmps(*args):
        """PerformKsmps(self) -> int"""
        return _csnd.Csound_PerformKsmps(*args)

    def PerformKsmpsAbsolute(*args):
        """PerformKsmpsAbsolute(self) -> int"""
        return _csnd.Csound_PerformKsmpsAbsolute(*args)

    def PerformBuffer(*args):
        """PerformBuffer(self) -> int"""
        return _csnd.Csound_PerformBuffer(*args)

    def Stop(*args):
        """Stop(self)"""
        return _csnd.Csound_Stop(*args)

    def Cleanup(*args):
        """Cleanup(self) -> int"""
        return _csnd.Csound_Cleanup(*args)

    def Reset(*args):
        """Reset(self)"""
        return _csnd.Csound_Reset(*args)

    def GetSr(*args):
        """GetSr(self) -> float"""
        return _csnd.Csound_GetSr(*args)

    def GetKr(*args):
        """GetKr(self) -> float"""
        return _csnd.Csound_GetKr(*args)

    def GetKsmps(*args):
        """GetKsmps(self) -> int"""
        return _csnd.Csound_GetKsmps(*args)

    def GetNchnls(*args):
        """GetNchnls(self) -> int"""
        return _csnd.Csound_GetNchnls(*args)

    def Get0dBFS(*args):
        """Get0dBFS(self) -> float"""
        return _csnd.Csound_Get0dBFS(*args)

    def GetStrVarMaxLen(*args):
        """GetStrVarMaxLen(self) -> int"""
        return _csnd.Csound_GetStrVarMaxLen(*args)

    def GetSampleFormat(*args):
        """GetSampleFormat(self) -> int"""
        return _csnd.Csound_GetSampleFormat(*args)

    def GetSampleSize(*args):
        """GetSampleSize(self) -> int"""
        return _csnd.Csound_GetSampleSize(*args)

    def GetInputBufferSize(*args):
        """GetInputBufferSize(self) -> long"""
        return _csnd.Csound_GetInputBufferSize(*args)

    def GetOutputBufferSize(*args):
        """GetOutputBufferSize(self) -> long"""
        return _csnd.Csound_GetOutputBufferSize(*args)

    def GetInputBuffer(*args):
        """GetInputBuffer(self) -> float"""
        return _csnd.Csound_GetInputBuffer(*args)

    def GetOutputBuffer(*args):
        """GetOutputBuffer(self) -> float"""
        return _csnd.Csound_GetOutputBuffer(*args)

    def GetSpin(*args):
        """GetSpin(self) -> float"""
        return _csnd.Csound_GetSpin(*args)

    def GetSpout(*args):
        """GetSpout(self) -> float"""
        return _csnd.Csound_GetSpout(*args)

    def GetOutputFileName(*args):
        """GetOutputFileName(self) -> char"""
        return _csnd.Csound_GetOutputFileName(*args)

    def SetHostImplementedAudioIO(*args):
        """SetHostImplementedAudioIO(self, int state, int bufSize)"""
        return _csnd.Csound_SetHostImplementedAudioIO(*args)

    def GetScoreTime(*args):
        """GetScoreTime(self) -> double"""
        return _csnd.Csound_GetScoreTime(*args)

    def IsScorePending(*args):
        """IsScorePending(self) -> int"""
        return _csnd.Csound_IsScorePending(*args)

    def SetScorePending(*args):
        """SetScorePending(self, int pending)"""
        return _csnd.Csound_SetScorePending(*args)

    def GetScoreOffsetSeconds(*args):
        """GetScoreOffsetSeconds(self) -> float"""
        return _csnd.Csound_GetScoreOffsetSeconds(*args)

    def SetScoreOffsetSeconds(*args):
        """SetScoreOffsetSeconds(self, double time)"""
        return _csnd.Csound_SetScoreOffsetSeconds(*args)

    def RewindScore(*args):
        """RewindScore(self)"""
        return _csnd.Csound_RewindScore(*args)

    def ScoreSort(*args):
        """ScoreSort(self, FILE inFile, FILE outFile) -> int"""
        return _csnd.Csound_ScoreSort(*args)

    def ScoreExtract(*args):
        """ScoreExtract(self, FILE inFile, FILE outFile, FILE extractFile) -> int"""
        return _csnd.Csound_ScoreExtract(*args)

    def Message(*args):
        """Message(self, char format, v(...) ?)"""
        return _csnd.Csound_Message(*args)

    def MessageS(*args):
        """MessageS(self, int attr, char format, v(...) ?)"""
        return _csnd.Csound_MessageS(*args)

    def GetMessageLevel(*args):
        """GetMessageLevel(self) -> int"""
        return _csnd.Csound_GetMessageLevel(*args)

    def SetMessageLevel(*args):
        """SetMessageLevel(self, int messageLevel)"""
        return _csnd.Csound_SetMessageLevel(*args)

    def InputMessage(*args):
        """InputMessage(self, char message)"""
        return _csnd.Csound_InputMessage(*args)

    def KeyPress(*args):
        """KeyPress(self, char c)"""
        return _csnd.Csound_KeyPress(*args)

    def ScoreEvent(*args):
        """ScoreEvent(self, char type, float pFields, long numFields) -> int"""
        return _csnd.Csound_ScoreEvent(*args)

    def NewOpcodeList(*args):
        """NewOpcodeList(self, opcodeListEntry opcodelist) -> int"""
        return _csnd.Csound_NewOpcodeList(*args)

    def DisposeOpcodeList(*args):
        """DisposeOpcodeList(self, opcodeListEntry opcodelist)"""
        return _csnd.Csound_DisposeOpcodeList(*args)

    def AppendOpcode(*args):
        """
        AppendOpcode(self, char opname, int dsblksiz, int thread, char outypes, 
            char intypes, int iopadr, int kopadr, int aopadr) -> int
        """
        return _csnd.Csound_AppendOpcode(*args)

    def GetDebug(*args):
        """GetDebug(self) -> int"""
        return _csnd.Csound_GetDebug(*args)

    def SetDebug(*args):
        """SetDebug(self, int debug)"""
        return _csnd.Csound_SetDebug(*args)

    def TableLength(*args):
        """TableLength(self, int table) -> int"""
        return _csnd.Csound_TableLength(*args)

    def TableGet(*args):
        """TableGet(self, int table, int index) -> float"""
        return _csnd.Csound_TableGet(*args)

    def TableSet(*args):
        """TableSet(self, int table, int index, double value)"""
        return _csnd.Csound_TableSet(*args)

    def GetTable(*args):
        """GetTable(self, float tablePtr, int tableNum) -> int"""
        return _csnd.Csound_GetTable(*args)

    def CreateGlobalVariable(*args):
        """CreateGlobalVariable(self, char name, size_t nbytes) -> int"""
        return _csnd.Csound_CreateGlobalVariable(*args)

    def QueryGlobalVariable(*args):
        """QueryGlobalVariable(self, char name) -> void"""
        return _csnd.Csound_QueryGlobalVariable(*args)

    def QueryGlobalVariableNoCheck(*args):
        """QueryGlobalVariableNoCheck(self, char name) -> void"""
        return _csnd.Csound_QueryGlobalVariableNoCheck(*args)

    def DestroyGlobalVariable(*args):
        """DestroyGlobalVariable(self, char name) -> int"""
        return _csnd.Csound_DestroyGlobalVariable(*args)

    def GetRtRecordUserData(*args):
        """GetRtRecordUserData(self) -> void"""
        return _csnd.Csound_GetRtRecordUserData(*args)

    def GetRtPlayUserData(*args):
        """GetRtPlayUserData(self) -> void"""
        return _csnd.Csound_GetRtPlayUserData(*args)

    def RunUtility(*args):
        """RunUtility(self, char name, int argc, char argv) -> int"""
        return _csnd.Csound_RunUtility(*args)

    def ListUtilities(*args):
        """ListUtilities(self) -> char"""
        return _csnd.Csound_ListUtilities(*args)

    def DeleteUtilityList(*args):
        """DeleteUtilityList(self, char lst)"""
        return _csnd.Csound_DeleteUtilityList(*args)

    def GetUtilityDescription(*args):
        """GetUtilityDescription(self, char utilName) -> char"""
        return _csnd.Csound_GetUtilityDescription(*args)

    def GetChannelPtr(*args):
        """GetChannelPtr(self, float p, char name, int type) -> int"""
        return _csnd.Csound_GetChannelPtr(*args)

    def ListChannels(*args):
        """ListChannels(self,  lst) -> int"""
        return _csnd.Csound_ListChannels(*args)

    def DeleteChannelList(*args):
        """DeleteChannelList(self,  lst)"""
        return _csnd.Csound_DeleteChannelList(*args)

    def SetControlChannelParams(*args):
        """SetControlChannelParams(self, char name, int type, double dflt, double min, double max) -> int"""
        return _csnd.Csound_SetControlChannelParams(*args)

    def GetControlChannelParams(*args):
        """GetControlChannelParams(self, char name, float dflt, float min, float max) -> int"""
        return _csnd.Csound_GetControlChannelParams(*args)

    def SetChannel(*args):
        """
        SetChannel(self, char name, double value)
        SetChannel(self, char name, char value)
        """
        return _csnd.Csound_SetChannel(*args)

    def GetChannel(*args):
        """GetChannel(self, char name) -> float"""
        return _csnd.Csound_GetChannel(*args)

    def ChanIKSet(*args):
        """ChanIKSet(self, double value, int n) -> int"""
        return _csnd.Csound_ChanIKSet(*args)

    def ChanOKGet(*args):
        """ChanOKGet(self, float value, int n) -> int"""
        return _csnd.Csound_ChanOKGet(*args)

    def ChanIASet(*args):
        """ChanIASet(self, float value, int n) -> int"""
        return _csnd.Csound_ChanIASet(*args)

    def ChanOAGet(*args):
        """ChanOAGet(self, float value, int n) -> int"""
        return _csnd.Csound_ChanOAGet(*args)

    def PvsBusInit(*args):
        """
        PvsBusInit(self, int N=1024, int olaps=256, int wsize=256, int wtype=1, 
            int format=0)
        PvsBusInit(self, int N=1024, int olaps=256, int wsize=256, int wtype=1)
        PvsBusInit(self, int N=1024, int olaps=256, int wsize=256)
        PvsBusInit(self, int N=1024, int olaps=256)
        PvsBusInit(self, int N=1024)
        PvsBusInit(self)
        """
        return _csnd.Csound_PvsBusInit(*args)

    def PvsBusDestroy(*args):
        """PvsBusDestroy(self)"""
        return _csnd.Csound_PvsBusDestroy(*args)

    def PvsinSet(*args):
        """
        PvsinSet(self, float val, int k, int n)
        PvsinSet(self,  value, int n) -> int
        """
        return _csnd.Csound_PvsinSet(*args)

    def PvsoutGet(*args):
        """
        PvsoutGet(self, int k, int n) -> float
        PvsoutGet(self,  value, int n) -> int
        """
        return _csnd.Csound_PvsoutGet(*args)

    def CreateConfigurationVariable(*args):
        """
        CreateConfigurationVariable(self, char name, void p, int type, int flags, void min, void max, 
            char shortDesc, char longDesc) -> int
        """
        return _csnd.Csound_CreateConfigurationVariable(*args)

    def SetConfigurationVariable(*args):
        """SetConfigurationVariable(self, char name, void value) -> int"""
        return _csnd.Csound_SetConfigurationVariable(*args)

    def ParseConfigurationVariable(*args):
        """ParseConfigurationVariable(self, char name, char value) -> int"""
        return _csnd.Csound_ParseConfigurationVariable(*args)

    def QueryConfigurationVariable(*args):
        """QueryConfigurationVariable(self, char name)"""
        return _csnd.Csound_QueryConfigurationVariable(*args)

    def ListConfigurationVariables(*args):
        """ListConfigurationVariables(self)"""
        return _csnd.Csound_ListConfigurationVariables(*args)

    def DeleteConfigurationVariable(*args):
        """DeleteConfigurationVariable(self, char name) -> int"""
        return _csnd.Csound_DeleteConfigurationVariable(*args)

    def SetChannelIOCallback(*args):
        """SetChannelIOCallback(self, CsoundChannelIOCallback_t func)"""
        return _csnd.Csound_SetChannelIOCallback(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> Csound
        __init__(self, void hostData) -> Csound
        """
        this = _csnd.new_Csound(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_Csound
    __del__ = lambda self : None;
    def EnableMessageBuffer(*args):
        """EnableMessageBuffer(self, int toStdOut)"""
        return _csnd.Csound_EnableMessageBuffer(*args)

    def GetFirstMessage(*args):
        """GetFirstMessage(self) -> char"""
        return _csnd.Csound_GetFirstMessage(*args)

    def GetFirstMessageAttr(*args):
        """GetFirstMessageAttr(self) -> int"""
        return _csnd.Csound_GetFirstMessageAttr(*args)

    def PopFirstMessage(*args):
        """PopFirstMessage(self)"""
        return _csnd.Csound_PopFirstMessage(*args)

    def GetMessageCnt(*args):
        """GetMessageCnt(self) -> int"""
        return _csnd.Csound_GetMessageCnt(*args)

    def DestroyMessageBuffer(*args):
        """DestroyMessageBuffer(self)"""
        return _csnd.Csound_DestroyMessageBuffer(*args)

Csound_swigregister = _csnd.Csound_swigregister
Csound_swigregister(Csound)

class CsoundThreadLock(_object):
    """Proxy of C++ CsoundThreadLock class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundThreadLock, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundThreadLock, name)
    __repr__ = _swig_repr
    def Lock(*args):
        """
        Lock(self, size_t milliseconds) -> int
        Lock(self)
        """
        return _csnd.CsoundThreadLock_Lock(*args)

    def TryLock(*args):
        """TryLock(self) -> int"""
        return _csnd.CsoundThreadLock_TryLock(*args)

    def Unlock(*args):
        """Unlock(self)"""
        return _csnd.CsoundThreadLock_Unlock(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> CsoundThreadLock
        __init__(self, int locked) -> CsoundThreadLock
        """
        this = _csnd.new_CsoundThreadLock(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundThreadLock
    __del__ = lambda self : None;
CsoundThreadLock_swigregister = _csnd.CsoundThreadLock_swigregister
CsoundThreadLock_swigregister(CsoundThreadLock)

class CsoundMutex(_object):
    """Proxy of C++ CsoundMutex class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMutex, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMutex, name)
    __repr__ = _swig_repr
    def Lock(*args):
        """Lock(self)"""
        return _csnd.CsoundMutex_Lock(*args)

    def TryLock(*args):
        """TryLock(self) -> int"""
        return _csnd.CsoundMutex_TryLock(*args)

    def Unlock(*args):
        """Unlock(self)"""
        return _csnd.CsoundMutex_Unlock(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> CsoundMutex
        __init__(self, int isRecursive) -> CsoundMutex
        """
        this = _csnd.new_CsoundMutex(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMutex
    __del__ = lambda self : None;
CsoundMutex_swigregister = _csnd.CsoundMutex_swigregister
CsoundMutex_swigregister(CsoundMutex)

class CsoundRandMT(_object):
    """Proxy of C++ CsoundRandMT class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundRandMT, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundRandMT, name)
    __repr__ = _swig_repr
    def Random(*args):
        """Random(self) -> uint32_t"""
        return _csnd.CsoundRandMT_Random(*args)

    def Seed(*args):
        """
        Seed(self, uint32_t seedVal)
        Seed(self, uint32_t initKey, int keyLength)
        """
        return _csnd.CsoundRandMT_Seed(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> CsoundRandMT
        __init__(self, uint32_t seedVal) -> CsoundRandMT
        __init__(self, uint32_t initKey, int keyLength) -> CsoundRandMT
        """
        this = _csnd.new_CsoundRandMT(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundRandMT
    __del__ = lambda self : None;
CsoundRandMT_swigregister = _csnd.CsoundRandMT_swigregister
CsoundRandMT_swigregister(CsoundRandMT)

class CsoundTimer(_object):
    """Proxy of C++ CsoundTimer class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundTimer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundTimer, name)
    __repr__ = _swig_repr
    def GetRealTime(*args):
        """GetRealTime(self) -> double"""
        return _csnd.CsoundTimer_GetRealTime(*args)

    def GetCPUTime(*args):
        """GetCPUTime(self) -> double"""
        return _csnd.CsoundTimer_GetCPUTime(*args)

    def Reset(*args):
        """Reset(self)"""
        return _csnd.CsoundTimer_Reset(*args)

    def __init__(self, *args): 
        """__init__(self) -> CsoundTimer"""
        this = _csnd.new_CsoundTimer(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundTimer
    __del__ = lambda self : None;
CsoundTimer_swigregister = _csnd.CsoundTimer_swigregister
CsoundTimer_swigregister(CsoundTimer)

class CsoundOpcodeList(_object):
    """Proxy of C++ CsoundOpcodeList class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundOpcodeList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundOpcodeList, name)
    __repr__ = _swig_repr
    def Count(*args):
        """Count(self) -> int"""
        return _csnd.CsoundOpcodeList_Count(*args)

    def Name(*args):
        """Name(self, int ndx) -> char"""
        return _csnd.CsoundOpcodeList_Name(*args)

    def OutTypes(*args):
        """OutTypes(self, int ndx) -> char"""
        return _csnd.CsoundOpcodeList_OutTypes(*args)

    def InTypes(*args):
        """InTypes(self, int ndx) -> char"""
        return _csnd.CsoundOpcodeList_InTypes(*args)

    def Clear(*args):
        """Clear(self)"""
        return _csnd.CsoundOpcodeList_Clear(*args)

    def __init__(self, *args): 
        """
        __init__(self, CSOUND csound) -> CsoundOpcodeList
        __init__(self, Csound csound) -> CsoundOpcodeList
        """
        this = _csnd.new_CsoundOpcodeList(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundOpcodeList
    __del__ = lambda self : None;
CsoundOpcodeList_swigregister = _csnd.CsoundOpcodeList_swigregister
CsoundOpcodeList_swigregister(CsoundOpcodeList)

class CsoundChannelList(_object):
    """Proxy of C++ CsoundChannelList class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundChannelList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundChannelList, name)
    __repr__ = _swig_repr
    def Count(*args):
        """Count(self) -> int"""
        return _csnd.CsoundChannelList_Count(*args)

    def Name(*args):
        """Name(self, int ndx) -> char"""
        return _csnd.CsoundChannelList_Name(*args)

    def Type(*args):
        """Type(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_Type(*args)

    def IsControlChannel(*args):
        """IsControlChannel(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_IsControlChannel(*args)

    def IsAudioChannel(*args):
        """IsAudioChannel(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_IsAudioChannel(*args)

    def IsStringChannel(*args):
        """IsStringChannel(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_IsStringChannel(*args)

    def IsInputChannel(*args):
        """IsInputChannel(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_IsInputChannel(*args)

    def IsOutputChannel(*args):
        """IsOutputChannel(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_IsOutputChannel(*args)

    def SubType(*args):
        """SubType(self, int ndx) -> int"""
        return _csnd.CsoundChannelList_SubType(*args)

    def DefaultValue(*args):
        """DefaultValue(self, int ndx) -> double"""
        return _csnd.CsoundChannelList_DefaultValue(*args)

    def MinValue(*args):
        """MinValue(self, int ndx) -> double"""
        return _csnd.CsoundChannelList_MinValue(*args)

    def MaxValue(*args):
        """MaxValue(self, int ndx) -> double"""
        return _csnd.CsoundChannelList_MaxValue(*args)

    def Clear(*args):
        """Clear(self)"""
        return _csnd.CsoundChannelList_Clear(*args)

    def __init__(self, *args): 
        """
        __init__(self, CSOUND csound) -> CsoundChannelList
        __init__(self, Csound csound) -> CsoundChannelList
        """
        this = _csnd.new_CsoundChannelList(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundChannelList
    __del__ = lambda self : None;
CsoundChannelList_swigregister = _csnd.CsoundChannelList_swigregister
CsoundChannelList_swigregister(CsoundChannelList)

class CsoundUtilityList(_object):
    """Proxy of C++ CsoundUtilityList class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundUtilityList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundUtilityList, name)
    __repr__ = _swig_repr
    def Count(*args):
        """Count(self) -> int"""
        return _csnd.CsoundUtilityList_Count(*args)

    def Name(*args):
        """Name(self, int ndx) -> char"""
        return _csnd.CsoundUtilityList_Name(*args)

    def Clear(*args):
        """Clear(self)"""
        return _csnd.CsoundUtilityList_Clear(*args)

    def __init__(self, *args): 
        """
        __init__(self, CSOUND csound) -> CsoundUtilityList
        __init__(self, Csound csound) -> CsoundUtilityList
        """
        this = _csnd.new_CsoundUtilityList(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundUtilityList
    __del__ = lambda self : None;
CsoundUtilityList_swigregister = _csnd.CsoundUtilityList_swigregister
CsoundUtilityList_swigregister(CsoundUtilityList)

class CsoundMYFLTArray(_object):
    """Proxy of C++ CsoundMYFLTArray class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMYFLTArray, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMYFLTArray, name)
    __repr__ = _swig_repr
    def GetPtr(*args):
        """
        GetPtr(self) -> float
        GetPtr(self, int ndx) -> float
        """
        return _csnd.CsoundMYFLTArray_GetPtr(*args)

    def SetPtr(*args):
        """SetPtr(self, float ptr)"""
        return _csnd.CsoundMYFLTArray_SetPtr(*args)

    def SetValue(*args):
        """SetValue(self, int ndx, double value)"""
        return _csnd.CsoundMYFLTArray_SetValue(*args)

    def GetValue(*args):
        """GetValue(self, int ndx) -> double"""
        return _csnd.CsoundMYFLTArray_GetValue(*args)

    def SetValues(*args):
        """
        SetValues(self, int ndx, double v0, double v1)
        SetValues(self, int ndx, double v0, double v1, double v2)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4, double v5)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4, double v5, double v6)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4, double v5, double v6, double v7)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4, double v5, double v6, double v7, 
            double v8)
        SetValues(self, int ndx, double v0, double v1, double v2, double v3, 
            double v4, double v5, double v6, double v7, 
            double v8, double v9)
        SetValues(self, int ndx, int n, float src)
        """
        return _csnd.CsoundMYFLTArray_SetValues(*args)

    def GetValues(*args):
        """GetValues(self, float dst, int ndx, int n)"""
        return _csnd.CsoundMYFLTArray_GetValues(*args)

    def SetStringValue(*args):
        """SetStringValue(self, char s, int maxLen)"""
        return _csnd.CsoundMYFLTArray_SetStringValue(*args)

    def GetStringValue(*args):
        """GetStringValue(self) -> char"""
        return _csnd.CsoundMYFLTArray_GetStringValue(*args)

    def Clear(*args):
        """Clear(self)"""
        return _csnd.CsoundMYFLTArray_Clear(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> CsoundMYFLTArray
        __init__(self, int n) -> CsoundMYFLTArray
        """
        this = _csnd.new_CsoundMYFLTArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMYFLTArray
    __del__ = lambda self : None;
CsoundMYFLTArray_swigregister = _csnd.CsoundMYFLTArray_swigregister
CsoundMYFLTArray_swigregister(CsoundMYFLTArray)

class CsoundArgVList(_object):
    """Proxy of C++ CsoundArgVList class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundArgVList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundArgVList, name)
    __repr__ = _swig_repr
    def argc(*args):
        """argc(self) -> int"""
        return _csnd.CsoundArgVList_argc(*args)

    def argv(*args):
        """
        argv(self) -> char
        argv(self, int ndx) -> char
        """
        return _csnd.CsoundArgVList_argv(*args)

    def Insert(*args):
        """Insert(self, int ndx, char s)"""
        return _csnd.CsoundArgVList_Insert(*args)

    def Append(*args):
        """Append(self, char s)"""
        return _csnd.CsoundArgVList_Append(*args)

    def Clear(*args):
        """Clear(self)"""
        return _csnd.CsoundArgVList_Clear(*args)

    def __init__(self, *args): 
        """__init__(self) -> CsoundArgVList"""
        this = _csnd.new_CsoundArgVList(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundArgVList
    __del__ = lambda self : None;
CsoundArgVList_swigregister = _csnd.CsoundArgVList_swigregister
CsoundArgVList_swigregister(CsoundArgVList)

class CsoundCallbackWrapper(_object):
    """Proxy of C++ CsoundCallbackWrapper class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundCallbackWrapper, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundCallbackWrapper, name)
    __repr__ = _swig_repr
    def MessageCallback(*args):
        """MessageCallback(self, int attr, char msg)"""
        return _csnd.CsoundCallbackWrapper_MessageCallback(*args)

    def InputValueCallback(*args):
        """InputValueCallback(self, char chnName) -> double"""
        return _csnd.CsoundCallbackWrapper_InputValueCallback(*args)

    def OutputValueCallback(*args):
        """OutputValueCallback(self, char chnName, double value)"""
        return _csnd.CsoundCallbackWrapper_OutputValueCallback(*args)

    def YieldCallback(*args):
        """YieldCallback(self) -> int"""
        return _csnd.CsoundCallbackWrapper_YieldCallback(*args)

    def MidiInputCallback(*args):
        """MidiInputCallback(self, CsoundMidiInputBuffer p)"""
        return _csnd.CsoundCallbackWrapper_MidiInputCallback(*args)

    def MidiOutputCallback(*args):
        """MidiOutputCallback(self, CsoundMidiOutputBuffer p)"""
        return _csnd.CsoundCallbackWrapper_MidiOutputCallback(*args)

    def ControlChannelInputCallback(*args):
        """ControlChannelInputCallback(self, char chnName) -> double"""
        return _csnd.CsoundCallbackWrapper_ControlChannelInputCallback(*args)

    def ControlChannelOutputCallback(*args):
        """ControlChannelOutputCallback(self, char chnName, double value)"""
        return _csnd.CsoundCallbackWrapper_ControlChannelOutputCallback(*args)

    def StringChannelInputCallback(*args):
        """StringChannelInputCallback(self, char chnName) -> char"""
        return _csnd.CsoundCallbackWrapper_StringChannelInputCallback(*args)

    def StringChannelOutputCallback(*args):
        """StringChannelOutputCallback(self, char chnName, char value)"""
        return _csnd.CsoundCallbackWrapper_StringChannelOutputCallback(*args)

    def SetMessageCallback(*args):
        """SetMessageCallback(self)"""
        return _csnd.CsoundCallbackWrapper_SetMessageCallback(*args)

    def SetInputValueCallback(*args):
        """SetInputValueCallback(self)"""
        return _csnd.CsoundCallbackWrapper_SetInputValueCallback(*args)

    def SetOutputValueCallback(*args):
        """SetOutputValueCallback(self)"""
        return _csnd.CsoundCallbackWrapper_SetOutputValueCallback(*args)

    def SetYieldCallback(*args):
        """SetYieldCallback(self)"""
        return _csnd.CsoundCallbackWrapper_SetYieldCallback(*args)

    def SetMidiInputCallback(*args):
        """SetMidiInputCallback(self, CsoundArgVList argv)"""
        return _csnd.CsoundCallbackWrapper_SetMidiInputCallback(*args)

    def SetMidiOutputCallback(*args):
        """SetMidiOutputCallback(self, CsoundArgVList argv)"""
        return _csnd.CsoundCallbackWrapper_SetMidiOutputCallback(*args)

    def SetChannelIOCallbacks(*args):
        """SetChannelIOCallbacks(self)"""
        return _csnd.CsoundCallbackWrapper_SetChannelIOCallbacks(*args)

    def GetCsound(*args):
        """GetCsound(self) -> CSOUND"""
        return _csnd.CsoundCallbackWrapper_GetCsound(*args)

    def CharPtrToString(*args):
        """CharPtrToString(char s) -> char"""
        return _csnd.CsoundCallbackWrapper_CharPtrToString(*args)

    if _newclass:CharPtrToString = staticmethod(CharPtrToString)
    __swig_getmethods__["CharPtrToString"] = lambda x: CharPtrToString
    def __init__(self, *args): 
        """
        __init__(self, Csound csound) -> CsoundCallbackWrapper
        __init__(self, CSOUND csound) -> CsoundCallbackWrapper
        """
        if self.__class__ == CsoundCallbackWrapper:
            args = (None,) + args
        else:
            args = (self,) + args
        this = _csnd.new_CsoundCallbackWrapper(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundCallbackWrapper
    __del__ = lambda self : None;
    def __disown__(self):
        self.this.disown()
        _csnd.disown_CsoundCallbackWrapper(self)
        return weakref_proxy(self)
CsoundCallbackWrapper_swigregister = _csnd.CsoundCallbackWrapper_swigregister
CsoundCallbackWrapper_swigregister(CsoundCallbackWrapper)

def CsoundCallbackWrapper_CharPtrToString(*args):
  """CsoundCallbackWrapper_CharPtrToString(char s) -> char"""
  return _csnd.CsoundCallbackWrapper_CharPtrToString(*args)

class CsoundMidiInputBuffer(_object):
    """Proxy of C++ CsoundMidiInputBuffer class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMidiInputBuffer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMidiInputBuffer, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(self, unsigned char buf, int bufSize) -> CsoundMidiInputBuffer"""
        this = _csnd.new_CsoundMidiInputBuffer(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMidiInputBuffer
    __del__ = lambda self : None;
    def SendMessage(*args):
        """
        SendMessage(self, int msg)
        SendMessage(self, int status, int channel, int data1, int data2)
        """
        return _csnd.CsoundMidiInputBuffer_SendMessage(*args)

    def SendNoteOn(*args):
        """SendNoteOn(self, int channel, int key, int velocity)"""
        return _csnd.CsoundMidiInputBuffer_SendNoteOn(*args)

    def SendNoteOff(*args):
        """
        SendNoteOff(self, int channel, int key, int velocity)
        SendNoteOff(self, int channel, int key)
        """
        return _csnd.CsoundMidiInputBuffer_SendNoteOff(*args)

    def SendPolyphonicPressure(*args):
        """SendPolyphonicPressure(self, int channel, int key, int value)"""
        return _csnd.CsoundMidiInputBuffer_SendPolyphonicPressure(*args)

    def SendControlChange(*args):
        """SendControlChange(self, int channel, int ctl, int value)"""
        return _csnd.CsoundMidiInputBuffer_SendControlChange(*args)

    def SendProgramChange(*args):
        """SendProgramChange(self, int channel, int pgm)"""
        return _csnd.CsoundMidiInputBuffer_SendProgramChange(*args)

    def SendChannelPressure(*args):
        """SendChannelPressure(self, int channel, int value)"""
        return _csnd.CsoundMidiInputBuffer_SendChannelPressure(*args)

    def SendPitchBend(*args):
        """SendPitchBend(self, int channel, int value)"""
        return _csnd.CsoundMidiInputBuffer_SendPitchBend(*args)

CsoundMidiInputBuffer_swigregister = _csnd.CsoundMidiInputBuffer_swigregister
CsoundMidiInputBuffer_swigregister(CsoundMidiInputBuffer)

class CsoundMidiInputStream(CsoundMidiInputBuffer):
    """Proxy of C++ CsoundMidiInputStream class"""
    __swig_setmethods__ = {}
    for _s in [CsoundMidiInputBuffer]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMidiInputStream, name, value)
    __swig_getmethods__ = {}
    for _s in [CsoundMidiInputBuffer]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMidiInputStream, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """
        __init__(self, CSOUND csound) -> CsoundMidiInputStream
        __init__(self, Csound csound) -> CsoundMidiInputStream
        """
        this = _csnd.new_CsoundMidiInputStream(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMidiInputStream
    __del__ = lambda self : None;
    def EnableMidiInput(*args):
        """EnableMidiInput(self, CsoundArgVList argv)"""
        return _csnd.CsoundMidiInputStream_EnableMidiInput(*args)

CsoundMidiInputStream_swigregister = _csnd.CsoundMidiInputStream_swigregister
CsoundMidiInputStream_swigregister(CsoundMidiInputStream)

class CsoundMidiOutputBuffer(_object):
    """Proxy of C++ CsoundMidiOutputBuffer class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMidiOutputBuffer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMidiOutputBuffer, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(self, unsigned char buf, int bufSize) -> CsoundMidiOutputBuffer"""
        this = _csnd.new_CsoundMidiOutputBuffer(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMidiOutputBuffer
    __del__ = lambda self : None;
    def PopMessage(*args):
        """PopMessage(self) -> int"""
        return _csnd.CsoundMidiOutputBuffer_PopMessage(*args)

    def GetStatus(*args):
        """GetStatus(self) -> int"""
        return _csnd.CsoundMidiOutputBuffer_GetStatus(*args)

    def GetChannel(*args):
        """GetChannel(self) -> int"""
        return _csnd.CsoundMidiOutputBuffer_GetChannel(*args)

    def GetData1(*args):
        """GetData1(self) -> int"""
        return _csnd.CsoundMidiOutputBuffer_GetData1(*args)

    def GetData2(*args):
        """GetData2(self) -> int"""
        return _csnd.CsoundMidiOutputBuffer_GetData2(*args)

CsoundMidiOutputBuffer_swigregister = _csnd.CsoundMidiOutputBuffer_swigregister
CsoundMidiOutputBuffer_swigregister(CsoundMidiOutputBuffer)

class CsoundMidiOutputStream(CsoundMidiOutputBuffer):
    """Proxy of C++ CsoundMidiOutputStream class"""
    __swig_setmethods__ = {}
    for _s in [CsoundMidiOutputBuffer]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundMidiOutputStream, name, value)
    __swig_getmethods__ = {}
    for _s in [CsoundMidiOutputBuffer]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundMidiOutputStream, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """
        __init__(self, CSOUND csound) -> CsoundMidiOutputStream
        __init__(self, Csound csound) -> CsoundMidiOutputStream
        """
        this = _csnd.new_CsoundMidiOutputStream(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundMidiOutputStream
    __del__ = lambda self : None;
    def EnableMidiOutput(*args):
        """EnableMidiOutput(self, CsoundArgVList argv)"""
        return _csnd.CsoundMidiOutputStream_EnableMidiOutput(*args)

CsoundMidiOutputStream_swigregister = _csnd.CsoundMidiOutputStream_swigregister
CsoundMidiOutputStream_swigregister(CsoundMidiOutputStream)

class CsoundPerformanceThread(_object):
    """Proxy of C++ CsoundPerformanceThread class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundPerformanceThread, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundPerformanceThread, name)
    __repr__ = _swig_repr
    def GetCsound(*args):
        """GetCsound(self) -> CSOUND"""
        return _csnd.CsoundPerformanceThread_GetCsound(*args)

    def GetStatus(*args):
        """GetStatus(self) -> int"""
        return _csnd.CsoundPerformanceThread_GetStatus(*args)

    def Play(*args):
        """Play(self)"""
        return _csnd.CsoundPerformanceThread_Play(*args)

    def Pause(*args):
        """Pause(self)"""
        return _csnd.CsoundPerformanceThread_Pause(*args)

    def TogglePause(*args):
        """TogglePause(self)"""
        return _csnd.CsoundPerformanceThread_TogglePause(*args)

    def Stop(*args):
        """Stop(self)"""
        return _csnd.CsoundPerformanceThread_Stop(*args)

    def ScoreEvent(*args):
        """ScoreEvent(self, int absp2mode, char opcod, int pcnt, float p)"""
        return _csnd.CsoundPerformanceThread_ScoreEvent(*args)

    def InputMessage(*args):
        """InputMessage(self, char s)"""
        return _csnd.CsoundPerformanceThread_InputMessage(*args)

    def SetScoreOffsetSeconds(*args):
        """SetScoreOffsetSeconds(self, double timeVal)"""
        return _csnd.CsoundPerformanceThread_SetScoreOffsetSeconds(*args)

    def Join(*args):
        """Join(self) -> int"""
        return _csnd.CsoundPerformanceThread_Join(*args)

    def FlushMessageQueue(*args):
        """FlushMessageQueue(self)"""
        return _csnd.CsoundPerformanceThread_FlushMessageQueue(*args)

    def __init__(self, *args): 
        """
        __init__(self, Csound ?) -> CsoundPerformanceThread
        __init__(self, CSOUND ?) -> CsoundPerformanceThread
        """
        this = _csnd.new_CsoundPerformanceThread(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundPerformanceThread
    __del__ = lambda self : None;
CsoundPerformanceThread_swigregister = _csnd.CsoundPerformanceThread_swigregister
CsoundPerformanceThread_swigregister(CsoundPerformanceThread)


def gatherArgs(*args):
  """gatherArgs(int argc, char argv, string commandLine)"""
  return _csnd.gatherArgs(*args)

def scatterArgs(*args):
  """
    scatterArgs(string commandLine, std::vector<(std::string,std::allocator<(std::string)>)> args, 
        std::vector<(p.char,std::allocator<(p.char)>)> argv)
    """
  return _csnd.scatterArgs(*args)

def trim(*args):
  """trim(string value) -> string"""
  return _csnd.trim(*args)

def trimQuotes(*args):
  """trimQuotes(string value) -> string"""
  return _csnd.trimQuotes(*args)

def parseInstrument(*args):
  """
    parseInstrument(string definition, string preNumber, string id, string name, 
        string postNumber) -> bool
    """
  return _csnd.parseInstrument(*args)
class CsoundFile(_object):
    """Proxy of C++ CsoundFile class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsoundFile, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsoundFile, name)
    __repr__ = _swig_repr
    __swig_setmethods__["libraryFilename"] = _csnd.CsoundFile_libraryFilename_set
    __swig_getmethods__["libraryFilename"] = _csnd.CsoundFile_libraryFilename_get
    if _newclass:libraryFilename = property(_csnd.CsoundFile_libraryFilename_get, _csnd.CsoundFile_libraryFilename_set)
    __swig_setmethods__["arrangement"] = _csnd.CsoundFile_arrangement_set
    __swig_getmethods__["arrangement"] = _csnd.CsoundFile_arrangement_get
    if _newclass:arrangement = property(_csnd.CsoundFile_arrangement_get, _csnd.CsoundFile_arrangement_set)
    def __init__(self, *args): 
        """__init__(self) -> CsoundFile"""
        this = _csnd.new_CsoundFile(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CsoundFile
    __del__ = lambda self : None;
    def generateFilename(*args):
        """generateFilename(self) -> string"""
        return _csnd.CsoundFile_generateFilename(*args)

    def getFilename(*args):
        """getFilename(self) -> string"""
        return _csnd.CsoundFile_getFilename(*args)

    def setFilename(*args):
        """setFilename(self, string name)"""
        return _csnd.CsoundFile_setFilename(*args)

    def load(*args):
        """
        load(self, string filename) -> int
        load(self, std::istream stream) -> int
        """
        return _csnd.CsoundFile_load(*args)

    def save(*args):
        """
        save(self, string filename) -> int
        save(self, std::ostream stream) -> int
        """
        return _csnd.CsoundFile_save(*args)

    def importFile(*args):
        """
        importFile(self, string filename) -> int
        importFile(self, std::istream stream) -> int
        """
        return _csnd.CsoundFile_importFile(*args)

    def importCommand(*args):
        """importCommand(self, std::istream stream) -> int"""
        return _csnd.CsoundFile_importCommand(*args)

    def exportCommand(*args):
        """exportCommand(self, std::ostream stream) -> int"""
        return _csnd.CsoundFile_exportCommand(*args)

    def importOrchestra(*args):
        """importOrchestra(self, std::istream stream) -> int"""
        return _csnd.CsoundFile_importOrchestra(*args)

    def exportOrchestra(*args):
        """exportOrchestra(self, std::ostream stream) -> int"""
        return _csnd.CsoundFile_exportOrchestra(*args)

    def importScore(*args):
        """importScore(self, std::istream stream) -> int"""
        return _csnd.CsoundFile_importScore(*args)

    def exportScore(*args):
        """exportScore(self, std::ostream stream) -> int"""
        return _csnd.CsoundFile_exportScore(*args)

    def importArrangement(*args):
        """importArrangement(self, std::istream stream) -> int"""
        return _csnd.CsoundFile_importArrangement(*args)

    def exportArrangement(*args):
        """exportArrangement(self, std::ostream stream) -> int"""
        return _csnd.CsoundFile_exportArrangement(*args)

    def exportArrangementForPerformance(*args):
        """
        exportArrangementForPerformance(self, string filename) -> int
        exportArrangementForPerformance(self, std::ostream stream) -> int
        """
        return _csnd.CsoundFile_exportArrangementForPerformance(*args)

    def importMidifile(*args):
        """importMidifile(self, std::istream stream) -> int"""
        return _csnd.CsoundFile_importMidifile(*args)

    def exportMidifile(*args):
        """exportMidifile(self, std::ostream stream) -> int"""
        return _csnd.CsoundFile_exportMidifile(*args)

    def getCommand(*args):
        """getCommand(self) -> string"""
        return _csnd.CsoundFile_getCommand(*args)

    def setCommand(*args):
        """setCommand(self, string commandLine)"""
        return _csnd.CsoundFile_setCommand(*args)

    def getOrcFilename(*args):
        """getOrcFilename(self) -> string"""
        return _csnd.CsoundFile_getOrcFilename(*args)

    def getScoFilename(*args):
        """getScoFilename(self) -> string"""
        return _csnd.CsoundFile_getScoFilename(*args)

    def getMidiFilename(*args):
        """getMidiFilename(self) -> string"""
        return _csnd.CsoundFile_getMidiFilename(*args)

    def getOutputSoundfileName(*args):
        """getOutputSoundfileName(self) -> string"""
        return _csnd.CsoundFile_getOutputSoundfileName(*args)

    def getOrchestra(*args):
        """getOrchestra(self) -> string"""
        return _csnd.CsoundFile_getOrchestra(*args)

    def setOrchestra(*args):
        """setOrchestra(self, string orchestra)"""
        return _csnd.CsoundFile_setOrchestra(*args)

    def getInstrumentCount(*args):
        """getInstrumentCount(self) -> int"""
        return _csnd.CsoundFile_getInstrumentCount(*args)

    def getOrchestraHeader(*args):
        """getOrchestraHeader(self) -> string"""
        return _csnd.CsoundFile_getOrchestraHeader(*args)

    def getInstrument(*args):
        """
        getInstrument(self, int number, string definition) -> bool
        getInstrument(self, string name, string definition) -> bool
        """
        return _csnd.CsoundFile_getInstrument(*args)

    def getScore(*args):
        """getScore(self) -> string"""
        return _csnd.CsoundFile_getScore(*args)

    def setScore(*args):
        """setScore(self, string score)"""
        return _csnd.CsoundFile_setScore(*args)

    def getArrangementCount(*args):
        """getArrangementCount(self) -> int"""
        return _csnd.CsoundFile_getArrangementCount(*args)

    def getArrangement(*args):
        """getArrangement(self, int index) -> string"""
        return _csnd.CsoundFile_getArrangement(*args)

    def addArrangement(*args):
        """addArrangement(self, string instrument)"""
        return _csnd.CsoundFile_addArrangement(*args)

    def setArrangement(*args):
        """setArrangement(self, int index, string instrument)"""
        return _csnd.CsoundFile_setArrangement(*args)

    def insertArrangement(*args):
        """insertArrangement(self, int index, string instrument)"""
        return _csnd.CsoundFile_insertArrangement(*args)

    def setCSD(*args):
        """setCSD(self, string xml)"""
        return _csnd.CsoundFile_setCSD(*args)

    def getCSD(*args):
        """getCSD(self) -> string"""
        return _csnd.CsoundFile_getCSD(*args)

    def addScoreLine(*args):
        """addScoreLine(self, string line)"""
        return _csnd.CsoundFile_addScoreLine(*args)

    def addNote(*args):
        """
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6, double p7, double p8, double p9, 
            double p10, double p11)
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6, double p7, double p8, double p9, 
            double p10)
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6, double p7, double p8, double p9)
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6, double p7, double p8)
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6, double p7)
        addNote(self, double p1, double p2, double p3, double p4, double p5, 
            double p6)
        addNote(self, double p1, double p2, double p3, double p4, double p5)
        addNote(self, double p1, double p2, double p3, double p4)
        addNote(self, double p1, double p2, double p3)
        """
        return _csnd.CsoundFile_addNote(*args)

    def exportForPerformance(*args):
        """exportForPerformance(self) -> bool"""
        return _csnd.CsoundFile_exportForPerformance(*args)

    def removeAll(*args):
        """removeAll(self)"""
        return _csnd.CsoundFile_removeAll(*args)

    def removeCommand(*args):
        """removeCommand(self)"""
        return _csnd.CsoundFile_removeCommand(*args)

    def removeOrchestra(*args):
        """removeOrchestra(self)"""
        return _csnd.CsoundFile_removeOrchestra(*args)

    def removeScore(*args):
        """removeScore(self)"""
        return _csnd.CsoundFile_removeScore(*args)

    def removeArrangement(*args):
        """
        removeArrangement(self, int index)
        removeArrangement(self)
        """
        return _csnd.CsoundFile_removeArrangement(*args)

    def removeMidifile(*args):
        """removeMidifile(self)"""
        return _csnd.CsoundFile_removeMidifile(*args)

    def loadOrcLibrary(*args):
        """
        loadOrcLibrary(self, char filename=0) -> bool
        loadOrcLibrary(self) -> bool
        """
        return _csnd.CsoundFile_loadOrcLibrary(*args)

CsoundFile_swigregister = _csnd.CsoundFile_swigregister
CsoundFile_swigregister(CsoundFile)

class MyfltVector(_object):
    """Proxy of C++ MyfltVector class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MyfltVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MyfltVector, name)
    __repr__ = _swig_repr
    def iterator(*args):
        """iterator(self, PyObject PYTHON_SELF) -> PySwigIterator"""
        return _csnd.MyfltVector_iterator(*args)

    def __iter__(self): return self.iterator()
    def __nonzero__(*args):
        """__nonzero__(self) -> bool"""
        return _csnd.MyfltVector___nonzero__(*args)

    def __len__(*args):
        """__len__(self) -> size_type"""
        return _csnd.MyfltVector___len__(*args)

    def pop(*args):
        """pop(self) -> value_type"""
        return _csnd.MyfltVector_pop(*args)

    def __getslice__(*args):
        """__getslice__(self, difference_type i, difference_type j) -> MyfltVector"""
        return _csnd.MyfltVector___getslice__(*args)

    def __setslice__(*args):
        """__setslice__(self, difference_type i, difference_type j, MyfltVector v)"""
        return _csnd.MyfltVector___setslice__(*args)

    def __delslice__(*args):
        """__delslice__(self, difference_type i, difference_type j)"""
        return _csnd.MyfltVector___delslice__(*args)

    def __delitem__(*args):
        """__delitem__(self, difference_type i)"""
        return _csnd.MyfltVector___delitem__(*args)

    def __getitem__(*args):
        """__getitem__(self, difference_type i) -> value_type"""
        return _csnd.MyfltVector___getitem__(*args)

    def __setitem__(*args):
        """__setitem__(self, difference_type i, value_type x)"""
        return _csnd.MyfltVector___setitem__(*args)

    def append(*args):
        """append(self, value_type x)"""
        return _csnd.MyfltVector_append(*args)

    def empty(*args):
        """empty(self) -> bool"""
        return _csnd.MyfltVector_empty(*args)

    def size(*args):
        """size(self) -> size_type"""
        return _csnd.MyfltVector_size(*args)

    def clear(*args):
        """clear(self)"""
        return _csnd.MyfltVector_clear(*args)

    def swap(*args):
        """swap(self, MyfltVector v)"""
        return _csnd.MyfltVector_swap(*args)

    def get_allocator(*args):
        """get_allocator(self) -> allocator_type"""
        return _csnd.MyfltVector_get_allocator(*args)

    def begin(*args):
        """
        begin(self) -> iterator
        begin(self) -> const_iterator
        """
        return _csnd.MyfltVector_begin(*args)

    def end(*args):
        """
        end(self) -> iterator
        end(self) -> const_iterator
        """
        return _csnd.MyfltVector_end(*args)

    def rbegin(*args):
        """
        rbegin(self) -> reverse_iterator
        rbegin(self) -> const_reverse_iterator
        """
        return _csnd.MyfltVector_rbegin(*args)

    def rend(*args):
        """
        rend(self) -> reverse_iterator
        rend(self) -> const_reverse_iterator
        """
        return _csnd.MyfltVector_rend(*args)

    def pop_back(*args):
        """pop_back(self)"""
        return _csnd.MyfltVector_pop_back(*args)

    def erase(*args):
        """
        erase(self, iterator pos) -> iterator
        erase(self, iterator first, iterator last) -> iterator
        """
        return _csnd.MyfltVector_erase(*args)

    def __init__(self, *args): 
        """
        __init__(self) -> MyfltVector
        __init__(self, MyfltVector ?) -> MyfltVector
        __init__(self, size_type size) -> MyfltVector
        __init__(self, size_type size, value_type value) -> MyfltVector
        """
        this = _csnd.new_MyfltVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args):
        """push_back(self, value_type x)"""
        return _csnd.MyfltVector_push_back(*args)

    def front(*args):
        """front(self) -> value_type"""
        return _csnd.MyfltVector_front(*args)

    def back(*args):
        """back(self) -> value_type"""
        return _csnd.MyfltVector_back(*args)

    def assign(*args):
        """assign(self, size_type n, value_type x)"""
        return _csnd.MyfltVector_assign(*args)

    def resize(*args):
        """
        resize(self, size_type new_size)
        resize(self, size_type new_size, value_type x)
        """
        return _csnd.MyfltVector_resize(*args)

    def insert(*args):
        """
        insert(self, iterator pos, value_type x) -> iterator
        insert(self, iterator pos, size_type n, value_type x)
        """
        return _csnd.MyfltVector_insert(*args)

    def reserve(*args):
        """reserve(self, size_type n)"""
        return _csnd.MyfltVector_reserve(*args)

    def capacity(*args):
        """capacity(self) -> size_type"""
        return _csnd.MyfltVector_capacity(*args)

    __swig_destroy__ = _csnd.delete_MyfltVector
    __del__ = lambda self : None;
MyfltVector_swigregister = _csnd.MyfltVector_swigregister
MyfltVector_swigregister(MyfltVector)

class CppSound(Csound,CsoundFile):
    """Proxy of C++ CppSound class"""
    __swig_setmethods__ = {}
    for _s in [Csound,CsoundFile]: __swig_setmethods__.update(_s.__swig_setmethods__)
    __setattr__ = lambda self, name, value: _swig_setattr(self, CppSound, name, value)
    __swig_getmethods__ = {}
    for _s in [Csound,CsoundFile]: __swig_getmethods__.update(_s.__swig_getmethods__)
    __getattr__ = lambda self, name: _swig_getattr(self, CppSound, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(self) -> CppSound"""
        this = _csnd.new_CppSound(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_CppSound
    __del__ = lambda self : None;
    def getCsound(*args):
        """getCsound(self) -> CSOUND"""
        return _csnd.CppSound_getCsound(*args)

    def getThis(*args):
        """getThis(self) -> long"""
        return _csnd.CppSound_getThis(*args)

    def getCsoundFile(*args):
        """getCsoundFile(self) -> CsoundFile"""
        return _csnd.CppSound_getCsoundFile(*args)

    def compile(*args):
        """
        compile(self, int argc, char argv) -> int
        compile(self) -> int
        """
        return _csnd.CppSound_compile(*args)

    def getSpoutSize(*args):
        """getSpoutSize(self) -> size_t"""
        return _csnd.CppSound_getSpoutSize(*args)

    def getOutputSoundfileName(*args):
        """getOutputSoundfileName(self) -> string"""
        return _csnd.CppSound_getOutputSoundfileName(*args)

    def perform(*args):
        """
        perform(self, int argc, char argv) -> int
        perform(self) -> int
        """
        return _csnd.CppSound_perform(*args)

    def performKsmps(*args):
        """performKsmps(self, bool absolute) -> int"""
        return _csnd.CppSound_performKsmps(*args)

    def cleanup(*args):
        """cleanup(self)"""
        return _csnd.CppSound_cleanup(*args)

    def inputMessage(*args):
        """inputMessage(self, char istatement)"""
        return _csnd.CppSound_inputMessage(*args)

    def write(*args):
        """write(self, char text)"""
        return _csnd.CppSound_write(*args)

    def getIsCompiled(*args):
        """getIsCompiled(self) -> bool"""
        return _csnd.CppSound_getIsCompiled(*args)

    def setIsPerforming(*args):
        """setIsPerforming(self, bool isPerforming)"""
        return _csnd.CppSound_setIsPerforming(*args)

    def getIsPerforming(*args):
        """getIsPerforming(self) -> bool"""
        return _csnd.CppSound_getIsPerforming(*args)

    def getIsGo(*args):
        """getIsGo(self) -> bool"""
        return _csnd.CppSound_getIsGo(*args)

    def stop(*args):
        """stop(self)"""
        return _csnd.CppSound_stop(*args)

    def setPythonMessageCallback(*args):
        """setPythonMessageCallback(self)"""
        return _csnd.CppSound_setPythonMessageCallback(*args)

CppSound_swigregister = _csnd.CppSound_swigregister
CppSound_swigregister(CppSound)


def csoundCsdCreate(*args):
  """csoundCsdCreate(CSOUND csound)"""
  return _csnd.csoundCsdCreate(*args)

def csoundCsdSetOptions(*args):
  """csoundCsdSetOptions(CSOUND csound, char options)"""
  return _csnd.csoundCsdSetOptions(*args)

def csoundCsdGetOptions(*args):
  """csoundCsdGetOptions(CSOUND csound) -> char"""
  return _csnd.csoundCsdGetOptions(*args)

def csoundCsdSetOrchestra(*args):
  """csoundCsdSetOrchestra(CSOUND csound, char orchestra)"""
  return _csnd.csoundCsdSetOrchestra(*args)

def csoundCsdGetOrchestra(*args):
  """csoundCsdGetOrchestra(CSOUND csound) -> char"""
  return _csnd.csoundCsdGetOrchestra(*args)

def csoundCsdAddScoreLine(*args):
  """csoundCsdAddScoreLine(CSOUND csound, char line)"""
  return _csnd.csoundCsdAddScoreLine(*args)

def csoundCsdAddEvent11(*args):
  """
    csoundCsdAddEvent11(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6, double p7, double p8, 
        double p9, double p10, double p11)
    """
  return _csnd.csoundCsdAddEvent11(*args)

def csoundCsdAddEvent10(*args):
  """
    csoundCsdAddEvent10(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6, double p7, double p8, 
        double p9, double p10)
    """
  return _csnd.csoundCsdAddEvent10(*args)

def csoundCsdAddEvent9(*args):
  """
    csoundCsdAddEvent9(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6, double p7, double p8, 
        double p9)
    """
  return _csnd.csoundCsdAddEvent9(*args)

def csoundCsdAddEvent8(*args):
  """
    csoundCsdAddEvent8(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6, double p7, double p8)
    """
  return _csnd.csoundCsdAddEvent8(*args)

def csoundCsdAddEvent7(*args):
  """
    csoundCsdAddEvent7(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6, double p7)
    """
  return _csnd.csoundCsdAddEvent7(*args)

def csoundCsdAddEvent6(*args):
  """
    csoundCsdAddEvent6(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5, double p6)
    """
  return _csnd.csoundCsdAddEvent6(*args)

def csoundCsdAddEvent5(*args):
  """
    csoundCsdAddEvent5(CSOUND csound, double p1, double p2, double p3, double p4, 
        double p5)
    """
  return _csnd.csoundCsdAddEvent5(*args)

def csoundCsdAddEvent4(*args):
  """csoundCsdAddEvent4(CSOUND csound, double p1, double p2, double p3, double p4)"""
  return _csnd.csoundCsdAddEvent4(*args)

def csoundCsdAddEvent3(*args):
  """csoundCsdAddEvent3(CSOUND csound, double p1, double p2, double p3)"""
  return _csnd.csoundCsdAddEvent3(*args)

def csoundCsdSave(*args):
  """csoundCsdSave(CSOUND csound, char filename) -> int"""
  return _csnd.csoundCsdSave(*args)

def csoundCsdCompile(*args):
  """csoundCsdCompile(CSOUND csound, char filename) -> int"""
  return _csnd.csoundCsdCompile(*args)

def csoundCsdPerform(*args):
  """csoundCsdPerform(CSOUND csound, char filename) -> int"""
  return _csnd.csoundCsdPerform(*args)

def csoundCompileCsd(*args):
  """csoundCompileCsd(CSOUND ?, char csdFilename) -> int"""
  return _csnd.csoundCompileCsd(*args)

def csoundPerformCsd(*args):
  """csoundPerformCsd(CSOUND ?, char csdFilename) -> int"""
  return _csnd.csoundPerformCsd(*args)
class Soundfile(_object):
    """Proxy of C++ Soundfile class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Soundfile, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Soundfile, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(self) -> Soundfile"""
        this = _csnd.new_Soundfile(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _csnd.delete_Soundfile
    __del__ = lambda self : None;
    def getFramesPerSecond(*args):
        """getFramesPerSecond(self) -> int"""
        return _csnd.Soundfile_getFramesPerSecond(*args)

    def setFramesPerSecond(*args):
        """setFramesPerSecond(self, int framesPerSecond)"""
        return _csnd.Soundfile_setFramesPerSecond(*args)

    def getChannelsPerFrame(*args):
        """getChannelsPerFrame(self) -> int"""
        return _csnd.Soundfile_getChannelsPerFrame(*args)

    def setChannelsPerFrame(*args):
        """setChannelsPerFrame(self, int channelsPerFrame)"""
        return _csnd.Soundfile_setChannelsPerFrame(*args)

    def getFormat(*args):
        """getFormat(self) -> int"""
        return _csnd.Soundfile_getFormat(*args)

    def setFormat(*args):
        """setFormat(self, int format)"""
        return _csnd.Soundfile_setFormat(*args)

    def getFrames(*args):
        """getFrames(self) -> int"""
        return _csnd.Soundfile_getFrames(*args)

    def open(*args):
        """open(self, string filename) -> int"""
        return _csnd.Soundfile_open(*args)

    def create(*args):
        """
        create(self, string filename, int framesPerSecond=44100, int channelsPerFrame=2, 
            int format=SF_FORMAT_WAV|SF_FORMAT_FLOAT) -> int
        create(self, string filename, int framesPerSecond=44100, int channelsPerFrame=2) -> int
        create(self, string filename, int framesPerSecond=44100) -> int
        create(self, string filename) -> int
        """
        return _csnd.Soundfile_create(*args)

    def seek(*args):
        """
        seek(self, int frames, int whence=0) -> int
        seek(self, int frames) -> int
        """
        return _csnd.Soundfile_seek(*args)

    def seekSeconds(*args):
        """
        seekSeconds(self, double seconds, int whence=0) -> double
        seekSeconds(self, double seconds) -> double
        """
        return _csnd.Soundfile_seekSeconds(*args)

    def readFrame(*args):
        """readFrame(self, double outputFrame) -> int"""
        return _csnd.Soundfile_readFrame(*args)

    def writeFrame(*args):
        """writeFrame(self, double inputFrame) -> int"""
        return _csnd.Soundfile_writeFrame(*args)

    def readFrames(*args):
        """readFrames(self, double outputFrames) -> int"""
        return _csnd.Soundfile_readFrames(*args)

    def writeFrames(*args):
        """writeFrames(self, double inputFrames) -> int"""
        return _csnd.Soundfile_writeFrames(*args)

    def mixFrames(*args):
        """mixFrames(self, double inputFrames, double mixedFrames) -> int"""
        return _csnd.Soundfile_mixFrames(*args)

    def updateHeader(*args):
        """updateHeader(self)"""
        return _csnd.Soundfile_updateHeader(*args)

    def close(*args):
        """close(self) -> int"""
        return _csnd.Soundfile_close(*args)

    def error(*args):
        """error(self)"""
        return _csnd.Soundfile_error(*args)

    def blank(*args):
        """blank(self, double duration)"""
        return _csnd.Soundfile_blank(*args)

Soundfile_swigregister = _csnd.Soundfile_swigregister
Soundfile_swigregister(Soundfile)



