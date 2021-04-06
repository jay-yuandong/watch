#命令函数
import click
from watchlist import db,app
from watchlist.models import User,Movie
@app.cli.command() #注册为命令
@click.option('--drop',is_flag=True,help='Create after drop.') #设置选项
def initdb(drop):  #执行flask initdb即可创建数据库
    """Initialize the database."""
    if drop: #如果执行命令参数带有drop，则先删除原有model
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') #输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    name = 'jyd'
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
    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login.')
#hide_input=True 隐藏密码,confirmation_prompt=True 二次确认
def admin(username,password):
    """Create user."""
    db.create_all()

    user=User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username=username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user=User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done.')
