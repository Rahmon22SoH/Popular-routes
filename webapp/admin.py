import os

from flask import redirect, request, url_for
from flask_admin import AdminIndexView, BaseView, expose, form
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import thumbgen_filename
from flask_login import current_user
from markupsafe import Markup
from wtforms import TextAreaField
from wtforms.validators import ValidationError

from webapp.extensions import db


file_path = os.path.join(os.path.dirname(__file__), "static", "media")
os.makedirs(file_path, exist_ok=True)

AREAS = [("Сочи", "Сочи"), ("Красная Поляна", "Красная Поляна")]
DIFFICULTIES = [
    ("лёгкий", "лёгкий"),
    ("средний", "средний"),
    ("сложный", "сложный"),
]


def _photo(view, context, model, name):
    """Показывает миниатюру файла из static/media."""
    filename = getattr(model, name, None)
    if not filename:
        return ""
    url = url_for("static", filename=f"media/{filename}")
    return Markup(
        f'<img src="{url}" alt="" style="max-height:64px;border-radius:6px">'
    )


def _media_name(filename):
    """Оставляет только имя файла, без пути."""
    name = os.path.basename(filename or "")
    if not name or name in {".", ".."}:
        return None
    return name


def _media_still_used(filename):
    """Проверяет, ссылается ли на файл другая запись."""
    from webapp.description.models import Coordinateformap, Visual
    from webapp.head.models import Route

    if db.session.scalar(db.select(Route.id).filter(Route.image == filename)):
        return True
    if db.session.scalar(db.select(Visual.id).filter(Visual.image == filename)):
        return True
    return db.session.scalar(
        db.select(Coordinateformap.id).filter(Coordinateformap.image_for_map == filename)
    ) is not None


def remove_media_file(filename):
    """Удаляет файл и миниатюру, если на них больше никто не ссылается."""
    name = _media_name(filename)
    if not name or _media_still_used(name):
        return
    for candidate in (name, thumbgen_filename(name)):
        path = os.path.join(file_path, candidate)
        if os.path.isfile(path):
            os.remove(path)


def _remember_files(model, names):
    """Запоминает файлы до удаления записи. Сотрём их после успешного сохранения."""
    model._media_to_remove = [_media_name(name) for name in names if _media_name(name)]


def _remove_remembered_files(model):
    for name in getattr(model, "_media_to_remove", ()):
        remove_media_file(name)


COORDINATE_HELP = """
<strong>Как добавить координаты линии.</strong>
<p>Каждая строка — одна точка. Карта соединяет их по полю «Порядок»: 0, затем 1, 2 и дальше до финиша. Нужны минимум две точки, иначе линии не будет.</p>
<ol>
<li>Откройте <a href="https://yandex.ru/maps" target="_blank" rel="noopener">Яндекс.Карты</a> или Google Maps и найдите место на тропе.</li>
<li>В Яндекс.Картах нажмите правой кнопкой по месту и выберите «Что здесь?». В Google Maps координаты стоят первой строкой меню по правому клику, их можно скопировать.</li>
<li>Пара выглядит так: <code>43.5492, 39.8231</code>. Первое число — широта, его пишите в поле «Широта». Второе — долгота.</li>
<li>Для Сочи и Красной Поляны широта около 43.5–43.7, долгота около 39.8–40.6. Если первое число около 40, поля перепутаны.</li>
<li>Пишите точку, не запятую: <code>43.55</code>, а не <code>43,55</code>.</li>
<li>Нажмите «Создать». Выберите маршрут. Порядок <code>0</code> — старт, следующая точка — <code>1</code>.</li>
<li>Кнопка «Сохранить и добавить новый объект» сразу открывает следующую точку того же маршрута.</li>
<li>Ставьте точки по ходу тропы: старт, развилка, перевал, финиш. Чем чаще точки на поворотах, тем точнее линия.</li>
</ol>
<p>Проверка — вкладка «Карта»: выберите маршрут и посмотрите линию, не открывая сайт.</p>
<p>Файл вместо ручного ввода: GeoJSON с линией (LineString) загружается на <code>/load/номер</code>, номер есть в списке маршрутов. В файле сначала долгота, потом широта — сайт ставит их сам. Повторная загрузка заменяет все точки этого маршрута, ручные тоже.</p>
<p>Пример формата, не готовая точка тропы: широта <code>43.55</code>, долгота <code>39.82</code>, порядок <code>0</code>.</p>
"""


class SecureAdminIndex(AdminIndexView):
    """Главная админки открыта только пользователю с ролью admin."""

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("user.login"))


class SecureModelView(ModelView):
    """Раздел админки с русской подсказкой и доступом только для admin."""

    help_html = ""
    list_template = "admin/model_help_list.html"
    create_template = "admin/model_help_create.html"
    edit_template = "admin/model_help_edit.html"
    can_view_details = True
    page_size = 20

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("user.login"))

    def render(self, template, **kwargs):
        kwargs["help_text"] = Markup(self.help_html)
        return super().render(template, **kwargs)


class RouteImageView(SecureModelView):
    column_list = ("title", "area", "difficulty", "distance_km", "duration", "image")
    column_searchable_list = ("title", "area")
    column_labels = {
        "title": "Название",
        "description": "Короткий текст",
        "video": "Видео",
        "image": "Обложка",
        "area": "Район",
        "difficulty": "Сложность",
        "distance_km": "Километры",
        "duration": "Сколько идти",
    }
    column_formatters = {"image": _photo}
    form_columns = (
        "title", "area", "difficulty", "distance_km", "duration",
        "description", "image", "video",
    )
    form_choices = {"area": AREAS, "difficulty": DIFFICULTIES}
    form_extra_fields = {
        "image": form.ImageUploadField(
            "Обложка",
            base_path=file_path,
            url_relative_path="media/",
            thumbnail_size=(320, 240, True),
            description="JPG или PNG. Это фото карточки на главной.",
        ),
        "description": TextAreaField(
            "Короткий текст",
            description="Одно-два предложения под названием на главной.",
        ),
        "video": TextAreaField(
            "Видео",
            description="Необязательно. Ссылка на YouTube, RuTube или VK либо HTML-код iframe. Ролик появится на странице маршрута.",
        ),
    }
    form_args = {
        "title": {"description": "Как маршрут называется в каталоге."},
        "area": {"description": "От этого значения зависит фильтр «Сочи» или «Красная Поляна» на главной."},
        "difficulty": {"description": "Фильтр на главной понимает только эти три слова."},
        "distance_km": {"description": "Число, например 8."},
        "duration": {"description": "Как на сайте: «4–5 часов» или «2 дня»."},
    }
    help_html = (
        "<strong>Карточка маршрута.</strong> Сначала создайте её здесь. "
        "Без этой записи описание, линия и фото не к чему привязать. "
        "Нажмите «Создать», заполните название, район и сложность, приложите обложку."
    )

    def on_model_delete(self, model):
        """Удаляет описание, линию, фото и метки вместе с карточкой."""
        names = [model.image]
        names.extend(item.image for item in model.visuals)
        names.extend(item.image_for_map for item in model.coordinateformap)
        _remember_files(model, names)
        related = (
            list(model.detail)
            + list(model.coordinates)
            + list(model.visuals)
            + list(model.coordinateformap)
        )
        for item in related:
            db.session.delete(item)

    def after_model_delete(self, model):
        """Стирает файлы обложки, галереи и меток, когда запись уже удалена."""
        _remove_remembered_files(model)


class DetailModelView(SecureModelView):
    column_list = ("route", "routestart", "workingmode")
    column_labels = {
        "route": "Маршрут",
        "description_start": "Что увидите",
        "description_basic": "Кому подходит",
        "routestart": "Откуда старт",
        "workingmode": "Когда идти",
        "order": "Порядок",
    }
    form_columns = (
        "route", "description_start", "description_basic",
        "routestart", "workingmode", "order",
    )
    form_overrides = {
        "description_start": TextAreaField,
        "description_basic": TextAreaField,
        "routestart": TextAreaField,
        "workingmode": TextAreaField,
    }
    form_args = {
        "route": {"description": "Выберите уже созданный маршрут. Одно описание на маршрут."},
        "description_start": {"label": "Что увидите", "description": "Абзац про саму тропу."},
        "description_basic": {"label": "Кому подходит", "description": "Сложность, обувь, нужен ли пропуск."},
        "routestart": {"label": "Откуда старт", "description": "Остановка, кордон или вход в долину."},
        "workingmode": {"label": "Когда идти", "description": "Сезон и когда тропу закрывают."},
        "order": {"description": "Оставьте 1, если описание одно."},
    }
    help_html = (
        "<strong>Текст страницы маршрута.</strong> Откройте «Создать», "
        "в списке «Маршрут» выберите карточку из первой вкладки и заполните четыре текста. "
        "Километры и сложность сюда не пишите: они задаются в карточке маршрута."
    )

    def on_model_change(self, form, model, is_created):
        """Не даёт привязать второе описание к тому же маршруту."""
        from webapp.description.models import Detail

        if not model.route_id:
            raise ValidationError("Сначала выберите маршрут.")
        existing = db.session.scalar(
            db.select(Detail).filter_by(route_id=model.route_id)
        )
        if existing is not None and existing.id != model.id:
            raise ValidationError(
                "У этого маршрута уже есть описание. Откройте его в списке и поправьте."
            )


class CoordinateModelView(SecureModelView):
    column_list = ("route", "order", "latitude", "longitude")
    column_default_sort = ("order", False)
    column_labels = {
        "route": "Маршрут",
        "latitude": "Широта",
        "longitude": "Долгота",
        "order": "Порядок",
    }
    form_columns = ("route", "order", "latitude", "longitude")
    form_args = {
        "route": {"description": "Маршрут, для которого рисуется линия."},
        "order": {"description": "0 — старт, дальше 1, 2, 3 до финиша."},
        "latitude": {"description": "Для Сочи и Красной Поляны это число около 43.5–43.7."},
        "longitude": {"description": "Около 39.8 у Сочи и около 40.1–40.6 у Красной Поляны."},
    }
    help_html = COORDINATE_HELP


class VisualModelView(SecureModelView):
    column_list = ("route", "title", "image")
    column_labels = {
        "route": "Маршрут",
        "title": "Подпись",
        "body": "Пояснение",
        "image": "Фото",
    }
    column_formatters = {"image": _photo}
    form_columns = ("route", "title", "body", "image")
    form_extra_fields = {
        "image": form.ImageUploadField(
            "Фото",
            base_path=file_path,
            url_relative_path="media/",
            thumbnail_size=(520, 520, True),
            description="Снимок для галереи на странице маршрута.",
        ),
        "body": TextAreaField(
            "Пояснение",
            description="Короткая подпись под фото. На сайте виден в основном заголовок.",
        ),
    }
    form_args = {
        "route": {"description": "К какому маршруту относится снимок."},
        "title": {"description": "Подпись, например «Нижний каскад»."},
    }
    help_html = (
        "<strong>Галерея.</strong> Создайте отдельную запись на каждое фото. "
        "Выберите маршрут, напишите подпись и загрузите файл. "
        "Обложка карточки задаётся не здесь, а во вкладке «Маршруты»."
    )

    def on_model_delete(self, model):
        """Запоминает файл галереи перед удалением записи."""
        _remember_files(model, [model.image])

    def after_model_delete(self, model):
        """Удаляет файл, если его не использует другая запись."""
        _remove_remembered_files(model)


class CoordinateformapModelView(SecureModelView):
    column_list = ("route", "title", "order", "latitude_for_image", "longitude_for_image", "image_for_map")
    column_labels = {
        "route": "Маршрут",
        "title": "Подпись метки",
        "latitude_for_image": "Широта",
        "longitude_for_image": "Долгота",
        "image_for_map": "Фото метки",
        "order": "Порядок",
    }
    column_formatters = {"image_for_map": _photo}
    form_columns = (
        "route", "title", "order", "latitude_for_image",
        "longitude_for_image", "image_for_map",
    )
    form_extra_fields = {
        "image_for_map": form.ImageUploadField(
            "Фото метки",
            base_path=file_path,
            url_relative_path="media/",
            thumbnail_size=(520, 520, True),
            description="Откроется во всплывающем окне на карте.",
        )
    }
    form_args = {
        "route": {"description": "Маршрут, на карте которого стоит метка."},
        "title": {"description": "Текст рядом с фото, например «Нижний водопад»."},
        "order": {"description": "Если меток несколько, 0 — первая."},
        "latitude_for_image": {"description": "Около 43.5–43.7, не долгота."},
        "longitude_for_image": {"description": "Около 39.8–40.6."},
    }
    help_html = (
        "<strong>Метка с фото на карте.</strong> Это не линия, а одна точка с картинкой. "
        "Линию задают во вкладке «Линия на карте». Здесь выберите маршрут, "
        "поставьте широту и долготу места и загрузите фото."
    )

    def on_model_delete(self, model):
        """Запоминает фото метки перед удалением записи."""
        _remember_files(model, [model.image_for_map])

    def after_model_delete(self, model):
        """Удаляет файл метки, если его не использует другая запись."""
        _remove_remembered_files(model)


class MapPreviewView(BaseView):
    """Та же карта, что на сайте, чтобы проверить линию не выходя из админки."""

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("user.login"))

    @expose("/")
    def index(self):
        from webapp.description.map import get_map
        from webapp.head.models import Route

        routes = db.session.scalars(db.select(Route).order_by(Route.title)).all()
        route_id = request.args.get("route_id", type=int)
        chosen = db.session.get(Route, route_id) if route_id else None
        if chosen is None and routes:
            chosen = routes[0]
        folium_html = None
        if chosen is not None:
            folium_html = Markup(get_map(chosen.id)._repr_html_())
        return self.render(
            "admin/map_preview.html",
            routes=routes,
            chosen=chosen,
            folium_html=folium_html,
        )
