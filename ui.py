from numpy import exp, angle
import streamlit as st
import pandas as pd
import streamlit_vertical_slider as svs
import numpy as np
import matplotlib.pyplot as plt
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy import pi
from scipy.fftpack import fft, ifft
from scipy.io.wavfile import write


st.set_page_config(layout="wide")

# css modification
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def plot_fig(x, y, x_label, y_label, title):
    fig, ax = plt.subplots(figsize=(11, 4), constrained_layout=True)
    ax.plot(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    return fig


if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = 0
if "not_enter" not in st.session_state:
    st.session_state.not_enter = 0
if "fig1" not in st.session_state:
    st.session_state.fig1 = plot_fig(
        np.zeros(10), np.zeros(10), "x_label", "y_label", "graph")
if "fig2" not in st.session_state:
    st.session_state.fig2 = plot_fig(
        np.zeros(10), np.zeros(10), "x_label", "y_label", "graph")
if "frequency_list" not in st.session_state:
    st.session_state.frequency_list = []
if "freq_data" not in st.session_state:
    st.session_state.freq_data = [0]*30
if "time" not in st.session_state:
    st.session_state.time = []
if "sr" not in st.session_state:
    st.session_state.sr = 0
# if "fig2" not in st.session_state:
#     st.session_state.fig2 = plot_fig(np.zeros(10),np.zeros(10),"x_label","y_label","graph")
# if "fig3" not in st.session_state:
#     st.session_state.fig3 = plot_fig(np.zeros(10),np.zeros(10),"x_label","y_label","graph")
# if "fig4" not in st.session_state:
#     st.session_state.fig4 = plot_fig(np.zeros(10),np.zeros(10),"x_label","y_label","graph")


with st.sidebar:
    # upload,play = st.columns(2)
    st.session_state.uploaded_file = st.file_uploader("file")


st.header("equalizer")

# signal_view1 = st.columns(2)
# signal_view2 = st.columns(2)


if st.session_state.uploaded_file != None and st.session_state.not_enter == 0:

    st.session_state.not_enter = 1
    scale, sr = librosa.load(st.session_state.uploaded_file)
    st.session_state.sr = sr
    st.session_state.freq_data = fft(scale)
    st.session_state.fig1 = plot_fig(np.array(time_plot), np.array(
        scale_plot), "time", "amp", "signal in time domain")


st.plotly_chart(st.session_state.fig1)

columns = st.columns(1)
sliders = [0] * len(columns)
for i in range(len(columns)):
    with columns[i]:
        sliders[i] = {"name": "piano", "value": 1,
                      }
        sliders[i]['value'] = svs.vertical_slider(
            key=i, default_value=1, step=0.01, min_value=0, max_value=1)
        if sliders[i]['value'] == None:
            sliders[i]['value'] = 1
with st.sidebar:
    generate = st.button("generate")


# if generate:


with st.sidebar:
    st.audio(st.session_state.uploaded_file, format="audio/wav", start_time=0)
    st.audio("test.wav", format="audio/wav", start_time=0)
