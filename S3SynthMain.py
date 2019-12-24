#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pyo import Server
from mido import MidiFile
from dependency import np, pd, sp
from S3DataUtils import create_FunctionFrame, train_S3
from S3Synth import S3Synth
from S3Utils import (find_maxsig, find_Ns, freq_calc, freq_from_autocorr,
                     freq_from_crossings, freq_from_fft, freq_from_HPS,
                     get_note, make_octaves)


class S3App:
    """Class to manage  interface of S3 Synthesiser """
    def __init__(self):
        pass

    def load_file(self, file_path: str):
        """Loads a Sample into the synthesiser"""

        self.Ss, self.wave = sp.io.wavfile.read(file_path, mmap=False)
        if len(self.wave.shape) == 2:
            self.wave = np.array(self.wave[:, 0])
        plt.plot(self.wave[:])
        plt.show()

        print("Enter indexes in which wave is sustained")
        a = input('Lower index: ')
        b = input('Upper index: ')
        self.waves = self.wave[int(a):int(b)] / max(self.wave)

    def load_trainedsynth(self):
        """Loads all properties of S3 trains S3 and initialises S3Synth"""

        freq = freq_calc(self.waves, self.Ss)
        freq1 = freq_from_HPS(self.waves, self.Ss)
        freq2 = freq_from_autocorr(self.waves, self.Ss)
        freq3 = freq_from_fft(self.waves, self.Ss)
        # freq4 = freq_from_crossings(self.waves, self.Ss)
        print()
        print("freq ", freq3)
        print("freqfft ", freq3)
        print("freqautocorr ", freq2)
        print("freqhps ", freq1)
        print("freqcross ", freq)
        self.Ss = int(self.Ss)
        fs = float(input('Enter frequency: '))
        self.freq, self.note = get_note(fs)
        self.Ns = int(find_Ns(self.freq, self.Ss))
        self.Fs = float(fs)
        print(freq, self.Ns, self.Ss, self.note)
        self.waves = self.waves / max(self.waves)

        # Creates a matrix of 40 sine harmonics vectors and
        # 40 cosine harmonic vectors and trains it using input waveform
        func_frame = create_FunctionFrame(self.Fs, len(self.waves), self.Ss)
        print(func_frame.shape)
        self.reg = train_S3(func_frame, self.waves)
        print(self.reg.score(func_frame, self.waves))



def main():
    '''Driver code'''

    app = S3App()
    app.load_file(input('Enter filename: '))
    app.load_trainedsynth()
    s = Server()
    s.setMidiInputDevice(99)  # Open all input devices.
    s.boot()
    def play_midi(filename:str):
        mid = MidiFile(filename)

    # ... and reading its content.
        for message in mid.play():
            # For each message, we convert it to integer data with the bytes()
            # method and send the values to pyo's Server with the addMidiEvent()
            # method. This method programmatically adds a MIDI message to the
            # server's internal MIDI event buffer.
            s.addMidiEvent(*message.bytes())

    Synthesiser = S3Synth(app.reg.coef_)
    a = Synthesiser.out()
    s.gui(locals())


if __name__ == '__main__':
    main()
