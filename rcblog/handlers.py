from functools import wraps
import threading

from flask import Flask, render_template, request, redirect, url_for, Response
from flask_bower import Bower

from rcblog import git
from rcblog import utils
from rcblog.db import DataBase

database = DataBase()

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
    post = get_post_by_id_test(post_id)
    for language, translation in post['translations'].items():
        translation['html'] = utils.md_to_html(open(translation['markdown_file']).read())
    import pprint; pprint.pprint(post)
    return render_template('post.html', post=post)


@app.route('/posts/add')
@requires_auth
def add_post():
    return render_template('add_post.html', languages=database.get_all_languages())


@app.route('/posts')
def posts_list():
    posts = get_all_posts_test()
    for post in posts:
        for language, translation in post['translations'].items():
            translation['html'] = utils.md_to_html(open(translation['markdown_file']).read())

    return render_template('posts.html', posts=posts)


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
            'translations': {
                'eng': {
                    'title': 'How to do something',
                    'markdown_file': 'rcblog/templates/test.md'
                },
                'rus': {
                    'title': 'Как сделать что-то',
                    'markdown_file': 'rcblog/templates/test.md'
                }
            },
        },
        {
            'id': 2,
            'translations': {
                'eng': {
                    'title': 'How to do something 2',
                    'markdown_file': 'rcblog/templates/test.md'
                },
                'rus': {
                    'title': 'Как сделать что-то 2',
                    'markdown_file': 'rcblog/templates/test.md'
                }
            },
        }
    ]


def get_post_by_id_test(*args):
    return {
        'id': 1,
        'translations': {
            'eng': {
                'title': 'How to do something',
                'markdown_file': 'rcblog/templates/test.md'
            },
            'rus': {
                'title': 'Как сделать что-то',
                'markdown_file': 'rcblog/templates/test.md'
            }
        },
    }
