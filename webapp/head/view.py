from flask import Blueprint, render_template
from flask_admin import form

from webapp.extensions import db
from webapp.head.models import Route
from webapp.weather import weather_by_city

blueprint = Blueprint('head', __name__)


@blueprint.route('/')
def index():
    map_rout = db.session.scalars(db.select(Route)).all()
    weather = weather_by_city("Sochi, Russia")
    return render_template("index.html", map_rout=map_rout,
                           thumbnail=form.thumbgen_filename, weather=weather)
