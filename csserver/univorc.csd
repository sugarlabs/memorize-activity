<CsoundSynthesizer>
<CsOptions>
-+rtaudio=alsa -idevaudio -odevaudio -m0 -W -s -d -b256 -B1024
</CsOptions>
<CsInstruments>
sr=44100
ksmps=100
nchnls=2

gaudp1  init 0
gaudp2  init 0
gainrev init 0
gaoutL init 0
gaoutR init 0

/*****************************************************************
Reverb + master out
*****************************************************************/
instr 200

koutGain chnget "masterVolume"
koutGain = koutGain * 0.01

ia	ftgen	89,	0, 64, -2, -1009, -1103, -1123, -1281, -1289, -1307, -1361, -1409, -1429, -1543, -1583, -1601, -1613, -1709, -1801, -1949, -2003, -2111, -2203, -2341, -2411, -2591, -2609, -2749, -2801, -2903, -3001, -3109, -3203, -3301, -3407, -3539, 0.82, 0.81,	0.8,	0.79, 0.78, 0.77, 0.76, 0.75, 0.74, 0.73, 0.72, 0.71, 0.7, 0.69, 0.68, 0.67, 0.66, 0.65, 0.64, 0.63, 0.62, 0.61, 0.6, 0.59, 0.58, 0.57, 0.56, 0.55, 0.54, 0.53, 0.52, 0.51

ib	ftgen	90,	0, 16, -2, -179, -223, -233, -311, -347, -409, -433, -509, 0.76, 0.74, 0.72, 0.7, 0.68, 0.64, 0.62, 0.6

ain		dcblock		gainrev*0.05	
arev	nreverb		ain, 2.8, 0.7, 0, 32, 89, 8, 90
arev	butterlp	arev, 5000
arev	butterlp	arev, 5000

		outs		(arev + gaoutL)*koutGain, (arev + gaoutR) * koutGain

        gaoutL = 0
        gaoutR = 0		
		gainrev	=	0
		
endin

/****************************************************************
Audio input recording
****************************************************************/
instr 201

ain inch 1
itable = 300 + p4
aindex line 0, p3, 1
kenv   adsr     0.005, 0.05, .9, 0.01
tabw  ain*kenv, aindex, itable, 1
endin

/****************************************************************
Soundfile player with tied notes
****************************************************************/
instr 101

ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10
ifiltType = p11 - 1
icutoff = p12

idurfadein     init    0.002
idurfadeout     init    0.098
iampe0    	init    1                    ; FADE IN           
iampe1    	=  	iamp				     ; SUSTAIN
iampe2    	init    1				     ; FADE OUT

itie     	tival                        ; VERIFIE SI LA NOTE EST LIEE 
if itie  ==  1     	igoto nofadein       ; SI NON "FADE IN"

idurfadein  init iatt
iampe0    	init     0                   ; FADE IN
iskip   =   1 
kpitch     	init  	ipit                 ; INIT FREQUENCE POUR LES NOTES NON-LIEES
kamp   init    iamp
kpan        init    ipan
krg         init    irg

nofadein:
iskip   =   0
igliss  =   0.005

if p3   < 	0       igoto nofadeout       ; VERIFIE SI LA NOTE EST TENUE, SI NON "FADE OUT"

idurfadeout     init    idecay
iampe2      init    0                     ; FADE OUT

nofadeout:

idelta  =   idurfadein+idurfadeout
if idelta > abs(p3) then
idelta = abs(p3)
endif

iampe0      =       iampe0 * iamp
iampe2      =       iampe2 * iamp
kenv     	linseg  iampe0, idurfadein, iampe1, abs(p3)-idelta, iampe1, idurfadeout,  iampe2		; AMPLITUDE GLOBALE

; SI LA NOTE EST LIEE, ON SAUTE LE RESTE DE L'INITIALISATION
           	tigoto  tieskip

kpitch     	portk  	ipit, igliss, ipit    	             ; GLISSANDO
kpan        portk   ipan, igliss, ipan
krg         portk   irg, igliss, irg
kcutoff     portk   icutoff, igliss, icutoff

a1	     flooper2	1, kpitch, .25, .5, .1, itab, 0, 0, 0, iskip

if ifiltType != -1 then
acomp   =  a1
a1      bqrez   a1, kcutoff, 6, ifiltType 
a1      balance     a1, acomp
endif

a1      =   a1*kenv

gaoutL = a1*(1-kpan)+gaoutL
gaoutR =  a1*kpan+gaoutR

gainrev	=	        a1*krg+gainrev

  tieskip:                                    
endin

/********************************************************************
soundfile player for percussion - resonance notes
********************************************************************/
instr 102

p3      =   p3
ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10
ifiltType = p11 - 1
icutoff = p12

a1	 flooper2	1, ipit, .25, .750, .2, itab

if ifiltType != -1 then
acomp   =   a1
a1      bqrez   a1, icutoff, 6, ifiltType 
a1      balance     a1, acomp
endif

kenv    expseg  0.001, .003, .6, p3 - .003, 0.001
klocalenv   adsr     iatt, 0.05, .8, idecay

a1      =   a1*kenv*klocalenv

gaoutL = a1*(1-ipan)+gaoutL
gaoutR = a1*ipan+gaoutR

gainrev	=	    a1*irg+gainrev

endin 

/***********************************************************************
Simple soundfile player
***********************************************************************/
instr 103

ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
p3      =   nsamp(itab) * 0.00002268
iatt    =   p9
idecay = p10
ifiltType = p11-1
icutoff = p12

a1      loscil  iamp, ipit, itab, 1

if ifiltType != -1 then
acomp = a1
a1      bqrez   a1, icutoff, 6, ifiltType 
a1      balance     a1, acomp
endif

kenv   adsr     iatt, 0.05, .8, idecay

a1  =   a1*kenv

gaoutL = a1*(1-ipan)+gaoutL
gaoutR = a1*ipan+gaoutR

gainrev =	    a1*irg+gainrev

endin 

/******************************************************************** 
soundfile simple crossfade player 
********************************************************************/
instr 104

ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10

a1	 flooper2    1, ipit, .25, .750, .2, itab
a2      =   a1

kenv   adsr     iatt, 0.05, .8, idecay

gaoutL = a1*kenv*iamp*(1-ipan)+gaoutL
gaoutR = a2*kenv*iamp*ipan+gaoutR

gainrev	=       (a1+a2)*irg*kenv*.5*iamp+gainrev

endin 


/********************************************************************* 
simple karplus-strong plucked string 
*********************************************************************/
instr 105

p3      =   p3+1
ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10

icps    = 261.626 * ipit

a1      pluck   20000, icps, icps, 0, 5, .495, .495
a1      butterlp a1, 4000
a2      =   a1

kenv   adsr     iatt, 0.05, .8, idecay

gaoutL = a1*kenv*iamp*(1-ipan)+gaoutL
gaoutR = a2*kenv*iamp*ipan+gaoutR

gainrev =	    (a1+a2)*irg*kenv*.5*iamp+gainrev

endin 

/********************************************************************** 
FM synth instrument 
**********************************************************************/
instr 106

ipit    =   p4
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10

kModDev randomi 0.995, 1.005, .45
kFondDev    randomi 0.9962, 1.0029, .93
kvibrato    vibrato .5, 5, 0.08, 0.5, 3, 5, 3, 5, 1

iImin   =   2
iImax   =   4
iamp    =   3000
kfond   =   261.626 * ipit * kFondDev + kvibrato
kformant    =   800
kPortFreq   =   kfond * 3
kModFreq    =   kfond * 2 * kModDev
kModFreq2   =   kfond * 2.001 * kModDev
kPortFreq2  =   int((kformant/kPortFreq) + 0.5) * kfond

kenv1   expseg  0.001, .05, iamp, p3 - .15, iamp, .1, 0.001 
kenv2   oscil1i  0, kModFreq*(iImax-iImin), p3, 44

amod    oscili  iImin*kModFreq+kenv2, kModFreq, 1
amod2   oscili  iImin*kModFreq2+kenv2, kModFreq2, 1 

aport1  oscili  kenv1, kPortFreq+amod+amod2, 1
aport2  oscili  kenv1*0.5, kPortFreq2+(amod*0.33), 1

a1    =   aport1+aport2
a2      =   a1

kenv   adsr     iatt, 0.05, .8, idecay

gaoutL = a1*kenv*iamp*(1-ipan)+gaoutL
gaoutR = a2*kenv*iamp*ipan+gaoutR

gainrev =	    (a1+a2)*irg*kenv*iamp+gainrev

    endin

/********************************************************************** 
Waveshaping instrument 
**********************************************************************/
instr 107

ipit    =   p4 * 261.626
irg     =   p5
iamp = p6
ipan    =   p7
itab    =   p8
iatt    =   p9
idecay = p10

kvib	vibr	2, 5, 53
kamp	line	.42, p3, .1
kampdev	randi	.07, .5, .666

asig	oscili	kamp+kampdev, ipit+kvib, 50

a1	table	asig, 51, 1, .5
a1  balance a1, asig
a1 = a1*10000
a2      delay   a1, .041

kenv   adsr     iatt, 0.05, .8, idecay

gaoutL = a1*kenv*iamp*(1-ipan)+gaoutL
gaoutR = a2*kenv*iamp*ipan+gaoutR

gainrev =	    (a1+a2)*irg*kenv*iamp+gainrev

endin


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



/**************************************************************************
UDP receiver
**************************************************************************/

instr 256
gaudp1 = 0
gaudp2 = 0
a1 = 0
outs a1, a1
endin 

</CsInstruments>
<CsScore>
f1 0 8192 10 1
f40 0 1024 10 1 0  .5 0 0 .3  0 0 .2 0 .1 0 0 0 0 .2 0 0 0 .05 0 0 0 0 .03 ; ADDITIVE SYNTHESIS WAVE
f41 0 8193 19 .5 .5 270 .5 ; SIGMOID FUNCTION
f44 0 8192 5 1 8192 0.001 ; EXPONENTIAL FUNCTION
f50 0 8192 10 1 .1 .005 ; forme d'onde de l'index
f51 0 8192 13 1 1 0 1 .7 .8 .3 .1 .3 .4 .3 .2 0 0 .2 .1 0 .6 0 0 .5 .4 .3 0 0 .6 .7 ; premiere fonction de Chebichev
f52 0 4096 4 51 1 ; table de correction d'amplitude
f53 0 512 10 1 ; VIBRATO WAVE

i256 0 600000
i200 0 600000

</CsScore>
</CsoundSynthesizer>
