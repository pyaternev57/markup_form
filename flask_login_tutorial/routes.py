"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from .forms import DataForm
from .models import ChunkData, Notebook, Chunk, History, db
from sqlalchemy.sql.expression import func
from .utils import open_pkl

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def get_notebook_id(db, current_user):
    notebook_id = db.session.query(func.max(History.notebook_id)).filter_by(user=current_user.username).first()[0]
    if not notebook_id:
        notebook_id = db.session.query(func.max(History.notebook_id)).first()[0]
        if not notebook_id:
            notebook_id = 0
    return notebook_id + 1


def get_chunk_id(db, current_user, notebook_id):
    chunk_id = db.session.query(func.max(Chunk.chunk_id)).filter_by(user=current_user, notebook_id=notebook_id).first()[
        0]
    print(chunk_id)
    if not chunk_id:
        chunk_id = -1
    chunk_id += 1
    link = Notebook.select("link").filter_by(notebook_id=notebook_id).first()
    if not os.path.exists(f"data/{notebook_id}.pkl"):
        data = get_chunks_from_notebook(conn, link, notebook_id)
        save_pkl(data, f"data/{notebook_id}.pkl")


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    chunk = ChunkData()
    form = DataForm()
    chunk.notebook_id = get_notebook_id(db, current_user)
    print(chunk.notebook_id)

    return render_template(
        'dashboard.jinja2',
        title='markup tool',
        template='dashboard-template',
        current_user=current_user,
        form=form
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
