from flask import Flask, render_template, send_file
from os import listdir

import pathlib
import datetime


class File:
    def __init__(self, name, filename, time, location):
        self.name = name
        self.filename = filename
        self.time = time
        self.location = location


class FileGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.name = filename.split('.')[0]
        self.location = f"./public/files/{filename}"
        self.time = self.get_time_from_file()

    def get_time_from_file(self):
        fname = pathlib.Path(self.location)
        mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
        return mtime.strftime("%Y-%m-%d %H:%M:%S")

    def generate(self):
        return File(self.name, self.filename, self.time, self.location)


def get_files():
    file_names = listdir("./public/files/")
    files = []
    for file_name in file_names:
        g = FileGenerator(file_name)
        files.append(g.generate())
    return files


app = Flask(__name__)


@app.route('/')
def home():
    files = get_files()
    return render_template('index.html', result=files)


@app.route('/public/files/<string:name>')
def return_file(name):
    try:
        return send_file(f"./public/files/{name}", attachment_filename=name)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
