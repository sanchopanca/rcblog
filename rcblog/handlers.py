from flask import Flask, render_template
import markdown


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/<int:post_id>')
def post(post_id):
    return markdown.markdown(open('rcblog/templates/test.md').read(),
                             ['markdown.extensions.extra'])
