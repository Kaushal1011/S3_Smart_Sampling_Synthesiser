#!/usr/bin/env python3
"""Synthesiser Class of S3"""

from dependency import LinearRegression, np, pd
from pyo import Server,Sine,STRev,Chorus,Mix,Follower,MidiAdsr,Adsr

class S3Synth:
    """Main Synth Class that manages backend of Synthesiser"""
    def __init__(self,filename:str,wavecoef_:np.ndarray):
        pass