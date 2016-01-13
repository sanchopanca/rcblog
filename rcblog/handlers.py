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


@app.route('/posts/<post_id>')
def show_post(post_id):
    selected_language = request.args.get('lang', 'eng')
    post = database.get_post_by_id(post_id)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
        md_file_path = str(utils.get_repository_path() / translation['markdown_file'])
        translation['html'] = utils.md_to_html(open(md_file_path).read())
    languages = database.get_languages_by_codes(*language_codes)
    return render_template('post.html',
                           post=post,
                           selected_language=selected_language,
                           languages=languages,
                           current_address='/posts/{}'.format(post_id))


@app.route('/drafts/<draft_id>')
def show_draft(draft_id):
    selected_language = request.args.get('lang', 'eng')
    post = database.get_post_by_id(draft_id)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
        translation['html'] = utils.md_to_html(open(translation['markdown_file']).read())
        translation['post'] = open(translation['markdown_file']).read()
    languages = database.get_languages_by_codes(*language_codes)
    all_languages = database.get_all_languages()
    remaining_languages = utils.complement_of_lists_of_dictionaries(all_languages, languages)
    for language in remaining_languages:
        post['translations'][language] = {'title': '', 'post': ''}
    return render_template('draft.html',
                           post=post,
                           selected_language=selected_language,
                           languages=all_languages,
                           values=post['translations'])


@app.route('/posts/add')
@requires_auth
def add_post():
    return render_template('add_post.html', languages=database.get_all_languages())


@app.route('/posts')
def posts_list():
    posts = database.get_all_posts()
    for post in posts:
        for language, translation in post['translations'].items():
            md_file_path = str(utils.get_repository_path() / translation['markdown_file'])
            translation['html'] = utils.md_to_html(open(md_file_path).read())

    return render_template('posts.html', posts=posts)


@app.route('/drafts')
def drafts_list():
    drafts = database.get_all_drafts()
    for draft in drafts:
        for language, translation in draft['translations'].items():
            md_file_path = str(utils.get_repository_path() / translation['markdown_file'])
            translation['html'] = utils.md_to_html(open(md_file_path).read())

    return render_template('drafts.html', posts=drafts)


@app.route('/posts', methods=['POST'])
def commit_post():
    post = {'translations': {}}
    language_codes = set()
    for key in request.form:
        if '$' in key:
            language_codes.add(key.split('$')[0])

    files_to_commit = []

    for language_code in language_codes:
        title = request.form.get(language_code + '$title', '')
        md = request.form.get(language_code + '$post', '')
        if title and md:
            file_name = '{}_{}.md'.format(title, language_code)
            file_path = utils.get_repository_path() / file_name
            files_to_commit.append(file_path)
            with open(str(file_path), 'w') as f:
                f.write(md)
            post['translations'][language_code] = {
                'title': title,
                'markdown_file': file_name
            }
    draft = bool(request.form.get('draft', False))
    database.add_post(post['translations'], [], draft)
    threading.Thread(target=git.commit, args=(utils.get_repository_path(),
                                              files_to_commit,
                                              'Add {}'.format('new post'))).run()
    return redirect(url_for('index'))
