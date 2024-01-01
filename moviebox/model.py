"""import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class movie_box(db.Model):  # 表名将会是 user（自动生成，小写处理）
    movie_id = db.Column(db.String(10), primary_key=True)  # 主键
    box = db.Column(db.Float)  # 票房

class movie_info(db.Model):  # 表名将会是 movie
    movie_id = db.Column(db.String(10), primary_key=True)  # 主键
    title = db.Column(db.String(20))  # 电影标题
    release_date = db.Column(db.DateTime)  # 电影上映日期
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))
    year = db.Column(db.INT)  # 电影年份

class actor_info(db.Model):
    actor_id = db.Column(db.String(10), primary_key=True)  # 主键
    gender = db.Column(db.String(2))  
    country = db.Column(db.String(20))  

class movie_actor_relation(db.Model):
    id = db.Column(db.String(10), primary_key=True)  # 主键
    movie_id = db.Column(db.String(10), db.ForeignKey("movie_info.movie_id"))  
    actor_id = db.Column(db.String(10), db.ForeignKey("actor_info.actor_id"))
    relation_type = db.Column(db.String(20)) 
"""