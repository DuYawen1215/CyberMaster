import os
import sys
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy #导入扩展类
from markupsafe import escape
import click

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    premix = 'sqlite:///'
else:  # 否则使用四个斜线
    premix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))     # 名字

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # 主键
    title = db.Column(db.String(60))    # 电影标题
    year = db.Column(db.String(40))     # 电影年份

@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='create after drop.')    # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialize database.')  # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Zoey'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.route('/')
# def hello():
#     return 'Welcom to CyberMaster!'

# @app.route('/user/<name>')
# def user_page(name):
#     return f'User: {escape(name)}'
#
# @app.route('/test')
# def test_url_for():
#     print(url_for('hello'))
#     print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
#     print(url_for('user_page', name='peter'))  # 输出：/user/peter
#     print(url_for('test_url_for'))  # 输出：/test
#     # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
#     print(url_for('test_url_for', num=2))  # 输出：/test?num=2
#     return 'Test page'

def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)



