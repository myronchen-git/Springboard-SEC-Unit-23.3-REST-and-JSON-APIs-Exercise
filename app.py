"""Flask app for Cupcakes"""

from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from models import Cupcake, connect_db, db
from secret_keys import APP_SECRET_KEY

# ==================================================


def create_app(db_name, testing=False):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres@localhost/{
        db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SECRET_KEY"] = APP_SECRET_KEY
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    if not testing:
        app.config["SQLALCHEMY_ECHO"] = True
    else:
        app.config["SQLALCHEMY_ECHO"] = False

        app.config["TESTING"] = True
        app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

    debug = DebugToolbarExtension(app)

    # --------------------------------------------------

    @app.route("/api/cupcakes")
    def get_cupcakes():
        """
        Get data for all cupcakes.
        Returns JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}.
        """

        flavor = request.args.get("flavor", "")
        cupcakes = db.session.query(Cupcake).filter(
            Cupcake.flavor.ilike(f"%{flavor}%")).all()
        serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]

        return jsonify(cupcakes=serialized_cupcakes)

    @app.route("/api/cupcakes/<int:cupcake_id>")
    def get_cupcake(cupcake_id):
        """
        Get data for one cupcake.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}.
        """

        cupcake = db.session.query(Cupcake).get_or_404(cupcake_id)
        serialized_cupcake = cupcake.serialize()

        return jsonify(cupcake=serialized_cupcake)

    @app.route("/api/cupcakes", methods=["POST"])
    def create_cupcake():
        """
        Create a cupcake.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}.
        """

        cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"],
                          rating=request.json["rating"], image=request.json.get("image"))

        db.session.add(cupcake)
        db.session.commit()

        serialized_cupcake = cupcake.serialize()

        return (jsonify(cupcake=serialized_cupcake), 201)

    @app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
    def update_cupcake(cupcake_id):
        """
        Updates a cupcake.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}.
        """

        if request.json:
            query = db.session.query(Cupcake)
            cupcake = query.get_or_404(cupcake_id)

            query.filter_by(id=cupcake_id).update(request.json)
            db.session.commit()

            serialized_cupcake = cupcake.serialize()

            return jsonify(cupcake=serialized_cupcake)
        else:
            return (jsonify(message="Empty inputs"), 400)

    @app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
    def delete_cupcake(cupcake_id):
        """
        Deletes a cupcake.
        Returns JSON {'message': "Deleted"}.
        """

        cupcake = db.session.query(Cupcake).get_or_404(cupcake_id)
        db.session.delete(cupcake)
        db.session.commit()

        return jsonify(message="Deleted")

    @app.route("/")
    def show_home():
        """ Shows the homepage. """

        return render_template("home.html")

    return app

# ==================================================


if __name__ == "__main__":
    app = create_app("cupcakes")
    connect_db(app)
    app.run(debug=True)
