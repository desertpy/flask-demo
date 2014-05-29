from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
)


app = Flask(__name__)
app.config.update({})


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
    Post('hello hipflask!', 'Trevor of the desertpy group people')
]


@app.route('/')
def index():
    return render_template('index.html', posts=POSTS)


@app.route('/posts', methods=['POST'])
def add_post():
    post = Post(request.form['body'], request.form['author'])
    POSTS.append(post)
    return redirect(url_for('index'))


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = reversed(POSTS)
    return jsonify(posts=[p.to_json() for p in posts])


@app.route('/error')
def raise_hell():
    the_answer = 42
    raise Exception("don't panic")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242)
