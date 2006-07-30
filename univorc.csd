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

#include "basic.instruments"


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
