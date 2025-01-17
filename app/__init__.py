import os

from flask import Flask

def create_app(test_config=None):
        # create and configure the app
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        from . import db
        db.init_app(app)

        from . import article
        app.register_blueprint(article.bp)

        from . import blog
        app.register_blueprint(blog.bp)
        app.add_url_rule("/", endpoint="index")

        from . import cli
        app.register_blueprint(cli.bp)
        cli.init_app(app)

        return app


def python_anywhere():
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,"app.sqlite"),
    )

    from . import db
    db.init_app(app)

    from . import article
    app.register_blueprint(article.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    from . import cli
    app.register_blueprint(cli.bp)
    cli.init_app(app)

    return app
