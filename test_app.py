import pytest
from app import app, db, GuestbookEntry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
    
    # 검증: 응답 코드가 200 OK 거나 302 Redirect
    assert response.status_code in [200, 302]
    
    # 검증: 데이터가 1개 증가하고 내용과 이름이 내가 보낸 것과 정확히 일치
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count + 1
        
        entry = GuestbookEntry.query.filter_by(author='Neo').first()
        assert entry is not None
        assert entry.content == 'Follow the white rabbit'


def test_guestbook_get_success(client):
    """2. 화면 정상 출력 테스트"""
    # 미리 2개의 데이터를 삽입
    with app.app_context():
        entry1 = GuestbookEntry(author='Trinity', content='Dodge this.')
        entry2 = GuestbookEntry(author='Morpheus', content='Welcome to the real world.')
        db.session.add_all([entry1, entry2])
        db.session.commit()
        
    response = client.get('/guestbook')
    
    # 검증: 응답 코드가 200 OK
    assert response.status_code == 200
    
    # 검증: HTML 텍스트 안에 DB에 넣은 내용이 포함되어 있는지
    html_data = response.data.decode('utf-8')
    assert 'Trinity' in html_data
    assert 'Dodge this.' in html_data
    assert 'Morpheus' in html_data
    assert 'Welcome to the real world.' in html_data


def test_guestbook_post_invalid(client):
    """3. 비정상 데이터 방어 테스트 (빈 값 검증)"""
    with app.app_context():
        initial_count = GuestbookEntry.query.count()
        
    # 작성자는 있지만 내용(content)이 빈 문자열인 경우
    response = client.post('/guestbook', data={
        'author': 'Agent Smith',
        'content': ''
    })
    
    # 검증: 잘못된 데이터이므로 DB Row 개수에 변동이 없어야 함
    with app.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count
