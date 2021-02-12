from flask import render_template, flash, redirect, url_for, request, make_response

from app import app
from app.forms import LoadForm

from werkzeug.utils import secure_filename

from werkzeug.urls import url_parse

import os
import time
import threading
import datetime
from drawbot import Drawbot


selected = ""

drawbot = Drawbot()

@app.route('/')
def index():
    global selected
    files = next(os.walk(app.config['UPLOAD_FOLDER']))[2]
    return render_template('index.html',
                            selected_file = selected,
                            file_list=files
                            )

# connect to the drawbot
@app.route('/connect',  methods=['POST'])
def connect():
    
    try:
        drawbot.connect()
    except:
        flash("CONNECTION NOT FOUND")

    response = make_response(redirect(url_for('index')))
    return(response) 


# home the drawbot
@app.route('/home',  methods=['POST'])
def homing():

    if drawbot.is_connected():
        drawbot.home()
    else:
        flash("NO CONNECTION")

    response = make_response(redirect(url_for('index')))
    return(response) 


# home the drawbot
@app.route('/stop',  methods=['POST'])
def stop():

    if drawbot.is_connected() and drawbot.is_running():
        drawbot.stop()
        flash("PROCESS STOPPED")
    else:
        flash("NO CONNECTION")

    response = make_response(redirect(url_for('index')))
    return(response) 



# select a file to run
@app.route('/select/<filename>')
def select(filename):   
    global selected

    selected = filename
    
    return redirect(url_for('index')) 


# run the current selected file
@app.route('/run', methods=['POST'])
def run():

    # check the connection
    if not drawbot.is_connected():
        flash("NO CONNECTION")
        return redirect('/')

    # run a parallel process
    global selected

    if not selected:
        flash("NO FILE SELECTED")
        return redirect('/')

    if not drawbot.run_async(selected):
        flash("PROCESS ALREADY RUNNING")
        return redirect('/')

    response = make_response(redirect(url_for('index')))
    return(response)


# open the upload html
@app.route('/upload')
def upload():
    return render_template('upload.html')
	

# upload a gcode file to the drawbot
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    def allowed_filename(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash("No file part?")
            return redirect('/upload')
        
        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect('/upload')
        
        if f and allowed_filename(f.filename):            
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
        else:
            flash('Invalid file type')
            return redirect('/upload')
        

