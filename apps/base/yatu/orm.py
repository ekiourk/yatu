import sqlalchemy
from sqlalchemy import (
    Table, Column, MetaData,
    String, Integer, DateTime, ForeignKey)
from sqlalchemy.orm import (
    clear_mappers, mapper, relationship, scoped_session, sessionmaker
)
from sqlalchemy import create_engine, func
from yatu.model import ShortUrl, User, AccessToken


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


class UserRepository(Repository):

    def get_by_token(self, token):
        try:
            token = self.session.query(AccessToken) \
                .filter_by(token=token).first()
        except sqlalchemy.orm.exc.NoResultFound:
            return
        return token.user


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

    @property
    def users(self):
        return UserRepository(self.session)


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
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('created_at', DateTime, default=func.now()),
            Column('visited_counter', Integer, default=0),
        )

        users_table = Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50)),
            Column('email', String(100)),
            Column('password', String(255)),
            Column('created_at', DateTime, default=func.now()),
        )

        access_tokens = Table(
            'access_tokens',
            metadata,
            Column('token', String(255), primary_key=True),
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('created_at', DateTime, default=func.now()),
        )

        # Mappings
        mapper(ShortUrl, short_urls_table, properties={
            'id': short_urls_table.c.id,
            'sid': short_urls_table.c.sid,
            'url': short_urls_table.c.url,
            'user_id': short_urls_table.c.user_id,
            'created_at': short_urls_table.c.created_at,
            'visited_counter': short_urls_table.c.visited_counter
        })

        mapper(User, users_table, properties={
            'id': users_table.c.id,
            'username': users_table.c.username,
            'email': users_table.c.email,
            'password': users_table.c.password,
            'created_at': users_table.c.created_at,
            'tokens': relationship(
                AccessToken,
                backref='user',
                single_parent=True,
                cascade="all, delete-orphan"),
            'urls': relationship(
                ShortUrl,
                backref='user',
                single_parent=True,
                cascade="all, delete-orphan")
        })

        mapper(AccessToken, access_tokens, properties={
            'token': access_tokens.c.token,
            'user_id': access_tokens.c.user_id,
            'created_at': access_tokens.c.created_at
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