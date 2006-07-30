###############
# Game - Memory
###############

Files: 
       memory.py: The game itself.	
       alphasound.memory: The definition of the pool of pictures and songs(soundfiles) placed in the 
			  folders pics and audio.
       universe.py: The csound server waiting on port 40002 for requests.
       univorc.csd: Definition of the csound orchestra and score.
       basic.instruments: The definition of the soundfile player instrument. This file is included in 'univorc.csd'.
       csnd.py, _csnd.so: Shared csound library with python bindings.

