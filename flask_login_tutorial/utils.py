from .models import Notebook, History, Chunk, User
import kaggle
import json
import pickle as pkl


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
