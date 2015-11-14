from functools import wraps
import os.path
import threading

from flask import Flask, render_template, request, redirect, url_for, Response
from flask_bower import Bower
from rcblog import git
from rcblog import utils

app = Flask(__name__)
Bower(app)


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
    post_html = utils.md_to_html(open('rcblog/templates/test.md').read())
    post = {
        'title': 'Title',
        'html': post_html,
    }
    return render_template('post.html', post=post)


@app.route('/posts/add')
@requires_auth
def add_post():
    return render_template('add_post.html')


@app.route('/posts')
def posts_list():
    return render_template('posts.html', posts=get_all_posts_test())


@app.route('/posts', methods=['POST'])
def commit_post():
    title = request.form['title']
    md = request.form['post']
    file_name = '{}.md'.format(title)
    file_path = utils.get_repository_path() / file_name
    with open(str(file_path), 'w') as f:
        f.write(md)
    threading.Thread(target=git.commit, args=(utils.get_repository_path(), [file_name], "Add {}".format(file_name)))
    return redirect(url_for('index'))


def get_all_posts_test():
        return [
            {
                'id': 1,
                'title': 'How to do something',
                'html': utils.md_to_html(open('rcblog/templates/test.md').read()),
            },
            {
                'id': 2,
                'title': 'How to do something 2',
                'html': utils.md_to_html(open('rcblog/templates/test.md').read()),
            }
        ]
