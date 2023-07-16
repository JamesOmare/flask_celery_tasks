import os

from flask import Flask, render_template
from .extensions import db, migrate 
from .utils import celery_init_app
from .config import config 
from .main.views import main



def create_app(config_name=None):  # updated
    # new
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)

   
    # set config
    app.config.from_object(config[config_name])
    
    
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            broker_connection_retry=False,
            broker_connection_retry_on_startup=True,
            broker_connection_max_retries=10,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # register blueprints
    app.register_blueprint(main)
    
    # create_database(app)
    with app.app_context():
        db.create_all()

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app