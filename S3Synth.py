#!/usr/bin/env python3
"""Synthesiser Class of S3"""

from dependency import LinearRegression, np, pd
from S3DataUtils import create_FunctionFrame, predict_fs
from S3SignalUtils import filt_bp, filt_hp, filt_lp
from S3Utils import create_env


class Envelope:
    def __init__(self, sig: np.ndarray, Fs: int, Ns: int, Ss: int):
        self.init_env = create_env(sig, Fs, Ss, Ns)
        self.env = self.init_env
        self.Ns=Ns

    def create_env_s3(self, initalenv: np.ndarray, Ns: int):
        self.env=initalenv

class S3Synth:
    """Main Synth Class that manages backend of Synthesiser"""
    Ss = 0
    Ns = 0

    def __init__(self, note_array: np.ndarray, reg: LinearRegression, Ns: int,
                 Ss: int):
        """creates base signal dataframe"""
        self.Ns = Ns
        self.Ss = Ss
        self.note_sigs = pd.DataFrame()
        for i in range(8):
            for j in range(12):
                self.note_sigs[str(i) + str(j + 1)] = predict_fs(
                    note_array[i][j], Ns, Ss, reg)
        self.filtered_sigs=self.note_sigs
        # self.env_sigs=self.note_sigs

    def filter_keyframe(self,
                        filter_type: str,
                        Cfs: int,
                        Cfs1=None,
                        order=5,
                        Ns1=Ns,
                        Ss1=Ss):
        """creates filtered signal datframe"""
        self.Filter_Options = {
            "LowPass": filt_lp,
            "HighPass": filt_hp,
            "BandPass": filt_bp
        }
        self.filtered_sigs = pd.DataFrame()
        for Name, Value in self.note_sigs.iteritems():
            self.filtered_sigs[Name] = self.Filter_Options[filter_type](Value,
                                                                        Ss1,
                                                                        Cfs,
                                                                        Cfs1,
                                                                        order)

    def enveloped_keyframe(self, env: Envelope):
        """creates enveloped signal dataframe"""
        self.env_sigs = pd.DataFrame()
        reps=env.Ns//self.Ns
        for Name, Value in self.filtered_sigs.iteritems():
            self.env_sigs[Name]=np.tile(Value/max(Value),reps) * env.env[0:self.Ns*reps]
        # for i in range(1,reps-1):
        #     for Name, Value in self.filtered_sigs.iteritems():
        #         self.env_sigs[Name].append(Value * env.env[i*self.Ns:(i+1)*self.Ns],ignore_index=True)

    def initialise_frames(self,
                          filter_type: str,
                          Cfs: int,
                          Cfs1=None):
        """intialises all data frames from base frame: run when filter parameters are changed"""
        self.filter_keyframe(filter_type, Cfs, Cfs1)
        
    def changed_filter(self,filter_type:str,env:Envelope,Cfs:int,Cfs1=None):
        self.initialise_frames(filter_type,Cfs,Cfs1)
        self.enveloped_keyframe(env)
    
    def changed_env(self,env:Envelope):
        self.enveloped_keyframe(env)

    # def initilise_env(self, env: Envelope):
    #     """intialises envelope frame from filtered key frame: run when envelope parameters are changed """
    #     self.enveloped_keyframe(env)
