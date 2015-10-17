from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, Response
from rcblog import utils

app = Flask(__name__)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/<int:post_id>')
def post(post_id):
    return utils.md_to_html(open('rcblog/templates/test.md').read())


@app.route('/posts/add')
@requires_auth
def add_post():
    return render_template('add_post.html')


@app.route('/posts')
def posts_list():
    return render_template('posts.html', posts=utils.get_posts_list())


@app.route('/posts', methods=['POST'])
def commit_post():
    title = request.form['title']
    md = request.form['post']
    with open('/home/sanchopanca/src/rcblog/rcblog/posts_repository/{}.md'.format(title), 'w') as f:
        f.write(md)
    return redirect(url_for('index'))
