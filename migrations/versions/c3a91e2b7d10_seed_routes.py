"""Поля фильтра и стартовые маршруты заповедника.

Revision ID: c3a91e2b7d10
Revises: 55f757a26d67
Create Date: 2026-10-28 19:55:00
"""
from alembic import op
import sqlalchemy as sa


revision = "c3a91e2b7d10"
down_revision = "55f757a26d67"
branch_labels = None
depends_on = None


ROUTES = [
    {
        "title": "Агурские водопады",
        "area": "Сочи",
        "difficulty": "лёгкий",
        "distance_km": 3,
        "duration": "2–3 часа",
        "image": "agur.jpg",
        "description": "Короткий выход к каскаду водопадов в ущелье реки Агура. Удобный маршрут на полдня рядом с Сочи.",
        "description_start": "Тропа идёт по ущелью среди самшита и скал. По пути три основных каскада, смотровые площадки и купель у нижнего водопада.",
        "description_basic": "Маршрут подходит для первой прогулки в горы. Обувь нужна с протектором: после дождя камни скользкие. На территорию заповедника берут пропуск.",
        "routestart": "Старт от остановки «Спутник» или от ворот Агурского ущелья. Дальше одна тропа вверх по реке, без развилок на сами водопады.",
        "workingmode": "Светлое время суток. Зимой и после ливней часть лестниц закрывают.",
        "photos": [
            ("agur.jpg", "Нижний каскад", "Первый водопад, до него доходят почти все."),
            ("agurskie_vodopady_3.jpg", "Верхние каскады", "Выше по ущелью тропа становится уже."),
        ],
        "line": [(43.5458, 39.8095), (43.5482, 39.8168), (43.5514, 39.8232)],
        "points": [(43.5514, 39.8232, "Нижний водопад", "agur.jpg")],
    },
    {
        "title": "Орлиные скалы",
        "area": "Сочи",
        "difficulty": "лёгкий",
        "distance_km": 2,
        "duration": "1–2 часа",
        "image": "orlinie-skaly-3-min.jpg",
        "description": "Смотровая над ущельем Агуры. Короткий подъём и вид на каньон, море остаётся за хребтом.",
        "description_start": "Скалы стоят над каньоном. С площадки видно русло Агуры и стену леса на противоположном склоне.",
        "description_basic": "Идти можно вместе с Агурскими водопадами: это соседняя тропа. С детьми удобнее остановиться на нижней смотровой.",
        "routestart": "От развилки в Агурском ущелье указатель «Орлиные скалы». Подъём короткий, но крутой.",
        "workingmode": "Круглый год в ясную погоду. В грозу на скалы не выходят.",
        "photos": [
            ("orlinie-skaly-3-min.jpg", "Смотровая", "Основная точка маршрута."),
            ("orlin_skal.jpg", "Каньон", "Вид вниз по ущелью."),
        ],
        "line": [(43.5488, 39.8255), (43.5510, 39.8310), (43.5524, 39.8348)],
        "points": [(43.5524, 39.8348, "Орлиные скалы", "orlinie-skaly-3-min.jpg")],
    },
    {
        "title": "Ачипсинские водопады",
        "area": "Красная Поляна",
        "difficulty": "средний",
        "distance_km": 8,
        "duration": "4–5 часов",
        "image": "achipsinskie-vodopady-sochi-1024x576.jpg",
        "description": "Долина реки Ачипсе у Красной Поляны: лес, пороги и несколько водопадов по одной тропе.",
        "description_start": "Тропа начинается в долине и набирает высоту вдоль реки. Водопады открываются по очереди, самый заметный — в конце прогулочной части.",
        "description_basic": "Набор высоты умеренный, но день получается длинным. Возьмите воду и куртку: в ущелье прохладнее, чем на поляне.",
        "routestart": "Красная Поляна, вход в долину Ачипсе. До старта удобнее доехать до посёлка, дальше пешком.",
        "workingmode": "Лучше с мая по октябрь. Весной тропу размывает.",
        "photos": [
            ("achipsinskie-vodopady-sochi-1024x576.jpg", "Водопад", "Один из каскадов на Ачипсе."),
            ("achipsk.jpg", "Долина", "Река между склонами."),
        ],
        "line": [(43.5960, 40.0550), (43.6015, 40.0680), (43.6070, 40.0790)],
        "points": [(43.6070, 40.0790, "Водопад на Ачипсе", "achipsk.jpg")],
    },
    {
        "title": "Бзерпинский карниз",
        "area": "Красная Поляна",
        "difficulty": "сложный",
        "distance_km": 14,
        "duration": "7–8 часов",
        "image": "bzerp.jpg",
        "description": "Хребет над Красной Поляной. Длинный день с набором высоты и видом на Главный Кавказский хребет.",
        "description_start": "Карниз — узкая тропа по склону хребта Аибга. С него видно долину Мзымты и снежные вершины.",
        "description_basic": "Нужна целодневная готовность: перепад высоты большой, погода на гребне меняется быстро. Это уже не прогулка у Сочи.",
        "routestart": "Красная Поляна, подъём в сторону хребта Аибга. Точную точку старта лучше сверить с пропуском заповедника.",
        "workingmode": "Июнь–сентябрь, только в устойчивую погоду. Зимой маршрут лавиноопасный.",
        "photos": [
            ("bzerp.jpg", "Хребет", "Склон над долиной."),
            ("verh.jpg", "Верхняя точка", "Вид ближе к гребню."),
        ],
        "line": [(43.6420, 40.1750), (43.6510, 40.1880), (43.6585, 40.2010)],
        "points": [(43.6585, 40.2010, "Карниз", "bzerp.jpg")],
    },
    {
        "title": "Озеро Кардывач",
        "area": "Красная Поляна",
        "difficulty": "сложный",
        "distance_km": 22,
        "duration": "2 дня",
        "image": "kar.jpg",
        "description": "Высокогорное озеро в глубине заповедника. Самый дальний из стартовых маршрутов, с ночёвкой.",
        "description_start": "Тропа уходит от Красной Поляны в долину и выводит к озеру под скалами. Вода холодная даже в августе.",
        "description_basic": "Без пропуска в заповедник на озеро не попасть. Идите с запасом еды и палаткой: за один световой день туда и обратно обычно не возвращаются.",
        "routestart": "Красная Поляна, кордон на пути в долину. Дальше набор высоты к озеру.",
        "workingmode": "Июль и август. В остальное время тропа под снегом или закрыта.",
        "photos": [
            ("kar.jpg", "Озеро", "Кардывач в ясную погоду."),
            ("panar1.jpeg", "Хребет над озером", "Склоны вокруг чаши озера."),
        ],
        "line": [(43.6200, 40.3500), (43.5950, 40.5000), (43.5730, 40.6260)],
        "points": [(43.5730, 40.6260, "Озеро Кардывач", "kar.jpg")],
    },
]


def upgrade():
    op.add_column("route", sa.Column("area", sa.String(length=40), nullable=True))
    op.add_column("route", sa.Column("difficulty", sa.String(length=20), nullable=True))
    op.add_column("route", sa.Column("distance_km", sa.Float(), nullable=True))
    op.add_column("route", sa.Column("duration", sa.String(length=40), nullable=True))

    conn = op.get_bind()
    existing = conn.execute(sa.text("SELECT COUNT(*) FROM route")).scalar()
    if existing:
        return

    for item in ROUTES:
        result = conn.execute(
            sa.text(
                """
                INSERT INTO route
                    (title, description, video, image, area, difficulty, distance_km, duration)
                VALUES
                    (:title, :description, '', :image, :area, :difficulty, :distance_km, :duration)
                """
            ),
            item,
        )
        route_id = result.lastrowid
        conn.execute(
            sa.text(
                """
                INSERT INTO detail
                    (route_id, description_start, description_basic, routestart, workingmode, "order")
                VALUES
                    (:route_id, :description_start, :description_basic, :routestart, :workingmode, 1)
                """
            ),
            {**item, "route_id": route_id},
        )
        for position, (lat, lon) in enumerate(item["line"]):
            conn.execute(
                sa.text(
                    """
                    INSERT INTO coordinate (route_id, longitude, latitude, "order")
                    VALUES (:route_id, :longitude, :latitude, :ord)
                    """
                ),
                {
                    "route_id": route_id,
                    "latitude": lat,
                    "longitude": lon,
                    "ord": position,
                },
            )
        for position, (lat, lon, title, image) in enumerate(item["points"]):
            conn.execute(
                sa.text(
                    """
                    INSERT INTO coordinateformap
                        (route_id, longitude_for_image, latitude_for_image, title, image_for_map, "order")
                    VALUES
                        (:route_id, :longitude, :latitude, :title, :image, :ord)
                    """
                ),
                {
                    "route_id": route_id,
                    "latitude": lat,
                    "longitude": lon,
                    "title": title,
                    "image": image,
                    "ord": position,
                },
            )
        for image, title, body in item["photos"]:
            conn.execute(
                sa.text(
                    """
                    INSERT INTO visual (image, title, body, route_id)
                    VALUES (:image, :title, :body, :route_id)
                    """
                ),
                {
                    "image": image,
                    "title": title,
                    "body": body,
                    "route_id": route_id,
                },
            )


def downgrade():
    conn = op.get_bind()
    titles = [item["title"] for item in ROUTES]
    for title in titles:
        route_id = conn.execute(
            sa.text("SELECT id FROM route WHERE title = :title"),
            {"title": title},
        ).scalar()
        if not route_id:
            continue
        for table in ("visual", "coordinateformap", "coordinate", "detail"):
            conn.execute(
                sa.text(f"DELETE FROM {table} WHERE route_id = :route_id"),
                {"route_id": route_id},
            )
        conn.execute(
            sa.text("DELETE FROM route WHERE id = :route_id"),
            {"route_id": route_id},
        )
    op.drop_column("route", "duration")
    op.drop_column("route", "distance_km")
    op.drop_column("route", "difficulty")
    op.drop_column("route", "area")
