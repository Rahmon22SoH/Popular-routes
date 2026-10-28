from urllib.parse import parse_qs, urlparse

from flask import Blueprint, abort, render_template
from markupsafe import Markup, escape

from webapp.description.map import get_map
from webapp.description.models import Detail, Visual
from webapp.extensions import db
from webapp.head.models import Route

blueprint = Blueprint("description", __name__)


def video_embed(raw):
    """Готовит ролик для страницы маршрута: ссылку или код iframe.

    Ссылка на YouTube и RuTube становится встроенным роликом.
    Остальные http-ссылки показываются как ссылка. Код со script не выводится.
    """
    text = (raw or "").strip()
    if not text or "<script" in text.lower():
        return ""
    lowered = text.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        embed = _embed_url(text)
        if embed:
            src = escape(embed)
            return Markup(
                f'<iframe src="{src}" title="Видео маршрута" '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                f'gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>'
            )
        safe = escape(text)
        if lowered.split("?", 1)[0].endswith((".mp4", ".webm", ".ogg")):
            return Markup(f'<video controls src="{safe}"></video>')
        return Markup(f'<p><a href="{safe}">Открыть видео</a></p>')
    if "<iframe" in lowered or "<video" in lowered:
        return Markup(text)
    return ""


def _embed_url(url):
    """Превращает адрес страницы ролика в адрес для iframe."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
        return f"https://www.youtube.com/embed/{video_id}" if video_id else None
    if host in {"youtube.com", "m.youtube.com", "youtube-nocookie.com"}:
        if parsed.path.startswith("/embed/"):
            return url
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        return f"https://www.youtube.com/embed/{video_id}" if video_id else None
    if host == "rutube.ru":
        parts = [part for part in parsed.path.split("/") if part]
        if "video" in parts:
            index = parts.index("video") + 1
            video_id = parts[index] if index < len(parts) else ""
            return f"https://rutube.ru/play/embed/{video_id}" if video_id else None
        if parsed.path.startswith("/play/embed/"):
            return url
    return None


@blueprint.route("/<int:pk>")
def detail(pk):
    """Страница маршрута: текст, галерея, ролик и карта."""
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
        folium_map=folium_map._repr_html_(),
        video_html=video_embed(maps_routes.video),
    )
