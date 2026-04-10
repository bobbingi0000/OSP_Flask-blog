from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, GuestbookEntry  # noqa: F401 - test_app.py에서 재사용
from routes import register_routes

app = Flask(__name__)

# 테스트 시 덮어쓸 수 있도록 환경설정 허용
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get(
    'SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
register_routes(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
