from app import app, mail

from flask.ext.mail import Message
from flask import render_template
from threading import Thread

def render_email(template, **kwargs):
    body = render_template(template + '.txt', **kwargs)
    html = render_template(template + '.html', **kwargs)
    return body, html


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, html, text=None):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.html = html
    if text:
        msg.body = text
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr