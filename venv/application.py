# _*_ encoding:utf-8 _*_
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/hello/')

@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)