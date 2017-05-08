#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
	name = StringField(u'이름을 입력하세요', validators=[Required()])
	submit = SubmitField(u'제출')

class EditProfileForm(FlaskForm):
	name = StringField(u'실제이름', validators=[Length(0,64)])
	location = StringField(u'위치', validators=[Length(0,64)])
	about_me = TextAreaField(u'내 소개')
	submit = SubmitField(u'제출')
	
class EditProfileAdminForm(FlaskForm):
	email = StringField(u'이메일', validators=[Required(), Length(1, 64), Email()])
	username = StringField(u'사용자 ID', validators=[Required(), Length(1, 64), \
			Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0 , u'사용자 ID 작성 시 문자, 숫자, 점 또는 밑줄 만 사용할 수 있습니다')])
			
	confirmed = BooleanField(u'확인')
	role = SelectField(u'역할', coerce=int)
	name = StringField(u'실제 이름', validators=[Length(0, 64)])
	location = StringField(u'위치', validators=[Length(0, 64)])
	about_me = TextAreaField(u'내 소개')
	submit = SubmitField(u'제출')
	
	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user
		
	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError(u'이미 사용 중인 이메일입니다.')
			
	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError(u'이미 사용 중인 사용자 ID입니다.')


class PostForm(FlaskForm):
		body = PageDownField(u'지금 무슨 생각이 드나요?', validators=[Required()])
		submit = SubmitField(u'제출')

class CommentForm(FlaskForm):
		body = StringField('', validators=[Required()])
		submit = SubmitField(u'제출')