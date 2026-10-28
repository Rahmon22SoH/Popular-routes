import json

from flask import Blueprint, abort, flash, redirect, render_template, request

from webapp.description.models import Coordinate
from webapp.extensions import db
from webapp.head.models import Route
from webapp.user.decorators import admin_required


blueprint = Blueprint("load", __name__)


def _line_points(payload):
    """Достаёт пары широта/долгота из GeoJSON LineString.

    В файле координата записана как долгота, широта. На сайт уходит наоборот.
    """
    geometry = {}
    if isinstance(payload, dict) and payload.get("type") == "FeatureCollection":
        feature = next(iter(payload.get("features") or []), None) or {}
        geometry = feature.get("geometry") or {}
    elif isinstance(payload, dict) and payload.get("type") == "LineString":
        geometry = payload
    points = []
    for point in geometry.get("coordinates") or []:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            continue
        longitude, latitude = float(point[0]), float(point[1])
        points.append((latitude, longitude))
    return points


@blueprint.route("/load/<int:pk>", methods=["GET", "POST"])
@admin_required
def upload_file(pk):
    """Заменяет линию маршрута точками из файла GeoJSON."""
    route = db.session.get(Route, pk)
    if route is None:
        abort(404)
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded is None or uploaded.filename == "":
            flash("Выберите файл GeoJSON.")
            return redirect(request.url)
        try:
            payload = json.loads(uploaded.read().decode("utf-8"))
            points = _line_points(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
            flash("Файл не читается как GeoJSON с линией.")
            return redirect(request.url)
        if not points:
            flash("В файле нет линии. Нужна геометрия LineString.")
            return redirect(request.url)
        for old_point in list(route.coordinates):
            db.session.delete(old_point)
        for position, (latitude, longitude) in enumerate(points):
            db.session.add(Coordinate(
                latitude=latitude,
                longitude=longitude,
                route_id=route.id,
                order=position,
            ))
        db.session.commit()
        flash(f"Линия обновлена: {len(points)} точек. Старые точки этого маршрута заменены.")
        return redirect(request.url)
    return render_template("download.html", route=route)
