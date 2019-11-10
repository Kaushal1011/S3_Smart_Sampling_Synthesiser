#!/usr/bin/env python3

import keyboard
from dependency import np, pd, sp
from S3Synth import S3Synth, envelope


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
