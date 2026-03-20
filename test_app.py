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

def test_guestbook_sql_injection_defense(client):
    """4. SQL Injection 방어 테스트 (SQLAlchemy ORM)"""
    malicious_sql = "' OR 1=1; DROP TABLE guestbook_entry; --"
    client.post('/guestbook', data={
        'author': 'SQLHacker',
        'content': malicious_sql
    })
    
    # 공격 쿼리가 실행되지 않고 단순 문자열로 취급되어 정상 저장되어야 함
    with app.app_context():
        count = GuestbookEntry.query.count()
        assert count > 0 # 테이블 파괴 안 됨
        entry = GuestbookEntry.query.filter_by(content=malicious_sql).first()
        assert entry is not None # 입력값이 이스케이프되어 온전히 저장됨

def test_guestbook_xss_defense(client):
    """5. XSS 공격 방어 테스트 (Jinja2 Auto-escape)"""
    xss_payload = '<script>alert("XSS")</script>'
    client.post('/guestbook', data={
        'author': 'XSSHacker',
        'content': xss_payload
    })
    
    response = client.get('/guestbook')
    html_data = response.data.decode('utf-8')
    
    # 렌더링 시 HTML 태그가 무효화(&lt;, &gt;) 되어야 함
    assert '&lt;script&gt;alert(' in html_data
    # 원본 페이로드(실행 가능한 형태)가 문서 안에 있으면 안 됨
    assert xss_payload not in html_data

def test_guestbook_post_length_limit(client):
    """6. 페이로드 크기 방어 테스트 (500자 초과)"""
    with app.app_context():
        initial_count = GuestbookEntry.query.count()
        
    long_content = "A" * 501
    response = client.post('/guestbook', data={
        'author': 'Spammer',
        'content': long_content
    })
    
    # 500 인터널 서버 에러가 나면 안 되고, 에러 메시지와 함께 정상 처리되거나 
    # 최소한 DB 저장이 차단되어야 함
    assert response.status_code in [200, 302, 400]
    
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count # DB에 추가되면 안 됨

def test_guestbook_post_whitespace_bypass(client):
    """7. 공백(Whitespace) 우회 방어 테스트"""
    with app.app_context():
        initial_count = GuestbookEntry.query.count()
        
    # 공백으로만 이루어진 데이터 전송
    response = client.post('/guestbook', data={
        'author': '   ',
        'content': '          '
    })
    
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        # 방명록이 비어있음에도 유령으로 등록되면 안 됨
        assert final_count == initial_count

def test_guestbook_get_pagination(client):
    """8. .all() 메소드로 인한 메모리 취약점 방어 테스트 (페이징)"""
    # 15개의 방명록 데이터를 강제로 밀어넣음
    with app.app_context():
        entries = [GuestbookEntry(author=f'User{i}', content=f'Test_Content_{i}') for i in range(15)]
        db.session.add_all(entries)
        db.session.commit()
    
    # 파라미터 없이 GET 요청 시, 최근 N개(에: 10개)까지만 가져와야 함
    response = client.get('/guestbook')
    html_data = response.data.decode('utf-8')
    
    # 최신 글인 14번재 글은 화면에 보여야 함
    assert 'Test_Content_14' in html_data
    # 10개씩 페이징 처리된다면 초창기 글인 0번째 글은 1페이지 화면에 보이면 안 됨 (RED 조건 발동 지점)
    assert 'Test_Content_0' not in html_data
