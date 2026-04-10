from flask import render_template, request, redirect, url_for
from models import db, GuestbookEntry


def register_routes(app):
    # 1. 홈페이지
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html')

    # 2. 글쓰기 페이지
    # TODO: Post 모델 구현 후 DB 저장 기능 활성화 예정 (feature_ready=True로 전환)
    @app.route('/write', methods=['GET', 'POST'])
    def write():
        if request.method == 'POST':
            title = request.form.get('title')
            return render_template('write.html', title=title, feature_ready=False)
        return render_template('write.html', feature_ready=False)

    # 3. 방명록 페이지
    @app.route('/guestbook', methods=['GET', 'POST'])
    def guestbook():
        if request.method == 'POST':
            author = request.form.get('author', '').strip()
            content = request.form.get('content', '').strip()

            if not author or not content:
                return redirect(url_for('guestbook'))
            if len(author) > 50 or len(content) > 500:
                return redirect(url_for('guestbook'))

            entry = GuestbookEntry(author=author, content=content)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('guestbook'))

        entries = GuestbookEntry.query.order_by(GuestbookEntry.created_at.desc()).limit(10).all()
        return render_template('guestbook.html', entries=entries)
