from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# 테스트 시 덮어쓸 수 있도록 환경설정 허용
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'app.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 1. 홈 페이지
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# 2. 글쓰기 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        return render_template('write.html', title=title)
    return render_template('write.html')

# 3. 방명록 페이지
@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        
        if author is not None and content is not None:
            author = author.strip()
            content = content.strip()
            
            if len(author) > 0 and len(content) > 0 and len(author) <= 50 and len(content) <= 500:
                entry = GuestbookEntry(author=author, content=content)
                db.session.add(entry)
                db.session.commit()
            
        return redirect(url_for('guestbook'))
        
    entries = GuestbookEntry.query.order_by(GuestbookEntry.created_at.desc()).limit(10).all()
    return render_template('guestbook.html', entries=entries)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
