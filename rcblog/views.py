import urllib.parse

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bower import Bower
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.contrib.atom import AtomFeed

from rcblog import utils
from rcblog import crypto
from rcblog.db import DataBase
from rcblog.user import User

database = DataBase()

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)
Bower(app)
login_manager = LoginManager()
login_manager.init_app(app)


POSTS_PER_PAGE = 10


def common_values():
    return {
        'logged_in': current_user.is_authenticated,
    }


def make_external(url):
    return urllib.parse.urljoin(request.url_root, url)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/')
def index():
    return redirect(url_for('posts_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', **common_values())
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = None
        credentials = database.get_credentials(username)
        if credentials:
            credentials_are_correct = crypto.check_password(password,
                                                            credentials['password_hash'],
                                                            credentials['salt'])
            if credentials_are_correct:
                user = User()
        if user:
            login_user(user, remember)
            return redirect(url_for('posts_list'))
        else:
            flash('Invalid credentials', category='danger')
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/posts')
def posts_list():
    accept_language = request.headers.get('Accept-Language')
    user_languages = utils.parse_accept_language(accept_language)
    tag = request.args.get('tag', None)
    page = request.args.get('page', 0, int)
    posts = database.get_posts(skip=page*POSTS_PER_PAGE,
                               limit=POSTS_PER_PAGE,
                               tag=tag)
    posts_to_show = []
    for post in posts:
        language = utils.choose_language(list(post['translations'].keys()), user_languages)
        if language is not None:
            post['language'] = language
            url = make_external('posts/{}/{}'.format(post['id'], utils.urlify(post['translations'][language]['title'])))
            post['external_url'] = url
            posts_to_show.append(post)

    total_number_of_posts = database.get_number_of_posts(tag)
    posts_before = page > 0
    posts_after = total_number_of_posts > (page + 1) * POSTS_PER_PAGE

    for post in posts_to_show:
        post['url'] = utils.urlify(post['translations'][post['language']]['title'])

    base_path = '/posts?tag={}&'.format(tag) if tag else '/posts?'
    previous_page_path = base_path + 'page={}'.format(page - 1)
    next_page_path = base_path + 'page={}'.format(page + 1)
    return render_template('posts.html',
                           posts=posts_to_show,
                           page=page,
                           posts_before=posts_before,
                           posts_after=posts_after,
                           previous_page_path=previous_page_path,
                           next_page_path=next_page_path,
                           **common_values())


@app.route('/posts/<post_id>')
@app.route('/posts/<post_id>/<title>')
def show_post(post_id, title):
    accept_language = request.headers.get('Accept-Language')
    user_languages = utils.parse_accept_language(accept_language)
    post = database.get_post_by_id(post_id)
    selected_language = utils.choose_language(list(post['translations'].keys()), user_languages)
    if selected_language is None:
        abort(404)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
    languages = database.get_languages_by_codes(*language_codes)
    url = make_external('posts/{}/{}'.format(post['id'],
                                             utils.urlify(post['translations'][selected_language]['title'])))
    post['external_url'] = url
    return render_template('post.html',
                           post=post,
                           selected_language=selected_language,
                           languages=languages,
                           **common_values())


@app.route('/drafts/<draft_id>')
def show_draft(draft_id):
    selected_language = request.args.get('lang', 'eng')
    post = database.get_post_by_id(draft_id)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
    languages = database.get_languages_by_codes(*language_codes)
    all_languages = database.get_all_languages()
    remaining_languages = utils.difference_of_dictionaries(all_languages, languages)
    for language in remaining_languages:
        post['translations'][language] = {'title': '', 'markdown': '', 'html': ''}
    return render_template('draft.html',
                           draft=post['draft'],
                           selected_language=selected_language,
                           languages=all_languages,
                           values=post['translations'],
                           tags=post['tags'],
                           post_id=post['id'],
                           **common_values())


@app.route('/posts/add')
@login_required
def add_post():
    return render_template('draft.html',
                           languages=database.get_all_languages(),
                           selected_language='eng',
                           **common_values())


@app.route('/drafts')
@login_required
def drafts_list():
    accept_language = request.headers.get('Accept-Language')
    user_languages = utils.parse_accept_language(accept_language)
    drafts = database.get_drafts()
    drafts_to_show = []
    for draft in drafts:
        language = utils.choose_language(list(draft['translations'].keys()), user_languages)
        if language is not None:
            draft['language'] = language
            drafts_to_show.append(draft)
    return render_template('drafts.html', posts=drafts_to_show, **common_values())


@app.route('/posts', methods=['POST'])
@login_required
def commit_post():
    post = {'translations': {}}
    language_codes = set()
    for key in request.form:
        if '$' in key:
            language_codes.add(key.split('$')[0])

    for language_code in language_codes:
        title = request.form.get(language_code + '$title', '')
        md = request.form.get(language_code + '$post', '')
        if title and md:
            post['translations'][language_code] = {
                'title': title,
                'markdown': md,
            }
    post_id = request.form.get('post-id', None)
    tags = request.form.get('tags')
    tags = tags.split(', ') if tags else []
    draft = bool(request.form.get('draft', False))
    if post_id:
        database.update_post(post_id, post['translations'], tags, draft)
    else:
        database.add_post(post['translations'], tags, draft)
    return redirect(url_for('index'))


@app.route('/atom.xml')
def atom():
    feed = AtomFeed('kovalev.engineer blog',
                    feed_url=request.url, url=request.url_root)
    posts = database.get_posts(limit=10)
    for post in posts:
        language = utils.choose_language(list(post['translations'].keys()), 'eng')
        feed.add(post['translations'][language]['title'],
                 post['translations'][language]['html'],
                 content_type='html',
                 author='Aleksandr Kovalev',
                 url=make_external('posts/{}/{}'.format(post['id'],
                                                        utils.urlify(post['translations'][language]['title']))),
                 updated=post['update_date'],
                 published=post['publish_date'])
    return feed.get_response()
