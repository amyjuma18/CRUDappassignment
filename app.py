import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
# render_template : allows us to return a html output using desired data
# app references the object from the flask package
# creating the first application instance
app = Flask(__name__)
# we need a secret key: key used to secure sessions, flash will store messages in this session
app.config['SECRET_KEY'] = 'ba9f0733223fdb4dfe0fad025f81b0de0d6c6320646d1982'
# by creation of the instance above you can use it to handle incoming web requests and send response to users
# app.route is a decorator. it turns a regular python function into a flask view function(user can see elements)
# the flask view function converts function return value into a http response to be displayed by a http client such as
# a web browser
# decorator marker :@app.route('/')
# @app.route('/')
# def hello_world():  # put application's code here
#     return '<h1>Hello World!</h1>'
# @app.route('/')
# def hello_new server():  # put application's code here
#     return '<h1>Hello World!</h1>'
#

# create a connection to our sqlite db
# we define a row factory : gives name-base access to columns in a database
def get_db_connection():
    conn = sqlite3.Connection('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
   # validate the post id exists
    if posts is None:
        abort(404)
   # when post is found
    return posts

# DEFINE ROUTES FOR DISPLAYING POSTS
# fetchall() returns our rows from sql as a python dictionary
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# posting data
# GET requests are used tO retrieve data from a server/POST is used to post data to a specific route
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        #  pick up values from form
        title = request.form["title"]
        content = request.form["content"]
        # validate values are not empty

        if not title:
            flash('Title is required')
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template('create.html')

# edit route

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash('Title required')
        elif not content:
            flash("Content required")
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            return redirect(url_for('index'))

    return render_template("edit.html", post=post)

@app.route('/<int:id>/delete/', methods=('GET','POST'))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if post is not None:
        flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()