from flask import render_template, request, redirect, url_for
from models import db, GuestbookEntry


def register_routes(app):
    # 1. 홈페이지
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
