import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt


def fourier(signal):
    n_samples = len(signal)
    f_hat = np.fft.fft(signal, n_samples)
    l = (len(f_hat)-2)//2
    f = f_hat[:l]
    return f


def get_time(scale, sr):
    return np.arange(0, len(scale)/sr, 1/sr)


def Instrument(f, piano_mag, guitar_mag):

    # piano
    print(piano_mag)
    f[301211: 303045] = f[301211: 303045] * piano_mag
    f[21211: 201211] = f[21211: 201211] * piano_mag

#   #guitar
    f[8211: 21211] = f[8211: 21211] * guitar_mag

    return f


def play(f):
    x = np.fft.ifft(f)
    return x
#   ipd.Audio(x,rate=round(sr/2))


def inverse_fourier(frequency_list):
    return np.fft.ifft(frequency_list)

def manipulate_vowels(freq, A_factor, Y_factor, V_factor, Ch_factor, Th_factor, S_factor, O_factor, R_factor, N_factor, D_factor):
    # A frequancies
    freq[31500:32700] *= A_factor
    freq[95000:96000] *= A_factor
    freq[110000:120000] *= A_factor

    # Y
    freq[20000:29000] *= Y_factor
    freq[36000:38000] *= Y_factor
    freq[92000:95000] *= Y_factor

    # V
    freq[29000:31500] *= V_factor
    freq[96000:99000] *= V_factor

    #Th
    freq[45700:49700] *= Th_factor

    #Ch
    freq[49700:54000] *= Ch_factor

    #S
    freq[56000:60000] *= S_factor
    freq[106400:109000] *= S_factor

    #O
    freq[54000:56000] *= O_factor
    freq[100800:102000] *= O_factor
    
    #R
    freq[33000:35500] *= R_factor
    freq[104400:106400] *= R_factor

    #N
    freq[80000:89000] *= N_factor
    freq[103000:104400] *= N_factor
    freq[113000:116000] *= N_factor

    #D
    freq[116000:119000] *= D_factor
    freq[35500:37500] *= D_factor
    freq[43000:49000] *= D_factor
    
