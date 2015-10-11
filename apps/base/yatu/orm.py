import sqlalchemy
from sqlalchemy import (
    Table, Column, MetaData,
    String, Integer, DateTime, ForeignKey)
from sqlalchemy.orm import (
    clear_mappers, mapper, relationship, scoped_session, sessionmaker
)
from sqlalchemy import create_engine, func
from yatu.model import ShortUrl


class Repository:

    def __init__(self, session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)


class ShortUrlRepository(Repository):

    def get(self, sid):
        try:
            return self.session.query(ShortUrl) \
                .filter_by(sid=sid).first()
        except sqlalchemy.orm.exc.NoResultFound:
            return


class SqlAlchemyUnitOfWorkManager:

    def __init__(self, session_maker):
        self.session_maker = session_maker

    def start(self):
        return SqlAlchemyUnitOfWork(self.session_maker)


class SqlAlchemyUnitOfWork:

    def __init__(self, sessionfactory):
        self.sessionfactory = sessionfactory

    def __enter__(self):
        self.session = self.sessionfactory()
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def short_urls(self):
        return ShortUrlRepository(self.session)


class SqlAlchemy:

    def __init__(self, connection_string):
        self.postgres_engine = create_engine(connection_string, echo=False, encoding='utf-8')
        self._session_maker = scoped_session(sessionmaker(self.postgres_engine))

    def unit_of_work_manager(self):
        return SqlAlchemyUnitOfWorkManager(self._session_maker)

    def configure_mappings(self):

        metadata = MetaData(self.postgres_engine)
        clear_mappers()

        # Tables
        short_urls_table = Table(
            'short_urls',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('sid', String(50)),
            Column('url', String(255)),
            Column('created_at', DateTime, default=func.now())
        )

        # Mappings
        mapper(ShortUrl, short_urls_table, properties={
            'id': short_urls_table.c.id,
            'sid': short_urls_table.c.sid,
            'url': short_urls_table.c.url,
            'created_at': short_urls_table.c.created_at
        })

    def session(self):
        return SqlAlchemySessionContext(self._session_maker)


class SqlAlchemySessionContext:

    def __init__(self, session_maker):
        self._session_maker = session_maker

    def __enter__(self):
        self._session = self._session_maker()

    def __exit__(self, type, value, traceback):
        self._session_maker.remove()