#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, forms