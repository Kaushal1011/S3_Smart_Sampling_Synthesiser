#!/usr/bin/env python3
"""Utils Functions for S3 Synthesiser App"""
from __future__ import division
from typing import Tuple

from scipy.interpolate import interp1d

from dependency import np

from numpy.fft import rfft
from numpy import argmax, mean, diff, log, nonzero
from scipy.signal import  correlate
from scipy import signal
from time import time
import sys
import soundfile as sf

from parabolic import parabolic


def freq_calc(sig: np.ndarray, Ss: int) -> float:
    """Calculates the average frequency of the input signal (of a recorded note)"""
    rep = 0
    for i in range(len(sig)-1):
        if sig[i + 1] >= 0 and sig[i] <= 0:
            rep += 1
    return Ss / (len(sig) / (3 * rep))


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
    if freq < 30.0:
        raise ValueError(f'{freq} Hz too low')

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
    else:
        raise ValueError(f'{freq} Hz too high')


def create_partial_envelope(sig: np.ndarray, Fs: int, Ss: int) -> np.ndarray:
    """
    Creates a partial envelope using min and max of in one cycle.
    """

    max_val = []
    # min_val = []
    for i in range(0, len(sig), 1 + (Ss // Fs)):
        max_val.append(max(sig[i:i + Ss // Fs]))
        # min_val.append(min(sig[i:i + Ss//Fs]))
    return np.array(max_val)


def make_natural_env(env: np.ndarray, Ns: int) -> np.ndarray:
    """
    Returns an envelope in natural time for the
    signal by upsampling and uniforming partial envelope
    """
    divs = (Ns // len(env))
    y = np.zeros(Ns)
    for i in range(len(env) - 1):
        y[i * divs:divs * (i + 1)] = np.linspace(env[i], env[i + 1], num=divs)
    return y


def create_env(sig: np.ndarray, Fs: int, Ss: int, Ns: int) -> np.ndarray:
    """return envelope of signal"""
    return make_natural_env(create_partial_envelope(sig, Fs, Ss), Ns)


def find_Ns(Freq: float, Ss: int) -> int:
    """Finds the Ns for Training Phase"""
    return 4 * ((Ss // Freq) + 1)


def find_maxsig(sig: np.ndarray, Ns: int) -> np.ndarray:
    """returns part of signal where its in constant sustain"""
    min1 = 10e9
    sig_ret = np.array(sig[0:Ns])
    for i in range(1, len(sig) // Ns):
        # print(i)
        if (32768 - np.max(sig[i * Ns:(i + 1) * Ns])) < min1:
            min1 = (32768 - np.max(sig[i * Ns:(i + 1) * Ns]))
            sig_ret = sig[i * Ns:(i + 1) * Ns]

    return sig_ret

def freq_from_crossings(sig, fs):
    """
    Estimate frequency by counting zero crossings
    """
    # Find all indices right before a rising-edge zero crossing
    indices = nonzero((sig[1:] >= 0) & (sig[:-1] < 0))[0]

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    # crossings = indices

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever

    return fs / mean(diff(crossings))


def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * signal.blackmanharris(len(sig))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic(log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation and throw away the negative lags
    corr = correlate(sig, sig, mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = diff(corr)
    start = nonzero(d > 0)[0][0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px


def freq_from_HPS(sig, fs):
    """
    Estimate frequency using harmonic product spectrum (HPS)
    """
    windowed = sig * signal.blackmanharris(len(sig))

    from pylab import subplot, plot, log, copy, show

    # harmonic product spectrum:
    c = abs(rfft(windowed))
    maxharms = 4
    # subplot(maxharms, 1, 1)
    # plot(log(c))
    for x in range(2, maxharms):
        a = copy(c[::x])  # Should average or maximum instead of decimating
        # max(c[::x],c[1::x],c[2::x],...)
        c = c[:len(a)]
        i = argmax(abs(c))
        true_i = parabolic(abs(c), i)[0]
        print('Pass %d: %f Hz' % (x, fs * true_i / len(windowed)))
        c *= a
        # subplot(maxharms, 1, x)
        # plot(log(c))
    # show()
    return fs * true_i / len(windowed)





if __name__ == '__main__':
    print(get_note(235))
