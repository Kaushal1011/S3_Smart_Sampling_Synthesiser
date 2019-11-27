#!/usr/bin/env python3

import keyboard
from dependency import np, pd, sp
from S3Synth import S3Synth, Envelope
from S3Utils import freq_calc,find_Ns,get_note,find_maxsig,make_octaves
from S3DataUtils import train_S3,create_FunctionFrame

class S3App:
    """Class to manage  interface of S3 Synthesiser """
    def __init__(self):
        pass

    def load_file(self,file_path:str):
        """Loads a Sample into the synthesiser"""
        self.Ss,self.wave=sp.io.wavfile.read('flute1.wav', mmap=False)

    def load_properties(self):
        """Loads all properties of S3App"""
        freq=freq_calc(self.wave)
        self.note,self.freq=get_note(freq)
        self.Ns=find_Ns(self.freq,self.Ss)
        self.Fs=self.freq
        self.wave_sampled=find_maxsig(self.wave,self.Ns)
        self.env=Envelope(self.wave,self.Fs,len(self.wave),self.Ss)
        func_frame=create_FunctionFrame(self.Fs,self.Ns,self.Ss)
        self.reg=train_S3(func_frame,self.wave_sampled)
        self.s3=S3Synth(make_octaves(),self.reg,self.Ns,self.Ss)
        


