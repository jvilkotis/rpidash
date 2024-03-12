# THIRD PARTY
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

engine = None  # pylint: disable=invalid-name
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=None,
    )
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(database_uri: str):
    """
    Create the database engine.
    Bind the scoped session to the engine.
    Create all the tables defined by the models.
    """
    global engine  # pylint: disable=global-statement
    engine = create_engine(database_uri)
    db_session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
