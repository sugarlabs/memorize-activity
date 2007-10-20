<CsoundSynthesizer>
<CsOptions>
-+rtaudio=alsa -odac -m0 -d -b2048 -B4096
</CsOptions>
<CsInstruments>
sr=22050
ksmps=100
nchnls=2

/**************************************************************************
 General ogg-vorbis Soundfile Player
**************************************************************************/

instr 100
/* soundfile play control
  p4 : filename
  p5 : unique instance ID
  p6 : output gain (0-1)
  p7 : offset in seconds

  channels:
  sfplay.<ID>.on  - instance control channel (1:on 0: off)
  sfplay.<ID>.gain - soundfile play gain (0-1)
  sfplay.<ID>.flen  - holds the channel length
*/
S1 strget p4
inst = p5
ich = 1
iln = 10
ioffset = p7

Slen  sprintf "sfplay.%d.flen", p5  ; file length channel
chnset iln, Slen

Splay sprintf "sfplay.%d.on", inst  ; instance control channel
Sname sprintf "sfplay.%d.fname", inst  ; filename channel
Sgain sprintf "sfplay.%d.gain", inst ; gain channel
chnset S1, Sname
chnset 1,  Splay
chnset p6, Sgain
event_i "i",101,0,iln,inst,ich,ioffset
turnoff
endin


instr 101
/* soundfile player
  This is the actual soundfile player.
  It never gets called directly
*/
ich = p5
inst= p4
ioffset = p6
Splay sprintf "sfplay.%d.on", inst  ; instance control channel
Sname sprintf "sfplay.%d.fname", inst  ; filename channel
Sgain sprintf "sfplay.%d.gain", inst ; gain channel
kon chnget Splay
kg1 chnget Sgain
S1  chnget Sname
if kon == 0 then
printf "sfplay:%d OFF\n", 1, inst
turnoff
endif
if ich = 1 then
a1 oggplay S1, ioffset
a2 = a1
else
a1,a2 oggplay S1, ioffset
endif
     outs a1*kg1, a2*kg1
printf_i "sfplay:%d\n", 1, inst
endin


/**************************************************************************
 General wav, aiff Soundfile Player
**************************************************************************/

instr 102
/* soundfile play control
  p4 : filename
  p5 : unique instance ID
  p6 : output gain (0-1)
  p7 : offset in seconds

  channels:
  sfplay.<ID>.on  - instance control channel (1:on 0: off)
  sfplay.<ID>.gain - soundfile play gain (0-1)
  sfplay.<ID>.flen  - holds the channel length
*/
S1 strget p4
inst = p5
ich    filenchnls S1
iln    filelen  S1
ioffset = p7

Slen  sprintf "sfplay.%d.flen", p5  ; file length channel
chnset iln, Slen

if ioffset >= iln then
turnoff
else
iln = iln - ioffset
endif

Splay sprintf "sfplay.%d.on", inst  ; instance control channel
Sname sprintf "sfplay.%d.fname", inst  ; filename channel
Sgain sprintf "sfplay.%d.gain", inst ; gain channel 
chnset S1, Sname
chnset 1,  Splay
chnset p6, Sgain
event_i "i",103,0,iln,inst,ich,ioffset
turnoff
endin


instr 103
/* soundfile player
  This is the actual soundfile player.
  It never gets called directly
*/
ich = p5
inst= p4
ioffset = p6
Splay sprintf "sfplay.%d.on", inst  ; instance control channel
Sname sprintf "sfplay.%d.fname", inst  ; filename channel
Sgain sprintf "sfplay.%d.gain", inst ; gain channel
kon chnget Splay
kg1 chnget Sgain
S1  chnget Sname
if kon == 0 then
printf "sfplay:%d OFF\n", 1, inst
turnoff
endif
if ich = 1 then
a1 diskin2 S1,1,ioffset,1
a2 = a1
else
a1,a2 diskin2 S1,1,ioffset,1
endif
     outs a1*kg1, a2*kg1
endin


</CsInstruments>
<CsScore>
f0 600000

</CsScore>
</CsoundSynthesizer>
