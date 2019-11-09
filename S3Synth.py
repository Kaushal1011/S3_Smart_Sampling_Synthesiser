from dependency import np, pd, LinearRegression
from S3DataUtils import create_FunctionFrame, predict_fs
from S3SignalUtils import filt_hp, filt_lp
"""Synthesiser Class of S3"""


class S3Synth():
    """Main Synth Class that manages backend of Synthesiser"""

    def __init__(self, note_array: np.ndarray, reg: LinearRegression, Ns: int, Ss: int):
        """sreates base signal dataframe"""
        self.note_sigs = pd.DataFrame()
        for i in range(8):
            for j in range(12):
                self.note_sigs[str(i)+str(j+1)
                               ] = predict_fs(note_array[i][j], Ns, Ss, reg)

    def filter_keyframe(self):
        """creates filtered signal datframe"""
        pass

    def enveloped_keyframe(self):
        """creates enveloped signal dataframe"""
        pass
