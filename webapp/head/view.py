from flask import Blueprint, render_template, request
from sqlalchemy import or_

from webapp.extensions import db
from webapp.head.models import Route

blueprint = Blueprint("head", __name__)

AREAS = ("Сочи", "Красная Поляна")
DIFFICULTIES = ("лёгкий", "средний", "сложный")


@blueprint.route("/")
def index():
    query = request.args.get("q", "").strip()
    area = request.args.get("area", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    stmt = db.select(Route).order_by(Route.id)
    if query:
        like = f"%{query}%"
        stmt = stmt.where(or_(
            Route.title.ilike(like),
            Route.description.ilike(like),
            Route.area.ilike(like),
        ))
    if area in AREAS:
        stmt = stmt.where(Route.area == area)
    if difficulty in DIFFICULTIES:
        stmt = stmt.where(Route.difficulty == difficulty)

    map_rout = db.session.scalars(stmt).all()
    return render_template(
        "index.html",
        map_rout=map_rout,
        query=query,
        area=area,
        difficulty=difficulty,
        areas=AREAS,
        difficulties=DIFFICULTIES,
    )
