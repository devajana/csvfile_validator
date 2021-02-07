from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import os

app.secret_key = "secret key"
app.config["ALLOWED_EXTS"] = ["CSV"]
app.config["ALLOWED_ROW_COUNT"] = [10]
app.config["ALLOWED_COL_COUNT"] = [3]

@app.route('/')
def index():
    print ('Index page')
    return render_template('index.html')


def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTS"]:
        return True
    else:
        return False


def check_filedata(filedata):
    print('In check file')

    df = pd.read_csv(filedata, header=None)

    if not df.empty:
        row_count, column_count = df.shape

        if not row_count == app.config["ALLOWED_ROW_COUNT"] and column_count == app.config["ALLOWED_COL_COUNT"]:
            return [False, 'Incorrect Size. Please ensure the file contains ' + app.config["ALLOWED_ROW_COUNT"] + ' rows and ' + app.config["ALLOWED_COL_COUNT"] + ' columns.']
        
        if df.isnull().values.any():
            return [False, 'Incomplete Dataset. Please ensure all that there are no incomplete columns or rows in the file.']

        for row in df.dtypes:
            if not row == "int64":
                return [False, 'Incorrect Datatype. Please ensure the datatype of all the elements in the table are numbers.']

        return [True, 'Successfully Uploaded']
    return [False, 'DF empty']
    


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if request.files:
            csvfile = request.files["csvfile"]

            # csvfile.seek(0, os.SEEK_END)
            # if csvfile.tell() == 0:
            #     return jsonify({'error' : 'Tried to add empty'})

            # file_size = os.stat(csvfile)
            # print(file_size.st_size)
            if csvfile.filename == "":
                print('File should have a filename')
                return render_template('upload.html', filename=csvfile.filename, status="Invalid name. Please ensure the file has a name.")

            if not allowed_file(csvfile.filename):
                print('That file is not allowed')
                return render_template('upload.html', filename=csvfile.filename, status="Invalid format. Please upload only .csv files.")

            filename = secure_filename(csvfile.filename)
        
            accurate_file = check_filedata(csvfile)
            return render_template('upload.html', filename=csvfile.filename, status=accurate_file[1])


    return "Not a POST request"