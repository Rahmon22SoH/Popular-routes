import json

from flask import Blueprint, flash, redirect, render_template, request

from webapp.description.models import Coordinate
from webapp.extensions import db
from webapp.head.models import Route
from webapp.user.decorators import admin_required


blueprint = Blueprint('load', __name__)


@blueprint.route('/load/<int:pk>', methods=['GET', 'POST'])
@admin_required
def upload_file(pk):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file:
            read_file = file.read().decode('utf-8')
            coordinate_for_file = json.loads(read_file)
            route = next(iter(coordinate_for_file.get("features", [])), None)
            route_coordinates = route.get('geometry', {}).get('coordinates',
                                                              [])
            route = db.session.get(Route, pk)

            for position, coordinates in enumerate(route_coordinates):
                coordinates = Coordinate(
                    latitude=coordinates[1],
                    longitude=coordinates[0],
                    route_id=route.id,
                    order=position)
                db.session.add(coordinates)
            db.session.commit()
    return render_template("download.html")
