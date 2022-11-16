from scipy.io import wavfile
from flask import Flask, render_template, send_file, request, redirect
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
import Audio_Files.functions as functions
app = Flask(__name__)
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


@app.route('/', methods=['GET', "POST", "put"])
def music():
    dict_sliders = {}
    if request.method == "POST":
        n_of_sliders = int(request.form.get("num_sliders"))
        for i in range(n_of_sliders):
            dict_sliders[f"slider{i}"] = request.form.get(
                f"slider{i}")
        f = request.files['file']
        if f.filename != "":
            path = os.path.join(app.config['UPLOAD_FOLDER'], "test.wav")
            f.save(path)
        else:
            path = "static/audio/test.wav"

        scale, sr = librosa.load(path)
        f = functions.fourier(scale)
        t = functions.get_time(scale, sr)
        if n_of_sliders == 3:
            scaleProcess = functions.split_arrhythmia(f, dict_sliders)
            sf.write('static/audio/sig.wav', scaleProcess.real, round(sr/2))
        elif n_of_sliders == 4:
            scaleProcess = functions.split_music(f, dict_sliders)
            sf.write('static/audio/sig.wav', scaleProcess.real, round(sr/2))
        elif n_of_sliders == 10:
            scaleProcess = functions.split_vowels(scale, dict_sliders)
            sf.write('static/audio/sig.wav', scaleProcess.real, round(sr))

        path1 = 'static/audio/sig.wav'
        return render_template('music.html', dict_values=dict_sliders, path=path, path1=path1, url="/",n_of_sliders = n_of_sliders)
    return render_template('music.html', dict_values=dict_sliders, path=None, path1=None, url="/")





if __name__ == '__main__':
    app.run(debug=True)
