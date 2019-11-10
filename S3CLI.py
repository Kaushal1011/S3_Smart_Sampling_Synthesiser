from dependency import np, sp, pd
from S3Synth import S3Synth
from S3Synth import envelope
import keyboard


class S3CLI:
    """Class to manage CLI interface of S3 Synthesiser """

    def __init__(self, s3: S3Synth):
        self.s3 = s3
        self.routed_sig = s3.enveloped_keyframe
        self.env = self.get_envelope()

    def get_envelope(self):
        """creates instance of class envelope from user and returns it"""
        env = envelope()
        return env
