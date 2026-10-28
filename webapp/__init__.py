from flask import Flask
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager
from sqlalchemy.orm import configure_mappers
from webapp.extensions import db, migrate
from webapp.user.model import User, ensure_demo_admin
from webapp.user.views import blueprint as user_blueprint
from webapp.admin import (
    CoordinateModelView, CoordinateformapModelView, DetailModelView,
    MapPreviewView, RouteImageView, SecureAdminIndex, VisualModelView,
)
from webapp.head.view import blueprint as head_blueprint
from webapp.load.view import blueprint as load_blueprint
from webapp.description.view import blueprint as description_blueprint
from webapp.head.models import Route
from webapp.weather import weather_by_city
from webapp.description.models import (Coordinate, Detail, Coordinateformap,
                                       Visual)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config["FLASK_ADMIN_SWATCH"] = 'cerulean'
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("В webapp/config.py не задан SECRET_KEY")
    app.register_blueprint(user_blueprint)
    register_extensions(app)
    Babel(app, locale_selector=lambda: "ru")
    admin = Admin(
        app,
        name="Маршруты",
        template_mode="bootstrap4",
        index_view=SecureAdminIndex(name="С чего начать", template="admin/dashboard.html"),
    )
    register_admin_views(admin)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(head_blueprint)
    app.register_blueprint(load_blueprint)
    app.register_blueprint(description_blueprint)

    @app.context_processor
    def inject_weather():
        city = app.config.get("WEATHER_DEFAULT_CITY", "Sochi, Russia")
        return {"weather": weather_by_city(city)}

    with app.app_context():
        ensure_demo_admin()

    return app


def register_admin_views(admin):
    """Подключает разделы в том порядке, в котором маршрут собирают."""
    configure_mappers()
    admin.add_view(RouteImageView(Route, db.session, name="Маршруты", endpoint="route"))
    admin.add_view(DetailModelView(Detail, db.session, name="Описание", endpoint="detail"))
    admin.add_view(CoordinateModelView(
        Coordinate, db.session, name="Линия на карте", endpoint="coordinate"
    ))
    admin.add_view(MapPreviewView(name="Карта", endpoint="mappreview"))
    admin.add_view(VisualModelView(Visual, db.session, name="Фото", endpoint="visual"))
    admin.add_view(CoordinateformapModelView(
        Coordinateformap, db.session, name="Метки на карте", endpoint="coordinateformap"
    ))


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    return None
