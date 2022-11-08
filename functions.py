import numpy as np


#-------------------------------------- Fourier/Inverse ------------------------------------------#
def fourier(signal):
    """
        Calculate fourier transform of the signal
        Parameters
        ----------
        signal : array of float
            signal points
        Return
        ----------
        f : array of complex
            fourier transform of the signal
    """
    n_samples = len(signal)
    f_hat = np.fft.fft(signal, n_samples)
    l = (len(f_hat)-2)//2
    f = f_hat[:l]
    return f


def inverse_fourier(frequency_list):
    """
        Calculate inverse fourier transform of the signal
        Parameters
        ----------
        frequency_list : array of float
            fourier transform of the signal
        Return
        ----------
        ifft : array of float
            inverse fourier transform of the signal
    """
    return np.fft.ifft(frequency_list)


#------------------------------------------ Time ----------------------------------------------#
def get_time(scale, sr):
    """
        Calculate the time of the signal using sampling rate
        Parameters
        ----------
        scale : array of float
            magnitude of the signal at each point
        sr : int
            number of sampling points per second
        Return
        ----------
        signal_time : array of float 
            time of the sampled signal
    """
    return np.arange(0, len(scale)/sr, 1/sr)


#---------------------------------------- Signal Spliters -----------------------------------------#

def split_arrhythmia(ecg_freq):
    """
        separate arithmia components
        Parameters
        ----------
        ecg_freq : array of complex
            arrithmia and normal components 

        Return
        ----------
        f_arrhythmia : array of complex 
        f_normal : array of complex 

    """
    artial_trachycardia = [0]*len(ecg_freq)
    artial_flutter = [0]*len(ecg_freq)
    artial_fibrillation = [0]*len(ecg_freq)
    # 230
    artial_trachycardia[220:240] = ecg_freq[220:240]
    # 300
    artial_flutter[290:310] = ecg_freq[290:310]
    # 350
    artial_fibrillation[340:360] = ecg_freq[340:360]

    f_normal = ecg_freq-artial_trachycardia-artial_flutter-artial_fibrillation

    return artial_trachycardia, artial_flutter, artial_fibrillation, f_normal


def split_music(music_freq, sliders):
    """
        separate music instruments
        Parameters
        ----------
        music_freq : array of complex
            array of music frequencies

        Return
        ----------
        f_piano : array of complex 
        f_guitar : array of complex 
        f_drums : array of complex 
        f_rest : array of complex 

    """
    f_piano = [0]*len(music_freq)
    f_guitar = [0]*len(music_freq)
    f_drums = [0]*len(music_freq)
    f_rest = [0]*len(music_freq)
    f_piano[301211: 303045] = music_freq[301211: 303045]
    f_piano[21211: 81211] = music_freq[21211: 81211]
    f_guitar[8211: 21211] = music_freq[8211: 21211]
    f_drums[100: 500] = music_freq[100: 500]

    f_rest = music_freq - f_piano - f_guitar
    return int(sliders["slider0"]["value"])*inverse_fourier(f_piano).real + int(sliders["slider1"]["value"])*inverse_fourier(f_guitar).real + int(sliders["slider2"]["value"])*inverse_fourier(f_drums).real + int(sliders["slider3"]["value"])*inverse_fourier(f_rest).real


def split_vowels(audio_freq, sliders):
    """
        separate audio vowels
        Parameters
        ----------
        audio_freq : array of complex
            array of Audio frequencies

        Return
        ----------
        f_A : Vowel A components
        f_Y : Vowel Y components
        f_V : Vowel V components
        f_th : Vowel Th components
        f_ch : Vowel Ch components
        f_s : Vowel S components
        f_o : Vowel O components
        f_r : Vowel R components
        f_n : Vowel N components
        f_d : Vowel D components
        f_rest : Vowel the other components

    """
    print(sliders)
# inizialization of components arrays
    f_A = [0]*len(audio_freq)
    f_Y = [0]*len(audio_freq)
    f_V = [0]*len(audio_freq)
    f_th = [0]*len(audio_freq)
    f_ch = [0]*len(audio_freq)
    f_s = [0]*len(audio_freq)
    f_o = [0]*len(audio_freq)
    f_r = [0]*len(audio_freq)
    f_n = [0]*len(audio_freq)
    f_d = [0]*len(audio_freq)

    # A
    f_A[31500:32700] = audio_freq[31500:32700]
    f_A[95000:96000] = audio_freq[95000:96000]
    f_A[110000:120000] = audio_freq[110000:120000]

    # Y
    f_Y[20000:29000] = audio_freq[20000:29000]
    f_Y[36000:38000] = audio_freq[36000:38000]
    f_Y[92000:95000] = audio_freq[92000:95000]

    # V
    f_V[29000:31500] = audio_freq[29000:31500]
    f_V[96000:99000] = audio_freq[96000:99000]

    # Th
    f_th[45700:49700] = audio_freq[45700:49700]

    # Ch
    f_ch[49700:54000] = audio_freq[49700:54000]

    # S
    f_s[56000:60000] = audio_freq[56000:60000]
    f_s[106400:109000] = audio_freq[106400:109000]

    # O
    f_o[54000:56000] = audio_freq[54000:56000]
    f_o[100800:102000] = audio_freq[100800:102000]

    # R
    f_r[33000:35500] = audio_freq[33000:35500]
    f_r[104400:106400] = audio_freq[104400:106400]

    # N
    f_n[80000:89000] = audio_freq[80000:89000]
    f_n[103000:104400] = audio_freq[103000:104400]
    f_n[113000:116000] = audio_freq[113000:116000]

    # D
    f_d[116000:119000] = audio_freq[116000:119000]
    f_d[35500:37500] = audio_freq[35500:37500]
    f_d[43000:49000] = audio_freq[43000:49000]

    f_rest = audio_freq - f_r - f_A - f_ch - f_d - \
        f_n - f_Y - f_th - f_o - f_n - f_s - f_V
    return np.add(f_A,  np.add(f_Y, np.add(f_V, np.add(f_th, np.add(f_ch, np.add(f_s, np.add(f_o, np.add(f_r, np.add(f_n, np.add(f_d, f_rest))))))))))
