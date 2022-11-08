from flask import Flask, render_template, send_file, request,redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
import io
import librosa.display
import base64
from wtforms.validators import InputRequired
import librosa
from glob import glob
import soundfile as sf
import numpy as np
from PIL import Image
import functions
app = Flask(__name__)
from scipy.io import wavfile
app.config['SECRET_KEY'] = 'supersecretkey'

app.config['UPLOAD_FOLDER'] = "static/audio"
app.config["SECRET_KEY"] = "superkey"
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def processed(y):
    fourier = function.fourier(y)
    f = function.Instrument(fourier.copy(
    ), 1.1, 1)
    edited_Audio = function.play(f)
    return edited_Audio.real


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")




def get_sliders(n, names):
    dict_sliders = {}
    for i in range(n):
        dict_sliders[f"slider{i}"] = {"value": 0, "name": names[i]}
    return dict_sliders


@app.route('/', methods=['GET', "POST","put"])
@app.route('/music', methods=['GET', "POST","put"])
def music():
    n_of_sliders = 4
    dict_sliders = get_sliders(
        n_of_sliders, ["piano", "guitar", "vioin", "drums"])
    f = None
    # if request.method ==  "put":
    #     pass

    # if request.method == "PUT":
    #     f = request.files['file']
    #     path = os.path.join(app.config['UPLOAD_FOLDER'], "test.wav")
    #     f.save(path)

    if request.method == "POST" :
        for i in range(n_of_sliders):
            dict_sliders[f"slider{i}"]["value"] = request.form.get(
                f"slider{i}")
        f = request.files['file']
        if f.filename != "" :
            path = os.path.join(app.config['UPLOAD_FOLDER'], "test.wav")
            f.save(path)
        else:
            path = "static/audio/test.wav"
            
        scale, sr = librosa.load(path)


        # except:
        #     samplerate,  f = wavfile.read('static/audio/test.wav')
        #     path = "static/audio/test.wav"
        #     scale, sr = librosa.load(path)


        f = functions.fourier(scale)
        t = functions.get_time(scale, sr)
        scaleProcess = functions.split_music(f, dict_sliders)
        sf.write('static/audio/sig.wav', scaleProcess.real, round(sr/2))
        path1 = 'static/audio/sig.wav'
        return render_template('music.html', dict_values=dict_sliders, path=path, path1=path1, url="/")

    return render_template('music.html', dict_values=dict_sliders, path=None, path1=None, url="/")


@app.route('/ecg', methods=['GET', "POST"])
def ecg():
    n_of_sliders = 3
    dict_sliders = get_sliders(n_of_sliders, ["low", "mid", "high"])
    if request.method == "POST":
        for i in range(n_of_sliders):
            dict_sliders[f"slider{i}"]["value"] = request.form.get(
                f"slider{i}")
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)

        return render_template('ecg.html', dict_values=dict_sliders, path=path)

    return render_template('ecg.html', dict_values=dict_sliders, path=None)


@app.route('/vocals', methods=['GET', "POST"])
def vocals():
    n_of_sliders = 10
    dict_sliders = get_sliders(
        n_of_sliders, ["A", "B", "C", 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
    if request.method == "POST":
        for i in range(n_of_sliders):
            dict_sliders[f"slider{i}"]["value"] = request.form.get(
                f"slider{i}")
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        scale, sr = librosa.load(path)
        processed = functions.split_vowels(scale)
        print(len(scale), len(processed))
        sf.write('static/audio/vocal.wav', processed, round(sr))
        path1 = 'static/audio/vocal.wav'
        return render_template('vocals.html', dict_values=dict_sliders, path=path, path1=path1)

    return render_template('vocals.html', dict_values=dict_sliders, path=None, path1=None, url="vocals")


if __name__ == '__main__':
    app.run(debug=True)
