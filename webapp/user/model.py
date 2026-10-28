from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from webapp.extensions import db

# Эти же имя и пароль написаны в README. Пароль меняется только если пользователя ещё нет.
DEMO_ADMIN_USERNAME = "admin"
DEMO_ADMIN_PASSWORD = "kavkaz2026"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={} id={}>' .format(self.username, self.id)


def ensure_demo_admin():
    """Создаёт администратора admin, если такого имени в базе ещё нет."""
    if not inspect(db.engine).has_table("user"):
        return None
    existing = db.session.scalar(
        db.select(User).filter_by(username=DEMO_ADMIN_USERNAME)
    )
    if existing is not None:
        return existing
    admin = User(
        username=DEMO_ADMIN_USERNAME,
        email="admin@example.com",
        role="admin",
    )
    admin.set_password(DEMO_ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()
    return admin
