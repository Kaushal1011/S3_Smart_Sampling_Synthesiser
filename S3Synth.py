#!/usr/bin/env python3
"""Synthesiser Class of S3"""

from dependency import LinearRegression, np, pd
from S3DataUtils import create_FunctionFrame, predict_fs
from S3SignalUtils import filt_bp, filt_hp, filt_lp


class S3Synth():
    """Main Synth Class that manages backend of Synthesiser"""
    def __init__(self, note_array: np.ndarray, reg: LinearRegression, Ns: int,
                 Ss: int):
        """sreates base signal dataframe"""
        self.note_sigs = pd.DataFrame()
        for i in range(8):
            for j in range(12):
                self.note_sigs[str(i) + str(j + 1)] = predict_fs(
                    note_array[i][j], Ns, Ss, reg)

    def filter_keyframe(self,
                        Ns: int,
                        Ss: int,
                        filter_type: str,
                        Cfs: int,
                        Cfs1=None,
                        order=5):
        """creates filtered signal datframe"""
        self.Filter_Options = {
            "LowPass": filt_lp,
            "HighPass": filt_hp,
            "BandPass": filt_bp
        }
        self.filtered_sigs = pd.DataFrame()
        for Name, Value in self.note_sigs.iteritems():
            self.filtered_sigs[Name] = self.Filter_Options[filter_type](Value,
                                                                        Ss,
                                                                        Cfs,
                                                                        Cfs1,
                                                                        order)

    def enveloped_keyframe(self):
        """creates enveloped signal dataframe"""
        pass
