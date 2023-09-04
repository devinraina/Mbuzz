from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.debug=True
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user_system'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
  
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user != None:
            if email == 'devin@gmail.com' and password == '123':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM movies')
                data=cursor.fetchall()
                size=len(data)
                return render_template('admin.html', data=data, size=size)
            else:
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']    
                mesage = 'Logged in successfully !'
                return clear()
        elif user == None:  
            mesage = 'Please enter correct email / password !'
            return render_template('login.html', mesage = mesage)
    return render_template('login.html')

@app.route('/search', methods =['GET', 'POST'])
def search():
    mesage = ''
    if request.method == 'POST' and 'movie_id' and 'movie_title' and 'movie_year' in request.form:
        movieId = str((request.form["movie_id"]))
        movieTitle =str(request.form['movie_title'])
        movieYear =str(request.form['movie_year'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        global size
        if movieId:
            cursor.execute('SELECT * FROM movies WHERE movie_id = % s', (movieId))
            s_movie = cursor.fetchone()
            size=0
            return render_template('user.html', mesage=mesage, s_movie=s_movie, size=size)
        elif movieTitle:
            cursor.execute('SELECT * FROM movies WHERE movie_title LIKE "%{}%"'.format(movieTitle,))
            s_movie = cursor.fetchall()
            size=len(s_movie)
            return render_template('user.html', mesage=mesage, s_movie=s_movie, size=size,)
        elif movieYear:
            cursor.execute('SELECT * FROM movies WHERE movie_year LIKE "%{}%"'.format(movieYear,))
            s_movie = cursor.fetchall()
            size=len(s_movie)
            return render_template('user.html', mesage=mesage, s_movie=s_movie, size=size,)
@app.route('/clear', methods =['GET', 'POST'])
def clear():
    mesage =''
    if request.method == 'GET' or request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM movies')
        data=cursor.fetchall()
        size=len(data)
    return render_template('user.html',mesage=mesage, data=data, size=size )

@app.route('/admin_sbutton', methods=['GET', 'POST'])
def admin_sbutton():
    mesage =''
    if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE' and 'movie_id' and 'movie_title' and 'movie_year' in request.form:
        movieId = str((request.form["movie_id"]))
        movieTitle =str(request.form['movie_title'])
        movieYear =str(request.form['movie_year'])
        movieDirec=str(request.form['movie_director'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM movies')
        data=cursor.fetchall()
        size=len(data)
        option=str(request.form['select'])
        if option == 'add':
             if movieId:
                 cursor.execute('SELECT * FROM movies')
                 data=cursor.fetchall()
                 size=len(data)
                 mesage='Don"t Put Movie ID it will be auto generated'
                 return render_template('admin.html', mesage=mesage, data=data, size=size)
             elif movieDirec and movieTitle and movieYear:
                 cursor.execute('insert into movies (movie_title,`movie_year`,`movie_director`)values(%s,%s,%s)',(movieTitle, movieYear,movieDirec,))
                 mysql.connection.commit()
                 cursor.execute('SELECT * FROM movies')
                 data=cursor.fetchall()
                 size=len(data)
                 mesage='Movie record inserted succesfully'
                 return render_template('admin.html', mesage=mesage, data=data, size=size)
             else:
                 cursor.execute('SELECT * FROM movies')
                 data=cursor.fetchall()
                 size=len(data)
                 mesage='Please Insert Complete Movie details!'
                 return render_template('admin.html', mesage=mesage, data=data, size=size)
        elif option == 'remove':
             cursor.execute('delete from movies where movie_id=%s',(movieId,))
             mysql.connection.commit()
             cursor.execute('SELECT * FROM movies')
             data=cursor.fetchall()
             size=len(data)
             mesage=('Movie deleted succesfully')
             return render_template('admin.html', mesage=mesage, data=data, size=size)
        elif option == 'edit':
             if movieTitle and movieId and movieYear and movieDirec:
                 cursor.execute('update movies set movie_title=%s, movie_year=%s, movie_director=%s where movie_id=%s',(movieTitle,movieYear,movieDirec,movieId,))
                 mysql.connection.commit()
                 cursor.execute('SELECT * FROM movies')
                 data=cursor.fetchall()
                 size=len(data)
                 mesage=('Movie edited succesfully')
                 return render_template('admin.html', mesage=mesage, data=data, size=size)
             else:
                 cursor.execute('SELECT * FROM movies')
                 data=cursor.fetchall()
                 size=len(data)
                 mesage=('Enter the Movie ID that you want to change and all the details. Please')
                 return render_template('admin.html', mesage=mesage, data=data, size=size)
        else:
            mesage='Not working'
            return render_template('admin.html', mesage=mesage, data=data, size=size)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)



    
if __name__ == "__main__":
    app.run()