#视图函数
from flask import render_template, request, flash, redirect, url_for
from flask_login import  login_required
from flask_login import login_user,logout_user,current_user
from watchlist import app,db
from watchlist.models import User,Movie

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        if not current_user.is_authenticated: #当前用户未认证
            return redirect(url_for('index'))
        #请求为post时，从表单获取信息
        title=request.form.get('title')
        year=request.form.get('year')
        #验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.') #显示错误提示
            return redirect(url_for('index')) #重定向回主页

        #保存数据
        movie=Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.') #提示添加成功
        return redirect(url_for('index'))

    movies=Movie.query.all()
    return render_template('index.html',movies=movies)

@app.errorhandler(404) #传入处理的错误代码
def page_not_found(e): #接收异常对象作为参数
    return render_template('404.html'),404 #返回模板和状态码

@app.route('/movie/edit/<int:movie_id>',methods=['POST','GET'])
@login_required
def edit(movie_id):
    #查不到id，返回404
    movie=Movie.query.get_or_404(movie_id)
    if request.method=='POST':
        title=request.form['title']
        year=request.form['year']
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('edit',movie_id=movie_id))

        #修改数据
        movie.title=title
        movie.year=year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)


@app.route('/movie/delete/<int:movie_id>',methods=['POST']) #安全，限定用post提交删除
@login_required
def delete(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user=User.query.first()
        #如果用户名和密码一致
        if username==user.username and user.validate_password(password):
            login_user(user) #登录用户
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/settings',methods=['POST','GET'])
@login_required
def settings():
    if request.method=='POST':
        name=request.form['name']
        if not name or len(name)>20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        #新修改的name不符合要求，会返回当前登录用户得数据库记录对象
        # current_user.name=name
        user=User.query.first()
        user.name=name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')
if __name__ == '__main__':
    app.run()