import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
# 强制用户登录
login.login_view = 'login'

if not os.path.exists('log'):
    os.mkdir('log')
file_handler = RotatingFileHandler('log/aswesome.log', maxBytes=1024 * 100, backupCount=1000)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
if app.debug:
    app.logger.setLevel(logging.ERROR)
    app.logger.info('aswesome startup in debug model')
else:
    app.logger.setLevel(logging.INFO)
    app.logger.info('aswesome startup')

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME']:
            auth = app.config['MAIL_USERNAME']
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

# 避免循环导入
from webapp import routes
# 程序运行需导入各个相关部分
import dao
from models import User
