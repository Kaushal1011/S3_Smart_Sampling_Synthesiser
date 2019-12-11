#!/usr/bin/env python3
""" Utils Functions involving usage of DataFrame"""

from dependency import LinearRegression, np, pd
from S3SignalUtils import cos, sawtooth, sin, triangle


def create_FunctionFrame(fs: int, Ns: int, Ss: int) -> pd.DataFrame:
    """
    Takes Sampling Frequency and returns a DataFrame
    with function vectors of frequencies
    """

    FuncFrame = pd.DataFrame()
    # Made a dictionary with key as func name and value ad function object
    Functions = {
        "sin": sin,
        "cos": cos,
        # "triangle": triangle,
        # "sawtooth": sawtooth
    }

    # Iterated on dictionary items
    for i in Functions.items():
        for j in range(1, 41):
            FuncFrame[i[0] + str(j)] = i[1](j * fs, Ns, Ss)

    # Add 1 Column filled with noise to FuncFane without forgetting

    return FuncFrame


def train_S3(FuncFrame: pd.DataFrame, sig: np.ndarray) -> LinearRegression:
    """
    Function That trains FuncFrame on input signal

    Returns:
        LinearRegression
    """

    return LinearRegression().fit(FuncFrame, sig)


def predict_fs(fs: int, Ns: int, Ss: int, reg: LinearRegression) -> np.ndarray:
    """
    Returns predicted signal of given frequency
    Ss is sample rate
    Fs is natural frequency
    Ns is number of samples
    """

    FuncFrame = create_FunctionFrame(fs, Ns, Ss)
    return reg.predict(FuncFrame)
