from datetime import datetime
from email.message import EmailMessage
from exceptions import EnvironmentUnsetError
from flask import Flask, render_template
from os import environ
from smtplib import SMTP_SSL
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, length

from models import db


def create_application():
    app = Flask(__name__)
    try:
        app.secret_key = environ['WFB_FLASK_SECRET_KEY']
    except KeyError:
        raise EnvironmentUnsetError('WFB_FLASK_SECRET_KEY')

    if 'WFB_DB_HOST' in environ and 'WFB_DB_NAME' in environ:
        sqlalchemy_database_uri = 'mysql+mysqlconnector://'
        if 'WFB_DB_USERNAME' in environ:
            sqlalchemy_database_uri += environ['WFB_DB_USERNAME']
            if 'WFB_DB_PASSWORD' in environ:
                sqlalchemy_database_uri += ':'
                sqlalchemy_database_uri += environ['WFB_DB_PASSWORD']
        sqlalchemy_database_uri += '@'
        sqlalchemy_database_uri += environ['WFB_DB_HOST']
        if 'WFB_DB_PORT' in environ:
            sqlalchemy_database_uri += ':'
            sqlalchemy_database_uri += environ['WFB_DB_PORT']
        sqlalchemy_database_uri += '/'
        sqlalchemy_database_uri += environ['WFB_DB_NAME']

        app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app


application = create_application()


class ContactForm(Form):
    name = StringField(
        'Name',
        validators=[DataRequired(), length(max=200)],
        render_kw={
            "placeholder": "Name",
            "class": "input",
            "maxlength": 200
        }
    )
    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message="Invalid email address"),
            length(max=200)
        ],
        render_kw={
            "placeholder": "Email",
            "class": "input",
            "maxlength": 200
        }
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(), length(max=5000)],
        render_kw={
            "placeholder": "Enter your message here...",
            "class": "textarea",
            "rows": 5,
            "maxlength": 5000
        }
    )
    submit = SubmitField(
        'Send',
        render_kw={
            "class": "button is-link"
        }
    )


@application.route('/', methods=['POST', 'GET'])
def about():
    return render_template(
        'index.html',
        title=environ['WFB_PROJECT_NAME'],
        year=datetime.now().year,
    )


def send_message(name, email, message):
    required_env_vars = [
        'WFB_SMTP_HOST',
        'WFB_SMTP_PORT',
    ]

    for var in required_env_vars:
        if var not in environ:
            raise EnvironmentUnsetError(var)

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = name + ' - {} Contact Form'.format(environ['WFB_PROJECT_NAME'])
    msg['From'] = email
    if 'WFB_SMTP_TARGET' in environ:
        msg['To'] = environ['WFB_SMTP_TARGET']
    elif 'WFB_SITE_URL' in environ:
        msg['To'] = 'contactform@{}'.format(environ['WFB_SITE_URL'])
    else:
        raise EnvironmentUnsetError('WFB_SMTP_TARGET', 'WFB_SITE_URL')

    sender = SMTP_SSL(
        environ['WFB_SMTP_HOST'],
        environ['WFB_SMTP_PORT'],
        environ['WFB_SITE_URL']
    )

    if 'WFB_SMTP_USERNAME' in environ and 'WFB_SMTP_PASSWORD' in environ:
        sender.login(
            environ['WFB_SMTP_USERNAME'],
            environ['WFB_SMTP_PASSWORD']
        )

    sender.send_message(msg)
    sender.quit()


if __name__ == '__main__':
    application.debug = True
    application.run()
