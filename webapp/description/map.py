from webapp.description.models import Coordinate, Coordinateformap
from webapp.extensions import db
import folium
from folium import IFrame
import base64
from pathlib import Path
import os


def get_map(pk):
    coordinates = db.session.scalars(
        db.select(Coordinate).filter_by(route_id=pk).order_by(Coordinate.order)
    ).all()
    coordinates_for_rout = db.session.scalars(
        db.select(Coordinateformap).filter_by(route_id=pk)
    ).all()
    loc = [(c.latitude, c.longitude) for c in coordinates]
    try:
        folium_map = folium.Map(location=loc[0],
                                zoom_start=13,
                                width="100%",
                                height=480
                                )

        polyline_options = {
            'color': 'blue',
            'weight': 5,
            'opacity': 0.8,
            }

        folium.PolyLine(loc, **polyline_options).add_to(folium_map)

        folium.Marker(
            location=loc[0],
            popup="Начало маршрута",
            icon=folium.Icon(icon='info-sign', color="red"),
            draggable=False).add_to(folium_map)

    except (IndexError):
        folium_map = folium.Map(location=[43.6, 40.2],
                                zoom_start=8,
                                width="100%",
                                height=480
                                )

    base_dir = Path(__file__).resolve().parent
    for coordinate_map in coordinates_for_rout:
        image_file = coordinate_map.image_for_map
        image_path = os.path.join(base_dir, '..', 'static', 'media',
                                  image_file)
        if not image_file or not os.path.isfile(image_path):
            continue
        title = f'{coordinate_map.title}'
        picture = base64.b64encode(open(image_path, 'rb').read()).decode()
        html = f'{title}<img src="data:image/JPG;base64,{picture}">'
        iframe = IFrame(html, width=632 + 20, height=420 + 20)
        popup = folium.Popup(iframe, max_width=1000)

        folium.Marker(
            location=(
                coordinate_map.latitude_for_image,
                coordinate_map.longitude_for_image
                ),
            popup=popup,
            icon=folium.Icon(icon='info-sign', color="blue"),
            draggable=False
            ).add_to(folium_map)

    return folium_map
