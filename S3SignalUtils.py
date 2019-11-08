from S3Dependency import np,sp,pd,wavutils
"""Utils function related to signals for S3"""

def sigin(wavname:str)->[int,np.array]:
    """Functions that reads wave file and return sample rate and singal as np.array"""
    return wavutils.read(wavname,mmap=False)

def sawtooth(fs: int,Ns:int,Ss:int)->np.array:
    """Returns a Sawtooth wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    return sp.signal.sawtooth(2 * np.pi * fs * Ss)[0:Ns]

def triangle(fs:int,Ns:int,Ss:int)->np.array:
    """Returns a Triangle wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    return sp.signal.sawtooth(2 * np.pi * fs * Ss,0.5)[0:Ns]

def sin(fs:int,Ns:int,Ss:int)->np.array:
    """Returns a Sine wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    t=np.arange(Ns)
    omega=2*np.pi*fs/Ss
    return np.sin(omega*t)

def cos(fs:int,Ns:int,Ss:int)->np.array:
    """Returns a Cosine wave of Sample rate Ss with Ns number of samples and Sample Frequency Fs"""
    t=np.arange(Ns)
    omega=2*np.pi*fs/Ss
    return np.cos(omega*t)
