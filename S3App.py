#!/usr/bin/env python3

import keyboard
from dependency import np, pd, sp
from S3Synth import S3Synth, Envelope


class S3App:
    """Class to manage  interface of S3 Synthesiser """

    def __init__(self, s3: S3Synth):
        self.s3 = s3
        self.routed_sig = s3.env_sigs