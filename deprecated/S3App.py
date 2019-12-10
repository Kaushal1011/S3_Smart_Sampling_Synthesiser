#!/usr/bin/env python3

# import keyboard
from dependency import np, pd, sp
# from S3Synth import S3Synth, Envelope
from S3Utils import freq_calc, find_Ns, get_note, find_maxsig, make_octaves
from S3DataUtils import train_S3, create_FunctionFrame
from matplotlib import pyplot as plt
from scipy.io.wavfile import write


class S3App:
    """Class to manage  interface of S3 Synthesiser """
    def __init__(self):
        pass

    def load_file(self, file_path: str):
        """Loads a Sample into the synthesiser"""
        self.Ss, self.wave = sp.io.wavfile.read(file_path, mmap=False)
        # self.wave=np.array(self.wave[:, 0])

    def load_trainedsynth(self):
        """Loads all properties of S3 trains S3 and initialises S3Synth"""
        
        freq = freq_calc(self.wave, self.Ss)
        self.Ss = int(self.Ss)
        self.freq, self.note = get_note(freq)
        self.Ns = int(find_Ns(self.freq, self.Ss))
        self.Fs = int(freq)
        print(freq, self.Ns, self.Ss, self.note)
        self.wave_sampled = find_maxsig(self.wave, self.Ns)
        
        print(self.env.Ns)
        func_frame = create_FunctionFrame(self.Fs, self.Ns, self.Ss)
        self.reg = train_S3(func_frame, self.wave_sampled)
        print(self.reg.score(func_frame, self.wave_sampled))
        

    


def main():
    kaypee = S3App()
    kaypee.load_file('flute1.wav')
    kaypee.load_trainedsynth()

    # play_note(kaypee.s3.env_sigs['51'], kaypee.Ss)
    # # play_note(kaypee.wave,kaypee.Ss)
    # write('violin2.wav', kaypee.Ss, kaypee.s3.env_sigs['51'])
    # print(kaypee.s3.env_sigs['51'].shape)
    # plt.plot(kaypee.s3.env_sigs['51'][10000:10100])
    # plt.show()


if __name__ == '__main__':
    main()
