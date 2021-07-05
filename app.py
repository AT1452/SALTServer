from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from os import makedirs
import pandas as pd
import matplotlib.pyplot as plt, mpld3
from matplotlib.colors import hsv_to_rgb
from math import atan2, hypot, degrees
from matplotlib import collections as matcoll
import numpy as np
from flask_socketio import SocketIO


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
    
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

async_mode = None
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secreto'
socketio = SocketIO(app, async_mode=async_mode)

def create_graph(data):
    av_coords = []
    angles = []
    colors = []
    magnitude = []


    for (v, a) in zip(data['valence'], data['arousal']):
        if(np.isnan(v) or np.isnan(a)):
            continue
        else:
            av_coords.append((v, a))
            magnitude.append(hypot(v, a))
            deg = (degrees(atan2(a, v)) + 360) % 360;
            angles.append(deg)

    for angle in angles:
        colors.append(hsv_to_rgb([angle/360, 1, 1]))
    
    fig, ax = plt.subplots()
    (markers, stemlines, baseline) = plt.stem(magnitude, markerfmt=' ')
    plt.setp(stemlines, linestyle="-", color=colors, linewidth=0.5 )

    mpld3.save_json(fig, "./static/tester.json")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            print(file.filename.rsplit('.', 1)[1].lower())
            if file.filename.rsplit('.', 1)[1].lower() == 'csv':
                df = pd.read_csv(file)
                create_graph(df)
            if file.filename.rsplit('.', 1)[1].lower() == 'mp4':
                file.save(os.path.join("./static", "source.mp4"))

    return render_template("index.html")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # return render_template("results.html")
    
