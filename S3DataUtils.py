from S3Dependency import np, pd, LinearRegression
from S3SignalUtils import sin, cos, triangle, sawtooth

""" Utils Functions involving usage of DataFrame"""


def create_FunctionFrame(fs: int, Ns: int, Ss: int) -> pd.DataFrame:
    """Takes Sampling Frequency and returns a Data frame with function vectors of frequencies"""
    FuncFrame = pd.DataFrame()
    # Made a dictionary with key as func name and value ad function object
    Functions = {"sin": sin, "cos": cos,
                 "triangle": triangle, "sawtooth": sawtooth}

    # Iterated on dictionary items
    for i in Functions.items():
        for j in range(10):
            FuncFrame[i[0]+str(j)] = i[1](j*fs, Ns, Ss)

    # Add 1 Column filled with noise to FuncFane without forgetting

    return FuncFrame


def train_S3(FuncFrame: pd.DataFrame, sig: np.array) -> LinearRegression:
    """Function That trains FuncFrame on input signal (returns Class LinearRergession)"""
    reg = LinearRegression()
    reg.fit(FuncFrame, sig)
    return reg


def predict_fs(fs: int, Ns: int, Ss: int, reg: LinearRegression) -> np.array:
    """returns predicted signal of given frequency"""
    FuncFrame = create_FunctionFrame(fs, Ns, Ss)
    pred_sig = reg.predict(FuncFrame)
    return pred_sig
