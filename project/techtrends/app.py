import sqlite3, logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection(conn_count):
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_count += 1
    return connection, conn_count

# Function to get a post using its ID
def get_post(post_id,conn_count):
    connection = get_db_connection(conn_count)
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    conn_count -= 1
    return post, conn_count

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application
@app.route('/')
def index():
    conn_count=0
    connection = get_db_connection(conn_count)
    posts = connection.execute('SELECT * FROM posts').fetchall()
    posts_count = connection.execute('SELECT * FROM posts').rowcount
    connection.close()
    conn_count -= 1
    return render_template('index.html', posts=posts), posts_count, conn_count

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logger.info("A non-existing article is accessed and a 404 page is returned.")
      logger.debug("A non-existing article is accessed and a 404 page is returned.")
      return render_template('404.html'), 404
    else:
      logger.info("Article post=%s retrieved", post)
      logger.debug("Article post=%s retrieved", post)
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info("The \"About Us\" page is retrieved.")
    logger.debug("The \"About Us\" page is retrieved.")
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create(conn_count):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection(conn_count)
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            conn_count -= 1
            logger.info("A new article is created. Title: title=%s", title)
            logger.debug("A new article is created. Title: title=%s", title)
            return redirect(url_for('index')), conn_count

    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Status request successful')
    app.logger.debug('DEBUG message')
    return response

@app.route('/metrics')
def metrics(conn_count, posts_count):
    response = app.response_class(
            response=json.dumps({"db_connection_count": conn_count, "post_count": posts_count}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info("Response: response=%s", response)
    app.logger.debug("Response: response=%s", response)
    return response

# start the application on port 3111
if __name__ == "__main__":
   logger = logging.getLogger(__name__)
   logger.setLevel("DEBUG")
   formatter=logging.Formatter(
       "{asctime} - {levelname} - {message}",
       style="{",
       datefmt="%Y-%m-%d %H:%M")
   console_handler = logging.StreamHandler()
   console_handler.setLevel("INFO")
   console_handler.setFormatter(formatter)
   file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
   file_handler.setLevel("DEBUG")
   file_handler.setFormatter(formatter)
   logger.addHandler(console_handler)
   logger.addHandler(file_handler)

   app.run(host='0.0.0.0', port='3111')
