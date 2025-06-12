from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    admin_token = StringField('管理员注册密钥', validators=[Optional()])
    submit = SubmitField('注册')

class ForgotPasswordForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('提交')
