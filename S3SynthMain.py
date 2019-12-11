#!/usr/bin/env python3

# import keyboard
from dependency import np, pd, sp
from S3Synth import S3Synth
from S3Utils import freq_calc, find_Ns, get_note, find_maxsig, make_octaves, freq_from_HPS,freq_from_autocorr,freq_from_autocorr,freq_from_crossings,freq_from_fft
from S3DataUtils import train_S3, create_FunctionFrame
from matplotlib import pyplot as plt
# from scipy.io.wavfile import write
from pyo import Server


class S3App:
    """Class to manage  interface of S3 Synthesiser """
    def __init__(self):
        pass

    def load_file(self, file_path: str):
        """Loads a Sample into the synthesiser"""
        self.Ss, self.wave = sp.io.wavfile.read(file_path, mmap=False)
        self.wave=np.array(self.wave[:, 0])
        plt.plot(self.wave[:])
        plt.show()
        print("Enter indexes in which wave is sustained")
        a=input()
        b=input()
        self.waves=self.wave[int(a):int(b)]


    def load_trainedsynth(self):
        """Loads all properties of S3 trains S3 and initialises S3Synth"""

        freq = freq_calc(self.waves, self.Ss)
        freq1= freq_from_HPS(self.waves,self.Ss)
        freq2= freq_from_autocorr(self.waves,self.Ss)
        freq3 = freq_from_fft(self.waves,self.Ss)
        freq4 = freq_from_crossings(self.waves,self.Ss)
        print("freq ",freq3,"freqfft ",freq3,"freqautocorr ",freq2,"freqhps ",freq1,"freqcross ",freq4)
        self.Ss = int(self.Ss)
        print("Enter Frequency")
        fs=float(input())
        self.freq, self.note = get_note(fs)
        self.Ns = int(find_Ns(self.freq, self.Ss))
        self.Fs = float(fs)
        print(freq, self.Ns, self.Ss, self.note)
        self.waves = self.waves/max(self.waves)

        # print(self.env.Ns)
        func_frame = create_FunctionFrame(self.Fs, len(self.waves), self.Ss)
        print(func_frame.shape)
        self.reg = train_S3(func_frame, self.waves)
        print(self.reg.score(func_frame, self.waves))





def main():
    kaypee = S3App()
    kaypee.load_file('Samples/PianoDiff.wav')
    kaypee.load_trainedsynth()
    s = Server()
    s.setMidiInputDevice(99) # Open all input devices.
    s.boot()

    Synthesiser=S3Synth(kaypee.reg.coef_)
    a=Synthesiser.out()
    s.gui(locals())
if __name__ == '__main__':
    main()
