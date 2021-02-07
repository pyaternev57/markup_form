def get_data():
    return {'Hyperparam_Tuning': ['find_best_score',
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

def save_pkl(data, path):
    ffile = open(path, "wb")
    print(data[0])
    pkl.dump(data, ffile)
    ffile.close() 

def open_pkl(path):
    ffile = open(path, "rb")
    return pkl.load(ffile)
    

def get_next_notebook(conn):
    next_id = conn.execute(f"select max(notebook_id) from chunks").fetchone()[0]
    if not next_id:
        return 1
    return next_id

def get_chunks_from_notebook(conn, link, num):
    author, name = link.split('/')[-2], link.split('/')[-1]
    kaggle.api.kernels_pull(f"{author}/{name}", 'notebooks')
    data = [el for el in json.load(open(f"notebooks/{name}.ipynb"))["cells"] if el["cell_type"] == 'code']
    res = conn.execute("select max(sim_id) from chunks").fetchone()[0]
    return data


def get_next_chunk(conn, notebook_id, chunk_id):
    link = conn.execute(f"select * from notebooks where notebook_id = {notebook_id}").fetchone()[1]
    if not os.path.exists(f"data/{notebook_id}.pkl"):
        data = get_chunks_from_notebook(conn, link, notebook_id)
        save_pkl(data, f"data/{notebook_id}.pkl")
    chunks = open_pkl(f"data/{notebook_id}.pkl")
    chunk_id = int(chunk_id)
    notebook_id = int(notebook_id)
    # print(chunks[chunk_id])
    if chunk_id >= len(chunks):
        notebook_id = get_next_notebook(conn)
        link = conn.execute(f"select * from notebooks where notebook_id = {notebook_id}").fetchone()[1]
        data = get_chunks_from_notebook(conn, link, notebook_id)
        save_pkl(data, f"data/{notebook_id}.pkl")
        chunks = data.copy()
        chunk_id = 1
    elif chunk_id < 0 and notebook_id > 1:
        notebook_id = notebook_id - 1
        chunk_id = 0
    elif chunk_id < 0:
        notebook_id = 1
        chunk_id = 0
    chunk = chunks[int(chunk_id)]
    print(notebook_id, link, chunk_id)
    return notebook_id, link, chunk_id, chunk

def write_chunk_data(conn, chunk, form):
    sim_id = conn.execute("select max(sim_id) from chunks").fetchone()[0]
    if not sim_id:
        sim_id = 1
    else:
        sim_id += 1
    ver = 1 # change to function
    sql = f'''insert into chunks 
    (sim_id, notebook_id, chunk_id, ver, data_format, graph_vertex, graph_vertex_subclass, errors, mark)
    values({sim_id}, {chunk.notebook_id}, {chunk.chunk_id}, {ver},
    '{form.data_format.data}', '{form.graph_vertex.data}', '{form.graph_vertex_subclass.data}', '{form.errors.data}', '{0}')'''
    conn.execute(sql)
