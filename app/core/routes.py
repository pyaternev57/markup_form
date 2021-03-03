"""Logged-in page routes."""
from typing import List, Any, Tuple

from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required, logout_user
from .forms import *
from .models import Graph, ChunkData, Notebook, Chunk, History, db
from .utils import *
import pandas as pd
import os
from sqlalchemy import func

path2csv = "../notebooks.csv"

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return render_template(
        'healthcheck.jinja2',
        text="Log In"
    )

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Logged-in User Dashboard."""
    form = StartPage()
    if form.is_submitted():
        if form.add_vertexes.data:
            return redirect(url_for("main_bp.add_vertexes"))
        elif form.add_notebooks.data:
            return redirect(url_for("main_bp.add_notebooks"))
        elif form.markup_tool.data:
            return redirect(url_for("main_bp.markup"))
        elif form.dashboard.data:
            return redirect(url_for("main_bp.dashboard"))
        else:
            return redirect(url_for("main_bp.logout"))
    return render_template(
        'home.jinja2',
        title='start page',
        current_user=current_user,
        form=form
    )

@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    sql = db.session.query(Chunk.username, func.count(Chunk.chunk_id).label("# chunks")).group_by(Chunk.username).statement
    table = pd.read_sql(sql, db.session.bind)
    return render_template(
        'dashboard.jinja2',
        title='dashboard',
        current_user=current_user,
        table=table.to_html(classes=["table", "thead-dark"])
    )

# todo add function fillform
@main_bp.route('/markup', methods=['GET', 'POST'])
@login_required
def markup():
    chunk = ChunkData()
    form = DataForm()
    form.graph_vertex_subclass.choices = [(vertex.id, vertex.graph_vertex_subclass) for vertex in
                                          Graph.query.filter_by(graph_vertex="Hyperparam_Tuning").all()]
    chunk.notebook_id, chunk.href = get_notebook_id(db, current_user)
    chunk.chunk_id, chunk.data, chunk.notebook_id = get_next_chunk_id(db, current_user)
    chunk_data = is_chunk_already_filled(chunk, current_user)
    if chunk_data:
        print(chunk_data.data_format)
        form.data_format.data = chunk_data.data_format
        form.graph_vertex.data = chunk_data.graph_vertex
        form.graph_vertex_subclass.data = chunk_data.graph_vertex_subclass
        form.errors_in_chunk.data = chunk_data.errors
        form.mark.data = chunk_data.marks
    if form.is_submitted():
        write2history(db, current_user, chunk)
        if form.back.data:
            return redirect(url_for('main_bp.back'))
        else:
            write2chunks(db, chunk, form, current_user)
            return redirect(url_for('main_bp.markup'))
    print(chunk.data)
    return render_template(
        'markup.jinja2',
        title='markup tool',
        current_user=current_user,
        form=form,
        data=chunk
    )


@main_bp.route('/markup/back', methods=['GET', 'POST'])
@login_required
def back():
    chunk = ChunkData()
    form = DataForm()
    form.graph_vertex_subclass.choices = [(vertex.id, vertex.graph_vertex_subclass) for vertex in
                                          Graph.query.filter_by(graph_vertex="Hyperparam_Tuning")]
    chunk.notebook_id, chunk.href = get_notebook_id(db, current_user)
    chunk.chunk_id, chunk.data, chunk.notebook_id = get_prev_ids(db, current_user)
    # chunk.data = get_chunk_data(db, chunk.notebook_id, chunk.chunk_id)
    chunk_data = is_chunk_already_filled(chunk, current_user)
    # print(chunk_data)
    if chunk_data:
        print(chunk_data.data_format)
        form.data_format.data = chunk_data.data_format
        form.graph_vertex.data = chunk_data.graph_vertex
        form.graph_vertex_subclass.data = chunk_data.graph_vertex_subclass
        form.errors_in_chunk.data = chunk_data.errors
        form.mark.data = chunk_data.marks
    if form.is_submitted():
        write2history(db, current_user, chunk)
        if form.back.data:
            return redirect(url_for('main_bp.back'))
        else:
            write2chunks(db, chunk, form, current_user)
            return redirect(url_for('main_bp.markup'))
    return render_template(
        'markup.jinja2',
        title='markup tool',
        current_user=current_user,
        form=form,
        data=chunk
    )


# TODO function for deleting notebooks
@main_bp.route("/add_notebooks", methods=['GET', 'POST'])
@login_required
def add_notebooks():
    form = AddNotebooks()
    if form.is_submitted():
        name = request.files[form.add.name]
        links = pd.read_csv(name)
        links.columns = [el.lower() for el in links.columns]
        links = links["links"].tolist()
        for link in links:
            if not db.session.query(Notebook).filter_by(link=link).first():
                add_notebook_by_link(db, link)
            else:
                print(f'This notebook {link} has already added')
        return redirect(url_for("main_bp.home"))
    return render_template(
        'add.jinja2',
        title='add notebooks',
        template='dashboard-template',
        current_user=current_user,
        form=form
    )


# TODO change to update from GS? or not?
@main_bp.route("/add_vertexes", methods=['GET', 'POST'])
@login_required
def add_vertexes():
    form = AddVertex()
    if form.is_submitted():
        if form.add.data:
            name = request.files[form.add.name]
            table = pd.read_csv(name)
            classes = table["graph_vertex"].tolist()
            subclasses = table["graph_vertex_subclass"].tolist()
            Graph.query.delete()
            for (gclass, gsubclass) in zip(classes, subclasses):
                add_vertex(db, gclass, gsubclass)
        elif form.add_one_vertex.data:
            if not db.session.query(Graph).filter_by(graph_vertex=form.graph_vertex.data,
                                                     graph_vertex_subclass=form.add_one_vertex.data).first():
                add_vertex(db, form.graph_vertex.data, form.add_one_vertex.data)
        return redirect(url_for('main_bp.home'))
    return render_template(
        'add.jinja2',
        title='add vertexes',
        current_user=current_user,
        text="vertexes",
        form=form
    )


@main_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route("/graph_vertex_subclass/<graph_vertex>", methods=['GET', 'POST'])
@login_required
def graph_vertex_subclass(graph_vertex):
    subclasses = db.session.query(Graph.id, Graph.graph_vertex_subclass).filter_by(graph_vertex=graph_vertex).all()
    choicesArr = []
    for subclass in subclasses:
        choiceObj = {}
        choiceObj["id"] = subclass[0]
        choiceObj["name"] = subclass[1]
        choicesArr.append(choiceObj)
    return jsonify({"subclasses": choicesArr})
