import os
import sys

import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.secret_key = 'yes'

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
import uuid

class movie_info(db.Model):  # 表名将会是 movie_info
    movie_id = db.Column(db.String(10), primary_key=True, default=lambda: str(uuid.uuid4()))  # 主键
    title = db.Column(db.String(20))  # 电影标题
    release_date = db.Column(db.String)  # 电影上映日期
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))
    year = db.Column(db.INT)  # 电影年份
    box = db.Column(db.Float)  # 票房

class actor_info(db.Model):
    actor_id = db.Column(db.String(10), primary_key=True,  default=lambda: str(uuid.uuid4()))  # 主键
    gender = db.Column(db.String(2))  
    country = db.Column(db.String(20))  

class movie_actor_relation(db.Model):
    id = db.Column(db.String(10), primary_key=True)  # 主键
    movie_id = db.Column(db.String(10), db.ForeignKey("movie_info.movie_id"))  
    actor_id = db.Column(db.String(10), db.ForeignKey("actor_info.actor_id"))
    relation_type = db.Column(db.String(20)) 

import click

'''@app.cli.command()   # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
'''

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def forge(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

    """Generate fake data."""
    # 全局的两个变量移动到这个函数内
    movies = [
        {'movie_id':'1001','title':'战狼2','release_date':'2017/7/27','country':'中国','type':'战争','year':'2017','box':'56.84'},
        {'movie_id':'1002','title':'哪吒之魔童降世','release_date':'2019/7/26','country':'中国','type':'动画','year':'2019','box':'50.15'},
        {'movie_id':'1003','title':'流浪地球','release_date':'2019/2/5','country':'中国','type':'科幻','year':'2019','box':'46.86'},
    ]

    for m in movies:
        movie = movie_info(title=m['title'], release_date=m['release_date'], #movie_id=m['movie_id'], 
                           country=m['country'], type=m['type'], year=m['year'], box=m['box'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


from flask import request, url_for, redirect, flash
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        type = request.form.get('type')
        country = request.form.get('country')
        box = request.form.get('box')
        
        # 验证数据 
        if not title or not year or not type or not country or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页

        # 保存表单数据到数据库
        movie = movie_info(title=title, year=year, type=type, country=country, box=box)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = movie_info.query.all()
    return render_template('index.html', movies=movies)

app.run()