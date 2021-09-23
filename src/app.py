import sqlite3

from flask import (Flask, flash, json, redirect, render_template,
                   request, url_for)
import os


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    app.logger.info('DB connection initiated')
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.logger.info('Successfully connected to DB')
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
        response=json.dumps({"status":"OK-healthy"}),
        status=200,
        mimetype='application/json'
    )
    
    app.logger.info('Healthcheck request successfully')
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    response = app.response_class(
        response=json.dumps({"post_count": posts, "get_db_connection_count":  os.system("lsof schema.sql")}),
        status=200,
        mimetype='application/json'
    )
    
    app.logger.info('Healthcheck request successfully')
    return response

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=sorted(posts, key=lambda x: x["created"], reverse=True))

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error("non-existing article",)
      return render_template('404.html'), 404
    else:
      app.logger.info('Access an article')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('Successfully access about us page')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    app.logger.info('Successfully creates an article')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
