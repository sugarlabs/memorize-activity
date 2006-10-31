<CsoundSynthesizer>
<CsOptions>
-odac -+rtaudio=alsa -d  
</CsOptions>

<CsInstruments>
sr=32000
ksmps=100
nchnls=2

gaudp1  init 0
gaudp2  init 0


instr 102
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


instr 254
/* udp receive instrument 
   p4 : unique instance ID

   channels:
   osc.<ID>.on  - instance control (1: on, 0: off)
ion = 1
inst = 0
Son   sprintf  "udprecv.%d.on"  , inst  ; instance control channel
chnset ion, Son
kon   chnget  Son

if kon == 0 then
printf "udprecv:%d OFF\n", 1, inst
turnoff
endif

asig sockrecv 40001, 32
outs asig, asig */
endin 


instr 255
/* udp send instrument 
socksends gaudp1, gaudp2, "1.1.25.90", 40000, 256     */
endin

instr 256
gaudp1 = 0
gaudp2 = 0
a1 = 0
outs a1, a1
endin 

</CsInstruments>

<CsScore>
f1 0 1024 10 1
i254 0 86400
i255 0 86400
i256 0 86400

; tests
; i 101 0 10 1 65 -16 -96
; i102 0 0.1 "coltrane.wav" 1 0.5 0 2
; i102 1 0.1 "jarrett.wav" 2  2 0 230

</CsScore>
</CsoundSynthesizer>
