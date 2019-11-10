#!/usr/bin/env python3
"""Function related to playing audio on key press using S3Synth Instance"""

from dependency import np
import sounddevice as sd


def play_note(note: np.ndarray, Ss: int, Dur=5.0) -> None:
    """
    Function that uses Sound device to play note at Ss no. samples per second
    for max duration 5.0S (To be added later)
    """
    sd.play(note, Ss)
