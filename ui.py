import streamlit as st
import streamlit_vertical_slider as svs
import numpy as np
import matplotlib.pyplot as plt
import librosa
import numpy as np
import matplotlib.pyplot as plt

import Audio_Files.functions as functions
import IPython.display as ipd
import scipy
import soundfile as sf


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


with st.sidebar:
    # upload,play = st.columns(2)
    st.session_state.uploaded_file = st.file_uploader("file")


st.header("equalizer")


if st.session_state.uploaded_file != None:

    st.session_state.not_enter = 1
    st.session_state.scale, sr = librosa.load(st.session_state.uploaded_file)
    st.session_state.freq_data = functions.fourier(st.session_state.scale)
    st.session_state.sr = sr
    time_plot = functions.get_time(st.session_state.scale, sr)
    st.session_state.fig1 = plot_fig(np.array(time_plot), np.array(
        time_plot), "time", "amp", "signal in time domain")
else:
    del st.session_state.uploaded_file
st.pyplot(st.session_state.fig1)
a = 0
columns = st.columns(2)
for column in columns:
    with column:
        a = svs.vertical_slider(key=f"slider{columns.index(column)}",
                                default_value=1,
                                step=1,
                                min_value=-100,
                                max_value=100,
                                thumb_color="#2481ce",
                                slider_color="#061724",
                                track_color="lightgray")

with st.sidebar:
    generate = st.button("generate")


if generate:
    a = st.session_state['slider0'] if st.session_state['slider0'] != None else 1
    orignal = functions.play(st.session_state.freq_data)

    f = functions.Instrument(st.session_state.freq_data.copy(
    ), a, 1)
    edited_Audio = functions.play(f)

    with st.sidebar:
        sf.write('signal.wav', edited_Audio.real, round(st.session_state.sr/2))
        st.audio('signal.wav', format="audio/wav", start_time=0)
