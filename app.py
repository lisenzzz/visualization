# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'lisenzzz'


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
