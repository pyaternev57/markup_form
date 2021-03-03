from sqlalchemy import *
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

engine = create_engine('mysql+pymysql://root:root@db:3306/nl2ml')
from sqlalchemy.ext.declarative import declarative_base
from config import Config
conf = Config()

Base = declarative_base()


class User(Base):
    """User account model."""

    __tablename__ = 'users'
    id = Column(
        Integer,
        primary_key=True
    )
    username = Column(
        String(100),
        nullable=False,
        unique=False
    )
    password = Column(
        String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Notebook(Base):
    """table with notebook data"""

    __tablename__ = 'notebooks'
    id = Column(
        Integer,
        primary_key=True
    )
    link = Column(
        String(100),
        nullable=False,
        unique=False
    )
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )


class Chunk(Base):
    """table with chunks data"""

    __tablename__ = 'chunks'
    id = Column(
        Integer,
        primary_key=True
    )
    notebook_id = Column(
        Integer,
        nullable=False,
        unique=False
    )
    chunk_id = Column(
        Integer,
        nullable=False,
        unique=False
    )
    data_format = Column(
        String(100),
        nullable=False,
        unique=False
    )
    graph_vertex = Column(
        String(100),
        nullable=False,
        unique=False
    )
    graph_vertex_subclass = Column(
        String(100),
        nullable=False,
        unique=False
    )
    errors = Column(
        String(10),
        nullable=False,
        unique=False
    )
    marks = Column(
        Integer,
        nullable=True,
        unique=False,
    )
    username = Column(
        String(100),
        nullable=False,
        unique=False
    )
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )


class Graph(Base):
    __tablename__ = 'graph_vertexes'
    id = Column(
        Integer,
        primary_key=True
    )
    graph_vertex = Column(
        String(100),
        nullable=False,
        unique=False
    )
    graph_vertex_subclass = Column(
        String(100),
        nullable=False,
        unique=False
    )
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )


class History(Base):
    __tablename__ = 'history'
    id = Column(
        Integer,
        primary_key=True
    )
    notebook_id = Column(
        Integer,
        nullable=False,
        unique=False
    )
    chunk_id = Column(
        Integer,
        nullable=False,
        unique=False
    )
    username = Column(
        String(100),
        nullable=False,
        unique=False
    )
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )


Base.metadata.create_all(engine)
