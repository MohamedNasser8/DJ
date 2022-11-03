import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt


def fourier(signal):
  n_samples=len(signal)
  f_hat=np.fft.fft(signal,n_samples)
  l = (len(f_hat)-2)//2
  f = f_hat[:l]

def Instrument(f, piano_mag, guitar_mag):
  #piano
  f[301211 : 303045] = f[301211 : 303045] * piano_mag
  f[21211 : 201211] = f[21211 : 201211] * piano_mag

  #guitar
  f[8211 : 21211] = f[8211 : 21211] * guitar_mag

def play(f,sr):
  x=np.fft.ifft(f)
  ipd.Audio(x,rate=round(sr/2))

def inverse_fourier(frequency_list):
    return np.fft.ifft(frequency_list)