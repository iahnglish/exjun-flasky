#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_

from flask import render_template, current_app
from threading import Thread
from . import mail
from flask_mail import Message




def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)
