import sqlite3, logging, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.config['conn_count'] += 1
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
# app.config['SECRET_KEY'] = 'your secret key'
with app.app_context():
    app.config['conn_count'] = 0
    app.config['posts_count'] = 0

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    app.config['posts_count'] = len(posts)
    connection.close()
    return render_template('index.html', posts=posts)
# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error("A non-existing article is accessed and a 404 page is returned.")
        return render_template('404.html'), 404
    else:
        app.logger.debug("Article post=%s retrieved", post)
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("The \"About Us\" page is retrieved.")
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
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
            app.logger.info("A new article is created. Title: title=%s", title)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthcheck():

    if healthcheck_db():
        result = "OK - DB Connection healthy"
        status_code = "200"
        app.logger.debug('DB Connection request successful')
    else:
        result = "NOK - DB connection broken"
        status_code = "503"
        app.logger.warning('DB Connection request failed')

    response = app.response_class(
            response=json.dumps({"result":result}),
            status = status_code,
            mimetype='application/json'
    )
    return response


def healthcheck_db():
    try:
        connection = get_db_connection()
        connection.execute('SELECT 1 FROM posts').fetchone()
    except Exception as e:
        print('Exception: {0}'.format(e))
        return False
    return True


@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"db_connection_count": app.config['conn_count'], "post_count": app.config['posts_count']}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug("Response: response=%s", response)
    return response

# start the application on port 3111
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    # stream handler
    # set logger to handle STDOUT and STDERR
    stdout_handler =  logging.StreamHandler(stream=sys.stdout)
    stderr_handler =  logging.StreamHandler()
    handlers = [stderr_handler, stdout_handler]
    # set default level
    # stdout_handler.setLevel("INFO")
    stderr_handler.setLevel("WARNING")
    # format output
    format_output = "{asctime} - {levelname} - {message}"
    logging.basicConfig(format=format_output,  style="{", datefmt="%Y-%m-%d %H:%M", level=logging.DEBUG, handlers=handlers)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # file handler
    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    file_handler.setLevel("DEBUG")
    formatter=logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    app.run(host='0.0.0.0', port='3111')
