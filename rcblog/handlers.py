from flask import Flask, render_template, request, redirect, url_for
from rcblog import utils


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/<int:post_id>')
def post(post_id):
    return utils.md_to_html(open('rcblog/templates/test.md').read())


@app.route('/posts/add')
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
