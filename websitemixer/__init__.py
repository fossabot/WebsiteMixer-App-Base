import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()  # done here so that db is importable
migrate = Migrate()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_pyfile('config.py', silent=True)

    #app.config.from_mapping(
    #    # store the database in the instance folder
    #    DATABASE=os.path.join(app.instance_path, 'websitemixer.sqlite'),
    #)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.update(test_config)

    app.debug = app.config['DEBUG']
    toolbar = DebugToolbarExtension(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    #from websitemixer.database import create_tables
    #create_tables()

    db.init_app(app)
    migrate.init_app(app, db)

    # apply the blueprints to the app
    #from websitemixer import auth, blog
    #app.register_blueprint(auth.bp)
    #app.register_blueprint(blog.bp)

    from websitemixer.plugins.Base import Base
    from websitemixer.plugins.Install import Setup
    app.register_blueprint(Base.bp)
    app.register_blueprint(Setup.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule('/', endpoint='home')

    return app

