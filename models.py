"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()


class Cupcake(db.Model):
    """Cupcake model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False,
                      default="https://tinyurl.com/demo-cupcake")

    def __repr__(self):
        """Show info about cupcake."""

        return (
            f"<Cupcake("
            f"id={self.id}, "
            f"flavor='{self.flavor}', "
            f"size='{self.size}', "
            f"rating={self.rating}, "
            f"image='{self.image}')>"
        )

    def serialize(self):
        """Serializes cupcake SQLAlchemy object to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
