#!/usr/bin/env python3
"""Utils function related to signals for S3"""

from typing import Tuple

import scipy.signal as sig

from dependency import np, wavutils


def sigin(wavname: str) -> Tuple[int, np.ndarray]:
    """Functions that reads wave file and return sample rate and signal as np.array"""
    return wavutils.read(wavname, mmap=False)


def sawtooth(fs: int, Ns: int, Ss: int) -> np.ndarray:
    """Returns a Sawtooth wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    Ss = np.linspace(0, 1, Ss)
    return sig.sawtooth(2 * np.pi * fs * Ss)[0:Ns]


def triangle(fs: int, Ns: int, Ss: int) -> np.ndarray:
    """Returns a Triangle wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    Ss = np.linspace(0, 1, Ss)
    return sig.sawtooth(2 * np.pi * fs * Ss, 0.5)[0:Ns]


def sin(fs: int, Ns: int, Ss: int) -> np.ndarray:
    """Returns a Sine wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    t = np.arange(Ns)
    omega = 2 * np.pi * fs / Ss
    return np.sin(omega * t)


def cos(fs: int, Ns: int, Ss: int) -> np.ndarray:
    """Returns a Cosine wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    t = np.arange(Ns)
    omega = 2 * np.pi * fs / Ss
    return np.cos(omega * t)

# Check tests3 in signals-systems to write these functions


def filt_lp(Cfs: int, sig: np.ndarray) -> np.ndarray:
    """return a filtered signal; low pass filter"""
    pass


def filt_hp(Cfs: int, sig: np.ndarray) -> np.ndarray:
    """return a filtered signal; high pass filter"""
    pass


def filt_bp(Cfs0: int, Cfs1: int, sig: np.ndarray) -> np.ndarray:
    """return a filtered signal; band pass filter"""
    pass


if __name__ == '__main__':
    from dependency import plt
    plt.plot(sin(100, 100, 100))
    plt.show()
