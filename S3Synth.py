#!/usr/bin/env python3
"""Synthesiser Class of S3"""

from dependency import LinearRegression, np, pd
from pyo import Server,Harmonizer,Disto,ButLP,ButBR,Linseg,Sine,Biquad,LFO,STRev,Sig, Chorus, Mix, Follower, MidiAdsr, Adsr, SfPlayer,Selector,Notein,EQ,HarmTable, Osc,Spectrum,Scope
from random import random

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
                            decay=1, sustain=.5, release=2, mul=.4)
        self.amp.ctrl(title="Envelope Control")
        # Anti-aliased stereo square waves, mixed from 10 streams to 1 stream
        # to avoid channel alternation on new notes.

        self.t=HarmTable(list(wavecoef_[0:20]))
#         self.t.graph()
        self.t2=HarmTable(list(wavecoef_[20:39]))
#         self.t2.graph()
        self.osc1 = Osc(table=self.t,freq=self.pit, mul=self.amp)


        # self.osc1.ctrl(title="Osc1")

        self.osc2 = Osc(table=self.t2,freq=self.pit,phase=0.25 , mul=self.amp)
        # self.osc2.ctrl()
        # Stereo mix.
        self.osc3 = LFO(self.pit, sharp=0.5, type=2, mul=self.amp)
        self.osc3.ctrl(title="Osc3 type 0=saw u 1=saw d 2=sq 3=tri 4=pulse 5=bipulse 6=s&h 7=Sine")


        self.osc4 = LFO(self.pit, sharp=0.5, type=2, mul=self.amp)
        self.osc4.ctrl(title="Osc3 type 0=saw u 1=saw d 2=sq 3=tri 4=pulse 5=bipulse 6=s&h 7=Sine")



        self.extrasel=Selector([self.osc3.mix(1),self.osc4.mix(1)],mul=0,voice=0.5)
        self.mainsel=Selector([self.osc1.mix(1),self.osc2.mix(1)],mul=1,voice=0.5)
        self.mainsel.ctrl(title="Main Oscillator Volume")
        self.extrasel.ctrl(title="Extra Oscillator Volume Ctrl")
        # self.extra=Mix(self.osc3.mix(1),self.osc4.mix(1),voices=2)

        self.mix = Mix([self.mainsel.mix(1),self.extrasel.mix(1)] ,voices=2)
        # self.mix = Mix([self.osc1, self.osc2], voices=2)

        # High frequencies damping.
        self.damp = ButLP(self.mix, freq=5000)

        # Moving notches, using two out-of-phase sine wave oscillators.
        self.lfo = Sine(.2, phase=[random(), random()]).range(250, 4000)
        self.lfo.ctrl(title=" Modulation")
        self.notch = ButBR(self.damp, self.lfo, mul=mul)

        self.scope=Scope(self.notch)

        self.eq=Biquad(self.notch,freq=20000)
        self.eq.ctrl(title="Equaliser type 0=lp 1=hp 2=bp 3=br 4=ap")
        self.spec=Spectrum(self.eq,size=512,wintitle='Spectrum')
        self.harmonized=Harmonizer(self.eq,mul=0)
        self.harmonized.ctrl()
        self.distortion=Disto(self.eq,drive=0)
        self.distortion.ctrl()
        self.pfx=Mix([self.distortion,self.harmonized],voices=2)


        self.chor=Chorus(self.pfx)
        self.chor.ctrl()

        self.rev=STRev(self.pfx)
        self.rev.ctrl()

        self.sel=Selector([self.rev,self.chor],0.5)
        self.sel.ctrl(title="Chorus vs Reverb")
        self.final=Mix(self.sel,voices=2,mul=1)


    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
#         self.notch.out()
        self.final.out()
        return self

    def sig(self):
        "Returns the synth's signal for future processing."
        return self.sel
