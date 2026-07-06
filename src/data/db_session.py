import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.pool import NullPool

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return
    engine = sa.create_engine(
        f'sqlite:///{db_file.strip()}',
        connect_args={"check_same_thread": False, "timeout": 20},
        poolclass=NullPool,
    )
    __factory = orm.sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    return __factory()
