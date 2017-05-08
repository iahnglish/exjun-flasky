#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
	email = StringField(u'이메일', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField(u'비밀번호', validators=[Required()])
	remember_me = BooleanField(u'로그인 유지')
	submit = SubmitField(u'로그인')
	
	
class RegistrationForm(FlaskForm):
	email = StringField(u'이메일', validators=[Required(), Length(1,64), Email()])
	username = StringField(u'사용자 ID', validators=[Required(), Length(1,64),\
				Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'사용자 ID 작성 시 문자, 숫자, 점 또는 밑줄 만 사용할 수 있습니다')])
				
	
	password = PasswordField(u'비밀번호', validators=[Required(), EqualTo('password2', message=u'비밀번호가 일치하지 않습니다.')])
	password2 = PasswordField(u'비밀번호 확인', validators=[Required()])
	submit = SubmitField(u'제출')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'이미 사용 중인 이메일입니다.')
			
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'이미 사용 중인 사용자ID 입니다.')
			
			
class ChangePasswordForm(FlaskForm):
	old_password = PasswordField(u'현재 비밀번호', validators=[Required()])
	password = PasswordField(u'새 비밀번호', validators=[Required(), EqualTo('password2', message=u'비밀번호가 일치하지 않습니다.')])
	password2 = PasswordField(u'새 비밀번호 확인', validators=[Required()])
	submit = SubmitField(u'제출')


class PasswordResetRequestForm(FlaskForm):
	email = StringField(u'이메일', validators=[Required(), Length(1, 64), Email()])
	submit = SubmitField(u'제출')



	
class PasswordResetForm(FlaskForm):
	email = StringField(u'이메일', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField(u'새 비밀번호', validators=[Required(), EqualTo('password2', message=u'비밀번호가 일치하지 않습니다')])
	password2 = PasswordField(u'새 비밀번호 확인', validators=[Required()])
	submit = SubmitField(u'제출')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError(u'등록되지 않은 이메일입니다.')
		
class ChangeEmailForm(FlaskForm):
	email = StringField(u'새 이메일', validators=[Required(), Length(1,64), Email()])
	password = PasswordField(u'비밀번호', validators=[Required()])
	submit = SubmitField(u'제출')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'이미 사용 중인 이메일입니다.')