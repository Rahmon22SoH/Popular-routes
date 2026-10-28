
from flask import Blueprint, render_template

from webapp.description.map import get_map
from webapp.description.models import Detail
from webapp.extensions import db
from webapp.head.models import Route

blueprint = Blueprint('description', __name__)


@blueprint.route('/<int:pk>')
def detail(pk):
    maps_routes = db.session.get(Route, pk)
    detail_routes = db.session.scalar(
        db.select(Detail).filter_by(route_id=pk)
    )
    folium_map = get_map(pk)

    return render_template(
        "detail.html",
        maps_routes=maps_routes,
        detail_routes=detail_routes,
        folium_map=folium_map._repr_html_()
        )
