from datetime import datetime
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session,
    jsonify,
    abort,
)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'keep it secret, keep it safe!'
})


class Post(object):
    def __init__(self, body, author):
        self.body = body
        self.author = author
        self.date = datetime.utcnow()

    def to_json(self):
        return {
            'body': self.body,
            'author': self.author,
            'date': self.date.strftime('%H:%M:%S')
        }


POSTS = [
    Post('Hello flask!', 'Trevor')
]


@app.route('/')
def index():
    return render_template('index.html',
        posts = POSTS,
        author = session.get('author', '')
    )


@app.route('/author/<author>')
def show_author(author):
    author = author.lower()
    posts = [p for p in POSTS if p.author.lower() == author]

    if not posts:
        abort(404)

    return render_template('index.html',
        posts = posts,
        author = session.get('author', ''),
        show_author = author,
    )


@app.route('/error')
def raise_error():
    raise Exception("Don't panic!")


@app.route('/posts', methods=['GET'])
def get_posts():
    author = request.args.get('author', '').lower()
    posts = reversed(POSTS)

    if author:
        posts = [p for p in posts if p.author.lower() == author]

    return jsonify(posts=[post.to_json() for post in posts])


@app.route('/posts', methods=['POST'])
def add_post():
    post = Post(request.form['body'], request.form['author'])
    POSTS.append(post)
    session['author'] = post.author
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
