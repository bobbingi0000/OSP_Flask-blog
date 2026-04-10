"""Guestbook feature test module.

Contains 8 test cases using pytest to verify the Y2K blog's
Guestbook functionality. Uses an in-memory SQLite database
to ensure test isolation.
"""

import pytest
from app import create_app
from app.models import db, GuestbookEntry


class TestConfig:
    """Test-only configuration class.

    Uses an in-memory SQLite database to ensure isolation
    between tests.

    Attributes:
        TESTING (bool): Enables Flask test mode. Defaults to True.
        SQLALCHEMY_DATABASE_URI (str): In-memory SQLite path.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables modification
            tracking. Defaults to False.
    """

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


@pytest.fixture
def client():
    """Test client fixture.

    Creates a fresh Flask app and in-memory DB for each test,
    and tears down after the test completes.

    Yields:
        FlaskClient: A Flask test client instance.
    """
    application = create_app(TestConfig)
    with application.test_client() as test_client:
        with application.app_context():
            db.create_all()
        yield test_client
        with application.app_context():
            db.drop_all()


@pytest.fixture
def app_context():
    """Application context fixture.

    Yields:
        Flask: A Flask app instance with an active ``app_context()``.
    """
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.drop_all()


def test_guestbook_post_success(client):
    """1. Successful data persistence test."""
    application = client.application
    with application.app_context():
        initial_count = GuestbookEntry.query.count()

    response = client.post('/guestbook', data={
        'author': 'Neo',
        'content': 'Follow the white rabbit'
    })

    assert response.status_code in [200, 302]

    with application.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count + 1

        entry = GuestbookEntry.query.filter_by(author='Neo').first()
        assert entry is not None
        assert entry.content == 'Follow the white rabbit'


def test_guestbook_get_success(client):
    """2. Successful page rendering test."""
    application = client.application
    with application.app_context():
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
    """3. Invalid data defense test (empty values should not alter DB)."""
    application = client.application
    with application.app_context():
        initial_count = GuestbookEntry.query.count()

    response = client.post('/guestbook', data={
        'author': 'Agent Smith',
        'content': ''
    })

    with application.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count


def test_guestbook_sql_injection_defense(client):
    """4. SQL Injection defense test (SQLAlchemy ORM)."""
    application = client.application
    malicious_sql = "' OR 1=1; DROP TABLE guestbook_entry; --"
    client.post('/guestbook', data={
        'author': 'SQLHacker',
        'content': malicious_sql
    })

    # Attack query should not execute; it should be stored as a plain string
    with application.app_context():
        count = GuestbookEntry.query.count()
        assert count > 0  # Table not destroyed
        entry = GuestbookEntry.query.filter_by(content=malicious_sql).first()
        assert entry is not None  # Input escaped and stored intact


def test_guestbook_xss_defense(client):
    """5. XSS attack defense test (Jinja2 Auto-escape)."""
    xss_payload = '<script>alert("XSS")</script>'
    client.post('/guestbook', data={
        'author': 'XSSHacker',
        'content': xss_payload
    })

    response = client.get('/guestbook')
    html_data = response.data.decode('utf-8')

    # HTML tags should be neutralized (&lt;, &gt;) when rendered
    assert '&lt;script&gt;alert(' in html_data
    # The raw payload (executable form) should not appear in the document
    assert xss_payload not in html_data


def test_guestbook_post_length_limit(client):
    """6. Payload size defense test (over 500 characters)."""
    application = client.application
    with application.app_context():
        initial_count = GuestbookEntry.query.count()

    long_content = "A" * 501
    response = client.post('/guestbook', data={
        'author': 'Spammer',
        'content': long_content
    })

    # Should not cause a 500 Internal Server Error; must be handled gracefully
    assert response.status_code in [200, 302, 400]

    with application.app_context():
        final_count = GuestbookEntry.query.count()
        assert final_count == initial_count  # Should not be added to DB


def test_guestbook_post_whitespace_bypass(client):
    """7. Whitespace bypass defense test."""
    application = client.application
    with application.app_context():
        initial_count = GuestbookEntry.query.count()

    # Submit data consisting only of whitespace
    response = client.post('/guestbook', data={
        'author': '   ',
        'content': '          '
    })

    with application.app_context():
        final_count = GuestbookEntry.query.count()
        # Should not register a ghost entry with empty content
        assert final_count == initial_count


def test_guestbook_get_pagination(client):
    """8. Memory vulnerability defense test via .all() method (pagination)."""
    application = client.application
    # Force-insert 15 guestbook entries
    with application.app_context():
        entries = [GuestbookEntry(author=f'User{i}', content=f'Test_Content_{i}') for i in range(15)]
        db.session.add_all(entries)
        db.session.commit()

    # GET request without parameters should return at most N (e.g., 10) entries
    response = client.get('/guestbook')
    html_data = response.data.decode('utf-8')

    # The most recent entry (#14) should be visible
    assert 'Test_Content_14' in html_data
    # With 10-per-page pagination, the earliest entry (#0) should not appear on page 1
    assert 'Test_Content_0' not in html_data
