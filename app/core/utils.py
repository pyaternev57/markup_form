from .models import *
from .forms import *
import pandas as pd
import os
import kaggle
import json
import pickle as pkl
from sqlalchemy.sql.expression import func


def get_data():
    result = Graph.query.all()
    data = {}
    for vertex in result:
        if vertex.graph_vertex in data.keys():
            data[vertex.graph_vertex].append(vertex.graph_vertex_subclass)
        else:
            data[vertex.graph_vertex] = [vertex.graph_vertex_subclass]
    return data

def create_first_graph(db):
    data = {'Hyperparam_Tuning': ['find_best_score',
                                  'find_best_params',
                                  'find_best_model_class',
                                  'Train model on different params, fit, eval',
                                  'choose model class',
                                  'define_search_space'],
            'Data_Transform': ['feature_engineering',
                               'sort_values',
                               'drop_column',
                               'concatenate',
                               'create dataframe',
                               'split',
                               'filter',
                               'randomize order',
                               'data type conversions',
                               'correct missing values',
                               'normalization',
                               'remove duplicates'],
            'Environment': ['import_modules', 'set_options'],
            'Data_Export': ['save_to_csv'],
            'Model_Train': ['grid_search',
                            'loss function computation',
                            'train model',
                            'predict (labels, distance, ...)',
                            'metric computation',
                            'choose model class'],
            'Visualization': ['distribution', 'missing_values'],
            'EDA': ['count_data_types',
                    'count_duplicates',
                    'count_missing_values',
                    'show_table_attributes',
                    'show_table'],
            'Data_Extraction': ['Load from CSV',
                                'Load from disk',
                                'Load from SQL',
                                'Load from URL'],
            'Hypothesis': ['pipeline type spec', 'statistical test'],
            'Model_Deploy': ['save weights', 'send to prod environment']}
    if not db.session.query(Graph.id).first():
        for graph_vertex in data.keys():
            for graph_vertex_subclass in data[graph_vertex]:
                add_vertex(db, graph_vertex, graph_vertex_subclass)





def prepared_chunk(chunk, output):
    old_chunk = chunk.split('\n')
    new_chunk = []
    n = 60
    for line in old_chunk:
        parts = ['    ' + line[i:i + n] if i > 0 else line[i:i + n] for i in range(0, len(line), n)]
        new_chunk.extend(parts)
    # print('<br/>'.join(new_chunk))
    old_outputs = output
    new_output = []
    for line in old_outputs:
        parts = ['    ' + line[i:i + n] if i > 0 else line[i:i + n] for i in range(0, len(line), n)]
        new_output.extend(parts)
    return '<br/>'.join(new_chunk), '<br/>'.join(new_output)


def save_pkl(data, path):
    ffile = open(path, "wb")
    pkl.dump(data, ffile)
    ffile.close()


def open_pkl(path):
    ffile = open(path, "rb")
    return pkl.load(ffile)


def download_chunks_from_notebook(link):
    author, name = link.split('/')[-2], link.split('/')[-1]
    kaggle.api.kernels_pull(f"{author}/{name}", 'notebooks')
    data = [prepared_chunk(el['source'], el['outputs']) for el in json.load(open(f"notebooks/{name}.ipynb"))["cells"] if
            el["cell_type"] == 'code']
    return data


def add_notebook_by_link(db, link):
    notebook = Notebook(
        link=link
    )
    db.session.add(notebook)
    db.session.commit()


def write2history(db, username, chunk):
    row = History(
        username=username.username,
        notebook_id=chunk.notebook_id,
        chunk_id=chunk.chunk_id
    )
    db.session.add(row)
    db.session.commit()


def write2chunks(db, chunk, form, current_user):
    row = Chunk(
        notebook_id=chunk.notebook_id,
        chunk_id=chunk.chunk_id,
        data_format=form.data_format.data,
        graph_vertex=form.graph_vertex.data,
        graph_vertex_subclass=form.graph_vertex_subclass.data,
        errors=form.errors_in_chunk.data,
        marks=form.mark.data,
        username=current_user.username
    )
    db.session.add(row)
    db.session.commit()


def get_notebook_id(db, current_user):
    notebook_id = db.session.query(func.max(History.notebook_id)).filter_by(username=current_user.username).first()[0]
    if not notebook_id:
        notebook_id = db.session.query(func.max(History.notebook_id)).first()[0]
        if not notebook_id:
            notebook_id = 1
        else:
            notebook_id += 1
    link = db.session.query(Notebook.link).filter_by(id=notebook_id).first()[0]
    return notebook_id, link


def get_chunk_data(db, notebook_id, chunk_id):
    link = db.session.query(Notebook.link).filter_by(id=notebook_id).first()[0]
    if not os.path.exists(f"data/{notebook_id}.pkl"):
        data = download_chunks_from_notebook(link)
        save_pkl(data, f"data/{notebook_id}.pkl")
    chunks = open_pkl(f"data/{notebook_id}.pkl")
    print(len(chunks))
    while chunk_id >= len(chunks):
        notebook_id = db.session.query(func.max(History.notebook_id)).first()[0] + 1
        print(notebook_id)
        chunks = download_chunks_from_notebook(link)
        save_pkl(chunks, f"data/{notebook_id}.pkl")
        chunk_id = 1
    chunk = chunks[chunk_id - 1]
    return chunk, notebook_id, chunk_id


def get_next_chunk_id(db, current_user):
    result = db.session.query(History.notebook_id, History.chunk_id)\
        .filter_by(username=current_user.username)\
        .order_by(History.created_on.desc())\
        .first()
    if result:
        notebook_id, last_chunk_id = result
    else:
        notebook_id, last_chunk_id = 1, 0
    chunk, notebook_id, chunk_id = get_chunk_data(db, notebook_id, last_chunk_id + 1)
    return chunk_id, chunk, notebook_id


def get_prev_ids(db, current_user):
    notebook_id, last_chunk_id = db.session.query(History.notebook_id, History.chunk_id) \
        .filter_by(username=current_user.username) \
        .order_by(History.created_on.desc()) \
        .first()
    if last_chunk_id == 1:
        chunk_id = 1
    else:
        chunk_id = last_chunk_id - 1
    chunk, notebook_id, chunk_id = get_chunk_data(db, notebook_id, chunk_id)
    return chunk_id, chunk, notebook_id


def add_notebook_by_link(db, link):
    notebook = Notebook(
        link=link
    )
    db.session.add(notebook)
    db.session.commit()


def add_vertex(db, graph_vertex, graph_vertex_subclass):
    vertex = Graph(
        graph_vertex=graph_vertex,
        graph_vertex_subclass=graph_vertex_subclass
    )
    db.session.add(vertex)
    db.session.commit()


def is_chunk_already_filled(chunk, current_user, how='user'):
    if how == 'user':
        result = Chunk.query.filter_by(chunk_id=chunk.chunk_id,
                                   notebook_id=chunk.notebook_id,
                                   username=current_user.username).order_by(Chunk.created_on.desc()).first()
    elif how == 'all':
        result = Chunk.query.filter_by(chunk_id=chunk.chunk_id,
                                       notebook_id=chunk.notebook_id).order_by(Chunk.created_on.desc()).first()
    else:
        result = None
    return result
