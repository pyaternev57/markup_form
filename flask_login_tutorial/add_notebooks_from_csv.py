from utils import add_notebook_by_link
from models import Notebook
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import pandas as pd

Session = sessionmaker(autoflush=False)

path2csv = "notebooks.csv"
links = pd.read_csv(path2csv)
print(links.columns)
links = links["Links"].tolist()
engine = create_engine('mysql://pyaternev:testpass@localhost/nl2ml')
session = Session(bind=engine)
for link in links:
    print(link)
    if db.session.query(Notebook).filter_by(link=link).first()[0]:
        print('This notebook has already added')
    else:
        add_notebook_by_link(session, link)



