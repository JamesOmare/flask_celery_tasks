from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()