import pytest
from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ==========================================
# 1. 앱 내부 로직 (GREEN 달성을 위한 구현)
# ==========================================
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        
        # 3번 시나리오 (Edge Case): author나 content가 빈 값이면 저장 불가
        if author and content:
            entry = GuestbookEntry(author=author, content=content)
            db.session.add(entry)
            db.session.commit()
            
        return redirect(url_for('guestbook'))
        
    # GET 시나리오: DB에서 데이터 불러오기
    entries = GuestbookEntry.query.order_by(GuestbookEntry.created_at.desc()).all()
    
    # guestbook.html 파일 대신, test_app.py 안에서 결과 검증이 가능하도록 임시 템플릿 사용
    template = '''
    {% for entry in entries %}
        [{{ entry.author }}] : {{ entry.content }}
    {% endfor %}
    '''
    return render_template_string(template, entries=entries)

# ==========================================
# 2. 테스트 환경 설정 및 테스트 케이스
# ==========================================
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_guestbook_post_success(client):
    """1. 정상 데이터 저장 테스트"""
    with app.app_context():
        initial_count = GuestbookEntry.query.count()
        
    response = client.post('/guestbook', data={
        'author': 'Neo',
        'content': 'Follow the white rabbit'
    })
    
    assert response.status_code in [200, 302]
    
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count + 1
        
        entry = GuestbookEntry.query.filter_by(author='Neo').first()
        assert entry is not None
        assert entry.content == 'Follow the white rabbit'

def test_guestbook_get_success(client):
    """2. 화면 정상 출력 테스트"""
    with app.app_context():
        entry1 = GuestbookEntry(author='Trinity', content='Dodge this.')
        entry2 = GuestbookEntry(author='Morpheus', content='Welcome to the real world.')
        db.session.add_all([entry1, entry2])
        db.session.commit()
        
    response = client.get('/guestbook')
    assert response.status_code == 200
    
    html_data = response.data.decode('utf-8')
    assert 'Trinity' in html_data
    assert 'Dodge this.' in html_data
    assert 'Morpheus' in html_data
    assert 'Welcome to the real world.' in html_data

def test_guestbook_post_invalid(client):
    """3. 비정상 데이터 방어 테스트 (빈 값 발생 시 DB 변동 없음)"""
    with app.app_context():
        initial_count = GuestbookEntry.query.count()
        
    response = client.post('/guestbook', data={
        'author': 'Agent Smith',
        'content': ''
    })
    
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count
