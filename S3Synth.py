#!/usr/bin/env python3
"""Synthesiser Class of S3"""

from dependency import LinearRegression, np, pd
from pyo import Server,STRev,Sig, Chorus, Mix, Follower, MidiAdsr, Adsr, SfPlayer,Selector,Notein,EQ,HarmTable, Osc,Spectrum,Scope


class S3Synth:
    """Main Synth Class that manages backend of Synthesiser"""

    def __init__(self,wavecoef_:np.ndarray, transpo=1, mul=1):
        
       
        # Transposition factor.
        
        self.transpo = Sig(transpo)
        # Receive midi notes, convert pitch to Hz and manage 10 voices of polyphony.
        self.note = Notein(poly=10, scale=1, first=0, last=127)
        self.note.keyboard()
        # Handle pitch and velocity (Notein outputs normalized amplitude (0 -> 1)).
        self.pit = self.note['pitch'] * self.transpo
        print(self.note.get('pitch'))
        self.amp = MidiAdsr(0.5*self.note['velocity'], attack=0.1,
                            decay=1, sustain=.5, release=2, mul=.1)
        self.amp.ctrl(title="Envelope Control")
        # Anti-aliased stereo square waves, mixed from 10 streams to 1 stream
        # to avoid channel alternation on new notes.
        self.t=HarmTable(list(wavecoef_[0:20]))
#         self.t.graph()
        self.t2=HarmTable(list(wavecoef_[20:39]))
#         self.t2.graph()
        self.osc1 = Osc(table=self.t,freq=self.pit, mul=0.4*self.amp)
        
        # self.osc1.ctrl(title="Osc1")
        self.osc2 = Osc(table=self.t2,freq=self.pit,phase=0.25 , mul=0.4*self.amp)
        # self.osc2.ctrl()
        # Stereo mix.
        self.mix = Mix([self.osc1.mix(1),self.osc2.mix(1)] ,voices=4)
        
        self.scope=Scope(self.mix)

        self.eq=EQ(self.mix)
        self.eq.ctrl(title="Equaliser")
        self.spec=Spectrum(self.eq,size=512,wintitle='Spectrum')

        self.chor=Chorus(self.eq)
        self.chor.ctrl()

        self.rev=STRev(self.eq)
        self.rev.ctrl()

        self.sel=Selector([self.rev,self.chor],1)
        self.sel.ctrl(title="Chorus vs Reverb") 
        self.final=Mix(self.sel,voices=2,mul=1)


    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
#         self.notch.out()
        self.sel.out()
        return self

    def sig(self):
        "Returns the synth's signal for future processing."
        return self.sel


   
    

