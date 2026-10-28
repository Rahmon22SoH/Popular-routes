from webapp.extensions import db


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    video = db.Column(db.Text(), nullable=True)
    image = db.Column(db.Unicode(128), nullable=True)
    area = db.Column(db.String(40), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    distance_km = db.Column(db.Float, nullable=True)
    duration = db.Column(db.String(40), nullable=True)
    coordinates = db.relationship('Coordinate', backref='route', lazy=True)
    detail = db.relationship('Detail', backref='route', lazy=True)
    visuals = db.relationship('Visual', backref='route', lazy=True)
    coordinateformap = db.relationship('Coordinateformap', backref='route',
                                       lazy=True)

    @property
    def image_path(self):
        if not self.image:
            return "media/panar4.jpeg"
        return f"media/{self.image}"

    def __str__(self):
        return self.title or f"Маршрут {self.id}"
