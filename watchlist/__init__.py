#包构造文件，创建程序实例
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os,sys
import click
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_required,UserMixin
from flask_login import login_user,logout_user,current_user
# 判断系统
WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=prefix+os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE','data_list.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #关闭对模型修改的监控

app.config['SECRET_KEY']=os.getenv('SECRET_KEY','dev')
#初始化扩展，传入程序实例app
db=SQLAlchemy(app)

login_manager=LoginManager(app) #实例化扩展
@login_manager.user_loader
def load_user(user_id): #创建用户加载回调函数
    from watchlist.models import User
    user=User.query.get(int(user_id)) #用ID作为user模型主键查询对应的用户
    return user

login_manager.login_view='login'

@app.context_processor #app.context_processor 装饰器注册一个模板上下文处理函数
def inject_user():
    from watchlist.models import User
    user=User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands