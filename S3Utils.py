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
    """Creates Octaves with their corresponding frequency"""
    C4_octave = [261.62556530059874]  # Value of C4
    for _ in range(11):
        C4_octave.append(C4_octave[-1] * 2**(1 / 12))
    C4_octave = np.array(C4_octave)
    return np.array([
        C4_octave / 8, C4_octave / 4, C4_octave / 2, C4_octave, C4_octave * 2,
        C4_octave * 4, C4_octave * 8, C4_octave * 16
    ])


def get_note(freq: float) -> Tuple[float, str]:
    """
    Returns the Note (and its Natural Frequency)
    corresponding to input frequency
    """
    f = []
    FREQ = make_octaves()
    for i in FREQ:
        f.extend(i)

    notes = ('C', 'C\u266f-D\u266d', 'D', 'D\u266f-E\u266d', 'E', 'F',
             'F\u266f-G\u266d', 'G', 'G\u266f-A\u266d', 'A', 'A\u266f-B\u266d',
             'B')

    for i in enumerate(f):
        if freq < i[1]:
            note = (f[i[0] - 1], f[i[0]])
            y = divmod(i[0], 12)
            mid = (note[0] + note[1]) / 2
            if freq < mid:
                return note[0], '{} {}'.format(notes[y[1] - 1], y[0] + 1)

            return note[1], '{} {}'.format(notes[y[1]], y[0] + 1)


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


if __name__ == '__main__':
    print(get_note(438))
