from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.extensions import db
from webapp.user.model import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня ', default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={"class": "form-control"}
        )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
        )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
        )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
        )
    remember_me = BooleanField(
        'Запомнить меня ',
        default=True,
        render_kw={"class": "form-check-input"}
        )
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = db.session.scalar(
            db.select(db.func.count()).select_from(User).filter_by(
                username=username.data
            )
        )
        if user_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        user_count = db.session.scalar(
            db.select(db.func.count()).select_from(User).filter_by(
                email=email.data
            )
        )
        if user_count > 0:
            raise ValidationError('Пользователь с такой почтой уже существует')
