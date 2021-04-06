#模型类

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from watchlist import db

#user表
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    username=db.Column(db.String(20)) #y用户名
    password_hash=db.Column(db.String(128)) #用户密码
    def set_password(self,password): #设置密码
        self.password_hash=generate_password_hash(password) #将生成的密码保存对应的user表字段
    def validate_password(self,password): #验证密码
        return check_password_hash(self.password_hash,password) #返回布尔值


class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60)) #电影标题
    year=db.Column(db.String(4)) #年份