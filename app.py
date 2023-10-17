from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080/"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/', methods=['GET'])
@app.route('/posts', methods=['GET'])
def get_posts():
    articles = Article.query.all()
    articles_list = [{'id': article.id, 'title': article.title, 'text': article.text} for article in articles]

    return jsonify({'articles': articles_list})


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    article = Article.query.get(id)

    if article is not None:
        article_data = {
            'id': article.id,
            'title': article.title,
            'text': article.text
        }
        return jsonify(article_data)
    else:
        return jsonify({'error': 'Пост с указанным ID не найден.'})


@app.route('/add_article', methods=['POST'])
def add_article():
    if request.method == 'POST':
        data = request.json  # Предполагается, что данные отправлены в формате JSON

        if 'title' in data and 'text' in data:
            title = data['title']
            text = data['text']

            new_article = Article(title=title, text=text)

            try:
                db.session.add(new_article)
                db.session.commit()
                return jsonify({'message': 'Статья успешно добавлена в базу данных'})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Недостаточно данных. Пожалуйста, укажите title и text в JSON-запросе.'})


if __name__ == "__main__":
    app.run(debug=True)