
from flask import Blueprint, abort, render_template

from webapp.description.map import get_map
from webapp.description.models import Detail, Visual
from webapp.extensions import db
from webapp.head.models import Route

blueprint = Blueprint('description', __name__)


@blueprint.route('/<int:pk>')
def detail(pk):
    maps_routes = db.session.get(Route, pk)
    if maps_routes is None:
        abort(404)
    detail_routes = db.session.scalar(
        db.select(Detail).filter_by(route_id=pk)
    )
    visuals = db.session.scalars(
        db.select(Visual).filter_by(route_id=pk)
    ).all()
    folium_map = get_map(pk)

    return render_template(
        "detail.html",
        maps_routes=maps_routes,
        detail_routes=detail_routes,
        visuals=visuals,
        folium_map=folium_map._repr_html_()
        )
