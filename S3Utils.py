#!/usr/bin/env python3
"""Utils Functions for S3 Synthesiser App"""

from typing import Tuple

from dependency import np


def freq_calc(sig: np.ndarray) -> float:
    """Calculates the average frequency of the input signal (of a recorded note)"""
    rep = 0
    for i in range(len(sig) - 1):
        if sig[i + 1] >= 0 and sig[i] <= 0:
            rep += 1
    return len(sig) / rep


def make_octaves() -> np.ndarray:
    """Creates Octaves with their corresponding frequncy"""
    A4_octave = [130.81278265]  # Value of C4
    for _ in range(11):
        A4_octave.append(A4_octave[-1] * 2**(1 / 12))
    A4_octave = np.array(A4_octave)
    return np.array([
        A4_octave / 8, A4_octave / 4, A4_octave / 2, A4_octave, A4_octave * 2,
        A4_octave * 4, A4_octave * 8, A4_octave * 16
    ])


def get_note(freq: float) -> Tuple[float, str]:
    """
    Returns the Note (and its Natural Frequency)
    corresponding to input frequency
    """
    pass


def create_partial_envelope(sig: np.ndarray) -> Tuple[list, list]:
    """
    Creates a partial envelope using min and max of in one cycle.
    Shift this functiong to np.array soon
    """

    max_val = []
    min_val = []
    for i in range(0, len(sig), 44):
        max_val.append(max(sig[i:i + 43]))
        min_val.append(min(sig[i:i + 43]))
    return (max_val, min_val)


def make_natural_env(max_val: np.ndarray, min_val: np.ndarray) -> np.ndarray:
    """
    Returns an envelope in natural time for the
    signal by upsampling and uniforming partial envelope
    """
    pass


def find_Ns(Freq: float, Ss: int) -> int:
    return Ss // Freq + 1
