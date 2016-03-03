from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bower import Bower
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from rcblog import utils
from rcblog import crypto
from rcblog.db import DataBase
from rcblog.user import User

database = DataBase()

app = Flask(__name__)
app.secret_key = 'so_secret'
Bower(app)
login_manager = LoginManager()
login_manager.init_app(app)


def common_values():
    return {
        'logged_in': current_user.is_authenticated,
    }


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
                user = User.get_by_id('1')  # TODO refactor
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
    tag = request.args.get('tag')
    if tag:
        posts = database.get_posts_by_tag(tag)
    else:
        posts = database.get_all_posts()
    for post in posts:
        for language, translation in post['translations'].items():
            translation['html'] = utils.md_to_html(translation['markdown'])

    return render_template('posts.html', posts=posts, **common_values())


@app.route('/posts/<post_id>')
def show_post(post_id):
    selected_language = request.args.get('lang', 'eng')
    post = database.get_post_by_id(post_id)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
        translation['html'] = utils.md_to_html(translation['markdown'])
    languages = database.get_languages_by_codes(*language_codes)
    return render_template('post.html',
                           post=post,
                           selected_language=selected_language,
                           languages=languages,
                           current_address='/posts/{}'.format(post_id),
                           **common_values())


@app.route('/drafts/<draft_id>')
def show_draft(draft_id):
    selected_language = request.args.get('lang', 'eng')
    post = database.get_post_by_id(draft_id)
    language_codes = []
    for language, translation in post['translations'].items():
        language_codes.append(language)
        translation['html'] = utils.md_to_html(translation['markdown'])
    languages = database.get_languages_by_codes(*language_codes)
    all_languages = database.get_all_languages()
    remaining_languages = utils.difference_of_dictionaries(all_languages, languages)
    for language in remaining_languages:
        post['translations'][language] = {'title': '', 'markdown': '', 'html': ''}
    return render_template('draft.html',
                           post=post,
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
    drafts = database.get_all_drafts()
    for draft in drafts:
        for language, translation in draft['translations'].items():
            translation['html'] = utils.md_to_html(translation['markdown'])

    return render_template('drafts.html', posts=drafts, **common_values())


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
