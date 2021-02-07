"""Database models."""
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Notebook(db.Model):
    """table with notebook data"""

    __tablename__ = 'notebooks'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    link = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )


class Chunk(db.Model):
    """table with chunks data"""

    __tablename__ = 'chunks'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    notebook_id = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    chunk_id = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    data_format = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    graph_vertex = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    graph_vertex_subclass = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    notebook_id = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    chunk_id = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )
    user = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )


class ChunkData:
    notebook_id = 1
    chunk_id = 1
    href = ""
    data = ""

    def __repr__(self):
        return f"notebook_id: {self.notebook_id}; chunk_id: {self.chunk_id}"
