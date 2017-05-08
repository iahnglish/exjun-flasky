#! /Users/exjun/Desktop/Python/myproject/venv/bin/python
# _*_ encoding: utf-8 _*_


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm,\
					ChangeEmailForm
from ..models import User
from . import auth
from .. import db
from ..email import send_email


@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] != 'auth.':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	else:
		return render_template('auth/unconfirmed.html')	
	


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'유효하지않은 username 또는 password 입니다.')
	return render_template('auth/login.html', form=form)
	
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'로그아웃 되었습니다.')
	return redirect(url_for('main.index'))
	
	
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, u'계정 확인 메일입니다', 'auth/email/confirm', user=user, token=token) 
		flash(u'계정 확인 메일이 전송되었습니다.')
		return redirect(url_for('main.index'))	
	return render_template('auth/register.html', form=form)
	

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, u'계정 확인 메일입니다', 'auth/email/confirm', user=user, token=token)
	flash(u'계정 확인 메일이 전송되었습니다.')
	return redirect(url_for('main.index'))	



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'계정 확인이 완료되었습니다.')
	else:
		flash(u'계정 확인 링크가 유효하지 않거나 만기되었습니다.')
	return redirect(url_for('main.index'))
	
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			return redirect(url_for('main.index'))
		else:
			flash(u'잘못된 비밀 번호입니다.')
	return render_template('auth/change_password.html', form=form)
	
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, u'비밀번호 재설정 메일입니다', 'auth/email/reset_password', user=user, token=token, next=request.args.get('next'))
		flash(u'비밀번호를 재설정을 위한 메일이 발송되었습니다.')
		return redirect(url_for('auth.login'))
	return render_template('auth/password_reset.html', form=form)
	
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash(u'비밀번호가 변경되었습니다.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/password_reset.html', form=form)
	
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email, u'이메일 주소 변경 확인', 'auth/email/change_email', user=current_user, token=token)
			flash(u'새 이메일 주소 확인을 위한 메일이 발송되었습니다.')
			return redirect(url_for('main.index'))
		else:
			flash(u'유효하지 않은 메일입니다.')
	
	return render_template('auth/change_email.html', form=form)
	
@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash(u'이메일 주소가 변경되었습니다.')
	else:
		flash(u'유효하지 않은 요청입니다.')
	return redirect(url_for('main.index'))
			
			
				
			
			
			
	
