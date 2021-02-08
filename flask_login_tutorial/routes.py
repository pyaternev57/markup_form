"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from .forms import DataForm
from .models import ChunkData, Notebook, Chunk, History, db
from sqlalchemy.sql.expression import func
from .utils import open_pkl, save_pkl, download_chunks_from_notebook
import pandas as pd
import os

path2csv = "../notebooks.csv"

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def write2history(db, username, chunk):
    row = History(
        username=username.username,
        notebook_id=chunk.notebook_id,
        chunk_id=chunk.chunk_id
    )
    db.session.add(row)
    db.session.commit()


def write2chunks(db, chunk, form):
    row = Chunk(
        notebook_id=chunk.notebook_id,
        chunk_id=chunk.chunk_id,
        data_format=form.data_format.data,
        graph_vertex=form.graph_vertex.data,
        graph_vertex_subclass=form.graph_vertex_subclass.data,
        errors=form.errors_in_chunk.data,
        marks=form.mark.data
    )
    db.session.add(row)
    db.session.commit()


def get_notebook_id(db, current_user):
    notebook_id = db.session.query(func.max(History.notebook_id)).filter_by(username=current_user.username).first()[0]
    if not notebook_id:
        notebook_id = db.session.query(func.max(History.notebook_id)).first()[0]
        if not notebook_id:
            notebook_id = 0
    link = db.session.query(Notebook.link).filter_by(id=notebook_id).first()[0]
    return notebook_id, link


def get_chunk_id(db, current_user, notebook_id):
    chunk_id = db.session.query(func.max(History.chunk_id)) \
        .filter_by(username=current_user.username, notebook_id=notebook_id).first()[0]
    print(chunk_id)
    if not chunk_id:
        chunk_id = 0
    chunk_id += 1
    link = db.session.query(Notebook.link).filter_by(id=notebook_id).first()[0]
    print(os.path.exists(f"data/{notebook_id}.pkl"))
    if not os.path.exists(f"data/{notebook_id}.pkl"):
        data = download_chunks_from_notebook(link)
        save_pkl(data, f"data/{notebook_id}.pkl")
    chunks = open_pkl(f"data/{notebook_id}.pkl")
    while chunk_id > len(chunks):
        notebook_id = db.session.query(func.max(History.notebook_id)).first()[0] + 1
        chunks = download_chunks_from_notebook(link)
        save_pkl(chunks, f"data/{notebook_id}.pkl")
        chunk_id = 1
    chunk = chunks[chunk_id - 1]
    return chunk_id, chunk


def add_notebook_by_link(db, link):
    notebook = Notebook(
        link=link
    )
    db.session.add(notebook)
    db.session.commit()


@main_bp.route('/', methods=['GET'])
@login_required
def home():
    """Logged-in User Dashboard."""
    return render_template(
        'home.jinja2',
        title='start page',
        template='dashboard-template',
        current_user=current_user
    )


@main_bp.route('/markup', methods=['GET', 'POST'])
@login_required
def dashboard():
    chunk = ChunkData()
    form = DataForm()
    chunk.notebook_id, link = get_notebook_id(db, current_user)
    chunk.chunk_id, chunk.data = get_chunk_id(db, current_user, chunk.notebook_id)
    if form.is_submitted():
        write2chunks(db, chunk, form)
        write2history(db, current_user, chunk)
        return redirect(url_for('main_bp.dashboard'))
    return render_template(
        'dashboard.jinja2',
        title='markup tool',
        template='dashboard-template',
        current_user=current_user,
        form=form,
        data=chunk
    )


@main_bp.route("/add", methods=['GET', 'POST'])
@login_required
def add_notebooks():
    path2csv = "notebooks.csv"
    links = pd.read_csv(path2csv)["Links"].tolist()
    for link in links:
        if not db.session.query(Notebook).filter_by(link=link).first():
            add_notebook_by_link(db, link)
        else:
            print('This notebook has already added')
    return render_template(
        'add.jinja2',
        title='add notebooks',
        template='dashboard-template',
        current_user=current_user
    )


@main_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
