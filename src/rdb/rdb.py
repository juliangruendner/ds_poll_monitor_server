from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.types as types
import config


db = SQLAlchemy()


class LowerCaseText(types.TypeDecorator):
    '''Converts strings to lower case on the way in.'''

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return value.lower()


def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + config.POSTGRES_USER + ':' + config.POSTGRES_PASSWORD + '@db:5432/' + config.POSTGRES_DB
    db.app = app
    db.init_app(app)


def create_all():
    """Create all db tables"""

    from rdb.models.user import User
    from rdb.models.environment import Environment
    # from rdb.models.userEnvironmentAccess import UserEnvironmentAccess
    from rdb.models.image import Image
    from rdb.models.mlModel import MLModel
    from rdb.models.feature import Feature
    from rdb.models.featureSet import FeatureSet
    from rdb.models.featureFeatureSet import FeatureFeatureSet
    from rdb.models.predictionOutcome import PredictionOutcome

    db.create_all()
    db.session.commit()


def create_admin_user():
    """create admin user while startup"""

    import rdb.models.user as User

    u = User.get_by_username('admin', raise_abort=False)

    if not u:
        u = User.create(username=config.ML_SERVICE_ADMIN_USERNAME, email=config.ML_SERVICE_ADMIN_EMAIL, password=config.ML_SERVICE_ADMIN_PASSWORD)

