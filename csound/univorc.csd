<CsoundSynthesizer>
<CsOptions>
-+rtaudio=alsa -odac -m0 -d -b2048 -B4096
</CsOptions>
<CsInstruments>
sr=22050
ksmps=100
nchnls=2

gaudp1  init 0
gaudp2  init 0


/**************************************************************************
 General Soundfile Player - Used by Memosono
**************************************************************************/

instr 108
/* soundfile play control
  p4 : filename
  p5 : unique instance ID
  p6 : output gain (0-1)
  p7 : udp send gain (0-1)
  p8 : offset in seconds

  channels:
  sfplay.<ID>.on  - instance control channel (1:on 0: off)
  sfplay.<ID>.gain - soundfile play gain (0-1)
  sfplay.<ID>.udpgain - udp send gain (0-1)
  sfplay.<ID>.flen  - holds the channel length
*/
S1 strget p4
inst = p5
ich    filenchnls S1
iln    filelen  S1
ioffset = p8

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
Sudp  sprintf "sfplay.%d.udpgain", inst ; udp gain channel  
chnset S1, Sname
chnset 1,  Splay
chnset p6, Sgain
chnset p7, Sudp
event_i "i",109,0,iln,inst,ich,ioffset
turnoff
endin


instr 109
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
Sudp  sprintf "sfplay.%d.udpgain", inst ; udp gain channel   
kon chnget Splay
kg1 chnget Sgain
kg2 chnget Sudp
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
gaudp1 = a1*kg2 + gaudp1
gaudp2 = a2*kg2 + gaudp2
printf_i "sfplay:%d\n", 1, inst
endin




</CsInstruments>
<CsScore>
f0 600000

</CsScore>
</CsoundSynthesizer>
